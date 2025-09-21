# filename: main.py
import requests
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"  # Replace with your OpenRouter API key

app = FastAPI()

# Allow frontend to connect (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to call GPT API
def fetch_gpt_response(prompt: str) -> str:
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        result = response.json()
        if "choices" in result and result["choices"]:
            # Extract the assistant's message content
            return result["choices"][0]["message"]["content"]
        elif "error" in result:
            return f"Error: {result['error'].get('message', 'Unknown error')}"
        else:
            return "Unknown response format from API."
    except Exception as e:
        return f"Request failed: {e}"

# WebSocket endpoint for real-time chat
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            user_message = await websocket.receive_text()
            gpt_response = fetch_gpt_response(user_message)

            # Stream response word by word
            words = gpt_response.split()
            streaming_text = ""
            for word in words:
                streaming_text += word + " "
                await websocket.send_text(streaming_text.strip())
                await asyncio.sleep(0.05)  # simulate typing delay
    except WebSocketDisconnect:
        print("Client disconnected")
