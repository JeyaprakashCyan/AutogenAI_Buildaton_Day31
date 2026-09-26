"""
PDF -> text extraction -> chunking -> OpenAI embeddings -> FAISS.
Run: python -m src.ingest
"""
import json, hashlib, time
from pathlib import Path
import faiss
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI

from .config import DATA_DIR, VECTOR_DIR, MANIFEST_FILE, OPENAI_API_KEY, EMBEDDING_MODEL, EMBEDDING_DIM, CHUNK_SIZE, CHUNK_OVERLAP

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing.")

client = OpenAI(api_key=OPENAI_API_KEY)
splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

def sha256(path: Path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def read_pdfs():
    records = []
    for path in sorted(DATA_DIR.rglob("*.pdf")):
        department = path.parent.name
        reader = PdfReader(str(path))
        for page_no, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            for chunk_no, chunk in enumerate(splitter.split_text(text)):
                records.append({
                    "text": chunk.strip(),
                    "source": path.name,
                    "path": str(path.relative_to(DATA_DIR)),
                    "department": department,
                    "page": page_no,
                    "chunk_id": f"{path.stem}-p{page_no}-c{chunk_no}",
                    "version": "1.0",
                    "sha256": sha256(path),
                })
    return records

def embed_texts(texts, batch_size=100):
    vectors = []
    for i in range(0, len(texts), batch_size):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[i:i+batch_size])
        vectors.extend([x.embedding for x in response.data])
        time.sleep(0.05)
    return vectors

def build():
    records = read_pdfs()
    if not records:
        raise RuntimeError(f"No PDFs found under {DATA_DIR}")

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    vectors = embed_texts([r["text"] for r in records])
    index = faiss.IndexFlatIP(EMBEDDING_DIM)
    import numpy as np
    arr = np.asarray(vectors, dtype="float32")
    faiss.normalize_L2(arr)
    index.add(arr)

    faiss.write_index(index, str(VECTOR_DIR / "support.index"))
    (VECTOR_DIR / "metadata.json").write_text(json.dumps(records, indent=2), encoding="utf-8")

    manifest = {
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "embedding_model": EMBEDDING_MODEL,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "documents": {}
    }
    for p in sorted(DATA_DIR.rglob("*.pdf")):
        manifest["documents"][str(p.relative_to(DATA_DIR))] = {
            "sha256": sha256(p), "version": "1.0", "pages": len(PdfReader(str(p)).pages)
        }
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Indexed {len(records)} chunks from {len(manifest['documents'])} PDFs.")

if __name__ == "__main__":
    build()
