---
slug: error-budget-policy-and-freeze-rules
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "4a96104b4377a778"
summary: Error Budget Policy And Freeze Rules delivers a concrete, testable methodology that turns the recurring task of 'Design SLOs + error budgets before first deploy' into an auditable artefact, addressing the gap: Once SLOs exist someone has to write the policy that converts burn int
tags: [infra, pro, policy, methodology]
---
# Error Budget Policy And Freeze Rules

## Summary

**One-sentence:** Error Budget Policy And Freeze Rules delivers a concrete, testable methodology that turns the recurring task of 'Design SLOs + error budgets before first deploy' into an auditable artefact, addressing the gap: Once SLOs exist someone has to write the policy that converts burn into action (ship freeze, reliability sprint). Currently nothing across all 1300+ methodologies addresses the org/policy side of SRE.

**One-paragraph:** Once SLOs exist someone has to write the policy that converts burn into action (ship freeze, reliability sprint). Currently nothing across all 1300+ methodologies addresses the org/policy side of SRE. Error Budget Policy And Freeze Rules closes this gap with a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. The methodology is anchored to the triggering work 'Design SLOs + error budgets before first deploy' (role-devops-engineer, pro tier). It produces a structured artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Design SLOs + error budgets before first deploy' (role: role-devops-engineer) is in your current workload at least once per cycle.
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
| `error_budget_policy_and_freeze_rules_template_fill` | haiku | Template fill, no judgment |
| `error_budget_policy_and_freeze_rules_evidence_check` | sonnet | Bounded comparison + judgment |
| `error_budget_policy_and_freeze_rules_synthesis` | opus | Cross-input synthesis + final write-up |

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
- triggering activity: `role-devops-engineer/Design SLOs + error budgets before first deploy`
- external: industry references cited inline in `content/01-core-rules.xml`
