"""Strict-mode SO schema with explicit refusal field.

Pattern: refusal first, every payload field nullable. The model writes
its decline reason into `refusal` and leaves payload fields null,
satisfying strict grammar without inventing fake values.
"""

from pydantic import BaseModel, Field


class MedicalExtract(BaseModel):
    """Extract clinical data from a chart note. Safety-aware."""

    model_config = {"extra": "forbid"}

    # 1. Refusal first — model can decline without grammar violation.
    refusal: str | None = Field(
        default=None,
        description=(
            "If you cannot or should not answer (PII concerns, "
            "out-of-scope, insufficient context), put the reason here. "
            "Otherwise null."
        ),
    )

    # 2. All payload fields are nullable so refusal-with-nulls is legal.
    diagnoses: list[str] | None = Field(default=None, description="ICD-10 codes; null on refusal.")
    medications: list[str] | None = Field(default=None, description="Active meds; null on refusal.")
    allergies: list[str] | None = Field(default=None, description="Known allergies; null on refusal.")


def handle(parsed: MedicalExtract) -> dict | None:
    """Single branch separates refusal from extracted payload."""
    if parsed.refusal:
        # Log to refusal counter, do not raise.
        return None
    return parsed.model_dump(exclude={"refusal"}, exclude_none=True)
