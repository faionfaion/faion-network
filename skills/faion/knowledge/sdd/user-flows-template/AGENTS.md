# user-flows.md Template

## Summary

**One-sentence:** Per-feature `user-flows.md` documents each user-facing flow as actor + preconditions + happy path + negative paths, mapping 1:1 to Playwright spec files.

**One-paragraph:** Replaces the old `test-plan.md` for user-facing work. Each flow has at least one positive and one negative case; the negative trumps the positive for unsexy edges (auth failure, network down, invalid input). Backend-only features skip this artefact entirely — they go through API tests in `tests/api/` instead.

**Ефективно для:**

- Web / mobile / TUI features with user-facing flow.
- Reviewers using the spec to navigate a Playwright suite (1:1 spec mapping).
- Subagent pipelines verifying that pos+neg coverage exists before close-out.

## Applies If (ALL must hold)

- Feature has at least one user-facing flow (the user takes a sequence of actions).
- Feature lives in `features/in-progress/F0NN-slug/`.
- The project uses Playwright (or equivalent) for E2E.

## Skip If (ANY kills it)

- Backend-only / API-only feature — go through `tests/api/` instead.
- Pure data work, migrations, infra.
- Internal refactor with no rendered change.

## Content

| File | What's inside |
|------|---------------|
| `content/01-when-required.xml` | Required only when feature has user-facing flow; backend-only → API tests in tests/api/, no user-flows.md. |
| `content/02-shape.xml` | Per-flow shape: Actor, Preconditions, Happy path (numbered steps + expected result), Negative paths (each with trigger + expected error UX), Playwright spec path. |
| `content/03-positive-negative.xml` | Every flow MUST have AT LEAST 1 positive AND 1 negative case. Negative trumps positive for unsexy edges. |

## Templates

| File | Purpose |
|------|---------|
| `templates/user-flows.md.tmpl` | Fillable Markdown template with one-flow stub. |

## Related

- [[readiness-checklist]] — item 6 (Playwright pos+neg) requires user-flows.md exists.
- [[ui-ux-design-template]] — sibling per-feature artefact; ui-ux-design.md covers heuristics, user-flows.md covers behaviour.
- [[quality-gates]] — user-facing → Playwright gate row.

## Decision tree

User-facing flow present → produce user-flows.md. Backend-only → skip and rely on API tests.
