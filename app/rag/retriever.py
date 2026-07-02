"""
Retriever module:
Retriever wrapper for querying the Chroma FAQ Collection
"""
import chromadb
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
CHROMA_PATH = str(DATA_DIR / "chroma_db")
COLLECTION_NAME = "fintech_faqs"

_client = None
_collection = None


def get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = _client.get_collection(COLLECTION_NAME)
    return _collection


def retrieve(query: str, n_results: int = 3):
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=n_results)

    hits = []
    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        hits.append({"document": doc, "category": meta["category"], "distance": dist})
    return hits