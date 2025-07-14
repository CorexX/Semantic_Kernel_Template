# foundry_agent.py
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import List
from app.models.pydantic.handoff import HandoffRuleItem

class FoundryAgentCreate(BaseModel):
    name: str = Field(..., example="SalesBot")
    description: str | None = Field(None, example="Betreut Vertriebsanfragen")
    resource_name: str = Field(..., example="my-foundry-resource")
    deployment_name: str = Field(..., example="sales-deployment")
    endpoint_url: HttpUrl
    auth_key: str
    default_language: str = Field("en")
    handoff_enabled: bool = Field(False)
    handoff_rules: List[HandoffRuleItem] = []

class FoundryAgentRead(FoundryAgentCreate):
    id: str
    created_at: datetime
    updated_at: datetime