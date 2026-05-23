"""
purpose: Cross-vendor agent-loop reference (Anthropic + OpenAI shapes) with parallel dispatch.
consumes: tool registry + vendor SDK client + executor
produces: final text answer; logs traces
depends-on: content/01-core-rules.xml r3, r4
token-budget-impact: bounded by MAX_TURNS x avg turn cost
"""
from __future__ import annotations

import concurrent.futures as cf
import json
from typing import Any, Callable

MAX_TURNS = 15


def run_anthropic(client, system: str, user: str, tools: list[dict], execute: Callable[[str, dict], str]) -> str:
    messages = [{"role": "user", "content": user}]
    for _ in range(MAX_TURNS):
        resp = client.messages.create(model="claude-sonnet-4-5", max_tokens=4096, system=system, tools=tools, messages=messages)
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            return next((b.text for b in resp.content if b.type == "text"), "")
        tool_uses = [b for b in resp.content if b.type == "tool_use"]
        with cf.ThreadPoolExecutor() as ex:
            futures = {b.id: ex.submit(execute, b.name, b.input) for b in tool_uses}
        results = [{"type": "tool_result", "tool_use_id": bid, "content": f.result()} for bid, f in futures.items()]
        messages.append({"role": "user", "content": results})
    return "max_turns_reached"


def run_openai(client, system: str, user: str, tools: list[dict], execute: Callable[[str, dict], str]) -> str:
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    for _ in range(MAX_TURNS):
        resp = client.chat.completions.create(model="gpt-4o", tools=tools, messages=messages)
        msg = resp.choices[0].message
        messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": [tc.model_dump() for tc in (msg.tool_calls or [])]})
        if not msg.tool_calls:
            return msg.content or ""
        with cf.ThreadPoolExecutor() as ex:
            futures = {tc.id: ex.submit(execute, tc.function.name, json.loads(tc.function.arguments)) for tc in msg.tool_calls}
        for tc in msg.tool_calls:
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": futures[tc.id].result()})
    return "max_turns_reached"
