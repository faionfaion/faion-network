<!--
purpose: Bias Audit Report skeleton for EU AI Act / ISO 42001 compliance
consumes: stratified validation set, protected-attribute labels, model under test
produces: signed bias audit report with statistical tables and CIs
depends-on: content/01-core-rules.xml
token-budget-impact: ~400 tokens when rendered
-->
# Bias Audit Report — {{system_name}}

| Field | Value |
|---|---|
| Audit date | {{audit_date}} |
| Auditor | {{auditor}} |
| Validation set | {{validation_set_id}} (n={{n}}) |
| Stratification | {{stratification_strategy}} |
| Model version | {{model_version}} |

## Demographic parity

| Protected attribute | Diff | 95% CI | Threshold | Result |
|---|---|---|---|---|
| {{attr_1}} | {{dp_diff_1}} | [{{dp_ci_low_1}}, {{dp_ci_high_1}}] | {{dp_threshold}} | {{result_1}} |
| {{attr_2}} | {{dp_diff_2}} | [{{dp_ci_low_2}}, {{dp_ci_high_2}}] | {{dp_threshold}} | {{result_2}} |

## Equalised odds

| Protected attribute | Diff | 95% CI | Threshold | Result |
|---|---|---|---|---|
| {{attr_1}} | {{eo_diff_1}} | [{{eo_ci_low_1}}, {{eo_ci_high_1}}] | {{eo_threshold}} | {{result_eo_1}} |

## Disparate impact

| Protected attribute | Ratio | 95% CI | Threshold | Result |
|---|---|---|---|---|
| {{attr_1}} | {{di_ratio_1}} | [{{di_ci_low_1}}, {{di_ci_high_1}}] | {{di_threshold}} | {{result_di_1}} |

## Notes

- Validation set was stratified to avoid GDPR concerns with live data: {{stratification_notes}}.
- Bootstrap resamples: {{bootstrap_n}}.
- All metrics computed pre-deployment; no production user data used.
