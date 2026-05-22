"""
purpose: Reference Gemini manual-mode function-calling loop with validation.
consumes: tool function dict + user message + Gemini client
produces: final text after function dispatch
depends-on: content/01-core-rules.xml r3, r4; content/04-procedure.xml
token-budget-impact: bounded by MAX_TURNS x avg turn cost
"""
from __future__ import annotations

import json
from typing import Callable

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

MAX_TURNS = 15


def run_manual_fc(client, model: str, system: str, user: str, tools: list[Callable], validators: dict[str, Callable]) -> str:
    """Manual-mode loop: caller dispatches the LLM-requested tool."""
    if types is None:
        raise SystemExit("google-genai required")
    chat = client.chats.create(model=model, config=types.GenerateContentConfig(system_instruction=system, tools=tools))
    msg = user
    for _ in range(MAX_TURNS):
        resp = chat.send_message(msg)
        if not resp.function_calls:
            return resp.text
        msg = []
        for fc in resp.function_calls:
            validator = validators.get(fc.name)
            args = dict(fc.args)
            if validator and not validator(args):
                msg.append(types.Part.from_function_response(name=fc.name, response={"error": "validation_failed"}))
                continue
            fn = next((t for t in tools if t.__name__ == fc.name), None)
            if not fn:
                msg.append(types.Part.from_function_response(name=fc.name, response={"error": "unknown_function"}))
                continue
            result = fn(**args)
            msg.append(types.Part.from_function_response(name=fc.name, response={"result": result}))
    return "max_turns_reached"
