# Judge Calibration Protocol

## Summary

**One-sentence:** Produces a calibrated LLM-as-judge with measured Cohen's κ ≥ 0.7 against a hand-labelled holdout — judge prompt, fixture, calibration report.

**One-paragraph:** Most "LLM-as-judge" setups are uncalibrated: the team writes a judge prompt, eyeballs a few cases, and gates production on the judge's verdicts. Without κ measurement the gate measures judge quality, not system quality, and any drift in either layer is invisible. This protocol hand-labels a holdout (≥30 cases), runs the judge against it, computes Cohen's κ + per-class confusion + false-pass / false-fail rates, and either ships the judge (κ ≥ 0.7) or returns it for revision. Re-calibrate quarterly or on any prompt/model change.

**Ефективно для:** binary-label judges (refused/complied, correct/incorrect, safe/unsafe), preference judges (a-better-than-b), rubric judges with ≤5 ordered categories.

## Applies If (ALL must hold)

- An LLM is being used to score model outputs (binary or ordinal label).
- A human can label ≥30 cases in the same time budget as one calibration cycle.
- The judge's verdict feeds into a gate, dashboard, or training signal — not just a research log.
- A storage location exists for the calibration fixture + report.

## Skip If (ANY kills it)

- Judge is purely advisory (no downstream action depends on its verdict).
- Cases are unlabelled in principle (subjective preferences with no ground truth) — use pairwise comparison protocol instead.
- Holdout is contaminated (already used in judge prompt examples).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Sample of system outputs | JSONL | production logs / eval runs |
| Reference labels | hand-typed by an operator | spreadsheet, 30+ rows |
| Judge prompt draft | Markdown | prior eval design |
| Compute budget | minutes of judge-model time | secrets / quota |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[ai-failure-mode-taxonomy]]` | Names the categories the judge labels. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: ≥30-case holdout, κ ≥ 0.7, confusion-matrix logged, recalibrate on prompt/model change, no judge-on-judge, contamination check | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for calibration-report.json | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: skipped calibration, contaminated holdout, single-rater label, κ-once-never-again, single-failure-class bias | ~600 |
| `content/04-procedure.xml` | medium | 6-step procedure: scope label → label holdout → run judge → compute κ → diagnose → ship or revise | ~900 |
| `content/06-decision-tree.xml` | essential | Root: "is the judge gating any downstream action?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Generate holdout sampling plan | sonnet | Stratify cases by category/risk. |
| Compute κ + confusion matrix | haiku | Deterministic numerical. |
| Diagnose disagreement clusters | opus | Cross-case reasoning. |
| Author refined judge prompt | opus | Adversarial creativity. |

## Templates

| File | Purpose |
|---|---|
| `templates/calibration-report.schema.json` | JSON Schema for the report. |
| `templates/holdout.jsonl` | Hand-label fixture skeleton (id + content + label slots). |
| `templates/judge-prompt-skeleton.md` | Binary-label judge prompt skeleton with positive/negative examples. |
| `templates/_smoke-test.jsonl` | 5-row fixture for the protocol smoke loop. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-judge-calibration-protocol.py` | Validates calibration-report.json against schema and asserts κ ≥ 0.7 + non-empty confusion matrix. | After computing report; CI before shipping the judge. |

## Related

- parent skill: `geek/ai/`
- `[[jailbreak-eval-suite-bootstrap]]` — primary consumer of calibrated judges
- `[[llm-drift-daily-triage]]` — re-runs calibration on model upgrade

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether to run calibration: skip when the judge is advisory; mandate when the judge gates production or training. Branches on holdout availability and contamination.
