import json
from .connections import ConnectionManager

class Session:
    def __init__(self, session_id, judge_id):
        self.session_id = session_id
        self.judge_id = judge_id
        self.human_id = None
        self.ai_id = None
        self.state = "pending"

    def add_participant(self, role, user_id):
        if role == "human":
            self.human_id = user_id
        elif role == "ai":
            self.ai_id = user_id
        elif role == "judge":
            self.judge_id = user_id
        self._update_state()

    def _update_state(self):
        if self.human_id and self.ai_id and self.judge_id:
            self.state = "active"
        elif (self.human_id or self.ai_id) and self.judge_id:
            self.state = "waiting"

    def get_all_participants(self):
        """Get list of all participants in the session"""
        participants = []
        if self.judge_id:
            participants.append(self.judge_id)
        if self.human_id:
            participants.append(self.human_id)
        if self.ai_id:
            participants.append(self.ai_id)
        return participants

    async def route_message(self, sender_id, message, manager: ConnectionManager):
        try:
            # Parse the message if it's JSON
            data = json.loads(message)
            message_type = data.get("type", "chat")
            content = data.get("content", message)
        except json.JSONDecodeError:
            # If it's not JSON, treat as plain text
            message_type = "chat"
            content = message

        if message_type == "chat":
            await self._handle_chat_message(sender_id, content, manager)
        elif message_type == "typing":
            await self._handle_typing_notification(sender_id, data.get("is_typing", False), manager)

    async def _handle_chat_message(self, sender_id, content, manager: ConnectionManager):
        # Determine sender role
        sender_role = "unknown"
        if sender_id == self.human_id:
            sender_role = "human"
        elif sender_id == self.ai_id:
            sender_role = "ai"
        elif sender_id == self.judge_id:
            sender_role = "judge"

        message_data = json.dumps({
            "type": "message",
            "sender_id": sender_id,
            "sender_role": sender_role,
            "content": content,
            "timestamp": str(int(__import__('time').time()))
        })

        # TURING TEST LOGIC: Only Judge communicates with AI and Human
        # AI and Human NEVER communicate directly with each other
        
        if sender_id == self.judge_id:
            # Judge messages go to BOTH AI and Human
            if self.human_id:
                await manager.send_to_user(self.human_id, message_data)
            if self.ai_id:
                await manager.send_to_user(self.ai_id, message_data)
        
        elif sender_id == self.human_id:
            # Human messages go ONLY to Judge (never to AI)
            if self.judge_id:
                await manager.send_to_user(self.judge_id, message_data)
        
        elif sender_id == self.ai_id:
            # AI messages go ONLY to Judge (never to Human)
            if self.judge_id:
                await manager.send_to_user(self.judge_id, message_data)

    async def _handle_typing_notification(self, sender_id, is_typing, manager: ConnectionManager):
        # Determine sender role
        sender_role = "unknown"
        if sender_id == self.human_id:
            sender_role = "human"
        elif sender_id == self.ai_id:
            sender_role = "ai"
        elif sender_id == self.judge_id:
            sender_role = "judge"

        typing_data = json.dumps({
            "type": "typing",
            "sender_id": sender_id,
            "sender_role": sender_role,
            "is_typing": is_typing
        })

        # TURING TEST TYPING LOGIC: Only show typing to Judge
        # AI and Human should not see each other's typing indicators
        
        if sender_id == self.judge_id:
            # Judge typing goes to both AI and Human
            if self.human_id:
                await manager.send_to_user(self.human_id, typing_data)
            if self.ai_id:
                await manager.send_to_user(self.ai_id, typing_data)
        
        elif sender_id == self.human_id:
            # Human typing goes only to Judge
            if self.judge_id:
                await manager.send_to_user(self.judge_id, typing_data)
        
        elif sender_id == self.ai_id:
            # AI typing goes only to Judge
            if self.judge_id:
                await manager.send_to_user(self.judge_id, typing_data)
