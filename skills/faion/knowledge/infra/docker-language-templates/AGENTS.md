# Docker Language Templates

## Summary

**One-sentence:** Generates a curated Dockerfile + Compose template per language (Python, Node, Go, Rust, Java, static) — multi-stage, non-root, health-checked, with optimization defaults applied.

**One-paragraph:** Generates a curated Dockerfile + Compose template per language (Python, Node, Go, Rust, Java, static) — multi-stage, non-root, health-checked, with optimization defaults applied. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Drop-in Dockerfile для Python (slim), Node (alpine LTS), Go (distroless), Rust (distroless), Java (jre-slim).
- Compose dev stack з bind-mounts + db service.
- HEALTHCHECK + non-root за замовчуванням.
- Base-image policy enforced per template.

## Applies If (ALL must hold)

- Service is written in one of the supported languages.
- Team accepts the opinionated template defaults (or will document deviations).
- Production image must follow the org base-image allowlist.

## Skip If (ANY kills it)

- Language not supported by the catalogue — author a tailored Dockerfile from `docker` instead.
- Existing Dockerfile already conforms to optimization + security baselines.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Language + framework | free-form (Python+FastAPI, Node+Next, Go+net/http, Java+Spring) | Application team |
| Base image allowlist | list | Platform / Security |
| Runtime port + healthcheck path | table | Application team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/docker/AGENTS.md` | Docker baseline |
| `pro/infra/devops-engineer/docker-image-optimization/AGENTS.md` | Optimization baseline |

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
| `draft-docker-language-templates` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-docker-language-templates.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[docker]]
- [[docker-image-optimization]]
- [[docker-security-hardening]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
