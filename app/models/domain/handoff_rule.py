# handoff_rule.py
from dataclasses import dataclass
from typing import Any

@dataclass
class HandoffRule:
    id: str
    trigger: str
    target_queue: str
    conditions: dict[str, Any] | None
    priority: int