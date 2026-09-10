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

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 11 testable rules: the 10 verbatim items (i1–i10) with rationale per item, conditional gates for 5/6/7 folded in, plus the empty-box-blocks gate | ~1800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for readiness.md — 10 items, evidence when ticked, reason when not-applicable, verdict — with valid / invalid examples and forbidden patterns | ~1700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: happy-path-only Playwright, the F001→F002 skill-trigger collision, unnamed surface check, scope by self-assessment, merge-equals-done | ~1000 |
| `content/04-procedure.xml` | essential | 7 steps: locate, derive conditional items from the git diff, tick 1–4, tick 5–7, spec delta, surface-coupling grep, deploy and gate | ~1300 |
| `content/05-examples.xml` | recommended | A rendered readiness.md, the public-surface inventory, the API-test and surface-coupling grep evidence examples, the F001→F002 anchor | ~900 |
| `content/06-decision-tree.xml` | essential | Lifecycle position → preconditions → what the git diff touches; routes to item rules, the empty-box gate, run or skip | ~850 |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-readiness-checklist.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[sdd-workflow-overview]] — readiness phase slots after tasks, before done/.
- [[sdd-promotion-gate-checklist]] — sibling methodology for the `backlog→todo` gate. Delegates the `in-progress→done` gate here.
- [[project-spec-structure]] — item 8 enforces the spec delta-update.
- [[quality-gates]] — stack-to-gate mapping consumed by item 5/6.

## Decision tree

If feature is in `in-progress/` and the developer believes it is done, run this methodology. Skip if any sibling methodology (promotion-gate, cr-bug-tracking) is the better fit for the lifecycle position.
