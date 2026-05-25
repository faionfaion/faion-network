# Readiness Checklist (in-progress → done gate)

## Summary

**One-sentence:** A 10-item checklist that lives as `features/in-progress/F0NN-slug/readiness.md` and is the hard gate for moving the feature to `done/`.

**One-paragraph:** Each item is a binary checkbox the reviewer (or main thread acting as reviewer) ticks with linked evidence. The 10 items cover ACs evidence, tasks done, commit hygiene, CI, conditional quality gates (API tests when backend touched; Playwright pos+neg when user-facing), UI heuristics, project-spec delta, surface-coupling review, deploy. Empty boxes block the transition.

**Ефективно для:**

- Solo dev who skips own diff in the final mile.
- Subagent pipelines closing features autonomously — gives a machine-checkable contract.
- Audit trail: readiness.md is the last artefact in done/, evidence-linked.

## Applies If (ALL must hold)

- Feature lives in `features/in-progress/F0NN-slug/`.
- SDD lifecycle is in use (features/{backlog,todo,in-progress,done}).
- Project has CI configured (lint + typecheck + unit at minimum).

## Skip If (ANY kills it)

- Standalone CR (use `cr-bug-tracking`'s lighter flow instead).
- Throwaway prototype with no done/ target.

## Content

| File | What's inside |
|------|---------------|
| `content/01-checklist.xml` | The 10 verbatim items with rationale per item; this is the canonical list. |
| `content/02-quality-gates.xml` | Conditional rules: API tests required when backend touched; Playwright when user-facing; pos+neg required for every Playwright file. |
| `content/03-surface-coupling.xml` | The surface-coupling failure mode (F001→F002 split lesson): public surfaces — skill triggers, API paths, CLI flags — need explicit coupling review. |

## Related

- [[sdd-workflow-overview]] — readiness phase slots after tasks, before done/.
- [[sdd-promotion-gate-checklist]] — sibling methodology for the `backlog→todo` gate. Delegates the `in-progress→done` gate here.
- [[project-spec-structure]] — item 8 enforces the spec delta-update.
- [[quality-gates]] — stack-to-gate mapping consumed by item 5/6.

## Decision tree

If feature is in `in-progress/` and the developer believes it is done, run this methodology. Skip if any sibling methodology (promotion-gate, cr-bug-tracking) is the better fit for the lifecycle position.
