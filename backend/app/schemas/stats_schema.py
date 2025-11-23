# backend/app/schemas/stats_schema.py

from typing import List
from pydantic import BaseModel


class FallsByDate(BaseModel):
    date: str        # "2025-11-23"
    count: int       # number of falls that day


class StatsResponse(BaseModel):
    total_incidents: int
    falls_today: int
    falls_by_date: List[FallsByDate]
