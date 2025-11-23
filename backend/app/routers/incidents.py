from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_incidents():
    # placeholder until DB is wired
    return {"incidents": []}
