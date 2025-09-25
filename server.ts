import express from "express";
import { createServer } from "http";
import { Server } from "socket.io";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

const httpServer = createServer(app);

// Initialize Socket.IO
const io = new Server(httpServer, {
  cors: { origin: "*" }, // allow all origins, adjust in production
});

// WebSocket connection
io.on("connection", (socket) => {
  console.log("User connected:", socket.id);

  // Listen for messages from clients
  socket.on("send_message", (data) => {
    // Broadcast to everyone
    io.emit("receive_message", data);
  });

  // Disconnect event
  socket.on("disconnect", () => {
    console.log("User disconnected:", socket.id);
  });
});

// Basic HTTP route
app.get("/", (req, res) => {
  res.send("Turing Chat Backend Running");
});

// Start server
const PORT = 5000;
httpServer.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
