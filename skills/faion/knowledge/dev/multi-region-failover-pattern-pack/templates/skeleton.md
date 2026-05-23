<!--
purpose: Canonical skeleton for the `multi-region-failover-pattern-pack` artefact.
consumes: A trigger URL + named owner + typed inputs from upstream methodologies.
produces: A committed artefact file at .product/multi-region-failover-pattern-pack/<instance>.md.
depends-on: templates/header.yaml, scripts/validate-multi-region-failover-pattern-pack.py.
token-budget-impact: ~500 tokens to fill end-to-end.
-->
---
version: 0.1.0
owner: role:<handle>
last_reviewed: YYYY-MM-DD
trigger_url: <URL>
---

# Trigger

- kind: <event | threshold | schedule>
- url:  <URL>

# Owner

- role:<handle>

# Inputs

- name: <input-name>
  value: <typed value>

# Decision

<single declarative sentence>

# Evidence

- <URL 1>
- <URL 2>

# Review

- cadence: monthly | quarterly
- next_review_at: YYYY-MM-DD
- outcome: <filled at the next review>
