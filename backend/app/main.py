from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from app.routers import analyze, incidents, stats, test_db


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI First Responder API",
        version="0.1.0",
        description="Backend for the AI Fall Detector / First Responder system."
    )

    # CORS for Flutter and local testing
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],   # TODO: Restrict in production
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(analyze.router, prefix="/analyze", tags=["Analyze"])
    app.include_router(incidents.router, prefix="/incidents", tags=["Incidents"])
    app.include_router(stats.router, prefix="/stats", tags=["Stats"])
    app.include_router(test_db.router, prefix="/test", tags=["Test"])

    return app


app = create_app()


@app.get("/health")
def health_check():
    return {"status": "ok"}
