<!--
purpose: Markdown skeleton for a django-quality-security audit report
consumes: outputs of steps 1-5 from content/04-procedure.xml
produces: a Markdown report whose frontmatter validates against 02-output-contract.xml
depends-on: scripts/validate-django-quality-security.py
token-budget-impact: ~200 tokens
-->
---
methodology: django-quality-security
target_repo: <owner/repo>
django_version: "5.2"
https_baseline:
  debug_false: true
  ssl_redirect: true
  hsts_seconds: 300
  csp_mode: report-only
  cookie_secure: true
rate_limits:
  auth_endpoints_throttled: false
  axes_installed: false
  stacked_libraries: false
input_validation:
  all_inputs_validated: false
  raw_sql_findings: 0
  file_upload_magic_check: false
secrets:
  env_loaded: false
  secret_key_default_check: false
  sentry_scrubber: false
check_deploy_verdict: warning
findings: []
---

# Django Production Security Audit

## Summary

What was audited, what is still gapped, and which deploys are blocked until remediation.

## HSTS ramp plan

| Week | SECURE_HSTS_SECONDS | INCLUDE_SUBDOMAINS | PRELOAD | Notes |
|------|--------------------|--------------------|---------|-------|
| 0 | 300 | false | false | initial public launch |
| 1 | 3600 | false | false | after 24h clean |
| 2 | 31536000 | true | false | after CSP enforce stable |
| 4 | 31536000 | true | true | submit to hstspreload.org |

## Findings

For every rule violation add an entry to `findings` with `rule_id`, `severity`, `file`, `line`, `fix`.
