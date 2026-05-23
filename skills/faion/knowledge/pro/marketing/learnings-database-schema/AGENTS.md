---
slug: learnings-database-schema
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Defines the minimal schema (test, hypothesis, result, why, where-applicable, owner, ts) for a marketing learnings DB so weekly A/B reviews compound across cycles.
content_id: "e6f18ca65625527c"
complexity: medium
produces: spec
est_tokens: 5300
tags: ["marketing", "experimentation", "knowledge-management", "schema", "pro"]
---
# Marketing Learnings Database Schema

## Summary

**One-sentence:** Defines the minimal schema (test, hypothesis, result, why, where-applicable, owner, ts) for a marketing learnings DB so weekly A/B reviews compound across cycles.

**One-paragraph:** Even pro marketing teams lose 80% of test learnings within 30 days. This methodology specifies a minimal nine-field schema for a learnings DB (test, hypothesis, variant, result, p_value, why, where_applicable, owner, ts), plus query patterns ('show all learnings where channel=meta and outcome=positive'), the weekly review ritual that updates it, and the retire/archive rule. Output is a spec the team can implement in Notion, Airtable, Postgres, or git-backed YAML.

**Ефективно для:**

- Команди, що запускають >=2 A/B експерименти на тиждень і втрачають learnings.
- Solo growth-marketer, який хоче cumulative compounding learnings 6+ місяців.
- Перехід від ad-hoc Notion-нотаток до структурованої схеми + querying.
- Quarterly review: 'що ми вже знаємо про meta-creative offer-led variants'.

## Applies If (ALL must hold)

- Team or solo runs >= 2 documented experiments per cycle (weekly or biweekly).
- Operator wants cross-cycle compounding (learnings retrievable 6+ months later).
- Storage substrate exists (Notion / Airtable / Postgres / YAML repo).
- Named owner reviews and curates learnings each cycle.

## Skip If (ANY kills it)

- Team runs < 2 experiments per quarter — schema overhead > value.
- No named curator — DB becomes write-only and rots within 90 days.
- Experiments not documented at hypothesis level — schema cannot anchor.

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
| `draft-learnings-database-schema` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Markdown spec skeleton |
| `templates/output.json` | JSON spec sidecar with __faion_header__ |
| `templates/_smoke-test.md` | Minimum viable filled spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-learnings-database-schema.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
