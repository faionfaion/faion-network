# GitOps — Repository Structure

## Summary

**One-sentence:** Generates a GitOps config-repo layout config (monorepo with base + overlays per env + Kustomize/Helm patterns + multi-team tenant structure + promotion via PRs).

**One-paragraph:** Generates a GitOps config-repo layout config (monorepo with base + overlays per env + Kustomize/Helm patterns + multi-team tenant structure + promotion via PRs). The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Multi-env (dev/staging/prod) deployments з shared base + overlays.
- Multi-team setup з tenant isolation в одному репозиторії.
- PR-based promotion (overlay change → PR → ArgoCD/Flux apply).
- Kustomize-heavy stacks; Helm wrap при потребі параметризації.

## Applies If (ALL must hold)

- Multiple environments (≥2: e.g. staging + prod).
- Shared base manifests with env-specific overrides.
- Multi-tenant or multi-team config sharing.
- Promotion model needs to live in Git (PRs between branches or env folders).

## Skip If (ANY kills it)

- Single-env single-tenant — overlays are overkill.
- Team prefers Helm-only with per-env values files (Kustomize layer adds no value).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Env list | YAML | Platform |
| Team list with isolation needs | YAML | Platform |
| Helm chart inventory | JSON | App teams |
| Promotion policy | table (env → env → who approves) | Platform |

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
| `draft-gitops-repository-structure` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gitops-repository-structure.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
