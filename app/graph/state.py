"""
Step 1:
Shared state schema:
LangGraph shared state schema for the support system
"""
from typing import Optional, Literal
from typing_extensions import TypedDict


class SupportState(TypedDict):
    query: str
    chat_history: Optional[str]
    route: Optional[Literal["kb", "escalation", "ticket","chitchat"]]
    response: Optional[str]
    ticket: Optional[dict]
    kb_sources: Optional[list]