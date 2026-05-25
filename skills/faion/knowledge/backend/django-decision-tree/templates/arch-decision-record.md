<!--
purpose: Markdown skeleton of a Django architectural decision record.
consumes: signals + decisions + dependencies from the methodology output.
produces: human-readable architecture doc kept in repo at docs/architecture.md.
depends-on: content/02-output-contract.xml.
token-budget-impact: ~150 tokens.
-->

# Architecture Decision — &lt;project&gt;

- **artefact_id**: &lt;kebab-case&gt;
- **owner**: &lt;handle/email — single accountable owner&gt;
- **version**: 1.0.0
- **last_reviewed**: 2026-05-22

## Signals at decision time

- team_size: &lt;n&gt;
- model_count: &lt;n&gt;
- traffic_req_s: &lt;n&gt;
- needs_admin: &lt;true/false&gt;
- needs_async: &lt;true/false&gt;
- bounded_contexts: &lt;n&gt;

## Decisions

| Axis | Choice | Rationale |
|---|---|---|
| framework | &lt;django/django-ninja-only/fastapi/flask&gt; | &lt;sentence citing signals&gt; |
| api_stack | &lt;drf/ninja/vanilla-django/n/a&gt; | &lt;sentence&gt; |
| layering | &lt;simple/service-layer/clean-arch&gt; | &lt;sentence&gt; |
| db | &lt;postgres/postgres-managed/mysql/sqlite&gt; | &lt;sentence&gt; |
| deployment | &lt;paas/vps/kubernetes/serverless&gt; | &lt;sentence&gt; |

## Dependencies

| Package | Verdict | recent_commits | django_compat | license_ok | no_known_cves |
|---|---|---|---|---|---|
| &lt;name&gt; | &lt;adopt/trial/hold/sunset&gt; | &lt;true/false&gt; | &lt;true/false&gt; | &lt;true/false&gt; | &lt;true/false&gt; |

## Re-walk triggers

- model_count crosses 50
- team_size crosses 10
- traffic_req_s crosses 1000
- 12 months elapsed since last_reviewed
