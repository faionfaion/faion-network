"""
purpose: Pydantic v2 BaseModel pair: <Entity>In + <Entity>Out with model_config.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

from pydantic import BaseModel, ConfigDict


class ItemIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str


class ItemOut(BaseModel):
    id: int
    name: str
