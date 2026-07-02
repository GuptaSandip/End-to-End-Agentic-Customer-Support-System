"""
Sanity test script:
Test script to sanity-check retrieval quality with sample.
"""
from app.rag.retriever import retrieve

TEST_QUERIES = [
    "my money got deducted but the payment failed",
    "how long does kyc take",
    "app is crashing on my phone",
    "what happens if I miss an EMI",
    "can I get my money back if I sent it to the wrong person",
    "My EMI payment failed, what happens now?",
]

if __name__ == "__main__":
    for q in TEST_QUERIES:
        print(f"\nQuery: {q}")
        hits = retrieve(q, n_results=2)
        for h in hits:
            print(f"  [{h['category']}] (distance={h['distance']:.3f})")
            print(f"  {h['document'][:120]}...")