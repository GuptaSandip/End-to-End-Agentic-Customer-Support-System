// location: frontend/src/components/ChatPanel.jsx

import { useState, useRef, useEffect } from "react";

export default function ChatPanel({ messages, onSend, loading }) {
    const [input, setInput] = useState("");
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!input.trim() || loading) return;
        onSend(input.trim());
        setInput("");
    };

    return (
        <div style={styles.container}>
            <div style={styles.messages}>
                {messages.length === 0 && (
                    <div style={styles.placeholder}>
                        Ask something like "How long does KYC take?" or "Someone made an
                        unauthorized transaction on my account"
                    </div>
                )}
                {messages.map((m, i) => (
                    <div key={i} style={styles.messageRow(m.role)}>
                        <div style={styles.bubble(m.role)}>{m.text}</div>
                    </div>
                ))}
                {loading && (
                    <div style={styles.messageRow("assistant")}>
                        <div style={styles.bubble("assistant")}>Thinking...</div>
                    </div>
                )}
                <div ref={bottomRef} />
            </div>

            <form onSubmit={handleSubmit} style={styles.form}>
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your support question..."
                    style={styles.input}
                    disabled={loading}
                />
                <button type="submit" style={styles.button} disabled={loading}>
                    Send
                </button>
            </form>
        </div>
    );
}

const styles = {
    container: {
        display: "flex",
        flexDirection: "column",
        height: "100%",
        borderRight: "1px solid #2a2a2a",
    },
    messages: {
        flex: 1,
        overflowY: "auto",
        padding: "16px",
        display: "flex",
        flexDirection: "column",
        gap: "10px",
    },
    placeholder: {
        color: "#888",
        fontSize: "14px",
        textAlign: "center",
        marginTop: "40px",
    },
    messageRow: (role) => ({
        display: "flex",
        justifyContent: role === "user" ? "flex-end" : "flex-start",
    }),
    bubble: (role) => ({
        maxWidth: "75%",
        padding: "10px 14px",
        borderRadius: "12px",
        fontSize: "14px",
        lineHeight: 1.4,
        backgroundColor: role === "user" ? "#3b6fed" : "#2a2a2a",
        color: "#fff",
    }),
    form: {
        display: "flex",
        gap: "8px",
        padding: "12px",
        borderTop: "1px solid #2a2a2a",
    },
    input: {
        flex: 1,
        padding: "10px 12px",
        borderRadius: "8px",
        border: "1px solid #333",
        backgroundColor: "#1a1a1a",
        color: "#fff",
        fontSize: "14px",
    },
    button: {
        padding: "10px 18px",
        borderRadius: "8px",
        border: "none",
        backgroundColor: "#3b6fed",
        color: "#fff",
        fontWeight: 600,
        cursor: "pointer",
    },
};