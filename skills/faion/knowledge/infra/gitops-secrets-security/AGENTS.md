# GitOps — Secrets and Security

## Summary

**One-sentence:** Generates a GitOps secrets-and-security config (SOPS with age/KMS or Sealed Secrets or External Secrets + RBAC least-privilege + AI-agent gotchas + secret rotation cadence).

**One-paragraph:** Generates a GitOps secrets-and-security config (SOPS with age/KMS or Sealed Secrets or External Secrets + RBAC least-privilege + AI-agent gotchas + secret rotation cadence). The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Зберігання secrets в Git без plaintext (SOPS + age / KMS).
- External secret stores (Vault, AWS Secrets Manager) via ESO.
- RBAC tightening: ServiceAccounts тільки на потрібні CRDs.
- Audit: rotation cadence + key revocation event capture.

## Applies If (ALL must hold)

- Kubernetes manifests are stored in Git.
- Secrets (DB passwords, API tokens, certificates) are required by workloads.
- Compliance / audit requirements apply to secret handling.
- Team can integrate KMS (cloud) OR age-keyring OR external secret store.

## Skip If (ANY kills it)

- Secrets are injected exclusively by a CSI driver and never appear in manifests.
- Single-dev cluster with no compliance obligation.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| KMS / age keyring availability | ARN / key path | Platform |
| Secret inventory | list of secrets per workload | App teams |
| Secret rotation policy | cadence per class | Security |
| RBAC baseline | ClusterRole + Role YAML | Platform |

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
| `draft-gitops-secrets-security` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gitops-secrets-security.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
