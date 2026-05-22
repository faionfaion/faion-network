<!--
purpose: Model Card skeleton for EU AI Act / ISO 42001 compliance
consumes: model artefact metadata, training data summary, eval metrics, fairness audit
produces: signed model card committed alongside model artefact
depends-on: content/01-core-rules.xml
token-budget-impact: ~500 tokens when rendered
-->
# Model Card — {{system_name}} v{{model_version}}

## Provenance

| Field | Value |
|---|---|
| Training data | {{training_dataset_summary}} |
| Window | {{training_window_start}} → {{training_window_end}} |
| Provider | {{provider}} |
| Base model | {{base_model}} |
| Fine-tune date | {{finetune_date}} |

## Intended use

- {{intended_use_primary}}
- {{intended_use_secondary}}

## Out of scope

- {{out_of_scope_1}}
- {{out_of_scope_2}}

## Evaluation metrics

| Metric | Value | CI |
|---|---|---|
| {{metric_1_name}} | {{metric_1_value}} | {{metric_1_ci}} |
| {{metric_2_name}} | {{metric_2_value}} | {{metric_2_ci}} |

## Fairness metrics

| Metric | Value | Threshold | Pass/Fail |
|---|---|---|---|
| demographic_parity_diff | {{dp_diff}} | {{dp_threshold}} | {{dp_result}} |
| equalised_odds_diff | {{eo_diff}} | {{eo_threshold}} | {{eo_result}} |

## Known limitations

- {{limit_1}}
- {{limit_2}}

## Human oversight

- Policy: `{{oversight_policy}}`
- Reviewers: `{{reviewers}}`
- Reversal SLA: `{{sla}}`

## Retention

Audit log retention: `{{retention_years}} years` at `{{audit_log_path}}`.
