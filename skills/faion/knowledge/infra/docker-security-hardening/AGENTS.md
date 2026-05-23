# Docker Security Hardening

## Summary

**One-sentence:** Generates a Docker security hardening spec: non-root user, capability drops, read-only filesystem, secrets policy, image signing, and CI vulnerability scan gate.

**One-paragraph:** Generates a Docker security hardening spec: non-root user, capability drops, read-only filesystem, secrets policy, image signing, and CI vulnerability scan gate. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Lock-down container з non-root + capDrop ALL + read-only FS.
- Secrets management через Docker Secrets / Vault / IRSA.
- Trivy / Docker Scout CI gate з fail-on-high.
- Image signing (cosign / Notary) перед production push.

## Applies If (ALL must hold)

- Production image runs untrusted code or processes sensitive data.
- Compliance regime (PCI / HIPAA / SOC2) requires container hardening evidence.
- CI pipeline can be modified to add scan + signing steps.

## Skip If (ANY kills it)

- Sandbox / experimental image with no compliance scope.
- Image runs only in an isolated cluster with no internet access and team has accepted the risk.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Compliance regime | list (PCI / HIPAA / SOC2 / none) | Security |
| Secrets inventory | list (name, source, scope) | Security |
| Scanner choice | Trivy / Docker Scout / Snyk | Platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/docker/AGENTS.md` | Docker baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-docker-security-hardening` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-docker-security-hardening.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[docker]]
- [[docker-image-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
