# Canonical agent pipeline output schema
# Usage: import AgentTaskResult and use as response_format in StructuredOutputService

from pydantic import BaseModel, Field
from typing import Optional, Literal, List


class AgentTaskResult(BaseModel):
    """Standard output contract for agent pipeline steps.

    All agents in the pipeline should return this schema so the orchestrator
    can make routing decisions based on status and next_action.
    """
    status: Literal["success", "partial", "failed"]
    output: str = Field(description="Primary result text from this step")
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="Agent's confidence in the output. 0.0=none, 1.0=certain")
    missing_data: List[str] = Field(
        default_factory=list,
        description="List of data items the agent could not extract or compute")
    next_action: Optional[str] = Field(
        default=None,
        description="Recommended follow-up action for the orchestrator, "
                    "or null if this step is complete")
