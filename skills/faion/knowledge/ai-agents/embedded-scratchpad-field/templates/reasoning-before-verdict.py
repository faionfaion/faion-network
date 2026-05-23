# purpose: Pydantic schema with reasoning declared before confidence + decision
# consumes: subject text + criteria
# produces: Verdict instance after model_validate_json
# depends-on: pydantic v2
# token-budget-impact: schema serialisation ~150 tokens
"""Reasoning-before-verdict template.

Schema field order = autoregressive generation order. The reasoning field
appears first so the model writes its working notes before committing to
confidence and decision. Strict mode + this schema reliably lifts accuracy
on multi-criteria decision tasks vs an answer-only schema.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Verdict(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reasoning: str = Field(
        description=(
            "Step-by-step analysis of the input against each criterion. "
            "Cap at 200 words. Cover: which criteria are met, which are "
            "borderline, which are missed."
        ),
        min_length=4,
        max_length=2000,
    )
    confidence: Literal["low", "medium", "high"] = Field(
        description="Confidence in the decision below; medium if any criterion is borderline."
    )
    decision: Literal["approve", "reject"] = Field(
        description="Final call. Must follow from reasoning above."
    )
