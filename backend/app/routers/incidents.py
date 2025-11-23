from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.incident_model import Incident
from app.schemas.incident_schema import IncidentRead

router = APIRouter(prefix="/incidents", tags=["incidents"])

@router.get("/", response_model=List[IncidentRead])
def list_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return (
        db.query(Incident)
        .order_by(Incident.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.get("/{incident_id}", response_model=IncidentRead)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident
