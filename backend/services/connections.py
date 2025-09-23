

import json

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}  # user_id -> websocket

    async def connect(self, user_id, websocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id):
        self.active_connections.pop(user_id, None)

    async def send_to_user(self, user_id, message):
        ws = self.active_connections.get(user_id)
        if ws:
            await ws.send_text(message)

    async def send_message(self, user_id, message):
        await self.send_to_user(user_id, message)

    async def broadcast_to_session(self, session_participants, message):
        """Broadcast message to all participants in a session"""
        for user_id in session_participants:
            await self.send_to_user(user_id, message)

    async def notify_user_joined(self, session_participants, new_user_id, role):
        """Notify all participants that a new user joined"""
        notification = json.dumps({
            "type": "user_joined",
            "user_id": new_user_id,
            "role": role
        })
        for user_id in session_participants:
            if user_id != new_user_id:  # Don't notify the user about themselves
                await self.send_to_user(user_id, notification)
