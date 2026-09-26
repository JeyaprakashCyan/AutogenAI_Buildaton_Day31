import json
from pathlib import Path
import faiss
import numpy as np
from openai import OpenAI
from rank_bm25 import BM25Okapi

from .config import VECTOR_DIR, OPENAI_API_KEY, EMBEDDING_MODEL, TOP_K_VECTOR, TOP_K_FINAL, RAG_MIN_SCORE

class RAGService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        index_path = VECTOR_DIR / "support.index"
        meta_path = VECTOR_DIR / "metadata.json"
        if not index_path.exists() or not meta_path.exists():
            raise RuntimeError("Vector DB not found. Run: python -m src.ingest")
        self.index = faiss.read_index(str(index_path))
        self.records = json.loads(meta_path.read_text(encoding="utf-8"))
        self.tokenized = [self._tokens(r["text"]) for r in self.records]
        self.bm25 = BM25Okapi(self.tokenized)

    @staticmethod
    def _tokens(text):
        return [x for x in text.lower().split() if x]

    def retrieve(self, query, department=None):
        qv = self.client.embeddings.create(model=EMBEDDING_MODEL, input=[query]).data[0].embedding
        qarr = np.asarray([qv], dtype="float32")
        faiss.normalize_L2(qarr)
        scores, ids = self.index.search(qarr, min(TOP_K_VECTOR, len(self.records)))

        candidates = []
        bm_scores = self.bm25.get_scores(self._tokens(query))
        max_bm = max(bm_scores) if max(bm_scores) else 1.0

        for raw_score, idx in zip(scores[0], ids[0]):
            if idx < 0:
                continue
            r = dict(self.records[idx])
            if department and r["department"] != department:
                continue
            vector_score = float(raw_score)
            lexical = float(bm_scores[idx] / max_bm) if max_bm else 0.0
            # Transparent hybrid reranking: semantic similarity + lexical relevance.
            r["vector_score"] = vector_score
            r["lexical_score"] = lexical
            r["rerank_score"] = 0.75 * vector_score + 0.25 * lexical
            candidates.append(r)

        candidates.sort(key=lambda x: x["rerank_score"], reverse=True)
        return candidates[:TOP_K_FINAL]

    def is_grounded_enough(self, results):
        return bool(results) and results[0]["rerank_score"] >= RAG_MIN_SCORE
