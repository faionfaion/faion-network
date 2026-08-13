# Kanban and SAFe Ceremonies

## Summary

**One-sentence:** Alternative ceremony cadence for continuous-flow Kanban teams + scaled SAFe programs: replenishment, flow review, ART sync, PI planning windows, with WIP and lead-time metrics.

**One-paragraph:** Kanban and SAFe Ceremonies defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 5 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Continuous-flow teams that find Scrum sprints harmful (interrupt-driven work).
- SAFe Agile Release Trains (ART) with 5-12 teams operating on a common cadence.
- Programs needing a written cadence to bridge multiple Scrum / Kanban teams.
- Operators tracking lead-time + throughput, not story-points + velocity.

## Applies If (ALL must hold)

- Team or program has decided NOT to use Scrum sprints.
- WIP-limit discipline is in place or about to be introduced.
- Flow metrics (lead time, cycle time, throughput) can be measured.
- Cadence owners (RTE for SAFe, Flow Manager for Kanban) are named.

## Skip If (ANY kills it)

- Team is happily on Scrum with predictable sprint velocity.
- Single team <5 people — SAFe ceremonies are overkill; lightweight Kanban is enough.
- Org cannot commit to a fixed cadence (PI window) — SAFe collapses without it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `kanban-scaled-agile-ceremonies_template_fill` | haiku | Bounded template fill, no judgement. |
| `kanban-scaled-agile-ceremonies_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `kanban-scaled-agile-ceremonies_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the ceremony cadence artefact. |
| `templates/kanban-metrics.md` | Markdown skeleton for lead-time / cycle-time / throughput / WIP report. |
| `templates/cycle-stats.py` | Reference script computing cycle stats from issue events. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-kanban-scaled-agile-ceremonies.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/kanban-scaled-agile-ceremonies.json",
  "type": "object",
  "required": [
    "program_id",
    "ceremony_set",
    "stages",
    "cadence",
    "flow_metrics"
  ],
  "properties": {
    "program_id": {
      "type": "string"
    },
    "ceremony_set": {
      "enum": [
        "kanban-lightweight",
        "kanban-cadenced",
        "safe-essential",
        "safe-full"
      ]
    },
    "stages": {
      "type": "array",
      "minItems": 3,
      "items": {
        "type": "object",
        "required": [
          "name",
          "wip_limit"
        ]
      }
    },
    "cadence": {
      "type": "object",
      "required": [
        "replenishment",
        "flow_review"
      ],
      "properties": {
        "replenishment": {
          "type": "string"
        },
        "flow_review": {
          "type": "string"
        },
        "pi_planning": {
          "type": "string"
        }
      }
    },
    "flow_metrics": {
      "type": "object",
      "required": [
        "lead_time_p50",
        "cycle_time_p50",
        "throughput",
        "wip"
      ]
    }
  }
}
```

### `templates/cycle-stats.py`

```python
"""


"""cycle-stats.py — compute throughput and cycle-time stats from JSONL of issues.

Input JSONL: one JSON object per line with fields:
    state: str          — "Done", "In Progress", etc.
    resolved_at: str    — ISO 8601 timestamp when state became "Done"
    started_at: str     — ISO 8601 timestamp when state became "In Progress" (optional)

Computes throughput over the last 28 days and cycle-time percentiles.

Usage:
    cat issues.jsonl | python3 cycle-stats.py
    python3 cycle-stats.py < issues.jsonl
"""
from __future__ import annotations

import json
import statistics
import sys
from datetime import datetime, timedelta, timezone


def main() -> int:
    issues = [json.loads(line) for line in sys.stdin if line.strip()]
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=28)

    done = [
        i for i in issues
        if i.get("state") == "Done"
        and datetime.fromisoformat(i["resolved_at"]).replace(tzinfo=timezone.utc) > cutoff
    ]

    cycle_days = [
        (
            datetime.fromisoformat(i["resolved_at"]).replace(tzinfo=timezone.utc)
            - datetime.fromisoformat(i["started_at"]).replace(tzinfo=timezone.utc)
        ).total_seconds() / 86400
        for i in done
        if i.get("started_at")
    ]

    weekly = len(done) / 4
    print(f"throughput_28d={len(done)}  weekly_avg={weekly:.1f}")

    if cycle_days:
        p50 = statistics.median(cycle_days)
        sorted_days = sorted(cycle_days)
        p85_idx = int(len(sorted_days) * 0.85)
        p85 = sorted_days[min(p85_idx, len(sorted_days) - 1)]
        print(
            f"cycle_p50={p50:.1f}d  "
            f"cycle_p85={p85:.1f}d  "
            f"cycle_max={max(cycle_days):.1f}d  "
            f"n={len(cycle_days)}"
        )
    else:
        print("No cycle-time data (missing started_at fields).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
```
