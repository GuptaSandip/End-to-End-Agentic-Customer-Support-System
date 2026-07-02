"""
KB Agent — retrieves FAQ context, answers only from it:
"""
# location: app/graph/kb_agent.py

from app.llm_provider import get_llm
from app.graph.state import SupportState
from app.rag.retriever import retrieve

KB_PROMPT = """You are a fintech customer support assistant. Answer the user's question
using the FAQ context below. The FAQs are ordered by relevance — FAQ 1 is the closest
match to the user's question.

Use the recent conversation only to understand what the user is referring to (e.g. "it",
"that issue") — don't repeat information you already gave them.

Give ONE direct, synthesized answer. Do NOT narrate which FAQ you're using or compare
them out loud — just answer naturally as if you already knew this. If the query is
ambiguous between what FAQ 1 and FAQ 2 cover, briefly address the most likely scenario
first, then mention the other possibility in one short sentence.

If neither FAQ actually answers the question, say you don't have enough information and
recommend the user contact support directly — do NOT make up an answer.

Recent conversation:
{history}

FAQ Context (ordered by relevance):
{context}

User question: {query}

Answer:"""


REWRITE_PROMPT = """Given the recent conversation and a follow-up user query, rewrite the
query into a standalone question that makes sense without the conversation. If the query
is already standalone, return it unchanged. Return ONLY the rewritten question, nothing else.

Recent conversation:
{history}

Follow-up query: {query}

Standalone question:"""


def _get_standalone_query(query: str, history: str) -> str:
    if not history:
        return query
    llm = get_llm()
    rewritten = llm.invoke(REWRITE_PROMPT.format(history=history, query=query))
    return rewritten.content.strip()


def kb_node(state: SupportState) -> SupportState:
    query = state["query"]
    history = state.get("chat_history") or ""
    search_query = _get_standalone_query(query, history)

    hits = retrieve(search_query, n_results=2)

    # Filter out weak matches (high distance = low relevance)
    relevant_hits = [h for h in hits if h["distance"] < 1.2]

    if not relevant_hits:
        return {
            **state,
            "response": "I couldn't find a specific FAQ match for this. Let me create a ticket for our team to look into it.",
            "kb_sources": [],
        }

    context = "\n\n".join(
        f"FAQ {i+1}:\n{h['document']}" for i, h in enumerate(relevant_hits)
    )

    llm = get_llm()
    answer = llm.invoke(
        KB_PROMPT.format(
            history=state.get("chat_history") or "(no prior messages)",
            context=context,
            query=query,
        )
    )

    return {
        **state,
        "response": answer.content,
        "kb_sources": [h["category"] for h in relevant_hits],
    }