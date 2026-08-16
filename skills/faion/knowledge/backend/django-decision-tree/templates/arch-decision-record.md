<!--
purpose: Markdown skeleton of a Django architectural decision record.
consumes: signals + decisions + dependencies from the methodology output.
produces: human-readable architecture doc kept in repo at docs/architecture.md.
depends-on: content/02-output-contract.xml.
token-budget-impact: ~150 tokens.
-->

# Architecture Decision — <project>

- **artefact_id**: <kebab_case>
- **owner**: <handle/email — single accountable owner>
- **version**: 1.0.0
- **last_reviewed**: 2026-05-22

## Signals at decision time

- team_size: <team_size>
- model_count: <model_count>
- traffic_req_s: <traffic_req_s>
- needs_admin: <true_false>
- needs_async: <true_false>
- bounded_contexts: <bounded_contexts>

## Decisions

| Axis | Choice | Rationale |
|---|---|---|
| framework | <django/django-ninja-only/fastapi/flask> | <sentence_citing_signals> |
| api_stack | <drf/ninja/vanilla-django/n/a> | <sentence> |
| layering | <simple/service-layer/clean-arch> | <sentence> |
| db | <postgres/postgres-managed/mysql/sqlite> | <sentence> |
| deployment | <paas/vps/kubernetes/serverless> | <sentence> |

## Dependencies

| Package | Verdict | recent_commits | django_compat | license_ok | no_known_cves |
|---|---|---|---|---|---|
| <name> | <adopt/trial/hold/sunset> | <true_false> | <true_false> | <true_false> | <true_false> |

## Re-walk triggers

- model_count crosses 50
- team_size crosses 10
- traffic_req_s crosses 1000
- 12 months elapsed since last_reviewed
