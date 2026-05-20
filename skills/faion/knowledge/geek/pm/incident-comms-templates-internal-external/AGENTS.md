---
slug: incident-comms-templates-internal-external
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "c6e2fff377c763df"
summary: "Incident Comms Templates Internal External — testable methodology for delivery, scheduling, RACI, throughput. Communications-management is generic. Incidents need ready-to-edit templates for status page, customer email, exec brief, and internal channel; absence costs minutes during outages."
tags: [pm, geek, methodology]
---
# Incident Comms Templates Internal External

## Summary

**One-sentence:** Incident Comms Templates Internal External — testable methodology for delivery, scheduling, RACI, throughput. Communications-management is generic. Incidents need ready-to-edit templates for status page, customer email, exec brief, and internal channel; absence costs minutes during outages.

**One-paragraph:** Incident Comms Templates Internal External closes a known gap in pm practice: Communications-management is generic. Incidents need ready-to-edit templates for status page, customer email, exec brief, and internal channel; absence costs minutes during outages. The methodology is anchored to the recurring activity 'Incident → postmortem → preventive backlog (role: p6-product-dev-team)' and produces an auditable artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Incident → postmortem → preventive backlog (role: p6-product-dev-team)' shows up in the user's workload at least once per cycle.
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
| `geek/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `geek/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3-5 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 4-8 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `incident_comms_templates_internal_external_template_fill` | haiku | Template fill, no judgement |
| `incident_comms_templates_internal_external_evidence_check` | sonnet | Bounded comparison + judgement |
| `incident_comms_templates_internal_external_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `geek/pm/` (see neighbouring methodologies)
- triggering activity: `Incident → postmortem → preventive backlog (role: p6-product-dev-team)`
- external: industry references cited inline in `content/01-core-rules.xml`
