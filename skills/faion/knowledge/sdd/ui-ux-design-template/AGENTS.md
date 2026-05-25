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

| File | What's inside |
|------|---------------|
| `content/01-when-required.xml` | Required cases (web, mobile, TUI); skipped cases (backend, API, data migrations); the explicit-skip rule. |
| `content/02-nielsen-five.xml` | The 5 Nielsen heuristics chosen for per-feature checking: N1 visibility of status, N3 user control & freedom, N4 consistency & standards, N5 error prevention, N6 recognition over recall. Why these five. |
| `content/03-norman-principles.xml` | Affordance (clickable looks clickable; references `hover-only-on-clickable` memory rule) and feedback (acknowledgment within 100ms). |
| `content/04-template-sections.xml` | The required sections in `ui-ux-design.md`: Intent, Layout, States (empty/loading/error/success/disabled), Nielsen audit (5 rows), Norman audit (2 rows), Copy & microcopy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ui-ux-design.md.tmpl` | Fillable Markdown template with the six sections and audit-row stubs. |

## Related

- [[readiness-checklist]] — item 7 enforces this audit.
- [[user-flows-template]] — sibling per-feature artefact when user-facing flow exists.
- [[quality-gates]] — UI → Nielsen + Norman audit gate row.

## Decision tree

If the feature changes any rendered output → produce ui-ux-design.md. If not → skip and note "no UI impact" in readiness.md item 7.
