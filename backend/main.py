from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from services.session import Session
from services.connections import ConnectionManager
import json
import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()
sessions = {}

AI_SERVICE_URL = "http://localhost:3001/api/ai/join"

async def trigger_ai_join(session_id: str):
    """Automatically trigger AI to join the session"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                AI_SERVICE_URL,
                json={
                    "session_id": session_id,
                    "websocket_url": f"ws://localhost:8000/ws/{session_id}"
                },
                timeout=10.0
            )
            if response.status_code == 200:
                print(f"AI service notified for session {session_id}")
            else:
                print(f"Failed to notify AI service: {response.status_code}")
    except Exception as e:
        print(f"Error triggering AI join: {e}")

@app.get("/")
async def root():
    return {"message": "Turing Test Backend API"}

@app.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """Get information about a session"""
    if session_id in sessions:
        session = sessions[session_id]
        return {
            "session_id": session.session_id,
            "state": session.state,
            "judge_id": session.judge_id,
            "human_id": session.human_id,
            "ai_id": session.ai_id
        }
    return {"error": "Session not found"}

@app.websocket("/ws/{session_id}/{user_id}/{role}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, user_id: str, role: str):
    await manager.connect(user_id, websocket)

    if session_id not in sessions:
        sessions[session_id] = Session(session_id, judge_id=None)

    session = sessions[session_id]
    
    session.add_participant(role, user_id)
    
    if role == "human" and not session.ai_id:
        asyncio.create_task(trigger_ai_join(session_id))
    
    await manager.notify_user_joined(session.get_all_participants(), user_id, role)
    
    session_state = json.dumps({
        "type": "session_state",
        "session_id": session_id,
        "state": session.state,
        "your_role": role,
        "participants": {
            "judge": session.judge_id,
            "human": session.human_id,
            "ai": session.ai_id
        }
    })
    await manager.send_to_user(user_id, session_state)

    try:
        while True:
            data = await websocket.receive_text()
            await session.route_message(user_id, data, manager)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        leave_notification = json.dumps({
            "type": "user_left",
            "user_id": user_id,
            "role": role
        })
        for participant_id in session.get_all_participants():
            if participant_id != user_id:
                await manager.send_to_user(participant_id, leave_notification)
