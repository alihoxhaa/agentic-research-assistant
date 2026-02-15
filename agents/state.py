from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class AgentTrace(BaseModel):
    step: str
    agent: str
    action: str
    outcome: str


class AgentState(BaseModel):
    # User input
    task: str

    # Planner output
    plan: Optional[List[str]] = None

    # Research agent output
    notes: Optional[List[str]] = None
    citations: Optional[List[Dict[str, str]]] = None

    # Writer output
    draft: Optional[str] = None

    # Verifier output
    verifier_feedback: Optional[str] = None

    # Final result
    final_output: Optional[str] = None

    # Errors / safety
    errors: Optional[List[str]] = Field(default_factory=list)

    # Traceability
    trace: List[AgentTrace] = Field(default_factory=list)

    # Retry control (to stabilize verifier variance)
    retried: bool = False
