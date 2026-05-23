---
slug: nginx-configuration
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Nginx server configuration: TLS profile, upstream health checks, rate-limit zones, security headers and proxy-cache sizing for production workloads."
content_id: "285a394fa7ff2179"
complexity: medium
produces: config
est_tokens: 4000
tags: [nginx, reverse-proxy, tls, rate-limit, load-balancer]
---
# Nginx Configuration Hardening

## Summary

**One-sentence:** Nginx server configuration: TLS profile, upstream health checks, rate-limit zones, security headers and proxy-cache sizing for production workloads.

**One-paragraph:** Nginx server configuration: TLS profile, upstream health checks, rate-limit zones, security headers and proxy-cache sizing for production workloads. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `config` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-nginx-configuration.py` before publication.

**Ефективно для:**

- Hardening публічного reverse-proxy перед запуском.
- Налаштування rate-limit zones для login / signup.
- Виставлення proxy_cache з sizing + cache lock.

## Applies If (ALL must hold)

- Input matches the methodology scope (nginx-configuration) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `config` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Upstream catalogue | service → host:port + health-check path | service team |
| TLS certificate source | ACME / Vault / file path per host | security team |
| Traffic profile | expected RPS + burst per route | product owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[kubernetes]] | upstream context likely already loaded when this methodology fires |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output/gate per step | ~800 |
| `content/06-decision-tree.xml` | essential | Root-question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| gather-and-validate-inputs | haiku | Mechanical inventory + freshness check. |
| apply-core-rules | sonnet | Rule-by-rule reasoning over the inputs. |
| draft-config-artefact | sonnet | Template filling with bounded judgement. |
| validate-and-publish | haiku | Script-driven validation + traceability wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nginx.conf` | Annotated configuration skeleton with required keys + comments per knob |
| `templates/_smoke-test.json` | Minimum viable filled-in version of the template used by `--self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nginx-configuration.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[kubernetes]]
- [[iac-pr-review-checklist]]
- [[gitops]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `tls-modern-profile` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.
