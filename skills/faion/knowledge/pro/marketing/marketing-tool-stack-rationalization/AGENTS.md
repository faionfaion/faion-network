---
slug: marketing-tool-stack-rationalization
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Audits a sprawling marketing tool stack, scores each tool on usage/value/lock-in, and emits a consolidate / keep / kill decision report with migration steps.
content_id: "f54829e7d179a701"
complexity: medium
produces: report
est_tokens: 5300
tags: ["marketing", "tooling", "stack-audit", "consolidation", "pro"]
---
# Marketing Tool Stack Rationalization

## Summary

**One-sentence:** Audits a sprawling marketing tool stack, scores each tool on usage/value/lock-in, and emits a consolidate / keep / kill decision report with migration steps.

**One-paragraph:** Marketing tool sprawl is the single biggest opex inefficiency in solo-to-mid teams. This methodology inventories every tool (login + monthly cost + last-used + named owner + workflow-tier), scores each on usage / replaceable / lock-in, and emits a rationalization report categorizing tools into Keep / Consolidate / Kill, with migration steps per Consolidate and decommission steps per Kill. Output: report + 30-day execution checklist.

**Ефективно для:**

- Marketing teams з >=8 SaaS, де ніхто не може назвати усіх власників.
- Skip-renewal цикл: який tool можна kill before billing date.
- Підготовка до budget cut або acquisition: дешевший stack у документі.
- Post-merger consolidation двох overlapping marketing stacks.

## Applies If (ALL must hold)

- Marketing stack >= 8 distinct tools with monthly billing.
- Stack monthly cost >= $300 (otherwise audit overhead exceeds savings).
- Operator can access all admin consoles (no shadow-IT).
- Named owner per workflow exists so migration / decommission can happen.

## Skip If (ANY kills it)

- Stack < 5 tools — too small to rationalize.
- Mid-renewal-cycle with multi-year contracts — wait until renewal window.
- Team in active growth mode adding tools weekly — stabilize first, audit in 90 days.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs source-of-truth | system / dashboard / transcript | operator-managed |
| Prior artefact (if any) | Markdown / JSON / YAML | prior cycle |
| Named consumer for output | team contact / agent task | operator-managed |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | parent group context (vocabulary, neighbours) |
| [[learnings-database-schema]] | shared cumulative-knowledge substrate (if available) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-marketing-tool-stack-rationalization` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/report.md` | Markdown report skeleton |
| `templates/_smoke-test.md` | Minimum viable filled report |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-marketing-tool-stack-rationalization.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
