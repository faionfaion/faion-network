"""Two versions of the same shape with a typed dispatcher.

Pattern: every shared SO model declares schema_version as a Literal
first field. The parser registry routes incoming payloads by version
so backfill jobs and consumers stay tolerant during rollouts.
"""

from typing import Literal
from pydantic import BaseModel, Field


class ArticleDraftV3(BaseModel):
    """Old schema kept registered during rollback window."""

    model_config = {"extra": "forbid"}
    schema_version: Literal["v3"] = "v3"
    body: str
    title: str
    tags: list[str] = Field(min_length=1, max_length=5)


class ArticleDraftV4(BaseModel):
    """New schema: `tags` renamed to `topics`; new `summary` field."""

    model_config = {"extra": "forbid"}
    schema_version: Literal["v4"] = "v4"
    body: str
    title: str
    topics: list[str] = Field(min_length=1, max_length=5)
    summary: str = Field(description="One-sentence article summary.")


PARSERS: dict[str, type[BaseModel]] = {
    "v3": ArticleDraftV3,
    "v4": ArticleDraftV4,
}


class UnknownSchemaVersion(Exception):
    """Raised when a payload has no registered parser."""


def parse_event(payload: dict) -> BaseModel:
    version = payload.get("schema_version")
    cls = PARSERS.get(version) if version else None
    if cls is None:
        raise UnknownSchemaVersion(f"no parser registered for version={version!r}")
    return cls.model_validate(payload)
