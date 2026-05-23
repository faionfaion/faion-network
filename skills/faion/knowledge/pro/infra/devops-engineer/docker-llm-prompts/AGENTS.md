---
slug: docker-llm-prompts
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a Docker LLM prompt library: parameterized prompts for Dockerfile generation, optimization audit, security review, troubleshooting, CI integration, and architecture review.
content_id: "ce291bf14ef8cc45"
complexity: light
produces: code
est_tokens: 4100
tags: [docker, llm, prompts, ai-assisted, templates]
---
# Docker LLM Prompt Templates

## Summary

**One-sentence:** Generates a Docker LLM prompt library: parameterized prompts for Dockerfile generation, optimization audit, security review, troubleshooting, CI integration, and architecture review.

**One-paragraph:** Generates a Docker LLM prompt library: parameterized prompts for Dockerfile generation, optimization audit, security review, troubleshooting, CI integration, and architecture review. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- "Generate production Dockerfile for FastAPI + Postgres + Redis" prompt.
- Security audit prompt — повертає structured findings list.
- Troubleshoot container start failure прийом-логів-як-input.
- Architecture review prompt для multi-container stack.

## Applies If (ALL must hold)

- Team uses an LLM (Claude / GPT / etc.) for Docker tasks ≥1×/week.
- Prompts can be versioned and reused across engineers.
- Output structure (Dockerfile / list / table) is desired — not free chat.

## Skip If (ANY kills it)

- Team does not adopt LLM-driven Docker workflows.
- Use case is one-off — a quick chat prompt is cheaper than a templated library.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target tasks | list of recurring Docker tasks | Platform team |
| Preferred LLM + model | free-form | Platform team |
| Output shape requirements | table (task → shape) | Platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/docker/AGENTS.md` | Docker baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-docker-llm-prompts` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-docker-llm-prompts.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[docker]]
- [[docker-image-optimization]]
- [[docker-security-hardening]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
