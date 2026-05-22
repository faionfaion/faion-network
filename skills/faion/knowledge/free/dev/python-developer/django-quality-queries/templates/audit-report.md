<!--
purpose: Markdown skeleton for a django-quality-queries audit report
consumes: profiling output from Debug Toolbar / nplusone + EXPLAIN ANALYZE
produces: a Markdown report whose frontmatter validates against 02-output-contract.xml
depends-on: scripts/validate-django-quality-queries.py
token-budget-impact: ~180 tokens
-->
---
methodology: django-quality-queries
target_repo: <owner/repo>
endpoints_audited: 0
n_plus_one_count: 0
indexes_recommended: 0
tests_added: 0
findings: []
---

# Django Query Optimisation Audit

## Summary

One paragraph: which endpoints were audited, how many N+1 spots were fixed, how many indexes were added, how many regression tests now lock query counts.

## Findings

For each finding add an entry to `findings` in the frontmatter with `rule_id`, `severity`, `file`, `line`, `fix`, `before_queries`, `after_queries`.

## Indexes added

| Migration | Table | Columns | EXPLAIN delta |
|-----------|-------|---------|---------------|
| | | | |
