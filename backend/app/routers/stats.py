from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.incident_model import Incident
from app.schemas.stats_schema import StatsResponse, FallsByDate

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    total_incidents = db.query(func.count(Incident.id)).scalar() or 0

    today_start = datetime.combine(date.today(), datetime.min.time())
    tomorrow_start = today_start + timedelta(days=1)

    falls_today = (
        db.query(func.count(Incident.id))
        .filter(
            Incident.timestamp >= today_start,
            Incident.timestamp < tomorrow_start,
            Incident.fall_detected == True,
        )
        .scalar()
        or 0
    )

    rows = (
        db.query(
            func.date(Incident.timestamp).label("date"),
            func.count(Incident.id).label("count"),
        )
        .filter(Incident.fall_detected == True)
        .group_by(func.date(Incident.timestamp))
        .order_by(func.date(Incident.timestamp))
        .all()
    )

    falls_by_date = [FallsByDate(date=str(r.date), count=r.count) for r in rows]

    return StatsResponse(
        total_incidents=total_incidents,
        falls_today=falls_today,
        falls_by_date=falls_by_date,
    )
