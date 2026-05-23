<!--
purpose: Markdown skeleton for a django-quality-logging audit report
consumes: outputs of steps 1-5 from content/04-procedure.xml
produces: a Markdown report whose frontmatter validates against 02-output-contract.xml
depends-on: scripts/validate-django-quality-logging.py
token-budget-impact: ~180 tokens
-->
---
methodology: django-quality-logging
target_repo: <owner/repo>
django_version: "5.2"
python_version: "3.12"
structlog_status:
  installed: false
  middleware_registered: false
  json_renderer: false
  issues: []
sentry_status:
  dsn_present: false
  traces_sample_rate: 0.1
  send_default_pii: false
  before_send_present: false
check_deploy_verdict: warning
findings: []
---

# Django Logging + Sentry Audit

## Summary

One paragraph: what the project currently does, what it should do, and which rules are violated.

## Findings

For every rule violation, append an entry under `findings` in the frontmatter with `rule_id`, `severity`, `file`, `line`, and `fix`.

## Recommended actions

Ordered list, one item per finding, each citing the rule id from `content/01-core-rules.xml`.
