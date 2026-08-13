# Learning Speed as Competitive Moat

## Summary

**One-sentence:** Framework treating organisational learning velocity (belief-update rate, decision throughput, evidence freshness) as the primary competitive advantage in AI-cloneable markets; outputs a quarterly belief-audit.

**One-paragraph:** Belief register + decision-velocity tracking + evidence-freshness thresholds + loss-attribution coding + pre-registered kill-criteria. Treats learning velocity as the moat: not what you ship, but how fast you change your mind in response to evidence. Output: quarterly belief-audit report with confidence deltas + stale-belief flags + loss-cause histogram.

**Ефективно для:**

- Post-PMF продукт у market з well-funded competitor.
- Quarterly review, де learning-velocity OKR контестується.
- Inherited roadmap із заплямованими assumptions, що потребує 30-day belief-audit.
- Team із 8+ plausible bets — bottleneck змістився від 'чи треба це?' до 'яке з них вибрати?'.

## Applies If (ALL must hold)

- A PM owns a product area against a well-funded competitor where the differentiation thesis depends on shipping the right thing next.
- Preparing for a quarterly business review and need to defend 'what we changed our minds about' with evidence.
- Setting OKRs where learning velocity (not feature throughput) is the contested promotion criterion.
- Inherited a roadmap built on stale assumptions — need a 30-day belief-audit before committing to next quarter.
- Post-PMF squad where the bottleneck has moved from 'does anyone want this?' to 'which of 8 plausible bets do we make first?'.

## Skip If (ANY kills it)

- Pre-PMF where customer-development is primary — beliefs are too thin to audit.
- Agency / consulting where each project is one-shot and no portfolio belief register accumulates.
- Commodity product competing only on price / distribution — learning velocity is not the moat.
- Pure execution sprint (rebrand, platform cutover) — wrong instrument; use stakeholder-management instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Strategy memo | markdown | PM / leadership |
| Competitive loss log | table {date, deal, competitor, cause} | sales / CRM |
| Quarterly OKRs | YAML | OKR cascade |
| Decision log | table {date, decision, owner, latency} | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[portfolio-strategy]] | Horizons frame which beliefs map to which bets. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: belief register, decision velocity, evidence freshness, loss attribution, kill criteria | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for belief-audit report | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: implicit beliefs, sunk-cost continuation, missing loss codes, stale evidence | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure: extract beliefs -> check freshness -> compute velocity -> tag losses -> audit memo | 800 |
| `content/05-examples.xml` | medium | Worked quarterly belief-audit with confidence deltas | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on stage + competitor density + audit window | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `belief-extract` | sonnet | Convert strategy memo into a structured belief register. |
| `evidence-freshness-audit` | haiku | Mechanical date comparison against thresholds. |
| `loss-attribution-synthesis` | opus | Cross-quarter pattern detection across loss codes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/belief-register.md` | Belief register skeleton (id, statement, confidence, last_update, evidence_type). |
| `templates/pm-learning-velocity.py` | Compute decision-velocity per category; emits JSON. |
| `templates/quarterly-audit-memo.md` | Quarterly belief-audit memo template. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-learning-speed-competitive-moat.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[portfolio-strategy]]
- [[product-lifecycle]]
- [[solo-pivot-decision-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pm-learning-velocity.py`

```python
"""

"""
pm_learning_velocity.py — score a PM's learning velocity from their decision log.
Inputs:
  decisions.yaml  (list of {id, ts, bet_id, decision, prediction, check_back_date, outcome, quarter, reversed_within_days})
Usage: python pm_learning_velocity.py decisions.yaml [--quarter 2026Q2]
"""
import sys, yaml, datetime, argparse, statistics

ap = argparse.ArgumentParser()
ap.add_argument("path")
ap.add_argument("--quarter", default=None)
args = ap.parse_args()

decisions = yaml.safe_load(open(args.path)) or []
if args.quarter:
    decisions = [d for d in decisions if d.get("quarter") == args.quarter]
if not decisions:
    sys.exit("no decisions in scope")

n = len(decisions)
reversed30 = sum(
    1 for d in decisions
    if d.get("reversed_within_days") and d["reversed_within_days"] <= 30
)
graded = [d for d in decisions if d.get("outcome") in ("hit", "miss")]
hit_rate = sum(1 for d in graded if d["outcome"] == "hit") / len(graded) if graded else None
kills = sum(1 for d in decisions if d["decision"] == "kill")
reframes = sum(1 for d in decisions if d["decision"] == "reframe")
mean_time_to_check = statistics.mean(
    [
        (
            datetime.date.fromisoformat(d["check_back_date"])
            - datetime.date.fromisoformat(d["ts"][:10])
        ).days
        for d in decisions if d.get("check_back_date")
    ]
) if decisions else 0

print(f"Decisions logged       : {n}")
print(f"Kill / reframe ratio   : {(kills + reframes) / n:.0%}  (target >=30%)")
print(f"Reversed within 30 days: {reversed30 / n:.0%}      (target <=15%)")
print(f"Mean time to check-back: {mean_time_to_check:.0f} days  (target <=21)")
if hit_rate is not None:
    print(f"Prediction hit rate    : {hit_rate:.0%}  (target 0.55-0.75 — outside = miscalibrated)")
else:
    print("Prediction hit rate    : insufficient graded sample")
```
