---
slug: sdlc-ai
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a routing decision-record that picks among 78 SDLC+AI methodologies (lang/lint/test/tracker/kb/task/mr/inc/sec/gov) for a given task signal.
content_id: "20eff135fbee0f93"
complexity: medium
produces: decision-record
est_tokens: 3400
tags: ["sdlc-ai", "domain-index", "routing", "overview"]
---
# SDLC + AI Domain Overview

## Summary

**One-sentence:** Produces a routing decision-record that picks among 78 SDLC+AI methodologies (lang/lint/test/tracker/kb/task/mr/inc/sec/gov) for a given task signal.

**One-paragraph:** SDLC + AI Domain Overview produces a decision-record that fixes a recurring decision in the sdlc-ai domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Підібрати правильну sub-methodology у sdlc-ai домені.
- Onboarding: огляд того, що домен охоплює.
- Audit: бачимо повний inventory методологій + last-review.
- Cross-cluster pick: lang vs lint vs test — швидкий router.
- Domain health check: які кластери порожні?

## Applies If (ALL must hold)

- Task signal involves wiring AI coding agents into the SDLC floor.
- Multiple sub-methodologies are candidates and disambiguation is needed.
- Reader is new to the sdlc-ai domain.

## Skip If (ANY kills it)

- Task is clearly outside sdlc-ai (e.g. UX research, marketing).
- Reader already knows the exact methodology slug.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal | Markdown / JSON | user |
| Domain INDEX.xml | XML | faion-network |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-sdlc-ai` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/routing-decision.md` | Markdown decision record naming task signal + chosen candidates + rationale |
| `templates/sdlc-ai-route.schema.json` | JSON Schema for the routing decision artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sdlc-ai.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[kb-agents-md-context-pyramid]]
- [[lint-precommit-floor]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
