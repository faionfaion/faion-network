"""Pytest replay harness: assert byte-for-byte parity with the corpus.

Each row in `tests/golden/corpus.jsonl` becomes one parametrized case so a
single failing input is reported with a precise id. Updating `expected` values
requires a separate commit whose message starts with `golden:`.
"""

from __future__ import annotations

import difflib
import json
import pathlib
from typing import Any

import pytest

from rewrite import process  # adapt import to the rewrite entry point
from corpus_normalize import normalize  # share normalize() with capture_corpus.py

CORPUS = pathlib.Path("tests/golden/corpus.jsonl")
CASES = [json.loads(line) for line in CORPUS.read_text().splitlines() if line.strip()]


def _diff(expected: Any, actual: Any) -> str:
    return "\n".join(
        difflib.unified_diff(
            json.dumps(expected, indent=2, sort_keys=True).splitlines(),
            json.dumps(actual, indent=2, sort_keys=True).splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm="",
        )
    )


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_golden_master(case: dict) -> None:
    actual = normalize(process(**case["input"]))
    expected = case["expected"]
    if actual != expected:
        pytest.fail(f"{case['id']} diverged:\n{_diff(expected, actual)}")
