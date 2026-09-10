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

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: required when user-facing flow, forbidden for backend-only, five fields per flow, numbered happy path with success last, negative trigger + UX, pos+neg per flow, 1:1 spec path | ~1250 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for user-flows.md — flows with actor, preconditions, happy_path, negative_paths, playwright_spec — with valid / invalid examples and forbidden patterns | ~1650 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: user-flows for a background worker, three positives zero negatives, missing field breaks the 1:1 mapping, undocumented flow is an untested flow | ~850 |
| `content/04-procedure.xml` | essential | 7 steps: decide applicability, instantiate template, enumerate flows, actor and preconditions, happy path, negative paths, spec path and gate on item 6 | ~950 |
| `content/05-examples.xml` | recommended | The five fields, the F-01 upgrade worked flow, the stripe-checkout illustration, the unsexy-edge list, skipped cases and what verifies them | ~1000 |
| `content/06-decision-tree.xml` | essential | User-facing flow? → artefact exists? → per-flow shape checks; routes to produce, a specific rule, run, or backend-only skip | ~850 |

## Templates

| File | Purpose |
|------|---------|
| `templates/user-flows.md.tmpl` | Fillable Markdown template with one-flow stub. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-user-flows-template.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[readiness-checklist]] — item 6 (Playwright pos+neg) requires user-flows.md exists.
- [[ui-ux-design-template]] — sibling per-feature artefact; ui-ux-design.md covers heuristics, user-flows.md covers behaviour.
- [[quality-gates]] — user-facing → Playwright gate row.

## Decision tree

User-facing flow present → produce user-flows.md. Backend-only → skip and rely on API tests.
