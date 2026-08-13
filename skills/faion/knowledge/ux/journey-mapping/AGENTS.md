# Customer Journey Mapping

## Summary

**One-sentence:** Generate a current-state customer journey map (stage × row matrix with persona, actions, touchpoints, thoughts, emotions, pain points, opportunities) grounded in cited research evidence.

**One-paragraph:** Visualise the complete experience a user has with a product over time. Inputs: persona definition + cited research artefacts (interview IDs, support tickets, analytics events). Output: a stage × row matrix covering all eight components (persona, stages, actions, touchpoints, thoughts, emotions, pain points, opportunities), every cell either citing an evidence ID or marked "no data". Use to find cross-channel friction and align stakeholders on the current-state experience before designing improvements.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Designing or redesigning a multi-step flow (onboarding, checkout, support, offboarding).
- Research data exists (interviews, observation, analytics, support tickets, surveys).
- A specific persona and journey scope (start point + end point) can be named.

## Skip If (ANY kills it)

- No research data exists — a purely imagined map creates false consensus.
- Single isolated interaction with no multi-step journey.
- Stakeholders want quantitative evidence; journey maps are qualitative synthesis, not metrics.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Persona definition (specific, research-based) | doc | UX research |
| Cited research artefacts (interview IDs, ticket IDs, analytics events) | spreadsheet or doc | research / ops |
| Journey scope (start + end point + persona) | one-paragraph | PM / UX |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/user-interviews` | Map cells must cite interview IDs. |
| `solo/ux/ux-ui-designer/usability-testing` | Pain points often surface in usability findings. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip-this-methodology fallback | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the journey-map artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 7-step procedure: scope → research → stages → rows → emotions → pain → opportunities | ~700 |
| `content/05-examples.xml` | medium | Worked e-commerce purchase journey end-to-end | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `synthesise-map` | sonnet | Stage × row matrix composition from structured research. |
| `extract-evidence` | haiku | Mechanical pull of interview IDs / ticket IDs from corpus. |
| `score-emotional-arc` | opus | Identify sharp dips vs smooth averages; rejects LLM smoothing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/journey-map.md` | Full journey map: stage × row matrix. |
| `templates/stage-detail.md` | Single-stage deep-dive template. |
| `templates/prompt-map.txt` | Agent prompt skeleton for journey-map synthesis. |
| `templates/funnel-to-stages.py` | Convert funnel CSV to stage summaries for ingest. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-journey-mapping.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[user-interviews]]
- [[usability-testing]]
- [[wireframing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named persona + scope, research evidence reachable) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-map.txt`

```text
Given the following user interview excerpts and support ticket summaries, produce a journey map
for [persona] doing [journey name]. Scope: from [start point] to [end point].

Output a markdown table with these rows:
Stage | Actions | Touchpoints | Thoughts | Emotions (1-5) | Pain Points | Opportunities

Rules:
- Base every cell on cited evidence from the input materials
- For each cell, add a citation: (Interview P3) or (Ticket #1234) or (Analytics: checkout page)
- If no evidence exists for a cell, write "no data" — do not invent content
- Emotions: use 1 (most negative/frustrated) to 5 (most positive/delighted)
- Identify sharp emotional dips (2+ point drop between stages) — these are the highest-priority pain points
- Do not smooth emotional arcs — report variance between participants explicitly
- Opportunities must be specific improvements, not generic ("improve the UX") — they must link to the pain point evidence

After the table, add:
- Top 3 pain points ranked by emotional impact and frequency
- 3 prioritized opportunities with backlog hypothesis statements

Note: this output is a research synthesis draft. Mark any inferences with [INFERRED].
Human review required before sharing with stakeholders.

INTERVIEW EXCERPTS:
[paste excerpts here]

SUPPORT TICKET SUMMARIES:
[paste ticket summaries here]

ANALYTICS FUNNEL DATA:
[paste stage summary JSON from funnel-to-stages.py or describe key drop-off points]
```

### `templates/funnel-to-stages.py`

```python
"""
Convert funnel analytics CSV to stage summaries for agent journey map ingestion.

Input CSV columns: stage, sessions, drop_off_pct, avg_time_sec
Output: JSON list of stage summary dicts for use as agent context.

Usage:
    python funnel-to-stages.py funnel.csv

Example CSV:
    stage,sessions,drop_off_pct,avg_time_sec
    Home,10000,15,45
    Product Page,8500,22,120
    Cart,6630,45,60
    Checkout,3647,38,180
    Confirmation,2261,0,30
"""

import csv
import json
import sys


def summarize(path: str) -> list:
    stages = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            drop_pct = float(row["drop_off_pct"])
            stages.append({
                "stage": row["stage"],
                "sessions": int(row["sessions"]),
                "drop_off_pct": drop_pct,
                "avg_time_sec": int(row["avg_time_sec"]),
                "risk": "high" if drop_pct > 30 else "normal",
                "note": (
                    f"High drop-off ({drop_pct:.0f}%) — likely pain point. Investigate."
                    if drop_pct > 30
                    else f"Normal drop-off ({drop_pct:.0f}%)."
                ),
            })
    return stages


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python funnel-to-stages.py <funnel.csv>")
        sys.exit(1)
    result = summarize(sys.argv[1])
    print(json.dumps(result, indent=2))

    high_risk = [s for s in result if s["risk"] == "high"]
    if high_risk:
        print(f"\nHigh-risk stages for journey map priority: {[s['stage'] for s in high_risk]}")


if __name__ == "__main__":
    main()
```
