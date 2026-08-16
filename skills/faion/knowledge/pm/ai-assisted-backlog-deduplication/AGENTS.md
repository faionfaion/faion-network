# Ai Assisted Backlog Deduplication

## Summary

**One-sentence:** End-to-end playbook for AI-assisted backlog deduplication — embeddings cluster, human review, merged/closed/kept decisions logged with traceability.

**One-paragraph:** End-to-end playbook for AI-assisted backlog deduplication — embeddings cluster, human review, merged/closed/kept decisions logged with traceability. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** Product/PM-у з backlog >300 items — щоб дублі знаходились автоматично, але рішення лишалось людським.

## Applies If (ALL must hold)

- Backlog has >= 300 items across >= 6 months of accumulation.
- Embeddings provider is available (OpenAI, Cohere, local model).
- A named PM owns the backlog and will sign off on merge/close decisions.
- Tracker supports bulk updates (Jira API, Linear API).

## Skip If (ANY kills it)

- Backlog < 100 items — manual review is cheaper than the pipeline.
- No tracker API — manual cleanup remains the only option.
- Team treats backlog as append-only memory — duplication is an explicit feature.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Backlog export | CSV/JSON | Jira / Linear |
| Embeddings API key | secret | OpenAI / Cohere / local |
| Owner sign-off path | approval workflow | PM tooling |
| Duplicate-threshold calibration set | labelled CSV | manual sample of 50 |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/pm/pm-agile/ai-assisted-velocity-anomaly-detection` | Companion AI-assist pipeline; shares the same prompt-injection guards. |
| `geek/pm/project-manager/ai-pm-tool-integration-recipes` | Tracker integration boilerplate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `embed-and-cluster` | haiku | Pure pipeline call — no judgement. |
| `threshold-calibration` | sonnet | Bounded judgement against labelled set. |
| `merge-decision-write-up` | opus | Cross-item synthesis for PM sign-off. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.py` | Python skeleton: load backlog → embed → cluster → emit review CSV → apply approved merges. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-assisted-backlog-deduplication.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-assisted-velocity-anomaly-detection]]
- [[ai-pm-tool-integration-recipes]]
- [[exception-driven-standup-protocol]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to run the dedupe pipeline (>=300 items + embeddings + owner + 50-label calibration), block until calibration exists, or skip (small backlog). Run before any embed call costs money.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/skeleton.py`

```python
"""Methodology scaffold — fill the gaps in `produce()` and pipe to scripts/validate-<slug>.py."""
from __future__ import annotations

import json
from datetime import date


def produce() -> dict:
    return {
        "header": {
            "version": "0.1.0",
            "owner": "<role>:<person>",
            "last_reviewed": date.today().isoformat(),
        },
        "body": {},
        "evidence": [],
        "decisions": {"next_actions": [], "next_review": "YYYY-MM-DD"},
    }


if __name__ == "__main__":
    print(json.dumps(produce(), indent=2))  # noqa: T201
```

### `templates/header.yaml`

```yaml
version: 0.1.0           # bump on every refresh; semver
owner: <role>:<person>   # named person, never a team
last_reviewed: YYYY-MM-DD
evidence_root: <link>    # URL or file path that anchors body claims
```
