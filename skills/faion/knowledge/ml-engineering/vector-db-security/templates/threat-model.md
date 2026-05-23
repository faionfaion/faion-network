<!--
purpose: threat model skeleton for vector DB deployment
consumes: deployment topology + compliance regime
produces: report (markdown threat model)
depends-on: security-config.yaml
token-budget-impact: 0
-->

# Threat Model: <vector DB instance>

## Assets
- Embeddings (vector data)
- Source documents (payload)
- API keys / OIDC tokens

## Threats
| ID | Threat | Vector | Impact | Likelihood | Mitigation |
|----|--------|--------|--------|------------|-----------|
| T1 | Public scanner finds open port | Internet | data exfil | high without auth | r1 + r3 |
| T2 | MITM on plain HTTP | network | PII leak | medium | r2 TLS |
| T3 | Disgruntled admin drops collection | insider | data loss | low | r4 audit + backup |
| T4 | GDPR erasure request | regulatory | fine + reputation | medium | r5 procedure |
| T5 | API key in git history | leak | full access | medium | secret manager |

## Mitigation status
<for each threat, link to security-config field + last verification date>
