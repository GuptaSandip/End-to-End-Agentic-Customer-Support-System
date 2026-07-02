"""
Step 2:
Supervisor node — structured classification:
Architected modular graph struture with stub implementations for validation

Setting up the file structure with state.py at app/graph/state.py, then create stub nodes for the knowledge base, escalation, and ticket handling 
that return placeholder responses so I can test the routing end-to-end today. The supervisor node will be the main focus for day 3, but I'll wire up the full 
graph with minimal implementations so we can validate the flow before fleshing out the actual logic on days 4 and 5.
"""
from typing import Literal
from pydantic import BaseModel, Field
from app.llm_provider import get_llm
from app.graph.state import SupportState


class RouteDecision(BaseModel):
    route: Literal["kb", "escalation", "ticket", "chitchat"] = Field(
        description=(
            "kb: common/factual question answerable from FAQ docs "
            "(account, KYC, payments, loans, app issues). "
            "escalation: complex, emotional, urgent, or sensitive queries "
            "(fraud, disputed charges, threats to close account, distress). "
            "ticket: anything that doesn't fit kb or escalation, "
            "or is too vague/specific to answer generically. "
            "chitchat: greetings, thanks, acknowledgments ('okay got it', 'thanks', "
            "'cool', 'that helps'), or small talk with no actual support need — "
            "the conversation is being wrapped up or hasn't started a real issue yet."
        )
    )
    reasoning: str = Field(description="One sentence explanation of the routing choice.")


SUPERVISOR_PROMPT = """You are a routing supervisor for a fintech customer support system.
Classify the user's query into exactly one route: kb, escalation, ticket, or chitchat.

Guidelines:
- kb: routine questions about KYC, payments, loans, app/technical issues that a FAQ would answer.
- escalation: emotionally charged, urgent, or sensitive issues — fraud, unauthorized transactions,
  threats, distress, or anything requiring human judgment and empathy.
- ticket: anything else — vague requests, account-specific issues needing manual lookup,
  or queries that don't clearly match kb or escalation, but ARE still a real support need.
- chitchat: no actual support need present — greetings ("hi"), acknowledgments ("okay got it",
  "thanks", "that helps", "cool"), or conversation closers. Do NOT create a ticket for these.

Use the recent conversation below ONLY to resolve references like "it" or "that issue" in
the current query. Base your routing decision on the current query's actual content.

Recent conversation:
{history}

Current user query: {query}
"""


def supervisor_node(state: SupportState) -> SupportState:
    llm = get_llm()
    structured_llm = llm.with_structured_output(RouteDecision)

    decision: RouteDecision = structured_llm.invoke(
        SUPERVISOR_PROMPT.format(
            history=state.get("chat_history") or "(no prior messages)",
            query=state["query"],
        )
    )

    return {**state, "route": decision.route}


def route_selector(state: SupportState) -> Literal["kb", "escalation", "ticket", "chitchat"]:
    """Conditional edge function — reads the route already set by supervisor_node."""
    return state["route"]