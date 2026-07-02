"""
4th agent chitchat:

"""
# location: app/graph/chitchat_agent.py

from app.llm_provider import get_llm
from app.graph.state import SupportState

CHITCHAT_PROMPT = """You are a friendly fintech customer support assistant. The user just
sent a message that's a greeting, acknowledgment, or small talk — not a real support
question. Respond naturally and briefly (1-2 sentences), and if it sounds like they're
wrapping up, let them know you're here if they need anything else.

User's message: {query}

Your response:"""


def chitchat_node(state: SupportState) -> SupportState:
    query = state["query"]

    llm = get_llm()
    answer = llm.invoke(CHITCHAT_PROMPT.format(query=query))

    return {
        **state,
        "response": answer.content,
    }