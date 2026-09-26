import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1536"))

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))
TOP_K_VECTOR = int(os.getenv("TOP_K_VECTOR", "12"))
TOP_K_FINAL = int(os.getenv("TOP_K_FINAL", "4"))
RAG_MIN_SCORE = float(os.getenv("RAG_MIN_SCORE", "0.38"))

DATA_DIR = ROOT / "data"
VECTOR_DIR = ROOT / "vector_store"
MANIFEST_FILE = VECTOR_DIR / "manifest.json"
EVAL_DIR = ROOT / "evals"

DEPARTMENTS = {
    "IT_Service_Desk_Agent": "it",
    "Product_Client_Success_Agent": "product",
    "People_Ops_HR_Policy_Agent": "hr",
    "Talent_Management_Growth_Agent": "talent",
    "Business_Ops_Corporate_Agent": "business",
}
