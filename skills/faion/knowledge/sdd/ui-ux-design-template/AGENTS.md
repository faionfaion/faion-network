# ui-ux-design.md Template

## Summary

**One-sentence:** Per-feature `ui-ux-design.md` is REQUIRED when the feature touches UI (web, mobile, CLI TUI); skipped for pure backend / API / data work.

**One-paragraph:** A focused 5-section template (Intent, Layout, States, Nielsen audit, Norman audit, Copy & microcopy) that forces explicit thought about affordance, feedback, and the boring-but-load-bearing UI states (empty, loading, error, success, disabled). Uses 5 of the 10 Nielsen heuristics per feature — the other 5 stay in education material because checking all 10 per feature is theatre.

**Ефективно для:**

- Solo UI work that historically skipped the heuristics audit.
- Subagent pipelines closing UI features and needing a machine-checkable artefact.
- Reviewers checking a feature against the empty / error / disabled states without running the app.

## Applies If (ALL must hold)

- The feature renders or modifies any user-visible UI element (page, component, form, button, TUI prompt).
- The feature lives in `features/in-progress/F0NN-slug/`.
- `readiness.md` item 7 (UI heuristics reviewed) is in play.

## Skip If (ANY kills it)

- Pure backend / API / data work — no visible surface.
- Internal refactor that does not change rendered output.
- Pure copy fix without layout / state change (use a one-line note in spec.md instead).

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules: required when UI touched, explicit skip in readiness item 7, exactly five Nielsen rows, affordance, hover-only-on-clickable, feedback within 100ms, six sections in order, States table all five | ~1500 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for ui-ux-design.md — intent, layout, five states, Nielsen N1/N3/N4/N5/N6, Norman affordance/feedback, copy — with valid / invalid examples and forbidden patterns | ~2150 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: just-in-case design doc, silent skip, auditing all ten, decorative hover, silent submit, success-only States | ~950 |
| `content/04-procedure.xml` | essential | 8 steps: decide applicability, instantiate template, intent and layout, States table, Nielsen audit, Norman audit, copy, shape check and close on item 7 | ~1100 |
| `content/05-examples.xml` | recommended | The five Nielsen heuristics with one-line tests and why these five, the feedback good/bad pair, required and skipped surface lists, a rendered ui-ux-design.md | ~1450 |
| `content/06-decision-tree.xml` | essential | Rendered output? → artefact exists? → shape checks; routes to produce, a specific rule, run, or explicit skip | ~850 |

## Templates

| File | Purpose |
|------|---------|
| `templates/ui-ux-design.md.tmpl` | Fillable Markdown template with the six sections and audit-row stubs. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ui-ux-design-template.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[readiness-checklist]] — item 7 enforces this audit.
- [[user-flows-template]] — sibling per-feature artefact when user-facing flow exists.
- [[quality-gates]] — UI → Nielsen + Norman audit gate row.

## Decision tree

If the feature changes any rendered output → produce ui-ux-design.md. If not → skip and note "no UI impact" in readiness.md item 7.
