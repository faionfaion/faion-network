# purpose: Pydantic BlogPost schema with body-first ordering
# consumes: article generation prompt
# produces: validated BlogPost instance with body before metadata fields
# depends-on: pydantic v2
# token-budget-impact: ~200 tokens of schema serialisation
"""Body-before-metadata schema for one-call article generation.

Field order is generation order in autoregressive SO. Body is declared
first so title/slug/tags can summarize the body that already exists.
"""

from typing import Literal
from pydantic import BaseModel, Field


class BlogPost(BaseModel):
    model_config = {"extra": "forbid"}  # additionalProperties: false

    # 1. Long-form content first — becomes the CoT trace for everything below.
    body: str = Field(
        description=(
            "600-800 word article in markdown. Use H2 headers, short "
            "paragraphs, at least one code or example block."
        )
    )

    # 2. Title summarizes the body that already exists in context.
    title: str = Field(
        description="6-10 word title that captures the body's main claim."
    )

    # 3. Slug derives from title (which derives from body).
    slug: str = Field(
        description="kebab-case URL slug, lowercase, ASCII only.",
        pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$",
    )

    # 4. Tags drawn from body topics.
    tags: list[str] = Field(
        description="3-5 lowercase one-word tags from body topics.",
        min_length=3,
        max_length=5,
    )

    # 5. Sentiment / tone metadata — last, because it summarizes the whole.
    tone: Literal["technical", "narrative", "tutorial", "opinion"]
