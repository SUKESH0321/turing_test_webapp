import { useState, useEffect, useRef } from "react";
import { io } from "socket.io-client";

const socket = io("http://localhost:5000");

export default function Chat({ username }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  useEffect(() => {
    socket.on("receive_message", (msg) => {
      setMessages((prev) => [...prev, msg]);
    });
    return () => socket.off("receive_message");
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = () => {
    if (!input.trim()) return;
    const msg = { user: username, text: input, timestamp: new Date() };
    socket.emit("send_message", msg);
    setInput("");
  };

  return (
    <div style={styles.container}>
      <div style={styles.chatWindow}>
        <h2 style={styles.header}>Turing Chat</h2>
        <div style={styles.chatBox}>
          {messages.map((m, i) => (
            <div
              key={i}
              style={{
                ...styles.message,
                alignSelf: m.user === username ? "flex-end" : "flex-start",
                backgroundColor: m.user === username ? "#cce4ff" : "#e6f0ff",
              }}
            >
              <strong>{m.user}: </strong>
              {m.text}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <div style={styles.inputContainer}>
          <input
            style={styles.input}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button style={styles.button} onClick={sendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    backgroundColor: "#e6f7ff",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: "20px",
    boxSizing: "border-box",
  },
  chatWindow: {
    width: "80%",
    maxWidth: "1000px",
    height: "90vh",
    backgroundColor: "white",
    borderRadius: "16px",
    boxShadow: "0 8px 24px rgba(0,0,0,0.15)",
    display: "flex",
    flexDirection: "column",
    padding: "20px",
  },
  header: {
    textAlign: "center",
    color: "#0077cc",
    marginBottom: "20px",
    fontSize: "28px",
  },
  chatBox: {
    flexGrow: 1,
    border: "1px solid #cce4ff",
    borderRadius: "12px",
    padding: "15px",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    marginBottom: "15px",
  },
  message: {
    padding: "10px 15px",
    borderRadius: "16px",
    maxWidth: "70%",
    fontSize: "16px",
  },
  inputContainer: {
    display: "flex",
    gap: "10px",
  },
  input: {
    flexGrow: 1,
    padding: "12px",
    borderRadius: "12px",
    border: "1px solid #cce4ff",
    fontSize: "16px",
  },
  button: {
    padding: "12px 25px",
    borderRadius: "12px",
    border: "none",
    backgroundColor: "#0077cc",
    color: "white",
    fontSize: "16px",
    cursor: "pointer",
  },
};
