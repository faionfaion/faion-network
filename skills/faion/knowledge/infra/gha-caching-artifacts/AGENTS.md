# GitHub Actions — Caching and Artifacts

## Summary

**One-sentence:** Generates a GHA cache + artifact config (ecosystem-specific cache keys + retention policy + Docker layer cache via Buildx + cache-vs-artifact decision per job).

**One-paragraph:** Generates a GHA cache + artifact config (ecosystem-specific cache keys + retention policy + Docker layer cache via Buildx + cache-vs-artifact decision per job). The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- CI pipelines з install-step >60s (npm, pip, maven, gradle).
- Docker builds де base-layer reused across jobs.
- Cross-job artifact handoff (build → test → deploy).
- Reusable workflows що шарять cache між викликами.

## Applies If (ALL must hold)

- Workflow has a dependency install step taking >60 seconds on cold cache.
- Multiple jobs in the same workflow need the same intermediate output.
- Docker builds participate in the pipeline.
- Cache key is computable from a deterministic file (lockfile, requirements, etc.).

## Skip If (ANY kills it)

- All builds finish under 2 minutes — caching overhead exceeds the saving.
- Cache key cannot be made deterministic (build inputs not pinned).
- Highly secret outputs that must not leak into cache layers.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workflow file | yaml | Eng team |
| Lockfile / dependency manifest | package-lock.json / requirements.txt / pom.xml | Repo |
| Retention policy | days int | Platform team |
| Storage quota baseline | MB used in GHA cache | GitHub admin |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/cicd-engineer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

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
| `draft-gha-caching-artifacts` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gha-caching-artifacts.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
