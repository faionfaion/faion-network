"""
purpose: Pipeline with Pydantic schema + Hub validators + on-fail.
consumes: see AGENTS.md ## Prerequisites
produces: code
depends-on: content/02-output-contract.xml schema for guardrails-ai-framework
token-budget-impact: ≤500 tokens to fill
"""

# Guardrails AI pipeline: Pydantic schema (r1) + pinned Hub validators (r6) + explicit on_fail (r3).
# Requires: pip install "guardrails-ai>=0.5"
#           guardrails hub install hub://guardrails/detect_pii hub://guardrails/toxic_language
# LLM calls go through litellm: "gpt-4o-mini" reads OPENAI_API_KEY, "anthropic/<model-id>" reads ANTHROPIC_API_KEY.

from __future__ import annotations

import logging
from typing import Literal

from guardrails import Guard, OnFailAction
from guardrails.hub import DetectPII, ToxicLanguage
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

LLM_MODEL = "gpt-4o-mini"
MAX_REASKS = 3  # r2: hard cap; output contract allows 0..5

# Mirrors content/02-output-contract.xml; scripts/validate-guardrails-ai-framework.py reads this shape.
PIPELINE_CONFIG = {
    "pipeline_name": "support-reply",
    "schema_path": __file__,
    "validators": [
        {"id": "hub:DetectPII@0.0.3", "on_fail": "fix"},        # r4: PII is fix/filter, never noop
        {"id": "hub:ToxicLanguage@0.0.5", "on_fail": "refrain"},
    ],
    "on_fail_default": "reask",
    "max_reasks": MAX_REASKS,
}


class SupportReply(BaseModel):
    """r1: the typed contract every validator checks against."""

    reply: str = Field(
        description="Customer-facing answer, 1-3 sentences.",
        validators=[
            DetectPII(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail=OnFailAction.FIX),
            ToxicLanguage(threshold=0.5, validation_method="sentence", on_fail=OnFailAction.REFRAIN),
        ],
    )
    category: Literal["billing", "technical", "account", "other"]
    confidence: float = Field(ge=0.0, le=1.0)


guard = Guard.for_pydantic(output_class=SupportReply)


def _log_validator_failures(reask_count: int) -> None:
    """r5: validator_id + reason + reask_count for every failed validation."""
    call = guard.history.last
    if call is None:
        return
    for iteration in call.iterations:
        for entry in iteration.validator_logs:
            result = entry.validation_result
            if result is not None and result.outcome == "fail":
                logger.warning(
                    "validator=%s field=%s reason=%s reask_count=%d",
                    entry.validator_name, entry.property_path, result.error_message, reask_count,
                )


def run(ticket_text: str) -> SupportReply | None:
    """Validated SupportReply, or None when a refrain validator or the reask cap stops the call."""
    outcome = guard(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "You are a support agent. Answer the ticket as JSON per the schema."},
            {"role": "user", "content": ticket_text},
        ],
        num_reasks=MAX_REASKS,
        temperature=0,
    )
    reask_count = max(0, len(guard.history.last.iterations) - 1) if guard.history.last else 0
    _log_validator_failures(reask_count)
    if not outcome.validation_passed or outcome.validated_output is None:
        logger.error("pipeline=%s refused after %d reasks: %s",
                     PIPELINE_CONFIG["pipeline_name"], reask_count, outcome.error)
        return None
    return SupportReply.model_validate(outcome.validated_output)


if __name__ == "__main__":
    import sys

    result = run(sys.argv[1] if len(sys.argv) > 1 else "My invoice from last month is wrong, can you check?")
    print(result.model_dump_json(indent=2) if result else "refrained")
