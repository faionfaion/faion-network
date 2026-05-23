---
slug: devops-lb-ssl-tls
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates an LB TLS spec: termination strategy (termination / re-encryption / passthrough), TLS 1.3 cipher list, HSTS policy, OCSP stapling, and cert lifecycle plan.
content_id: "9b5554f002d13f18"
complexity: medium
produces: config
est_tokens: 4400
tags: [ssl, tls, hsts, ocsp, load-balancer, security]
---
# SSL/TLS Termination at the Load Balancer

## Summary

**One-sentence:** Generates an LB TLS spec: termination strategy (termination / re-encryption / passthrough), TLS 1.3 cipher list, HSTS policy, OCSP stapling, and cert lifecycle plan.

**One-paragraph:** Generates an LB TLS spec: termination strategy (termination / re-encryption / passthrough), TLS 1.3 cipher list, HSTS policy, OCSP stapling, and cert lifecycle plan. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Default — TLS termination at L7 LB з HTTP-only backend pool.
- End-to-end encryption через re-encryption (LB→backend over TLS).
- PCI / regulated workload з passthrough mode.
- HSTS + OCSP stapling baseline 2025-2026.

## Applies If (ALL must hold)

- LB sits in front of HTTPS traffic (or will once TLS is enabled).
- Cert issuance and rotation are owned by the team (or via cert-manager / ACM).
- Compliance regime (PCI / HIPAA / GDPR) or general baseline requires modern TLS.

## Skip If (ANY kills it)

- All TLS terminates at the backend (LB is L4 passthrough by mandate and team has accepted this).
- Internal-only LB with no encryption requirement.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cert source | free-form (ACM / cert-manager / Let's Encrypt) | Cert team |
| Compliance regime | list (PCI / HIPAA / SOC2 / none) | Security |
| Domain list | list of FQDNs | Product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/devops-lb-haproxy/AGENTS.md` | LB config context |

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
| `draft-devops-lb-ssl-tls` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-lb-ssl-tls.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[devops-lb-haproxy]]
- [[devops-lb-kubernetes]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
