"""
purpose: Skeleton for a custom validator subclass.
consumes: see AGENTS.md ## Prerequisites
produces: code
depends-on: content/02-output-contract.xml schema for guardrails-ai-framework
token-budget-impact: ≤500 tokens to fill
"""

# Custom Guardrails validator: register once, attach to a Pydantic field or a Guard like a Hub validator.
# Requires: pip install "guardrails-ai>=0.5"

from __future__ import annotations

import logging
import re
from typing import Any, Callable

from guardrails import Guard, OnFailAction
from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

logger = logging.getLogger(__name__)


@register_validator(name="<org>/no_competitor_mention", data_type="string")
class NoCompetitorMention(Validator):
    """Fail when the text names a competitor; fix_value masks the name so on_fail=FIX works."""

    def __init__(
        self,
        competitors: list[str],
        on_fail: Callable | OnFailAction | None = None,  # r3: caller sets it explicitly at use site
        **kwargs: Any,
    ) -> None:
        # init args go through super() so the validator serialises into guard.history (r5)
        super().__init__(on_fail=on_fail, competitors=competitors, **kwargs)
        self._competitors = competitors
        self._patterns = [re.compile(re.escape(c), re.IGNORECASE) for c in competitors]

    def validate(self, value: Any, metadata: dict[str, Any]) -> ValidationResult:
        if not isinstance(value, str):
            return FailResult(error_message=f"expected str, got {type(value).__name__}")
        hits = [name for name, p in zip(self._competitors, self._patterns) if p.search(value)]
        if not hits:
            return PassResult()
        fixed = value
        for p in self._patterns:
            fixed = p.sub("[competitor]", fixed)
        reason = "mentions competitor(s): " + ", ".join(hits)
        logger.warning("validator=%s reason=%s", self.rail_alias, reason)
        return FailResult(error_message=reason, fix_value=fixed)


# Attach exactly like a Hub validator: on a Pydantic Field(validators=[...]) or on a Guard.
# Every attachment names its on_fail (r3); FIX here because a masked reply is still usable.
guard = Guard().use(
    NoCompetitorMention(competitors=["<competitor-a>", "<competitor-b>"], on_fail=OnFailAction.FIX),
)


if __name__ == "__main__":
    # Offline smoke test: validates a string without an LLM call.
    outcome = guard.validate("Our plan beats <competitor-a> on price.")
    print("passed:", outcome.validation_passed)
    print("output:", outcome.validated_output)
