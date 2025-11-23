from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_stats():
    return {
        "total_incidents": 0,
        "falls_today": 0,
        "falls_by_date": []
    }
