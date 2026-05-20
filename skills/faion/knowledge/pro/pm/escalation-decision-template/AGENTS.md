---
slug: escalation-decision-template
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "48445dab2b6ee817"
summary: Escalation Decision Template delivers a concrete, testable methodology that turns the recurring task of 'Run an escalation conversation with a stakeholder' into an auditable artefact, addressing the gap: stakeholder-engagement-advanced covers theory; missing a 1-pager template th
tags: [pm, pro, template, methodology]
---
# Escalation Decision Template

## Summary

**One-sentence:** Escalation Decision Template delivers a concrete, testable methodology that turns the recurring task of 'Run an escalation conversation with a stakeholder' into an auditable artefact, addressing the gap: stakeholder-engagement-advanced covers theory; missing a 1-pager template that forces options + tradeoffs + ask before the meeting.

**One-paragraph:** stakeholder-engagement-advanced covers theory; missing a 1-pager template that forces options + tradeoffs + ask before the meeting. Escalation Decision Template closes this gap with a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. The methodology is anchored to the triggering work 'Run an escalation conversation with a stakeholder' (role-project-manager, pro tier). It produces a structured artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Run an escalation conversation with a stakeholder' (role: role-project-manager) is in your current workload at least once per cycle.
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
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
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
| `escalation_decision_template_template_fill` | haiku | Template fill, no judgment |
| `escalation_decision_template_evidence_check` | sonnet | Bounded comparison + judgment |
| `escalation_decision_template_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies)
- triggering activity: `role-project-manager/Run an escalation conversation with a stakeholder`
- external: industry references cited inline in `content/01-core-rules.xml`
