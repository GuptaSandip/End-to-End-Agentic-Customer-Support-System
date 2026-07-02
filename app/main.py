# location: app/main.py
# location: app/main.py

from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.graph.build_graph import build_graph

app = FastAPI(title="Agentic Customer Support System")

# Allow the React dev server to call this API during local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compile the graph once at startup, not per-request
support_graph = build_graph()

# Simple in-memory session store: session_id -> list of {query, response} turns
# Fine for a demo; swap for Redis/DB if this ever needs to survive a restart.
session_store: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    route: str
    kb_sources: Optional[list] = None
    ticket: Optional[dict] = None


@app.get("/health")
def health():
    return {"status": "ok"}


def format_history(turns: list[dict], max_turns: int = 4) -> str:
    """Formats the last N turns as a simple transcript for context."""
    recent = turns[-max_turns:]
    if not recent:
        return ""
    lines = []
    for t in recent:
        lines.append(f"User: {t['query']}")
        lines.append(f"Assistant: {t['response']}")
    return "\n".join(lines)


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    prior_turns = session_store.get(req.session_id, [])
    history_str = format_history(prior_turns)

    initial_state = {
        "query": req.message,
        "chat_history": history_str,
        "route": None,
        "response": None,
        "ticket": None,
        "kb_sources": None,
    }

    result = support_graph.invoke(initial_state)

    # Track the turn in session history (for future multi-turn context / demo display)
    session_store.setdefault(req.session_id, []).append(
        {"query": req.message, "response": result.get("response")}
    )

    return ChatResponse(
        response=result.get("response") or "",
        route=result.get("route"),
        kb_sources=result.get("kb_sources"),
        ticket=result.get("ticket"),
    )


@app.get("/history/{session_id}")
def get_history(session_id: str):
    return {"session_id": session_id, "history": session_store.get(session_id, [])}