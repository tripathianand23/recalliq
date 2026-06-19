from __future__ import annotations

from datetime import datetime
from typing import Any, List

from pydantic import BaseModel


class InteractionCreate(BaseModel):
    prospect_name: str
    company: str
    role_title: str
    interaction_type: str
    meeting_notes: str

    objections: List[str] = []
    competitors: List[str] = []
    decision_makers: List[str] = []

    budget: str = ""
    timeline: str = ""
    next_steps: str = ""
    deal_id: str = ""


class Interaction(InteractionCreate):
    id: int
    prospect_id: int
    created_at: datetime


class Prospect(BaseModel):
    id: int
    name: str
    company: str
    role_title: str
    deal_id: str
    created_at: datetime
    updated_at: datetime


class MemoryActivity(BaseModel):
    id: int
    operation: str
    prospect_name: str
    company: str
    deal_id: str
    tags: list[str]
    content: str
    result: str
    provider: str
    fallback_mode: bool
    created_at: datetime


class GeneratedResponse(BaseModel):
    prospect: Prospect
    memory_mode: str
    memory_source: str
    memory_warning: str | None = None
    recalled_memories: list[dict[str, Any]]
    content: str


class DashboardStats(BaseModel):
    prospects: int
    interactions: int
    retained_memories: int
    top_objections: list[dict[str, Any]]
    recent_activity: list[MemoryActivity]
    fallback_mode: bool
    memory_health: dict[str, Any]


class Health(BaseModel):
    status: str
    memory_mode: str


class MemoryHealth(BaseModel):
    hindsight_enabled: bool
    configured: bool
    reachable: bool
    bank_id: str | None = None
    fallback_enabled: bool
    last_error: str | None = None
    memory_mode: str
