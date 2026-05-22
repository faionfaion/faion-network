# purpose: constrained-string field with format + example + forbidden patterns
# consumes: title text
# produces: validated slug field
# depends-on: pydantic v2
# token-budget-impact: ~90 tokens of description
"""Constrained-string template — slug from title."""

from pydantic import BaseModel, Field


class Article(BaseModel):
    title: str
    slug: str = Field(
        pattern=r"^[a-z0-9-]{1,60}$",
        description=(
            "kebab-case slug, max 60 chars, ASCII lowercase. Derived from `title`. "
            "DO NOT include articles (a/an/the). DO NOT include the year unless "
            "`title` mentions it. DO NOT use special characters or emoji."
        ),
    )
