"""
purpose: Pydantic v2 BaseModel with model_config and validators.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    name: str = Field(min_length=1, max_length=100)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
