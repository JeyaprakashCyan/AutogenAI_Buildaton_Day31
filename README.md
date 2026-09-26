# Multi-Agent Customer Support — AutoGen + RAG + FAISS

## Architecture
User -> Streamlit UI -> Guardrails -> OpenAI Router -> Department RAG -> FAISS semantic retrieval -> BM25/semantic hybrid reranking -> grounded answer.
If the internal score is below `RAG_MIN_SCORE`, the system calls Serper web search and gives the specialist only the external fallback context.

## Departments
IT, Product/Client Success, HR/People Ops, Talent/Growth, and Business/Corporate Operations.

## 1. Install
Python 3.13 or 3.14 is supported.

```bash
py -3.14 -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configure
Copy `.env.example` to `.env` and set `OPENAI_API_KEY`. Add `SERPER_API_KEY` if web fallback is required.

## 3. Build the vector database
```bash
python -m src.ingest
```
This extracts PDF pages, splits text, creates embeddings, normalizes vectors and writes FAISS plus metadata.

## 4. Run evaluations
```bash
python -m evals.evaluate_rag
```
The evaluation reports retrieval Hit Rate and MRR against expected department documents.

## 5. Run UI
```bash
streamlit run app.py
```

## Version maintenance
The ingestion manifest records SHA-256, version, page count and build time. When a PDF changes, update its version in `src/ingest.py` (or move to a database-backed document registry for production) and rebuild the index. Metadata remains attached to every chunk.

## Guardrails
The input guardrail blocks clearly out-of-scope/high-risk topics and limits length. Production systems should add authentication, authorization, PII redaction, prompt-injection detection, audit logs and per-document access controls.

## Reranking
The first-stage FAISS search returns up to 12 candidates. The second stage combines normalized vector similarity (75%) with BM25 lexical relevance (25%), then keeps the top 4. This is intentionally lightweight. A CrossEncoder/FlashRank reranker can be added later if latency and model size are acceptable.

## Important
The included PDFs are fictional mock knowledge. They are for demonstrating RAG and should not be treated as real company policy.
