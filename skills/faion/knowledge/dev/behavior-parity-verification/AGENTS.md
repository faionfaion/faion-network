# Behavior Parity Verification (Solo Tier)

## Summary

**One-sentence:** Validates that a rewritten code path produces the same observable behavior as the legacy path by shadowing real traffic and diffing outputs, with a lightweight setup a solo developer can stand up in a day.

**One-paragraph:** Major rewrites or framework migrations face a single hard question: did we break anything? Golden-master testing answers it via captured fixtures, but a solo developer often cannot afford the harness. Behavior parity verification offers the lighter alternative: route a small percentage of production traffic to both the old and new implementation, compare results in real time, and surface diffs. The methodology pins three things — what counts as observable, how to compare without leaking PII, and how to ramp safely from 1% to 100%. Output: a parity report per ramp stage that closes only when diff rate drops below a defined threshold for a defined window.

**Ефективно для:**

- Соло-розробник переписує сервіс на новий фреймворк/мові і боїться upgrade-regressions.
- Команда хоче безпечно вирізати legacy-шар без повного golden-master harness.
- AI-агент згенерував новий код-шлях і потрібен empirical gate перед видаленням старого.
- Міграція з monolith → service-extract, де хочеться dark-launch перед cutover.

## Applies If (ALL must hold)

- An existing code path is being replaced (new language, new framework, new algorithm) — not greenfield.
- The path is observable: defined input contract and a comparable output (HTTP response, file write, DB row, returned object).
- Production traffic is non-zero and reproducible (deterministic given inputs OR diffs can be tolerated probabilistically).
- The developer can deploy the new path behind a feature flag or routing layer.

## Skip If (ANY kills it)

- Pure UI changes — visual diffs need screenshot diffing, not behavioral parity.
- The legacy path is being removed in the same release — no shadow possible.
- Outputs include side-effects with no replay (sends real emails, charges real cards) — must be sandboxed first.
- Single-user dev tools without production traffic — replay captured logs instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Legacy implementation handle | code path / endpoint | repo |
| New implementation handle | code path / endpoint | repo |
| Feature flag / router | code | flag service or proxy layer |
| Diff store schema | SQL / KV definition | DBA / infra |
| Observable field list | Markdown | author of the rewrite |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/trunk-based-feature-flags` | Routing traffic between implementations is flag-gated. |
| `solo/dev/changelog-automation-conventional-commits` | Each ramp-stage promotion is a release event; the changelog records it. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: observable list, normalize-before-diff, staged ramp gates, freeze-on-regression | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema for parity-report artefact + valid/invalid examples + forbidden patterns | 700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: PII leak, timestamp false-positives, ramp-jump, async observables missed, permissive normalizer, skipped cluster analysis | 800 |
| `content/04-procedure.xml` | medium | 6-step procedure: define observables → write normalizer → deploy diff sampler → ramp 1%→100% with gates → cluster analysis → sign-off | 700 |
| `content/05-examples.xml` | reference | One worked example: pricing endpoint migration from legacy Python service to new Go service | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree: traffic-non-zero? observables-defined? normalizer-deterministic? gate-met? → ramp/freeze/revert | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `define-observable-fields` | sonnet | Bounded judgment on which response fields are observable vs incidental. |
| `write-diff-normalizer` | sonnet | Coding task: deterministic transforms (timestamp quantization, UUID canonicalization, list ordering). |
| `analyze-diff-clusters` | opus | Synthesis: cluster surviving diffs into root causes; cross-input pattern matching. |
| `score-parity-report` | haiku | Mechanical schema validation; pass/block computation against thresholds. |

## Templates

| File | Purpose |
|------|---------|
| `templates/parity-report.md.j2` | Markdown skeleton for the per-stage parity report (scope, observables, ramp window, diff metrics, sign-off). |
| `templates/parity-report.md` | Markdown skeleton for the per-stage parity report (scope, observables, ramp window, diff metrics, sign-off). Generated from `templates/parity-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/parity-report.json` | JSON Schema for the parity-report artefact (canonical contract). |
| `templates/diff-store-schema.sql` | Postgres DDL for the `parity_diffs` table the sampler writes to. |
| `templates/normalizer-skeleton.py` | Python skeleton of a deterministic diff normalizer (timestamp/UUID/list rules). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-behavior-parity-verification.py` | Validate a parity-report JSON against the schema and threshold rules. | After each ramp stage closes; before promoting to next stage. |

## Related

