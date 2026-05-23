# ACME TLS Renewal Automation

## Summary

**One-sentence:** Generates an automated ACME renewal pipeline (certbot / acme.sh / lego under systemd timer + renewal hooks) that eliminates manual rotation outages for public-facing TLS.

**One-paragraph:** ACME TLS Renewal Automation — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a config that the downstream agent can verify with the included validator.

**Ефективно для:**

- Public-facing TLS endpoints using Let's Encrypt / ZeroSSL / Buypass / Google Trust Services.
- Self-hosted reverse proxy (nginx, Caddy, HAProxy, Traefik standalone).
- Renewal needs to be hands-off + observable.

## Applies If (ALL must hold)

- Public-facing TLS endpoints using Let's Encrypt / ZeroSSL / Buypass / Google Trust Services.
- Self-hosted reverse proxy (nginx, Caddy, HAProxy, Traefik standalone).
- Renewal needs to be hands-off + observable.

## Skip If (ANY kills it)

- Managed LB (ACM, GCP managed cert, Cloudflare) handles ACME transparently.
- Internal-only services — use `cicd-mtls-deployment` with an internal CA instead.

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
| `content/01-core-rules.xml` | essential | 6 testable rules (systemd-timer-not-cron, renewal-hook-reload, staging-then-prod, expiry-alert-14-days, dns-01-for-wildcards, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the config + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-cicd-tls-renewal-automation` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/certbot-renew.timer` | systemd timer for daily certbot renewal attempt |
| `templates/certbot-renew.service` | systemd service invoking certbot renew + deploy hook |
| `templates/backup-config.example.json` | Filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cicd-tls-renewal-automation.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/`
- [[cicd-cert-rotation-pipeline]]
- [[cicd-tls-validation-gate]]
- [[cicd-mtls-deployment]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
