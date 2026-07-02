// location: frontend/src/api.js

const API_BASE = ["http://localhost:8000",
    "https://guptasandip-agentic-customer-support.hf.space"];

export async function sendMessage(sessionId, message) {
    const start = performance.now();

    const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, message }),
    });

    if (!res.ok) {
        throw new Error(`Request failed: ${res.status}`);
    }

    const data = await res.json();
    const latencyMs = Math.round(performance.now() - start);

    return { ...data, latencyMs };
}