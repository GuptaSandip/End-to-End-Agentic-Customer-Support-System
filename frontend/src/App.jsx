// location: frontend/src/App.jsx

import { useState } from "react";
import ChatPanel from "./components/ChatPanel";
import AgentDecisionPanel from "./components/AgentDecisionPanel";
import { sendMessage } from "./api";

const SESSION_ID = "demo-session-1"; // fine for a single-user demo

export default function App() {
  const [messages, setMessages] = useState([]);
  const [lastResult, setLastResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSend = async (text) => {
    setMessages((prev) => [...prev, { role: "user", text }]);
    setLoading(true);

    try {
      const result = await sendMessage(SESSION_ID, text);
      setMessages((prev) => [...prev, { role: "assistant", text: result.response }]);
      setLastResult(result);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Something went wrong reaching the backend." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.app}>
      <div style={styles.header}>Agentic Customer Support System</div>
      <div style={styles.body}>
        <div style={styles.chatColumn}>
          <ChatPanel messages={messages} onSend={handleSend} loading={loading} />
        </div>
        <div style={styles.sidePanel}>
          <AgentDecisionPanel lastResult={lastResult} />
        </div>
      </div>
    </div>
  );
}

const styles = {
  app: {
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    backgroundColor: "#111",
    color: "#fff",
    fontFamily: "system-ui, sans-serif",
  },
  header: {
    padding: "14px 20px",
    fontSize: "16px",
    fontWeight: 600,
    borderBottom: "1px solid #2a2a2a",
  },
  body: {
    display: "flex",
    flex: 1,
    minHeight: 0,
  },
  chatColumn: {
    flex: 2,
    minWidth: 0,
  },
  sidePanel: {
    flex: 1,
    minWidth: "280px",
    backgroundColor: "#161616",
  },
};