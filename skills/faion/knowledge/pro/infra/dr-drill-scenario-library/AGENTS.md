---
slug: dr-drill-scenario-library
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "674c7776b8755303"
summary: Dr Drill Scenario Library delivers a concrete, testable methodology that turns the recurring task of 'Disaster-recovery drill + plan refresh (4 weeks)' into an auditable artefact, addressing the gap: A reusable catalogue of DR scenarios (region loss, db corruption, secret-store l
tags: [infra, pro, runbook, methodology]
---
# Dr Drill Scenario Library

## Summary

**One-sentence:** Dr Drill Scenario Library delivers a concrete, testable methodology that turns the recurring task of 'Disaster-recovery drill + plan refresh (4 weeks)' into an auditable artefact, addressing the gap: A reusable catalogue of DR scenarios (region loss, db corruption, secret-store loss, dependency outage) with expected RTO/RPO bands. Backup methodologies exist but no scenario library.

**One-paragraph:** A reusable catalogue of DR scenarios (region loss, db corruption, secret-store loss, dependency outage) with expected RTO/RPO bands. Backup methodologies exist but no scenario library. Dr Drill Scenario Library closes this gap with a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. The methodology is anchored to the triggering work 'Disaster-recovery drill + plan refresh (4 weeks)' (role-devops-engineer, pro tier). It produces a structured artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Disaster-recovery drill + plan refresh (4 weeks)' (role: role-devops-engineer) is in your current workload at least once per cycle.
- You have authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the artefact — human reviewer OR downstream agent.
- An auditable source-of-truth is available for the inputs the methodology needs.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems / dashboards / docs that feed the methodology's inputs.
- A storage location for the produced artefact (git repo, doc, ticket) where the consumer can read it.
- Prior cycle's artefact (if any) accessible for carry-forward and trend comparison.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `dr_drill_scenario_library_template_fill` | haiku | Template fill, no judgment |
| `dr_drill_scenario_library_evidence_check` | sonnet | Bounded comparison + judgment |
| `dr_drill_scenario_library_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `pro/infra/` (see neighbouring methodologies)
- triggering activity: `role-devops-engineer/Disaster-recovery drill + plan refresh (4 weeks)`
- external: industry references cited inline in `content/01-core-rules.xml`
