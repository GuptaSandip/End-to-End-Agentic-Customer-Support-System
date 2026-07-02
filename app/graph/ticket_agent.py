"""
Ticket Agent
"""

# location: app/graph/ticket_agent.py

from typing import Literal
from pydantic import BaseModel, Field
from app.llm_provider import get_llm
from app.graph.state import SupportState


class SupportTicket(BaseModel):
    category: Literal["account_kyc", "payments", "loans", "app_technical", "other"] = Field(
        description="Best-fit category for this issue, even if imperfect."
    )
    priority: Literal["low", "medium", "high"] = Field(
        description="high: blocks user from core functionality or involves money stuck. "
        "medium: annoying but not urgent. low: minor/cosmetic or informational."
    )
    summary: str = Field(description="One clear sentence summarizing the issue for a support agent.")
    suggested_owner: str = Field(
        description="Which team should handle this, e.g. 'KYC Team', 'Payments Ops', "
        "'Loans Team', 'App Engineering', 'General Support'."
    )


TICKET_PROMPT = """A user submitted a support query that didn't match any FAQ or require
escalation. Create a structured ticket for the support team.

User query: {query}
"""


def ticket_node(state: SupportState) -> SupportState:
    query = state["query"]

    llm = get_llm()
    structured_llm = llm.with_structured_output(SupportTicket)
    ticket: SupportTicket = structured_llm.invoke(TICKET_PROMPT.format(query=query))

    return {
        **state,
        "ticket": ticket.model_dump(),
        "response": (
            f"I've created a support ticket for your issue "
            f"(category: {ticket.category}, priority: {ticket.priority}). "
            f"Our {ticket.suggested_owner} will follow up with you shortly."
        ),
    }