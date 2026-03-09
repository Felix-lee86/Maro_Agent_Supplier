import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from typing import List

app = FastAPI()

# CORS 설정 (React 연동)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 실시간 로그 저장을 위한 큐
log_queue = asyncio.Queue()

@app.get("/logs/recent")
async def get_recent_logs():
    # 시뮬레이션: 최근 로그 리턴 (실제 파일/DB 연동 가능)
    return [
        {"timestamp": "17:10:01", "type": "SYSTEM", "message": "Dashboard API Server Started."},
        {"timestamp": "17:10:05", "type": "KIM", "message": "CEO Room Monitoring Active."}
    ]

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            log_entry = await log_queue.get()
            await websocket.send_text(json.dumps(log_entry))
    except Exception as e:
        print(f"WS Disconnected: {e}")

def start_api_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_api_server()
