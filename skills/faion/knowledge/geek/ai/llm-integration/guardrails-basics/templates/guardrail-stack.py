"""
purpose: Reference 4-layer ordered guardrail runner with fail-closed default + telemetry.
consumes: input/output text + spec + classifier callable
produces: dict {ok, blocked_by, layer_latencies_ms}
depends-on: content/01-core-rules.xml; content/02-output-contract.xml
token-budget-impact: classifier call only on layers 4
"""
from __future__ import annotations

import re
import time
from typing import Callable


def regex_layer(text: str, patterns: list[str]) -> bool:
    return not any(re.search(p, text) for p in patterns)


def length_layer(text: str, max_chars: int) -> bool:
    return len(text) <= max_chars


def schema_layer(payload: dict, validate: Callable[[dict], bool]) -> bool:
    return validate(payload)


def classifier_layer(text: str, classify: Callable[[str], str]) -> bool:
    return classify(text) == "safe"


def run_stack(text: str, *, patterns: list[str], max_chars: int, schema_validate, classify, fail_closed: bool = True) -> dict:
    lat: dict[str, float] = {}
    try:
        t0 = time.perf_counter()
        if not regex_layer(text, patterns):
            lat["regex"] = (time.perf_counter() - t0) * 1000
            return {"ok": False, "blocked_by": "regex", "layer_latencies_ms": lat}
        lat["regex"] = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        if not length_layer(text, max_chars):
            lat["length"] = (time.perf_counter() - t0) * 1000
            return {"ok": False, "blocked_by": "length", "layer_latencies_ms": lat}
        lat["length"] = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        if schema_validate and not schema_validate({"text": text}):
            lat["schema"] = (time.perf_counter() - t0) * 1000
            return {"ok": False, "blocked_by": "schema", "layer_latencies_ms": lat}
        lat["schema"] = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        if not classifier_layer(text, classify):
            lat["classifier"] = (time.perf_counter() - t0) * 1000
            return {"ok": False, "blocked_by": "classifier", "layer_latencies_ms": lat}
        lat["classifier"] = (time.perf_counter() - t0) * 1000

        return {"ok": True, "blocked_by": None, "layer_latencies_ms": lat}
    except Exception as e:
        if fail_closed:
            return {"ok": False, "blocked_by": "exception", "error": str(e), "layer_latencies_ms": lat}
        raise
