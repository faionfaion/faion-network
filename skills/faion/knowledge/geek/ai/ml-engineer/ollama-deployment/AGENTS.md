---
slug: ollama-deployment
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Configures Ollama for production: GPU pinning, model preload, host binding, reverse proxy, auth layer, observability, and resource limits.
content_id: "61cae8bbdcece36a"
complexity: medium
produces: config
est_tokens: 4300
tags: [ollama, deployment, gpu, production, ops]
---
# Ollama Production Deployment

## Summary

**One-sentence:** Configures Ollama for production: GPU pinning, model preload, host binding, reverse proxy, auth layer, observability, and resource limits.

**One-paragraph:** Configures Ollama for production: GPU pinning, model preload, host binding, reverse proxy, auth layer, observability, and resource limits. The methodology assumes the inputs in Prerequisites and produces a `config` artefact validated by `scripts/validate-ollama-deployment.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** DevOps and ML ops engineers running Ollama in shared/team or single-tenant production environments.

## Applies If (ALL must hold)

- Deploying Ollama as a shared service for multiple applications or users.
- Running Ollama in a containerized environment (Docker, Kubernetes).
- Bare-metal production server where Ollama runs as a background service.
- Exposing Ollama through a reverse proxy with authentication and rate limiting.
- Creating custom model variants with fixed system prompts for specific use cases.

## Skip If (ANY kills it)

- Local development on a single machine — ollama serve directly is simpler.
- One-off batch jobs — Docker overhead is not justified for temporary use.
- Environments without GPU access — CPU-only inference is often better handled by cloud APIs at comparable cost.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[ollama-setup-models]]` | Adjacent context the agent normally already has when this methodology fires. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules with rationale and source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples for the output artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix. | ~800 |
| `content/04-procedure.xml` | medium | Five-step procedure with decision-gates. | ~700 |
| `content/05-examples.xml` | medium | One end-to-end worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether the methodology applies, ending in rule refs. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-defaults` | sonnet | Bounded judgment from inputs. |
| `emit-config` | haiku | Template fill. |
| `validate-config` | haiku | Schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.yaml` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/config.yaml.tmpl` | YAML config skeleton with the required keys and bounded defaults. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ollama-deployment.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[ollama-setup-models]]
- [[ollama-python-client]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `ollama-deployment` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
