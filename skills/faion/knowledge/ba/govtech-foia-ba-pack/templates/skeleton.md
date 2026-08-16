<!--
purpose: Canonical skeleton for the `govtech-foia-ba-pack` artefact.
consumes: A trigger URL + named owner + typed inputs from upstream methodologies.
produces: A committed artefact file at .product/govtech-foia-ba-pack/<instance>.md.
depends-on: templates/header.yaml, scripts/validate-govtech-foia-ba-pack.py.
token-budget-impact: ~500 tokens to fill end-to-end.
-->
---
version: 0.1.0
owner: role:<owner_handle>
last_reviewed: YYYY-MM-DD
trigger_url: <trigger_url>
---

# Trigger

- kind: <trigger_kind>
- url:  <trigger_url>

# Owner

- role:<owner_handle>

# Inputs

- name: <input_name>
  value: <typed_value>

# Decision

<decision_statement>

# Evidence

- <url_1>
- <url_2>

# Review

- cadence: monthly | quarterly
- next_review_at: YYYY-MM-DD
- outcome: <filled at the next review>
