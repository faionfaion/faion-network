---
slug: docker-llm-prompts
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Parameterized LLM prompt templates for the full range of Docker tasks: generating production Dockerfiles, optimizing existing ones, auditing for security, debugging container failures, integrating CI/CD scanning, and designing multi-container architectures.
content_id: "22314e55ceadbc01"
tags: [docker, llm-prompts, containerization, prompt-engineering, ci-cd]
---
# Docker LLM Prompts

## Summary

**One-sentence:** Parameterized LLM prompt templates for the full range of Docker tasks: generating production Dockerfiles, optimizing existing ones, auditing for security, debugging container failures, integrating CI/CD scanning, and designing multi-container architectures.

**One-paragraph:** Parameterized LLM prompt templates for the full range of Docker tasks: generating production Dockerfiles, optimizing existing ones, auditing for security, debugging container failures, integrating CI/CD scanning, and designing multi-container architectures. Fill in the bracketed variables and submit to any capable model.

## Applies If (ALL must hold)

- Generating a new Dockerfile for a language/framework combination not covered by the language templates.
- Auditing an existing Dockerfile against 2025-2026 best practices without reading the full methodology.
- Debugging a container build or runtime failure with structured context.
- Generating CI pipeline steps for Docker build, test, scan, and push.
- Designing multi-container architectures or migrating Docker Compose to Kubernetes.

## Skip If (ANY kills it)

- When the exact Dockerfile is available in docker-language-templates — use it directly instead of prompting.
- When the LLM output cannot be reviewed before deployment — always validate generated Dockerfiles against the checklist in docker-image-optimization and docker-security-hardening.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/devops-engineer/`
