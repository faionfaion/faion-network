---
slug: eu-sovereign-llm-deployment-bundle
tier: geek
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "5b50deb944430830"
summary: End-to-end bundle for deploying a sovereign EU-hosted LLM stack (Ollama / vLLM, networking, governance, evals) suitable for data-residency-bound customers.
tags: [llm, eu, sovereignty, data-residency, ollama, vllm]
---
# Eu Sovereign Llm Deployment Bundle

## Summary

**One-sentence:** End-to-end bundle for deploying a sovereign EU-hosted LLM stack (Ollama / vLLM, networking, governance, evals) suitable for data-residency-bound customers.

**One-paragraph:** Geek-tier builders selling to EU customers face data-residency demands. A bundled methodology covering Ollama / vLLM stack, networking, governance, eval would be a real differentiator. Eu Sovereign Llm Deployment Bundle closes this gap with a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. The methodology is anchored to the triggering work 'Multi-model gateway migration: lock-in to portability (2 months)' (p7-llm-agent-developer, geek tier). It produces a structured artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Multi-model gateway migration: lock-in to portability (2 months)' (role: p7-llm-agent-developer) is in your current workload at least once per cycle.
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
| `geek/infra/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `geek/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `eu_sovereign_llm_deployment_bundle_template_fill` | haiku | Template fill, no judgment |
| `eu_sovereign_llm_deployment_bundle_evidence_check` | sonnet | Bounded comparison + judgment |
| `eu_sovereign_llm_deployment_bundle_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `geek/infra/` (see neighbouring methodologies)
- triggering activity: `p7-llm-agent-developer/Multi-model gateway migration: lock-in to portability (2 months)`
- external: industry references cited inline in `content/01-core-rules.xml`
