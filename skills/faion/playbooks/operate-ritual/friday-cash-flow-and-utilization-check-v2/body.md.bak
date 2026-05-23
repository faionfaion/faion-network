# Friday cash-flow + utilization check

## Context

Founder reviews cash position, AR, AP, contractor utilization. Output: AR follow-up list + utilization heat map + go/no-go on next contractor hire.

## Outcome

By the end of this playbook, the operator has run the 3 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 3 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Pull the Numbers

Cash, AR, AP, utilization — fresh today.

Tasks:
- Pull current bank balance and 13-week cash projection
- Pull AR aging and AP aging
- Pull contractor and founder utilization for the week

Outputs:
- bank + cash projection
- AR + AP aging
- utilization snapshot

Decision gate: Advance only when all four numbers are current as of today.

### 2. Diagnose

Find the one thing to fix this week.

Tasks:
- Compare runway to target; flag if <90 days
- Look at AR aging; pick the chase-targets for Monday
- Compare utilization to capacity; spot over- or under-loading

Outputs:
- runway flag
- chase list
- utilization deltas

Decision gate: Advance when at most 3 items are tagged as this-week's focus.

### 3. Act on the Top Item

One concrete move before Monday.

Tasks:
- Send chase emails or invoices owed
- Move contractor / founder allocation if utilization is off
- Log the move in the recurring-actions sheet

Outputs:
- chases sent
- allocation changes
- actions logged

Decision gate: Required output: at least one written action sent today.

## Decision points

- Stage 1 (Pull the Numbers): Advance only when all four numbers are current as of today.
- Stage 2 (Diagnose): Advance when at most 3 items are tagged as this-week's focus.
- Stage 3 (Act on the Top Item): Required output: at least one written action sent today.

## References

- `ops-contractor-management`
- `ops-financial-basics`
- `ops-tax-basics`
- `ops-financial-planning`

Gaps (status: draft until empty):
- `agency-cash-flow-friday-routine` (see `gaps[]` in `playbook.yaml`)
- `contractor-utilization-heatmap` (see `gaps[]` in `playbook.yaml`)
