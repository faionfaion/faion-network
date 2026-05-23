# Modern BA Framework: BABOK for Agile, AI/ML, Cloud, and Platform Delivery

## Summary

**One-sentence:** Perspective routing wrapper over BABOK that maps the ask to a perspective (agile, AI/ML, cloud-native, platform, BI, BizArch, BPM) and adapts KA tasks + deliverables accordingly.

**One-paragraph:** A meta-framework for applying BABOK's six KAs to modern delivery contexts: agile, AI/ML, cloud-native, platform engineering, BI, BizArch, BPM. Without explicit perspective declaration, LLMs default to the Agile perspective and miss BI/BizArch/BPM concerns. Output is a perspective-aware BA approach record that adapts KA tasks for the chosen perspective set.

**Ефективно для:**

- Mixed-perspective programs (AI/ML + platform + BI).
- Cloud-native modernisation з infra + governance lenses.
- BI workstream з metric ownership + lineage acceptance criteria.
- Platform engineering з internal-developer-platform requirements.

## Applies If (ALL must hold)

- Mixed-perspective programme (e.g., AI/ML + platform + BI together).
- Cloud-native modernisation requiring infra + governance lens together.
- Agile programme that needs BPM perspective (process work).
- BI/analytics workstream that needs explicit metric ownership + lineage.
- Platform engineering with internal-developer-platform requirements.

## Skip If (ANY kills it)

- Pure single-perspective work (vanilla agile sprint).
- Hot fixes / single tickets.
- When the team has a fixed enterprise framework that overrides BABOK.
- Where ad-hoc routing in knowledge-areas-overview suffices.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Programme charter | Markdown | sponsor |
| Perspective set declaration | Markdown | BA / chief architect |
| KA routing record | JSON | knowledge-areas-overview |
| Deliverable expectations | Markdown | BA |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/knowledge-areas-overview` | Provides L1 KA routing. |
| `pro/ba/business-analyst/methodologies-detail` | Provides per-framework templates. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `perspective-classification` | sonnet | Map programme to perspective set. |
| `ka-adaptation` | sonnet | Adapt KA tasks per perspective. |
| `deliverable-templating-per-perspective` | haiku | Pick correct template variant. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ba-approach-init.sh` | Init script for a new perspective-aware BA approach record. |
| `templates/ba-approach.json` | JSON record of perspective + KA + deliverables. |
| `templates/_smoke-test.json` | Minimum filled-in approach record. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-modern-ba-framework.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[knowledge-areas-overview]]
- [[knowledge-areas-detail]]
- [[methodologies-detail]]
- [[process-mining-automation]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
