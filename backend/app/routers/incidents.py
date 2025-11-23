from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database.db import incident_collection
from app.schemas.incident import IncidentRead

router = APIRouter(prefix="/incidents", tags=["incidents"])

@router.get("/", response_model=list[IncidentRead])
async def list_incidents(skip: int = 0, limit: int = 100):
    cursor = (
        incident_collection
        .find()
        .sort("timestamp", -1)
        .skip(skip)
        .limit(limit)
    )

    incidents = []
    async for incident in cursor:
        incident["id"] = str(incident["_id"])
        incidents.append(incident)

    return incidents


@router.get("/{incident_id}", response_model=IncidentRead)
async def get_incident(incident_id: str):
    try:
        oid = ObjectId(incident_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid incident ID")

    incident = await incident_collection.find_one({"_id": oid})

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    incident["id"] = str(incident["_id"])
    return incident
