from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import Base, engine
from app.routers import analyze, incidents, stats

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fall Detection API",
    version="1.0.0",
)

# CORS so Flutter can call it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # later you can restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(analyze.router)
app.include_router(incidents.router)
app.include_router(stats.router)

@app.get("/")
def root():
    return {"message": "Fall Detection Backend is running 🚀"}
