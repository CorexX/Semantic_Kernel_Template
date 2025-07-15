from dataclasses import dataclass
from datetime import datetime
from typing import List
from models.domain.handoff_rule import HandoffRule

@dataclass
class FoundryAgent:
    id: str
    name: str
    description: str | None
    resource_name: str
    deployment_name: str
    endpoint_url: str
    auth_key: str
    default_language: str
    handoff_enabled: bool
    created_at: datetime
    updated_at: datetime
    handoff_rules: List[HandoffRule]