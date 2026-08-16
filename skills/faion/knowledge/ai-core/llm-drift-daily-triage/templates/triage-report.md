<!--

purpose: Daily triage report skeleton; owner fills 5 fields in <15 min.
consumes: runner-emitted deltas + failing traces
produces: decision + follow_up
depends-on: content/04-procedure.xml
token-budget-impact: docs-only
-->


# Drift triage — <artefact_date>

Owner: <owner_full_name>

## Deltas (vs 7d rolling)

| metric        | yesterday | 7d avg | delta   |
|---------------|-----------|--------|---------|
| eval score    |           |        | __ pp   |
| refusal rate  |           |        | __ pp   |
| cost per call |           |        | __ %    |

## Top 3 failing traces

1. `id=<trace-id>` — `<one-sentence summary>`; expected `<expected>`, got `<actual>`.
2. `id=<trace-id>` — ...
3. `id=<trace-id>` — ...

## Decision

`continue` | `mitigate` | `escalate`

Rationale (1 sentence):

## Follow-up

- ticket / channel / owner / date
