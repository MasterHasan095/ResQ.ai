from fastapi import APIRouter
from app.database import users_collection

router = APIRouter()

@router.get("/test-db")
async def test_db():
    doc = await users_collection.insert_one({"test": "ok"})
    return {"inserted_id": str(doc.inserted_id)}
