#!/usr/bin/env python3
"""Validate voice-agent-config artefact for voice-implementation methodology.

USAGE:
    validate-voice-implementation.py <input.json>   Validate config.
    validate-voice-implementation.py --self-test    Run built-in fixtures.
    validate-voice-implementation.py --help         Show this help.

EXIT CODES:
    0 valid
    1 schema violation
    2 usage / unreadable

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

VADS = {"silero", "webrtc", "energy"}
STACKS = {"stt_llm_tts", "openai_realtime"}
EXECUTORS = {"thread", "async_native", "process"}
AUDIT_FIELDS = {"input_transcript", "llm_response", "tool_calls", "audio_duration", "turn_latency_ms"}


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    for k in ("vad", "stack", "latency_budget_ms", "tool_executor", "context", "audit"):
        if k not in c:
            v.append(f"missing required field: {k}")
    if "vad" in c and c["vad"] not in VADS:
        v.append(f"vad must be one of {sorted(VADS)} (rule r1)")
    if "stack" in c and c["stack"] not in STACKS:
        v.append(f"stack must be one of {sorted(STACKS)}")
    if "latency_budget_ms" in c:
        b = c["latency_budget_ms"]
        if not isinstance(b, int) or b < 50 or b > 5000:
            v.append("latency_budget_ms out of range [50,5000]")
        if c.get("stack") == "stt_llm_tts" and isinstance(b, int) and b < 300:
            v.append("budget <300ms but stack=stt_llm_tts; switch to openai_realtime (rule r5)")
    te = c.get("tool_executor") or {}
    if te.get("mode") not in EXECUTORS:
        v.append(f"tool_executor.mode must be one of {sorted(EXECUTORS)} (rule r2)")
    ctx = c.get("context") or {}
    win = ctx.get("sliding_window_turns")
    mrt = ctx.get("max_response_tokens")
    if not isinstance(win, int) or win < 2 or win > 50:
        v.append("context.sliding_window_turns out of range [2,50] (rule r4)")
    if not isinstance(mrt, int) or mrt < 50 or mrt > 400:
        v.append("context.max_response_tokens out of range [50,400] (rule r4)")
    if c.get("tts_markdown_stripped") is not True:
        v.append("tts_markdown_stripped must be true (rule r3)")
    audit_fields = set((c.get("audit") or {}).get("fields") or [])
    missing = AUDIT_FIELDS - audit_fields
    if missing:
        v.append(f"audit.fields missing {sorted(missing)} (rule r6)")
    return v


GOOD = {
    "vad": "silero",
    "stack": "stt_llm_tts",
    "latency_budget_ms": 2500,
    "tool_executor": {"mode": "thread"},
    "context": {"sliding_window_turns": 12, "max_response_tokens": 180},
    "tts_markdown_stripped": True,
    "audit": {"fields": sorted(AUDIT_FIELDS)},
}
BAD = {
    "vad": "energy",
    "stack": "stt_llm_tts",
    "latency_budget_ms": 250,
    "tool_executor": {"mode": "async_native"},
    "context": {"sliding_window_turns": 100, "max_response_tokens": 500},
    "tts_markdown_stripped": False,
    "audit": {"fields": ["input_transcript"]},
}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy path failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("budget" in x for x in bad), "should flag budget"
    assert any("markdown" in x for x in bad), "should flag markdown"
    assert any("audit" in x for x in bad), "should flag audit"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-voice-implementation.py")
    p.add_argument("path", nargs="?", help="JSON config to validate")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        p.print_help()
        return 2
    out = validate(json.loads(Path(args.path).read_text()))
    if out:
        for x in out:
            sys.stdout.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
