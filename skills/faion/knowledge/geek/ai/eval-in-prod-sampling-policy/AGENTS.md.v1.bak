---
slug: eval-in-prod-sampling-policy
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "003a949839a5ff93"
summary: Eval In Prod Sampling Policy delivers a concrete, testable methodology that turns the recurring task of 'Observability + drift detection rollout (3 weeks)' into an auditable artefact, addressing the gap: Sampling N% of prod traffic for judge-eval has cost, privacy, and selection-
tags: [ai, geek, policy, methodology]
---
# Eval In Prod Sampling Policy

## Summary

**One-sentence:** Eval In Prod Sampling Policy delivers a concrete, testable methodology that turns the recurring task of 'Observability + drift detection rollout (3 weeks)' into an auditable artefact, addressing the gap: Sampling N% of prod traffic for judge-eval has cost, privacy, and selection-bias gotchas. Needs an opinionated policy methodology.

**One-paragraph:** Sampling N% of prod traffic for judge-eval has cost, privacy, and selection-bias gotchas. Needs an opinionated policy methodology. Eval In Prod Sampling Policy closes this gap with a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. The methodology is anchored to the triggering work 'Observability + drift detection rollout (3 weeks)' (p7-llm-agent-developer, geek tier). It produces a structured artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Observability + drift detection rollout (3 weeks)' (role: p7-llm-agent-developer) is in your current workload at least once per cycle.
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
| `geek/ai/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `geek/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `eval_in_prod_sampling_policy_template_fill` | haiku | Template fill, no judgment |
| `eval_in_prod_sampling_policy_evidence_check` | sonnet | Bounded comparison + judgment |
| `eval_in_prod_sampling_policy_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `geek/ai/` (see neighbouring methodologies)
- triggering activity: `p7-llm-agent-developer/Observability + drift detection rollout (3 weeks)`
- external: industry references cited inline in `content/01-core-rules.xml`
