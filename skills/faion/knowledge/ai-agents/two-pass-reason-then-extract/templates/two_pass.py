# purpose: two-pass cascade reference (Opus extended thinking → Haiku strict-SO extraction)
# consumes: question/input string + Pydantic schema
# produces: structured extraction conforming to content/02-output-contract.xml
# depends-on: 01-core-rules.xml (two-pass-required, strong-model-free-text, extractor-deterministic, transcript-bounded)
# token-budget-impact: pass-1 16K reasoning + pass-2 ~500 extraction tokens
"""Two-pass reasoning + extraction.

Pass 1: strong model reasons freely (extended thinking enabled).
Pass 2: cheap model extracts into a strict Pydantic schema.

Wire your own Anthropic + OpenAI / Anthropic clients; this file shows the
shape, not a runnable end-to-end demo.
"""

from typing import Literal

from pydantic import BaseModel, Field


class Verdict(BaseModel):
    """Strict extraction target — same schema regardless of reasoning depth."""

    model_config = {"extra": "forbid"}

    decision: Literal["approve", "reject", "needs_more_info"]
    confidence: Literal["low", "medium", "high"]
    primary_reason: str = Field(
        description="One sentence drawn directly from the analysis. No new claims."
    )


EXTRACTOR_SYSTEM = (
    "You extract structured verdicts from analysis text. "
    "Read only what the analysis explicitly states. "
    "If a field is not stated, set primary_reason to 'unstated' and decision to 'needs_more_info'."
)


def two_pass(
    question: str,
    *,
    strong_client,
    extractor_client,
    strong_model: str = "claude-opus-4-7",
    extractor_model: str = "claude-haiku-4-7",
    thinking_budget: int = 16000,
) -> Verdict:
    """Run free-form reasoning on the strong model, extract on the cheap one."""
    # Pass 1: free reasoning, no schema constraint.
    raw = strong_client.messages.create(
        model=strong_model,
        thinking={"type": "enabled", "budget_tokens": thinking_budget},
        messages=[{"role": "user", "content": question}],
    ).content[-1].text

    # Pass 2: strict extraction on a small model.
    return extractor_client.responses.parse(
        model=extractor_model,
        input=[
            {"role": "system", "content": EXTRACTOR_SYSTEM},
            {"role": "user", "content": f"Analysis:\n{raw}"},
        ],
        text_format=Verdict,
    )
