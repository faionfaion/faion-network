<!--
purpose: Markdown skeleton for an ML-specific postmortem
consumes: incident facts, traces, eval results, root-cause classification
produces: archive-ready postmortem
depends-on: content/01-core-rules.xml
token-budget-impact: ~500 tokens when rendered
-->
# Postmortem — {{incident_id}}

| Field | Value |
|---|---|
| Time window | {{start}} → {{end}} |
| Incident commander | {{incident_commander}} |
| Root-cause class | {{root_cause_class}} |
| Version | {{version}} |

## ML axes

| Axis | Before | After |
|---|---|---|
| Model | {{model_before}} | {{model_after}} |
| Prompt SHA | {{prompt_before}} | {{prompt_after}} |
| Eval set | {{eval_before}} | {{eval_after}} |

## Blast radius

| Metric | Value |
|---|---|
| Users affected | {{users_affected}} |
| Revenue impact (USD) | {{revenue_impact}} |
| Detect (min) | {{detect_min}} |
| Mitigate (min) | {{mitigate_min}} |
| Resolve (min) | {{resolve_min}} |

## Narrative (blameless)

{{narrative}}

## Fix

{{fix_summary}}

## Eval guard added

- Path: `{{eval_guard_path}}`
- Description: {{eval_guard_description}}

## Follow-up actions

| Action | Owner | Due date |
|---|---|---|
| {{action_1}} | {{owner_1}} | {{due_1}} |
| {{action_2}} | {{owner_2}} | {{due_2}} |
