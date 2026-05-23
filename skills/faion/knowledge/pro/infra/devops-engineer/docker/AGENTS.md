---
slug: docker
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a Docker baseline config: multi-stage Dockerfile skeleton, layer order for cache, non-root user, HEALTHCHECK, exec-form CMD, .dockerignore, and Compose service spec.
content_id: "014157b4f8b330ef"
complexity: medium
produces: config
est_tokens: 4400
tags: [docker, dockerfile, compose, containers, oci]
---
# Docker Core Operations

## Summary

**One-sentence:** Generates a Docker baseline config: multi-stage Dockerfile skeleton, layer order for cache, non-root user, HEALTHCHECK, exec-form CMD, .dockerignore, and Compose service spec.

**One-paragraph:** Generates a Docker baseline config: multi-stage Dockerfile skeleton, layer order for cache, non-root user, HEALTHCHECK, exec-form CMD, .dockerignore, and Compose service spec. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Перший Dockerfile в репо — multi-stage, non-root, HEALTHCHECK.
- Compose service file для local dev із bind-mounts.
- Layer order optimization (deps → src → COPY) для cache.
- Replace OCI defaults на pinned digests.

## Applies If (ALL must hold)

- Service ships as an OCI image (Docker / Podman / Buildah).
- Image is built in CI and consumed by production runtime.
- Image must survive a security scan + base-image rebuild pipeline.

## Skip If (ANY kills it)

- Application does not ship as a container (binary / serverless function).
- Existing image is fully managed by an external buildpack (Heroku-style) — no Dockerfile to author.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Runtime requirements | lang + version | Application team |
| Build secrets | list (build-time vs runtime) | Security |
| Base image policy | allowlist | Platform / Security |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/AGENTS.md` | Parent skill context |

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
| `draft-docker` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-docker.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[docker-image-optimization]]
- [[docker-security-hardening]]
- [[docker-language-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
