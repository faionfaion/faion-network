<!--
purpose: Decision-record skeleton linking incident → eval case path → fix PR → root-cause class
consumes: incident report + committed eval case + fix PR URL
produces: decision-record (markdown committed at docs/regressions/INC-XXX.md)
depends-on: content/01-core-rules.xml (decision-record-required, eval-before-fix)
token-budget-impact: low — ~200 tokens when loaded as context
-->

# Regression Eval Record — INC-XXX

| field | value |
|---|---|
| incident_id | INC-XXX |
| eval_case_path | `eval/regressions/INC-XXX.jsonl` |
| fix_pr | https://github.com/org/repo/pull/NNN |
| root_cause_class | prompt / tool / model / context-assembly / rag-retrieval / vendor-outage / user-input |
| ci_required_check_id | eval-suite |
| verdict | flipped / no-flip / regressed-others / no-fix-transient / no-fix-vendor |

## Reproduction

<deterministic input + observed vs expected>

## Fix summary

<one-paragraph description of the change>

## Lessons

<one or two bullets — what to do differently next time>
