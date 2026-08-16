<!--
purpose: Canonical skeleton for the `architectural-impact-pr-ranking` artefact.
consumes: A trigger URL + named owner + typed inputs from upstream methodologies.
produces: A committed artefact file at .product/architectural-impact-pr-ranking/<instance>.md.
depends-on: templates/header.yaml, scripts/validate-architectural-impact-pr-ranking.py.
token-budget-impact: ~500 tokens to fill end-to-end.
-->
---
version: 0.1.0
owner: role:<handle>
last_reviewed: YYYY-MM-DD
trigger_url: <URL>
---

# Trigger

- kind: <trigger_kind>
- url:  <URL>

# Owner

- role:<handle>

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
