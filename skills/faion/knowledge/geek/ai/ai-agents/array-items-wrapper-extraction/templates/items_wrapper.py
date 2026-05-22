# purpose: Pydantic envelope `{items, total_found, truncated}` for variable-cardinality extraction
# consumes: per-domain Entity model (replace the stub below)
# produces: strict-mode-valid structured output schema
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~150 tokens added to system schema per call
"""Batch-extraction schema with the items wrapper.

The wrapper is mandatory under OpenAI/Azure strict mode (which forbids
top-level arrays) and recommended on every other provider for consistent
zero/one/many parsing.
"""

from pydantic import BaseModel, Field


class Entity(BaseModel):
    """One extracted entity. Replace with your domain shape."""

    name: str = Field(description="Surface form of the entity as it appears in the source.")
    kind: str = Field(description="Entity kind, e.g. 'person', 'org', 'product'.")
    span_start: int = Field(ge=0, description="Inclusive character offset in the source.")
    span_end: int = Field(ge=0, description="Exclusive character offset in the source.")


class EntityList(BaseModel):
    """Top-level extraction result.

    items is the actual list; total_found and truncated expose diagnostics
    the consumer can use without recomputing.
    """

    model_config = {"extra": "forbid"}

    total_found: int = Field(
        ge=0,
        description="Count of entities found. 0 if none. Must equal len(items) unless truncated.",
    )
    truncated: bool = Field(
        description="True if more entities exist beyond the per-call limit and were dropped.",
    )
    items: list[Entity] = Field(
        description="Entities in order of appearance. May be empty.",
    )

    def is_empty(self) -> bool:
        return self.total_found == 0
