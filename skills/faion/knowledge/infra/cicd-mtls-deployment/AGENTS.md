# mTLS Service-to-Service Deployment

## Summary

**One-sentence:** Generates an mTLS deployment recipe (step-ca / Vault PKI as internal CA + nginx client-cert verification + short-lived per-pod certs) replacing shared long-lived client certs.

**One-paragraph:** mTLS Service-to-Service Deployment — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a config that the downstream agent can verify with the included validator.

**Ефективно для:**

- Multi-service architecture where service-to-service auth must be cryptographically verified (zero-trust internal network).
- Existing PKI capacity (step-ca, Vault PKI, or service-mesh issuer) is available or installable.
- Workloads can mount short-lived certs via SPIFFE/SPIRE, cert-manager + CSI, or sidecar.

## Applies If (ALL must hold)

- Multi-service architecture where service-to-service auth must be cryptographically verified (zero-trust internal network).
- Existing PKI capacity (step-ca, Vault PKI, or service-mesh issuer) is available or installable.
- Workloads can mount short-lived certs via SPIFFE/SPIRE, cert-manager + CSI, or sidecar.

## Skip If (ANY kills it)

- Single-service deployment with no internal service mesh.
- Application-layer auth (mTLS-equivalent OIDC/JWT with proof-of-possession) is already enforced and sufficient.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal / spec | text / Markdown | user |
| Domain context | XML | `pro/infra/cicd-engineer/AGENTS.md` |
| Inventory of in-scope resources | list / JSON | infra catalog |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cicd-cert-rotation-pipeline]] | Sibling methodology — shared vocabulary and patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (internal-ca-only, short-lived-certs, no-shared-cert, verify-client-cert-at-edge, crl-or-ocsp-stapling, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the config + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-cicd-mtls-deployment` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/step-ca-provisioner.json` | step-ca provisioner config for X509 service identities |
| `templates/nginx-mtls.conf` | nginx server block with ssl_verify_client on + DN forwarding |
| `templates/backup-config.example.json` | Filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cicd-mtls-deployment.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/`
- [[cicd-cert-rotation-pipeline]]
- [[cicd-tls-renewal-automation]]
- [[cicd-tls-validation-gate]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
