"""Discriminated-union template: agent action selector.

Use as a `text_format` (OpenAI Responses API) or `tools[*].input_schema`
(Anthropic Messages API). The discriminator (`kind`) is the FIRST field
of every branch so the model commits to a branch before any other token.
"""
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class SearchAction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["search"] = "search"
    query: str = Field(description="Web search query, plain text, no operators.")


class FetchAction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["fetch"] = "fetch"
    url: str = Field(description="Absolute https URL to fetch.")


class AskUserAction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["ask_user"] = "ask_user"
    question: str = Field(description="One concrete question for the user.")


class FinishAction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["finish"] = "finish"
    summary: str = Field(description="Final answer or short result summary.")


AgentAction = Annotated[
    SearchAction | FetchAction | AskUserAction | FinishAction,
    Field(discriminator="kind"),
]


class AgentTurn(BaseModel):
    """One turn of the agent loop. Reasoning first, then the chosen action."""

    model_config = ConfigDict(extra="forbid")
    reasoning: str = Field(description="Brief chain-of-thought before action.")
    action: AgentAction
