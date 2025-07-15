from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from services.agent_registry_service import (
    create_agent,
    get_agent,
    update_agent,
    delete_agent,
    list_agents,
)
from models.pydantic.foundry_agent import FoundryAgentCreate, FoundryAgentRead
from typing import List

router = APIRouter(prefix="/agents", tags=["agent_registry"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FoundryAgentRead)
def create_agent_endpoint(agent_data: FoundryAgentCreate, db: Session = Depends(get_db)):
    return create_agent(db, agent_data)

@router.get("/{agent_id}", response_model=FoundryAgentRead)
def get_agent_endpoint(agent_id: str, db: Session = Depends(get_db)):
    return get_agent(db, agent_id)

@router.put("/{agent_id}", response_model=FoundryAgentRead)
def update_agent_endpoint(agent_id: str, agent_data: FoundryAgentCreate, db: Session = Depends(get_db)):
    return update_agent(db, agent_id, agent_data)

@router.delete("/{agent_id}")
def delete_agent_endpoint(agent_id: str, db: Session = Depends(get_db)):
    delete_agent(db, agent_id)
    return {"message": "Agent deleted successfully"}

@router.get("/", response_model=List[FoundryAgentRead])
def list_agents_endpoint(db: Session = Depends(get_db)):
    return list_agents(db)
