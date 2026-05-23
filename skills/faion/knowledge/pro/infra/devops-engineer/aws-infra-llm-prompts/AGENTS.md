---
slug: aws-infra-llm-prompts
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces parameterized LLM prompt templates for AWS architecture design conversations with structured context, constraints, and required output format.
content_id: "990761440bc69874"
complexity: medium
produces: spec
est_tokens: 4500
tags: [aws, llm-prompts, infrastructure-design, prompt-engineering]
---
# AWS Infrastructure Design — LLM Prompt Templates

## Summary

**One-sentence:** Produces parameterized LLM prompt templates for AWS architecture design conversations with structured context, constraints, and required output format.

**One-paragraph:** Parameterized LLM prompt templates for AWS infrastructure design conversations. Each prompt includes context variables, workload characteristics, constraints, and required output format to produce actionable designs rather than generic advice. Templates cover: new architecture design, existing architecture review for security / cost / reliability gaps, IAM policy generation, DR runbook generation, database / workload migration planning. Output must conform to a JSON schema so downstream automation can consume the design.

**Ефективно для:**

- новий AWS architecture conversation — структуроване context elicitation.
- review existing architecture на security / cost / reliability gaps через LLM аналіз.
- generating IAM policies, DR runbooks, scaling configurations через LLM.
- planning database / workload migrations to AWS.

## Applies If (ALL must hold)

- Designer is starting or reviewing an AWS architecture conversation through an LLM.
- Workload context (request profile, data shape, latency target, compliance constraints) is documented.
- Output must conform to a JSON schema so downstream automation can consume the design.
- LLM provider is configured with the project's API key (not an inherited shared key).

## Skip If (ANY kills it)

- Direct CLI operations — use aws-cli-compute or aws-cli-containers-iac.
- Generating actual infrastructure code from scratch — use templates from aws-cfn-terraform-templates as the base instead.
- Compliance documentation — LLM output needs expert review for HIPAA / PCI / SOC2 submissions.
- Designer cannot articulate workload context — fix that upstream before prompting.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload context doc | Markdown | product |
| Constraints (compliance, budget) | Markdown | product |
| Required output schema | JSON Schema | downstream consumer |
| LLM provider API key | env var | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/aws-foundations` | architecture context assumed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/05-examples.xml` | medium | One full worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `select-prompt-template` | haiku | Match intent to design / review / IAM / DR / migration |
| `populate-context` | sonnet | Fill in workload + constraints + required output schema |
| `lint-output` | haiku | Verify response against schema before downstream use |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-prompt.md` | Parameterized architecture design prompt |
| `templates/review-prompt.md` | Architecture review prompt template |
| `templates/skeleton.json` | JSON shape for the prompt artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aws-infra-llm-prompts.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[aws-foundations]]
- [[aws-cfn-terraform-templates]]
- [[aws-cli-compute]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the AWS Infrastructure Design — LLM Prompt Templates methodology when in doubt about scope or fit.
