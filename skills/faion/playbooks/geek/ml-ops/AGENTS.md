# Geek / ML Ops

LLM production operations playbooks: monitoring, drift detection, cost tracking, and reliability. Citation scope: all four tiers (`knowledge/free/ + solo/ + pro/ + geek/`).

| Slug | Goal |
|------|------|
| `model-monitoring-drift` | Log every LLM call to Postgres/S3, run daily KL-divergence and refusal-rate aggregations, score samples with an LLM judge, and fire Slack alerts when thresholds breach |

Spec: `../../../../../.aidocs/conventions/playbooks/playbook-spec.md`. Validator: `python3 scripts/validate-tier-playbook.py <path>`.
