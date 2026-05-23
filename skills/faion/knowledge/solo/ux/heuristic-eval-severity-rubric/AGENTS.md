---
slug: heuristic-eval-severity-rubric
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Calibrated 0..4 severity scale for Nielsen-style heuristic evaluation with anchored examples per level so two evaluators rate the same violation within ±1 of each other.
content_id: "37cfe6af0d64c638"
complexity: medium
produces: rubric
est_tokens: 3600
tags: ["heuristic-evaluation", "severity", "rubric", "calibration", "ux"]
---
# Heuristic Eval Severity Rubric

## Summary

**One-sentence:** Calibrated 0..4 severity scale for Nielsen-style heuristic evaluation with anchored examples per level so two evaluators rate the same violation within ±1 of each other.

**One-paragraph:** Nielsen's heuristics methodology lacks an in-band severity rubric — evaluators drift on what 'major' means. This rubric pins a 0..4 scale anchored by examples: 0 cosmetic (no user impact), 1 minor (workaround obvious), 2 major (workaround painful), 3 catastrophic (task blocked), 4 catastrophic + safety/accessibility/regulatory. Each level carries a calibration example; pair-rating drift is measured and re-calibrated quarterly.

**Ефективно для:**

- Solo designer running quarterly heuristic walkthroughs who needs comparable scores over time.
- Two designers doing pair heuristic evaluation who need to converge on severity.
- AI agent generating heuristic reports that must rate findings within the rubric.
- Audit context where rating drift would invalidate the report.

## Applies If (ALL must hold)

- A heuristic evaluation (Nielsen 10 or comparable) is being run.
- At least 2 evaluators or 1 evaluator + 1 reviewer.
- Findings will be acted on (triage, fix, document) — not discarded.
- Calibration examples are available or can be drafted.

## Skip If (ANY kills it)

- Free-form discount usability test, not a heuristic eval — use critical-issue-triage-protocol.
- Single evaluator with no review — rubric overhead exceeds benefit.
- Heuristic eval is informal warm-up, not committed to triage.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Heuristic list (Nielsen 10 or variant) | list | Established heuristic source |
| Calibration examples per level | array of examples | Prior eval or rubric library |
| Pair-rating drift threshold | integer (max ±1) | Team agreement |
| Findings list | array | Eval session output |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/critical-issue-triage-protocol` | Triage consumes severity ratings. |
| `solo/ux/anti-pattern-rationale-template` | Repeated severity-3+ findings feed the bank. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `rate-finding` | sonnet | Per-finding judgement using the rubric. |
| `calibration-drift-check` | haiku | Deterministic delta calc between paired ratings. |
| `rubric-refresh` | opus | Quarterly recalibration with anchor refresh. |

## Templates

| File | Purpose |
|------|---------|
| `templates/heuristic-eval-severity-rubric.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/heuristic-eval-severity-rubric.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-heuristic-eval-severity-rubric.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[critical-issue-triage-protocol]]
- [[anti-pattern-rationale-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
