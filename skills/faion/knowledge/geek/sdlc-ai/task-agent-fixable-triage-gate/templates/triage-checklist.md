# Pre-label Triage Checklist for `agent-fixable`

> Apply this checklist BEFORE adding the `agent-fixable` label.
> If any item fails, do not label; route the issue to the appropriate
> human queue (`needs-spec`, `needs-repro`, `wontfix`, `dup-of-#N`).

## Solvability

- [ ] Acceptance criteria are explicit (≥ 3 testable bullets).
- [ ] Reproduction steps exist (for bug reports) or example I/O exists (for features).
- [ ] Files / paths the agent should touch are named OR inferable from the description.
- [ ] "Out of scope" section names what the agent must NOT change.

## Hygiene

- [ ] Not a duplicate (linked the original if related).
- [ ] Not spam, not a question, not a discussion thread.
- [ ] Title fits the agent's prompt budget (under ~120 chars).

## Risk

- [ ] No customer PII in the issue body.
- [ ] No production secrets or credential values pasted.
- [ ] Change does not require a product / legal decision (no `needs-spec`).

## Identity

- [ ] Triager has issue-write permission and is NOT a coding agent.
- [ ] Triager recorded the checklist outcome as an issue comment.

## Outcome

- [ ] All boxes ticked → apply `agent-fixable`.
- [ ] Any box unticked → apply the appropriate routing label instead.
