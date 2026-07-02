// location: frontend/src/components/AgentDecisionPanel.jsx
// location: frontend/src/components/AgentDecisionPanel.jsx

const ROUTE_LABELS = {
    kb: { label: "Knowledge Base Agent", color: "#3ba55d" },
    escalation: { label: "Escalation Agent", color: "#e0a63c" },
    ticket: { label: "Ticket Creator Agent", color: "#e05c5c" },
    chitchat: { label: "Chitchat", color: "#5c7ce0" },
};

export default function AgentDecisionPanel({ lastResult }) {
    return (
        <div style={styles.container}>
            <h3 style={styles.heading}>Agent Decision</h3>

            {!lastResult && (
                <div style={styles.placeholder}>
                    Send a message to see which agent handles it.
                </div>
            )}

            {lastResult && (
                <>
                    <div style={styles.section}>
                        <div style={styles.label}>Route</div>
                        <div
                            style={{
                                ...styles.routeBadge,
                                backgroundColor: ROUTE_LABELS[lastResult.route]?.color || "#555",
                            }}
                        >
                            {ROUTE_LABELS[lastResult.route]?.label || lastResult.route}
                        </div>
                    </div>

                    <div style={styles.section}>
                        <div style={styles.label}>Latency</div>
                        <div style={styles.value}>{lastResult.latencyMs} ms</div>
                    </div>

                    {lastResult.kb_sources && lastResult.kb_sources.length > 0 && (
                        <div style={styles.section}>
                            <div style={styles.label}>KB Sources Used</div>
                            <div style={styles.value}>
                                {lastResult.kb_sources.join(", ")}
                            </div>
                        </div>
                    )}

                    {lastResult.ticket && (
                        <div style={styles.section}>
                            <div style={styles.label}>Ticket Created</div>
                            <pre style={styles.jsonBlock}>
                                {JSON.stringify(lastResult.ticket, null, 2)}
                            </pre>
                        </div>
                    )}

                    <div style={styles.section}>
                        <a
                            href="https://smith.langchain.com"
                            target="_blank"
                            rel="noreferrer"
                            style={styles.link}
                        >
                            View full trace in LangSmith →
                        </a>
                    </div>
                </>
            )}
        </div>
    );
}

const styles = {
    container: {
        padding: "16px",
        height: "100%",
        overflowY: "auto",
    },
    heading: {
        fontSize: "15px",
        fontWeight: 600,
        marginBottom: "16px",
        color: "#fff",
    },
    placeholder: {
        color: "#888",
        fontSize: "13px",
    },
    section: {
        marginBottom: "18px",
    },
    label: {
        fontSize: "11px",
        textTransform: "uppercase",
        letterSpacing: "0.05em",
        color: "#888",
        marginBottom: "6px",
    },
    value: {
        fontSize: "14px",
        color: "#eee",
    },
    routeBadge: {
        display: "inline-block",
        padding: "4px 10px",
        borderRadius: "6px",
        fontSize: "13px",
        fontWeight: 600,
        color: "#fff",
    },
    jsonBlock: {
        backgroundColor: "#1a1a1a",
        padding: "10px",
        borderRadius: "6px",
        fontSize: "12px",
        color: "#9fd8a0",
        overflowX: "auto",
    },
    link: {
        fontSize: "13px",
        color: "#3b6fed",
    },
};