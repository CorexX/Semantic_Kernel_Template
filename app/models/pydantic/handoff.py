# handoff.py
from pydantic import BaseModel, Field
from typing import Any

class HandoffRuleItem(BaseModel):
    trigger: str = Field(..., example="fallback")
    target_queue: str = Field(..., example="support_queue")
    conditions: dict[str, Any] | None = Field(None, example={"min_confidence":0.7})
    priority: int = Field(0, example=10)