<!--
purpose: Canonical skeleton for the `dual-write-shadow-read-template` artefact.
consumes: A trigger URL + named owner + typed inputs from upstream methodologies.
produces: A committed artefact file at .product/dual-write-shadow-read-template/<instance>.md.
depends-on: templates/header.yaml, scripts/validate-dual-write-shadow-read-template.py.
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
