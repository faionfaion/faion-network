# purpose: Pydantic ticket schema with Literal enum fields wired for strict mode
# consumes: customer message text
# produces: Ticket instance with category/priority/sentiment enums
# depends-on: pydantic v2; OpenAI strict mode or Anthropic tool-call mode
# token-budget-impact: schema serialisation ~200 tokens
"""Strict-mode Pydantic schema with Literal enum fields.

Use with OpenAI:
    client.responses.parse(model="gpt-5", input=msgs, text_format=Ticket)

Or Anthropic tool-call mode:
    tools=[{"name": "submit_ticket", "input_schema": Ticket.model_json_schema()}]
    tool_choice={"type": "tool", "name": "submit_ticket"}
"""

from typing import Literal

from pydantic import BaseModel, Field

# Closed enums — every valid value listed; decoder masks all others.
Category = Literal["billing", "tech_support", "refund", "spam", "other"]
Priority = Literal["P0", "P1", "P2", "P3"]
Sentiment = Literal["angry", "frustrated", "neutral", "happy"]


class Ticket(BaseModel):
    """Support ticket classification.

    `extra=forbid` translates to JSON Schema `additionalProperties: false`,
    which is mandatory under OpenAI strict mode.
    """

    model_config = {"extra": "forbid"}

    reasoning: str = Field(
        description="Brief evidence for the labels below. Keep under 60 words."
    )
    category: Category = Field(description="Primary intent of the message.")
    priority: Priority = Field(description="Urgency level; P0 = service down.")
    sentiment: Sentiment = Field(description="Emotional tone of the customer.")
