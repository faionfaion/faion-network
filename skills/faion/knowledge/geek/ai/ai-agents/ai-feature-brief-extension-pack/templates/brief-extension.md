<!--
purpose: Markdown skeleton for the four AI sections appended to a base PRD
consumes: base PRD, model catalogue, eval inventory, compliance template, cost dashboard
produces: extended brief reviewed by product+engineering+finance
depends-on: content/01-core-rules.xml
token-budget-impact: ~600 tokens when rendered
-->
# AI Extension Pack — {{feature_name}}

> Append this section after the base PRD. Do not skip any field; mark N/A with a one-line reason if a row truly does not apply.

## 1. Model

| Field | Value |
|---|---|
| Chosen model | {{model_name}} |
| Version | {{model_version}} |
| Provider | {{provider}} |
| Fallback chain | {{fallback_chain}} |
| Deprecation window | {{deprecation_window_months}} months |

## 2. Eval set

| Field | Value |
|---|---|
| Golden set version | {{golden_set_version}} |
| n_examples | {{n_examples}} |
| Pass-rate threshold | {{threshold_pass_rate}} |
| CI width | {{ci_width}} |
| Eval methodology | {{eval_method_ref}} |

## 3. Hallucination policy

| Risk class | Policy |
|---|---|
| Factual claim with cited source | {{factual_claim_policy}} |
| Numerical summary | {{numerical_summary_policy}} |
| Legal / regulatory implication | {{legal_policy}} |

Audit log path: `{{audit_log_path}}`

## 4. Cost guardrails

| Cap | USD |
|---|---|
| Per-request soft cap | {{per_request_soft_cap_usd}} |
| Per-day hard cap | {{per_day_hard_cap_usd}} |
| Outlier alert threshold | {{outlier_alert_threshold_usd}} |

Billing owner: `{{billing_owner}}`
