from fastapi import APIRouter
from datetime import datetime, timedelta
from app.database import incident_collection
from app.schemas.stats_schema import StatsResponse, FallsByDate
from bson import ObjectId

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/", response_model=StatsResponse)
async def get_stats():
    # Total number of incidents
    total_incidents = await incident_collection.count_documents({})

    # Falls today
    today_start = datetime.combine(datetime.today(), datetime.min.time())
    tomorrow_start = today_start + timedelta(days=1)

    falls_today = await incident_collection.count_documents({
        "timestamp": {"$gte": today_start, "$lt": tomorrow_start},
        "fall_detected": True
    })

    # Falls by date (group by day)
    pipeline = [
        {"$match": {"fall_detected": True}},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}},
    ]

    rows = await incident_collection.aggregate(pipeline).to_list(length=None)

    falls_by_date = [
        FallsByDate(date=row["_id"], count=row["count"])
        for row in rows
    ]

    return StatsResponse(
        total_incidents=total_incidents,
        falls_today=falls_today,
        falls_by_date=falls_by_date
    )
