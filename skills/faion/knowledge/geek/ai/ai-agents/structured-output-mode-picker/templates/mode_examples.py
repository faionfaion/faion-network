"""Four constrained-decoding modes side by side.

One minimal call per mode so you can compare guarantees and pick by use
case rather than by API familiarity.
"""

from typing import Literal
from pydantic import BaseModel


class Verdict(BaseModel):
    decision: Literal["approve", "reject"]
    confidence: Literal["low", "medium", "high"]
    reason: str


# 1. JSON mode — legacy fallback only, no schema guarantee.
def call_json_mode(client, msgs):
    return client.chat.completions.create(
        model="gpt-5",
        messages=msgs,
        response_format={"type": "json_object"},
    )


# 2. Structured Outputs — full schema compliance.
def call_so_strict(client, msgs):
    return client.responses.parse(
        model="gpt-5",
        input=msgs,
        text_format=Verdict,
    )


# 3. Tool call — schema compliance + dispatch semantics.
def call_tool(client, msgs):
    return client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        messages=msgs,
        tools=[{"name": "submit_verdict", "input_schema": Verdict.model_json_schema()}],
        tool_choice={"type": "tool", "name": "submit_verdict"},
    )


# 4. Grammar mode — non-JSON DSLs and local models.
# Requires `pip install outlines` and a local-model provider.
def call_grammar(model, sql_grammar, prompt):
    import outlines  # noqa: PLC0415 — optional dep

    generator = outlines.generate.cfg(model, sql_grammar)
    return generator(prompt)
