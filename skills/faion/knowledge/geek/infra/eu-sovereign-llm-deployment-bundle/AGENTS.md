---
slug: eu-sovereign-llm-deployment-bundle
tier: geek
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Production deployment spec for EU-sovereign LLM stack: in-EU inference, EU-Act compliance hooks, in-EU vector store + observability, no-egress data plane."
content_id: "d5fcadc7f0bad15b"
complexity: deep
produces: spec
est_tokens: 4600
tags: [eu-ai-act, sovereign-cloud, llm, gaia-x, geek, infra]
---

# EU Sovereign LLM Deployment Bundle

## Summary

**One-sentence:** Production deployment spec for EU-sovereign LLM stack: in-EU inference, EU-Act compliance hooks, in-EU vector store + observability, no-egress data plane.

**One-paragraph:** Production deployment spec for EU-sovereign LLM stack: in-EU inference, EU-Act compliance hooks, in-EU vector store + observability, no-egress data plane. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`spec`) at a deep complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- EU-customer-facing AI workload subject to EU AI Act + GDPR.
- Customer contracts demand EU sovereign data plane (no US transfer).
- Risk class is high-risk OR limited-risk-with-sectoral-overlay (finance, health, public sector).

## Skip If (ANY kills it)

- Customers do not require EU sovereignty — generic deployment suffices.
- Workload is minimal-risk under the EU AI Act AND no PII — overhead unjustified.
- Pre-revenue prototype not yet customer-facing.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Risk classification | Markdown | eu-ai-act-compliance |
| In-EU inference provider | contract | procurement |
| In-EU vector store | service | infra |
| Audit logger | OTel + storage | compliance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/eu-ai-act-compliance` | Regulatory layer this deployment must satisfy. |
| `geek/infra/banking-core-data-residency-rules` | Residency framework reused for AI workloads. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/05-examples.xml` | medium | One end-to-end worked example | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `risk_classification` | opus | Regulatory judgment with cross-input synthesis. |
| `provider_due_diligence` | opus | Sub-processor chain + sovereignty audit. |
| `deployment_spec_draft` | sonnet | Bounded transform from policy to IaC spec. |

## Templates

| File | Purpose |
|------|---------|
| `templates/deployment-spec.md` | End-to-end deployment with residency + audit + monitoring. |
| `templates/provider-due-diligence.md` | Vendor sovereignty checklist. |
| `templates/audit-event-schema.json` | Required AI Act audit event shape. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-eu-sovereign-llm-deployment-bundle.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[eu-ai-act-compliance]]`
- `[[banking-core-data-residency-rules]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether eu-sovereign-llm-deployment-bundle applies: root question — "Is the workload EU-customer-facing AND classified high-risk OR sectoral overlay?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
