"""Critic structured-output schema for bounded generator-critic loops.

The critic MUST return all three fields. should_continue is the primary
signal — score and feedback are diagnostics for the next generator turn.
"""
from pydantic import BaseModel, Field


class CriticVerdict(BaseModel):
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Quality score in [0, 1]. Used for plateau detection across iterations.",
    )
    should_continue: bool = Field(
        ...,
        description=(
            "True if another generator iteration is likely to improve the output. "
            "False when the output meets the rubric or further work yields diminishing returns."
        ),
    )
    feedback: str = Field(
        ...,
        max_length=600,
        description=(
            "Concise actionable feedback the next generator turn must address. "
            "Empty when should_continue is False."
        ),
    )
