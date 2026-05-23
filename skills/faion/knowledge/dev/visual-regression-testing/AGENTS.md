# Visual Regression Testing

## Summary

**One-sentence:** Catches unintended visual drift in design-system components by wiring Storybook snapshot baselines into CI with owner-signed thresholds and a quarantine flow for flakes.

**One-paragraph:** Catches unintended visual drift in design-system components by wiring Storybook snapshot baselines into CI with owner-signed thresholds and a quarantine flow for flakes. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Component library is published as a reusable Storybook + ships to ≥ 1 downstream app.
- There is a named visual-owner who can approve / reject baseline diffs in PRs.
- CI can run snapshot capture on every PR within token + minute budget.

## Skip If (ANY kills it)

- Greenfield prototype with no public surface — visual drift cost is zero.
- Team has no published Storybook (snapshot harness has nothing to feed).
- All visual review is manual + on-demand (no CI gate desired).

**Ефективно для:**

- Design-system component libraries (Storybook + Chromatic / Percy / Loki / Playwright snapshot).
- PR-gate що блокує мердж при незатвердженому візуальному дрейфі.
- Якщо є чіткий named owner для виносу false-positives у quarantine.
- Кросбраузерні snapshot-метрики на хоча б Chromium + WebKit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev` | Parent role context. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `apply-checklist` | haiku | Per-item binary check against artefact. |
| `classify-decision` | sonnet | Mitigated / accepted / deferred / N-A judgment. |
| `escalate-stride-conflict` | opus | Cross-category interaction analysis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Checklist with category headings + decision-per-prompt rows. |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-visual-regression-testing.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
