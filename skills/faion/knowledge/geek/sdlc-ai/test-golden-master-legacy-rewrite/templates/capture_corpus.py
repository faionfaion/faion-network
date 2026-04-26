"""Capture a golden-master corpus by wrapping the legacy callable.

Run:
    python -m capture_corpus < production_inputs.jsonl

Inputs file: one JSON object per line, each with `id` and `input` (kwargs dict).
Output: appends `(id, input, expected)` rows to `tests/golden/corpus.jsonl`.

Normalization is REQUIRED. Without it the replay test goes flaky and gets
disabled, which destroys the whole gate. Extend `normalize()` for your domain.
"""

from __future__ import annotations

import json
import pathlib
import random
import sys
from typing import Any

import freezegun  # type: ignore[import-not-found]

from legacy import process  # adapt import to the legacy entry point

CORPUS = pathlib.Path("tests/golden/corpus.jsonl")
FROZEN_AT = "2026-01-01T00:00:00Z"
SEED = 42


def normalize(value: Any) -> Any:
    """Strip volatile data so replay is deterministic.

    Sort dict keys, strip UUID-shaped strings, round floats, sort lists by stable
    key when order is irrelevant. Add domain-specific rules here.
    """
    if isinstance(value, dict):
        return {k: normalize(value[k]) for k in sorted(value)}
    if isinstance(value, list):
        return [normalize(v) for v in value]
    if isinstance(value, float):
        return round(value, 6)
    return value


def main() -> None:
    random.seed(SEED)
    CORPUS.parent.mkdir(parents=True, exist_ok=True)
    seen = {json.loads(line)["id"] for line in CORPUS.read_text().splitlines() if line.strip()} if CORPUS.exists() else set()

    with freezegun.freeze_time(FROZEN_AT), CORPUS.open("a") as out:
        for line in sys.stdin:
            case = json.loads(line)
            if case["id"] in seen:
                continue
            expected = normalize(process(**case["input"]))
            out.write(json.dumps({"id": case["id"], "input": case["input"], "expected": expected}, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
