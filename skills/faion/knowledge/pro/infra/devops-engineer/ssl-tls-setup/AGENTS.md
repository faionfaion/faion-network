---
slug: ssl-tls-setup
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "SSL/TLS setup spec: TLS 1.3 default, modern cipher suite, automated cert renewal (cert-manager / Let's Encrypt), HSTS preload, OCSP stapling, mTLS for service-to-service where applicable."
content_id: "71a17850391f13f6"
complexity: medium
produces: config
est_tokens: 3700
tags: [ssl, tls, certificates, lets-encrypt, cert-manager]
---

# SSL/TLS Setup

## Summary

**One-sentence:** SSL/TLS setup spec: TLS 1.3 default, modern cipher suite, automated cert renewal (cert-manager / Let's Encrypt), HSTS preload, OCSP stapling, mTLS for service-to-service where applicable.

**One-paragraph:** TLS configuration in 2026 is straightforward when you follow the modern recipe: TLS 1.3 default, TLS 1.2 fallback only for legacy clients, ChaCha20-Poly1305 + AES-GCM cipher suites, HSTS with preload, OCSP stapling, automated cert renewal via cert-manager / Let's Encrypt. The failure modes are the same as 2015: expired certs, weak ciphers left from copy-paste configs, missing HSTS, certs renewed manually in a runbook nobody read. This methodology codifies the modern defaults + the automation rules + the post-deploy verification (testssl.sh, ssllabs-scan).

**Ефективно для:**

- Уникнення expired-cert outage через cert-manager auto-renew.
- TLS 1.3 + sane cipher suite за один template (без CipherSuite-арбітра).
- HSTS preload + OCSP stapling без manual nginx tuning.
- mTLS для service-to-service в K8s через service mesh.

## Applies If (ALL must hold)

- Public-facing HTTPS endpoints (web, API, ingress)
- Service-to-service traffic where compliance or zero-trust requires mTLS
- Cert lifecycle automation needed (cert-manager + Let's Encrypt or internal CA)
- Compliance framework requires evidence of modern TLS (SOC2, PCI-DSS, HIPAA)

## Skip If (ANY kills it)

- Internal-only HTTP traffic on a private network with no compliance requirement — overhead exceeds value
- Long-lived single-host setup that already runs cert-manager and modern config — re-applying is churn

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| DNS control + public hostname (for Let's Encrypt) | DNS records + ACME-challenge access | DNS owner |
| Reverse proxy / ingress (nginx / Traefik / Envoy / Istio) | config access | platform team |
| cert-manager installed in cluster | Helm release | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[security-as-code]] | Policy enforcement of TLS posture |
| [[secrets-management]] | Cert key storage in a secrets backend |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory_scan` | haiku | Mechanical testssl.sh result parsing |
| `config_diff` | sonnet | Compose nginx/Envoy diff to Modern profile |
| `waiver_review` | opus | Cross-team judgment on legacy TLS 1.2 fallback |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ssl-tls-setup.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[secrets-management]]
- [[security-as-code]]
- [[external-secrets-operator-recipe]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
