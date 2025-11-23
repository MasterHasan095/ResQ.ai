from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import analyze, incidents, stats


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Fall Detector Backend",
        version="0.1.0",
        description="Backend for the AI Fall Detector / First Responder system."
    )

    # CORS so Flutter can call backend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],   # in production, we restrict this
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(analyze.router, prefix="/analyze", tags=["Analyze"])
    app.include_router(incidents.router, prefix="/incidents", tags=["Incidents"])
    app.include_router(stats.router, prefix="/stats", tags=["Stats"])

    return app


app = create_app()
