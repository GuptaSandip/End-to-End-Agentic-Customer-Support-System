"""
Step 4:
Wire the graph together:
LangGraph StateGraph wiring supervisor to the three condition branches
"""
from langgraph.graph import StateGraph, END
from app.graph.state import SupportState
from app.graph.supervisor import supervisor_node, route_selector
from app.graph.kb_agent import kb_node
from app.graph.escalation_agent import escalation_node
from app.graph.ticket_agent import ticket_node
from app.graph.chitchat_agent import chitchat_node


def build_graph():
    graph = StateGraph(SupportState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("kb", kb_node)
    graph.add_node("escalation", escalation_node)
    graph.add_node("ticket", ticket_node)
    graph.add_node("chitchat", chitchat_node)

    graph.set_entry_point("supervisor")

    graph.add_conditional_edges(
        "supervisor",
        route_selector,
        {
            "kb": "kb",
            "escalation": "escalation",
            "ticket": "ticket",
            "chitchat": "chitchat",
        },
    )

    graph.add_edge("kb", END)
    graph.add_edge("escalation", END)
    graph.add_edge("ticket", END)
    graph.add_edge("chitchat", END)

    return graph.compile()


if __name__ == "__main__":
    app_graph = build_graph()

    test_queries = [
        "How long does KYC verification take?",
        "Someone made an unauthorized transaction on my account, I'm panicking, please help",
        "asdkjasd random gibberish issue",
        "My EMI payment failed, what happens now?",
    ]

    for q in test_queries:
        print(f"\nQuery: {q}")
        result = app_graph.invoke({"query": q, "route": None, "response": None, "ticket": None, "kb_sources": None})
        print(f"  Route: {result['route']}")
        print(f"  Response: {result.get('response')}")
        print(f"  KB Sources: {result.get('kb_sources')}")
        print(f"  Ticket: {result.get('ticket')}")