from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict

router = APIRouter(prefix="/agents", tags=["agent_registry"])

class AgentRegistryRequest(BaseModel):
    agent_id: str
    metadata: Dict[str, str]


@router.post("/register")
def register_agent(req: AgentRegistryRequest):
    return {"message": "Agent registered successfully", "agent_id": req.agent_id, "metadata": req.metadata}
