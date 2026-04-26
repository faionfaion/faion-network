"""
Entity extraction Pydantic schema.
Works with OpenAI native structured output and instructor (Claude/others).
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class EntityType(str, Enum):
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    DATE = "date"
    MONEY = "money"
    PRODUCT = "product"
    EVENT = "event"
    CONCEPT = "concept"


class Entity(BaseModel):
    text: str = Field(description="Entity text as it appears in source")
    type: EntityType = Field(description="Entity category")
    normalized: Optional[str] = Field(default=None, description="Canonical form")
    confidence: float = Field(ge=0, le=1, default=1.0, description="Extraction confidence")
    raw_quote: str = Field(description="Verbatim quote from source that supports this entity")


class EntityExtractionResult(BaseModel):
    entities: List[Entity] = Field(description="All extracted entities")
    summary: str = Field(description="One-sentence summary of the source text")
    language: str = Field(default="en", description="Detected language (ISO 639-1)")
