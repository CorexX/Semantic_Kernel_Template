from sqlalchemy.orm import Session
from models.orm.foundry_agent import FoundryAgent
from models.pydantic.foundry_agent import FoundryAgentCreate
from typing import List, Optional
import uuid
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

def create_agent(db: Session, agent_data: FoundryAgentCreate) -> FoundryAgent:
    new_agent = FoundryAgent(id=str(uuid.uuid4()), **agent_data.dict())
    try:
        db.add(new_agent)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Agent with this name already exists.")
    db.refresh(new_agent)
    return new_agent

def get_agent(db: Session, agent_id: str) -> FoundryAgent:
    agent = db.query(FoundryAgent).filter(FoundryAgent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

def update_agent(db: Session, agent_id: str, agent_data: FoundryAgentCreate) -> FoundryAgent:
    agent = get_agent(db, agent_id)
    for key, value in agent_data.dict().items():
        setattr(agent, key, value)
    db.commit()
    db.refresh(agent)
    return agent

def delete_agent(db: Session, agent_id: str) -> None:
    agent = get_agent(db, agent_id)
    db.delete(agent)
    db.commit()

def list_agents(db: Session) -> List[FoundryAgent]:
    return db.query(FoundryAgent).all()