- [[trunk-based-feature-flags]] — flag plumbing that gates the shadow router.
- [[ci-quality-gate-design]] — same artefact-gate pattern at the CI layer.
- [[characterization-test-recipes]] — orthogonal: pre-rewrite test capture.

## Decision tree

See `content/06-decision-tree.xml`. The tree first checks whether production traffic is non-zero and whether the observable list has been written — these are hard prerequisites. It then branches on diff-rate vs threshold at each ramp stage, routing to one of `promote-next-stage`, `freeze-investigate`, or `revert-previous-stage`. Each leaf references a rule id in `01-core-rules.xml`. Use it before every ramp-promotion decision.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/parity-report.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/behavior-parity-verification.json",
  "type": "object",
  "required": [
    "artefact_id",
    "scope",
    "observable_fields",
    "ramp_stage",
    "window_start",
    "window_end",
    "total_compared",
    "diff_rate",
    "clusters",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^bpv-[a-z0-9-]{6,}$"
    },
    "scope": {
      "type": "string",
      "minLength": 1
    },
    "observable_fields": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "ramp_stage": {
      "type": "integer",
      "enum": [
        1,
        2,
        3,
        4
      ]
    },
    "window_start": {
      "type": "string",
      "format": "date-time"
    },
    "window_end": {
      "type": "string",
      "format": "date-time"
    },
    "total_compared": {
      "type": "integer",
      "minimum": 1000
    },
    "diff_rate": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "clusters": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "cluster_id",
          "sample_count",
          "disposition"
        ],
        "properties": {
          "cluster_id": {
            "type": "string"
          },
          "sample_count": {
            "type": "integer",
            "minimum": 1
          },
          "disposition": {
            "enum": [
              "fixed",
              "accepted-with-justification",
              "open"
            ]
          },
          "justification": {
            "type": "string"
          }
        }
      }
    },
    "verdict": {
      "enum": [
        "promote",
        "freeze",
        "revert"
      ]
    },
    "signed_off_by": {
      "type": "string"
    },
    "signed_off_at": {
      "type": "string",
      "format": "date"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    }
  }
}
```

### `templates/diff-store-schema.sql`

```sql
CREATE TABLE IF NOT EXISTS parity_diffs (
    id                BIGSERIAL PRIMARY KEY,
    scope             TEXT NOT NULL,
    ramp_stage        SMALLINT NOT NULL CHECK (ramp_stage BETWEEN 1 AND 4),
    sampled_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    input_fingerprint TEXT NOT NULL,
    legacy_hash       TEXT NOT NULL,
    new_hash          TEXT NOT NULL,
    diff_json         JSONB NOT NULL,
    cluster_id        TEXT,
    redaction_applied BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_parity_diffs_scope_stage  ON parity_diffs (scope, ramp_stage);
CREATE INDEX IF NOT EXISTS idx_parity_diffs_cluster      ON parity_diffs (cluster_id) WHERE cluster_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_parity_diffs_sampled_at   ON parity_diffs (sampled_at);

COMMENT ON COLUMN parity_diffs.redaction_applied IS 'MUST be true on insert. PII redaction precedes persistence.';
```

### `templates/normalizer-skeleton.py`

```python
from __future__ import annotations

import hashlib
import re
import uuid
from typing import Any


_UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z?$")


def quantize_timestamp(s: str) -> str:
    """Drop sub-second precision so independently-generated times can match."""
    if _TS_RE.match(s):
        return s[:19] + "Z"
    return s


def canonicalize_uuid(s: str) -> str:
    """Normalise UUID casing; non-UUIDs pass through."""
    if _UUID_RE.match(s):
        return str(uuid.UUID(s))
    return s


def redact_pii(value: str) -> str:
    """Hash PII rather than persist plaintext. Email-shaped strings only."""
    if "@" in value and "." in value.split("@")[-1]:
        return "pii:" + hashlib.sha1(value.encode()).hexdigest()[:12]
    return value


def normalize(value: Any) -> Any:
    """Recursive canonicalizer. Same code path for legacy and new outputs."""
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        items = [normalize(v) for v in value]
        # Sort only if items are scalar or shape allows deterministic ordering.
        if all(isinstance(i, (str, int, float, bool)) for i in items):
            items = sorted(items, key=lambda x: (type(x).__name__, str(x)))
        return items
    if isinstance(value, str):
        return redact_pii(canonicalize_uuid(quantize_timestamp(value)))
    return value
```
