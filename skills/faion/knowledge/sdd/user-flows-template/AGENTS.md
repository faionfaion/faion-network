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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[readiness-checklist]] — item 6 (Playwright pos+neg) requires user-flows.md exists.
- [[ui-ux-design-template]] — sibling per-feature artefact; ui-ux-design.md covers heuristics, user-flows.md covers behaviour.
- [[quality-gates]] — user-facing → Playwright gate row.

## Decision tree

User-facing flow present → produce user-flows.md. Backend-only → skip and rely on API tests.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/user-flows.md.tmpl`

```markdown
- Actor: <who>
- Preconditions: <what state>
- Happy path:
  1. <action> → <expected result>
  2. <action> → <expected result>
  3. <action> → <expected result>
- Negative paths:
  - <negative case 1>:
    - Trigger: <what causes the error>
    - Expected UX: <what the user sees>
  - <negative case 2 — optional>:
    - Trigger:
    - Expected UX:
- Playwright spec: `<path/to/spec.ts>`

## Flow F-02: <next flow>

(Repeat the shape above per flow. Every flow needs at least one positive AND one negative case.)
```
