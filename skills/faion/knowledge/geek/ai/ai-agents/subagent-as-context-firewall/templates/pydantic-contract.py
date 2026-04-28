from pydantic import BaseModel, Field
from typing import Literal

class SubagentReport(BaseModel):
    summary: str = Field(description="3-5 sentences. What you found, what matters.")
    refs: list[str] = Field(description="paths/URLs/IDs the parent should re-load.")
    follow_up_questions: list[str] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"]
