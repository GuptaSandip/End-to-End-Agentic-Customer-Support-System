"""
Escalation Agent — drafts empathetic response, does NOT try to resolve:
Escalation Agent node 
"""
# location: app/graph/escalation_agent.py

from app.llm_provider import get_llm
from app.graph.state import SupportState

ESCALATION_PROMPT = """You are a fintech customer support agent handling a sensitive or
urgent issue that requires human review. Your job is NOT to solve the problem — a human
specialist will handle resolution. Your job is to:

1. Acknowledge the user's concern with genuine empathy, without being overly dramatic.
2. Reassure them the issue is being taken seriously and escalated to a specialist.
3. Ask for any critical details that would help resolve this faster (e.g. transaction ID,
   approximate date/time, amount involved) — only ask for what's relevant to this specific issue.
   Don't re-ask for details they already gave in the recent conversation.
4. Do NOT promise specific outcomes, refund amounts, or timelines you can't guarantee.
5. Keep it short — 3-4 sentences max.

Recent conversation:
{history}

User's message: {query}

Your response:"""


def escalation_node(state: SupportState) -> SupportState:
    query = state["query"]

    llm = get_llm()
    answer = llm.invoke(
        ESCALATION_PROMPT.format(
            history=state.get("chat_history") or "(no prior messages)",
            query=query,
        )
    )

    return {
        **state,
        "response": answer.content,
    }