# Golden-Master Corpus for AI-Driven Legacy Rewrites

## Summary

**One-sentence:** Capture inputs and outputs of the current legacy implementation into a committed corpus; an AI rewrite passes only when it reproduces every pair byte-for-byte (or each diff is explicitly approved row-by-row).

**One-paragraph:** When you ask a coding agent to rewrite a 5000-line legacy module, you have no spec — you have current behaviour. Capture inputs and outputs of the current implementation from production traffic, fixtures, or a fuzzer into a committed corpus of (input, expected_output) pairs; the agent's rewrite passes only when it reproduces every pair, byte-for-byte, or each diff is explicitly approved row-by-row. This is the only test that scales to AI-driven rewrites of untested legacy: it is the spec the legacy never had, captured automatically, and it gives the agent a deterministic GREEN signal that does not depend on human ability to read the old code.

**Ефективно для:**

- 5k-LoC legacy module без юніт-тестів — corpus стає specs.
- AI rewrite, де human can't read the old code чи валідувати manually.
- Strangler-fig migration: corpus гарантує parity step-by-step.
- Compliance: byte-for-byte parity proof для audit.

## Applies If (ALL must hold)

- Legacy module ≥ 500 LoC slated for AI-driven rewrite.
- Production traffic or fixtures exist to sample inputs from.
- Outputs are deterministic (or non-determinism can be canonicalized).

## Skip If (ANY kills it)

- Module is 50 LoC where a hand-written test suite is faster.
- Outputs depend on wall-clock time or external state that cannot be mocked.
- No traffic source exists and inputs cannot be generated synthetically.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Legacy module source | code | repo |
| Traffic capture or fixture source | HAR / pickle / DB dump | ops |
| Canonicalization function (if non-deterministic) | code | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/capture_corpus.py` | Python script sampling top-N+tail+fuzz inputs and capturing legacy outputs. |
| `templates/golden_master_test.py` | pytest runner that diffs (input, expected) pairs and checks `approved_diffs.yaml`. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-golden-master-legacy-rewrite.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[test-mutation-feedback-loop]]
- [[test-property-based-llm-invariants]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/capture_corpus.py`

```python
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
```

### `templates/golden_master_test.py`

```python
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
```
