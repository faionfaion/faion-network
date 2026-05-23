# AI Feature De-Risking

## Summary

**One-sentence:** A pre-registered AI-feature de-risking pipeline — pre-committed kill-criteria, frozen versioned eval set, n + mean + CI reporting, quarterly judge-LLM recalibration, and bounded eval cost — so quality is comparable across runs and features stop shipping without measurable value.

**One-paragraph:** Geek tier covers agentic-AI product development conceptually but ships no de-risking pipeline (fake-door, Wizard-of-Oz, eval harness, kill-criteria pre-registration). The gap lets AI features ship on vibes and silently regress. This methodology pins five testable rules: kill-criteria committed BEFORE the first eval run, eval ground-truth versioned and frozen per comparison, every report carries n + mean + confidence interval, judge-LLM recalibrated against ≥20 human-labeled examples per quarter, and per-example eval cost logged with a 2×-of-daily-prod-cost ceiling. Output: a versioned eval report + a published kill-criteria record + a quarterly judge calibration log.

**Ефективно для:** AI PM, який не хоче, щоб новий prompt версією 4.7 тихо просів на 8% і ніхто цього не помітив.

## Applies If (ALL must hold)

- Stabilising or comparing AI feature behaviour across model / prompt / retrieval versions.
- A ground-truth set ≥30 examples exists OR can be assembled in one work-cycle.
- Eval results gate at least one production decision (deploy, rollback, freeze).
- Cost ceiling per eval run is defined before the first run.
- A judge model (LLM or human) is available for scoring.

## Skip If (ANY kills it)

- Pre-MVP exploration where output quality is judged by founders eyeballing.
- Features so niche that authoring a ground-truth set takes longer than 3 sprints.
- Cost-prohibitive evals when cheaper proxies (regression of intermediate metric) cover the risk.
- Single-vendor managed AI feature with no version control over prompt or model.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Ground-truth set (≥30 examples) | jsonl / csv | QA / eval engineering |
| Pre-registered kill-criteria | YAML | product spec, committed |
| Judge function (LLM or human) | code / SOP | eval engineering |
| Cost dashboard or per-run budget | URL | finance + AI eng |
| Named owner | role + person | product team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/product/product-manager/ai-native-product-development` | Provides product-positioning context. |
| `geek/product/product-manager/agentic-ai-product-development` | Sibling that consumes the de-risking output as a gate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: kill-criteria pre-registered, frozen eval set, n + mean + CI, judge recalibration, bounded cost | ~1000 |
| `content/02-output-contract.xml` | essential | Eval report schema + forbidden patterns + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Pre-registered? + frozen-set? + cost-ceiling? gates | ~340 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `eval_runner_orchestration` | haiku | Test harness driver, deterministic. |
| `judge_scoring` | sonnet | LLM-as-judge per rubric. |
| `regression_diagnosis` | opus | Cross-version drift analysis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/eval-report.md` | Markdown skeleton for the versioned eval report. |
| `templates/kill-criteria.yaml` | YAML schema for pre-registered thresholds. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-feature-de-risking.py` | Enforce the eval-report contract (kill-criteria present, set version pinned, n + mean + CI present, cost logged). | After every eval run, before commit / publish. |

## Related

- [[ai-native-product-development]] — sibling methodology providing positioning context.
- [[agentic-ai-product-development]] — peer methodology consuming the de-risking output as a gate.
- [[ai-product-success-metrics-catalog]] — peer that consumes the same reports.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether kill-criteria are pre-registered AND the eval set is frozen AND a cost ceiling is set. If any are missing → block. Otherwise → run the eval and emit the report.
