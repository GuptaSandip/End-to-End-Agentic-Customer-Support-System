"""
Step 3:
 Stub worker nodes (placeholders — we'll build these out on Day 4/5):
 Temporary stub nodes so graph can be tested ent to end.
"""

from app.graph.state import SupportState


def kb_node_stub(state: SupportState) -> SupportState:
    return {**state, "response": "[KB STUB] Would answer from FAQ knowledge base here."}


def escalation_node_stub(state: SupportState) -> SupportState:
    return {**state, "response": "[ESCALATION STUB] Would draft empathetic escalation response here."}


def ticket_node_stub(state: SupportState) -> SupportState:
    return {**state, "ticket": {"category": "unclassified", "summary": state["query"]}}