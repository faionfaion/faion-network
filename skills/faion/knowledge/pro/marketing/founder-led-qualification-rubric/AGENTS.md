---
slug: founder-led-qualification-rubric
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "a70d99a327f1358d"
summary: "Founder Led Qualification Rubric — testable methodology for growth, acquisition, content, GTM. Founders without sales background overqualify; a simple yes/no rubric prevents wasted proposal cycles."
tags: [marketing, pro, methodology]
---
# Founder Led Qualification Rubric

## Summary

**One-sentence:** Founder Led Qualification Rubric — testable methodology for growth, acquisition, content, GTM. Founders without sales background overqualify; a simple yes/no rubric prevents wasted proposal cycles.

**One-paragraph:** Founder Led Qualification Rubric closes a known gap in marketing practice: Founders without sales background overqualify; a simple yes/no rubric prevents wasted proposal cycles. The methodology is anchored to the recurring activity 'Discovery call run (45 min) (role: p5-micro-agency-founder)' and produces an auditable artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Discovery call run (45 min) (role: p5-micro-agency-founder)' shows up in the user's workload at least once per cycle.
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
| `pro/marketing/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3-5 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 4-8 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `founder_led_qualification_rubric_template_fill` | haiku | Template fill, no judgement |
| `founder_led_qualification_rubric_evidence_check` | sonnet | Bounded comparison + judgement |
| `founder_led_qualification_rubric_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `pro/marketing/` (see neighbouring methodologies)
- triggering activity: `Discovery call run (45 min) (role: p5-micro-agency-founder)`
- external: industry references cited inline in `content/01-core-rules.xml`
