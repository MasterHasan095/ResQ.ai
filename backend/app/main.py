import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.core.websocket_manager import manager
from app.core.detector_loop import detection_loop   # ⬅️ new
from app.routers import analyze, incidents, stats, test_db, ws


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI First Responder API",
        version="0.1.0",
        description="Backend for the AI Fall Detector / First Responder system."
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],   # TODO: Restrict in production
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(analyze.router, prefix="/analyze", tags=["Analyze"])
    app.include_router(incidents.router, prefix="/incidents", tags=["Incidents"])
    app.include_router(stats.router, prefix="/stats", tags=["Stats"])
    app.include_router(test_db.router, prefix="/test", tags=["Test"])
    app.include_router(ws.router)

    return app


app = create_app()


@app.on_event("startup")
async def start_detection_loop():
    loop = asyncio.get_running_loop()
    loop.create_task(detection_loop())
    print("✅ Detection loop started")


@app.websocket("/ws/falls")
async def falls_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


@app.get("/health")
def health_check():
    return {"status": "ok"}
