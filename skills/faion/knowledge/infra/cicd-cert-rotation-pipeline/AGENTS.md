# Certificate Rotation Pipeline (cert-manager / Terraform / Compose)

## Summary

**One-sentence:** Generates an IaC-driven certificate rotation pipeline using cert-manager Certificate CRDs, Terraform ACM/GCP, or Docker Compose + Traefik — author → render → scan → apply, with no private keys in Git.

**One-paragraph:** Certificate Rotation Pipeline (cert-manager / Terraform / Compose) — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a config that the downstream agent can verify with the included validator.

**Ефективно для:**

- Production TLS endpoints requiring periodic certificate renewal without manual intervention.
- Multiple environments (dev/staging/prod) each holding their own cert lifecycle.
- Compliance regime mandates documented cert rotation procedure with audit trail.

## Applies If (ALL must hold)

- Production TLS endpoints requiring periodic certificate renewal without manual intervention.
- Multiple environments (dev/staging/prod) each holding their own cert lifecycle.
- Compliance regime mandates documented cert rotation procedure with audit trail.

## Skip If (ANY kills it)

- Single-host static site behind a managed load balancer that handles TLS termination natively.
- Internal cluster traffic only — use mTLS (`cicd-mtls-deployment`) instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal / spec | text / Markdown | user |
| Domain context | XML | `pro/infra/cicd-engineer/AGENTS.md` |
| Inventory of in-scope resources | list / JSON | infra catalog |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cicd-mtls-deployment]] | Sibling methodology — shared vocabulary and patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (no-private-keys-in-git, iac-author-render-scan-apply, renewal-30-days-before-expiry, expiry-alert-7-days, issuer-isolated-per-env, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the config + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-cicd-cert-rotation-pipeline` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/certificate.yaml` | cert-manager Certificate CRD skeleton with renewBefore + secretName |
| `templates/terraform-acm.tf` | Terraform aws_acm_certificate skeleton with validation |
| `templates/backup-config.example.json` | Filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cicd-cert-rotation-pipeline.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/`
- [[cicd-mtls-deployment]]
- [[cicd-tls-renewal-automation]]
- [[cicd-tls-validation-gate]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
