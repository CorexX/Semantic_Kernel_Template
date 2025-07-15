# handoff_rule.py
from sqlalchemy import Column, String, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship
from core.database import Base

class HandoffRule(Base):
    __tablename__ = "handoff_rules"

    id           = Column(String, primary_key=True, index=True)
    agent_id     = Column(String, ForeignKey("foundry_agents.id"), nullable=False)
    trigger      = Column(String, nullable=False)   # z.B. "fallback", "timeout", "escalation"
    target_queue = Column(String, nullable=False)   # z.B. "support_queue"
    conditions   = Column(JSON, nullable=True)      # Freies JSON für Filter
    priority     = Column(Integer, default=0)

    agent        = relationship("FoundryAgent", back_populates="handoff_rules")
