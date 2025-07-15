# foundry_agent.py
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from core.database import Base
import datetime

class FoundryAgent(Base):
    __tablename__ = "foundry_agents"

    id              = Column(String, primary_key=True, index=True)
    name            = Column(String, unique=True, nullable=False)
    description     = Column(String, nullable=True)
    resource_name   = Column(String, nullable=False)    # Azure Resource Name
    deployment_name = Column(String, nullable=False)    # Foundry Deployment
    endpoint_url    = Column(String, nullable=False)
    auth_key        = Column(String, nullable=False)
    default_language= Column(String, default="en")
    handoff_enabled = Column(Boolean, default=False)

    created_at      = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at      = Column(
                        DateTime,
                        default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow,
                     )

    handoff_rules   = relationship(
                        "HandoffRule",
                        back_populates="agent",
                        cascade="all, delete-orphan"
                      )
