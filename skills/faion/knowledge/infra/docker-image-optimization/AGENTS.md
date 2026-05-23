# Docker Image Optimization

## Summary

**One-sentence:** Generates a Docker image optimization plan: target size, base-image choice, multi-stage layering, cache mounts, .dockerignore, and per-language minification recipes.

**One-paragraph:** Generates a Docker image optimization plan: target size, base-image choice, multi-stage layering, cache mounts, .dockerignore, and per-language minification recipes. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Reduce image size 70-90% (1 GB → 80-150 MB).
- CI build speed-up через cache-mounts (apt, pip, go-mod).
- Distroless / Alpine / slim base choice по language.
- Strip dev deps + lockfile-only install у production stage.

## Applies If (ALL must hold)

- Existing image >300 MB and is deployed to production.
- CI build time per image exceeds 5 minutes.
- Owner has authority to change Dockerfile + CI build steps.

## Skip If (ANY kills it)

- Image size and build time are already within SLO and team agrees.
- Image is fully managed by a vendor (e.g. cloud function build pipeline).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current image size + layer breakdown | `docker image history` / Dive output | SRE |
| CI build timings | table (step, seconds) | Platform |
| Runtime dependency list | language manifests | Application team |

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
| `draft-docker-image-optimization` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-docker-image-optimization.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[docker]]
- [[docker-language-templates]]
- [[docker-security-hardening]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
