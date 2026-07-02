"""
Creating crhomadb index:
For embeddings, I'll use ChromaDB's built-in default embedding function (onnxruntime-based, runs locally, no API key, no extra cost) — cleanest choice for a demo since it removes one more moving part. Neither Groq nor OpenRouter need to be involved for embeddings at all.
"""
import json
import chromadb
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
FAQ_PATH = DATA_DIR / "faqs.json"
CHROMA_PATH = str(DATA_DIR / "chroma_db")

COLLECTION_NAME = "fintech_faqs"


def build_index():
    with open(FAQ_PATH, "r", encoding="utf-8") as f:
        faqs = json.load(f)

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Fresh build each time this script runs
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME)

    ids = [f["id"] for f in faqs]
    documents = [f"Q: {f['question']}\nA: {f['answer']}" for f in faqs]
    metadatas = [{"category": f["category"], "question": f["question"]} for f in faqs]

    collection.add(ids=ids, documents=documents, metadatas=metadatas)

    print(f"Indexed {len(faqs)} FAQs into collection '{COLLECTION_NAME}' at {CHROMA_PATH}")


if __name__ == "__main__":
    build_index()