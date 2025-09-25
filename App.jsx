import Chat from "./components/Chat";
import { useState } from "react";

function App() {
  const [username, setUsername] = useState("");
  const [entered, setEntered] = useState(false);

  return (
    <div style={styles.app}>
      {!entered ? (
        <div style={styles.loginBox}>
          <h2 style={{ color: "#0077cc", fontSize: "32px" }}>
            Enter your name to join
          </h2>
          <input
            style={styles.input}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Your name"
          />
          <button
            style={styles.button}
            onClick={() => username && setEntered(true)}
          >
            Join
          </button>
        </div>
      ) : (
        <Chat username={username} />
      )}
    </div>
  );
}

const styles = {
  app: {
    minHeight: "100vh",
    backgroundColor: "#e6f7ff",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontFamily: "Arial, sans-serif",
  },
  loginBox: {
    backgroundColor: "white",
    padding: "50px",
    borderRadius: "16px",
    boxShadow: "0 8px 24px rgba(0,0,0,0.15)",
    textAlign: "center",
    width: "400px",
  },
  input: {
    padding: "12px",
    width: "100%",
    marginBottom: "20px",
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

export default App;
