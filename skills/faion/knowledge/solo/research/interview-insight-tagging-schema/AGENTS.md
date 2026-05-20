---
slug: interview-insight-tagging-schema
tier: solo
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "c2b02925c7e1fd90"
summary: "Interview Insight Tagging Schema — testable methodology for interviews, evidence, synthesis. Existing user-interviews methodology covers running interviews; there is no shared taxonomy for atomic-insight tagging that feeds an opportunity tree."
tags: [research, solo, methodology]
---
# Interview Insight Tagging Schema

## Summary

**One-sentence:** Interview Insight Tagging Schema — testable methodology for interviews, evidence, synthesis. Existing user-interviews methodology covers running interviews; there is no shared taxonomy for atomic-insight tagging that feeds an opportunity tree.

**One-paragraph:** Interview Insight Tagging Schema closes a known gap in research practice: Existing user-interviews methodology covers running interviews; there is no shared taxonomy for atomic-insight tagging that feeds an opportunity tree. The methodology is anchored to the recurring activity 'User interview prep + run (role: role-product-manager)' and produces an auditable artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'User interview prep + run (role: role-product-manager)' shows up in the user's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — the artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems, dashboards, or transcripts that feed the methodology's inputs.
- A storage location for the produced artefact (git repo, doc, ticket) where the consumer can read it.
- Prior cycle's artefact (if any) accessible for carry-forward and trend comparison.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `solo/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3-5 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 4-8 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `interview_insight_tagging_schema_template_fill` | haiku | Template fill, no judgement |
| `interview_insight_tagging_schema_evidence_check` | sonnet | Bounded comparison + judgement |
| `interview_insight_tagging_schema_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `solo/research/` (see neighbouring methodologies)
- triggering activity: `User interview prep + run (role: role-product-manager)`
- external: industry references cited inline in `content/01-core-rules.xml`
