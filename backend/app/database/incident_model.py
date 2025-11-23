# backend/app/database/incident_model.py

from datetime import datetime
from sqlalchemy import Column, Integer, Float, Boolean, String, DateTime

from .db import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    fall_detected = Column(Boolean, default=False, index=True)
    confidence = Column(Float, nullable=False)

    severity = Column(String, nullable=True)
    device_id = Column(String, nullable=True)
