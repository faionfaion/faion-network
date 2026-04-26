"""Reasoning-item-preserving agent loop on the OpenAI Responses API.

Two paths:
  - Stateful (default): chain via previous_response_id. Cheapest, simplest.
  - ZDR (store=false):  round-trip include=["reasoning.encrypted_content"].

Both preserve reasoning items between turns; without preservation, agentic
benchmarks regress 20-40% because the model re-derives plans every turn.
"""

from openai import OpenAI

client = OpenAI()


def step_stateful(prior_id: str | None, new_input, *, model="o4-mini", tools=None):
    """One turn of a stateful (store=true) reasoning loop.

    Pass prior_id=None on the first call. After that, pass the .id of the
    previous response and ONLY the new input items (user msg, tool results) —
    do not reconstruct the message history.
    """
    kwargs = {"model": model, "input": new_input}
    if tools is not None:
        kwargs["tools"] = tools
    if prior_id is not None:
        kwargs["previous_response_id"] = prior_id
    return client.responses.create(**kwargs)


def step_zdr(prior_response, new_input, *, model="o4-mini", tools=None):
    """One turn of a ZDR (store=false) reasoning loop.

    Caller passes the WHOLE prior response object so we can extract its
    encrypted reasoning items and prepend them to the new input. previous_response_id
    is intentionally NOT used — it is silently ignored when store=false.
    """
    base = []
    if prior_response is not None:
        base = [i for i in prior_response.output if i.type == "reasoning"]
    kwargs = {
        "model": model,
        "store": False,
        "include": ["reasoning.encrypted_content"],
        "input": base + list(new_input),
    }
    if tools is not None:
        kwargs["tools"] = tools
    return client.responses.create(**kwargs)
