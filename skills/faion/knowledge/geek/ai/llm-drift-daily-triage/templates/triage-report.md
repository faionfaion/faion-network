<!--
purpose: Daily triage report skeleton; owner fills 5 fields in <15 min.
consumes: runner-emitted deltas + failing traces
produces: decision + follow_up
depends-on: content/04-procedure.xml
token-budget-impact: docs-only
-->
# Drift triage — {{date}}

Owner: {{owner}}

## Deltas (vs 7d rolling)

| metric        | yesterday | 7d avg | delta   |
|---------------|-----------|--------|---------|
| eval score    |           |        | __ pp   |
| refusal rate  |           |        | __ pp   |
| cost per call |           |        | __ %    |

## Top 3 failing traces

1. id={{id}} — {{1-sentence summary}}; expected {{e}}, got {{g}}.
2. id={{id}} — ...
3. id={{id}} — ...

## Decision

`continue` | `mitigate` | `escalate`

Rationale (1 sentence):

## Follow-up

- ticket / channel / owner / date
