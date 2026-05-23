# Design System Drift Dashboard

## Summary

**One-sentence:** Produces a quantitative drift report tracking token adoption, hardcoded values, and v1→v2 migration ROI across every consumer repo on a weekly cadence.

**One-paragraph:** Design-system v1→v2 migrations stall because adoption is invisible — teams keep paying for old tokens while new ones rot in storybook. This methodology produces a dashboard report that scans every consumer repo for hardcoded colours / spacings / typography, computes adoption % per component, and surfaces drift week over week. Output is a JSON drift report + Markdown exec summary tied to a sign-off threshold (≥90 % adoption + ≤2 % drift) that gates closure of the migration epic.

**Ефективно для:** tech lead, що рухає v1→v2 міграцію дизайн-системи і потребує weekly metric для stakeholders.

## Applies If (ALL must hold)

- Multi-team migration v1→v2 design system at scale (≥3 consumer repos).
- Tokens codified in machine-readable source (Style Dictionary, JSON, CSS vars).
- CI has access to clone consumer repos and read source files.

## Skip If (ANY kills it)

- Single repo, single team — manual visual inspection is faster.
- Tokens not codified machine-readably.
- Migration already accepted — switch to ds-ops methodology.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Consumer repo list | JSON array of clone URLs | platform team |
| v2 token map | JSON / Style Dictionary | design system team |
| Token→component mapping | YAML | design system team |
| Sign-off threshold | JSON | engineering leadership |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[ai-enhanced-design-systems]] | Token automation context. |
| [[ai-design-assistant-patterns]] | Companion design-tool integration patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end. | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-report` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/drift-report.md` | Markdown skeleton: scan date, adoption %, drift count, top-10 hardcoded findings, signoff verdict. |
| `templates/drift-report.json` | JSON template matching the output contract. |
| `templates/_smoke-test.json` | Filled minimum-viable drift report. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-design-system-drift-dashboard.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[ai-enhanced-design-systems]]
- [[ai-design-assistant-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the report; mis-routing leads to producing the wrong artefact shape.
