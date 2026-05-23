# Mobile UX Patterns

## Summary

**One-sentence:** Apply touch-target, gesture, navigation, and feedback patterns proven on mobile so flows respect thumb reach, network variance, and platform conventions.

**One-paragraph:** Apply touch-target, gesture, navigation, and feedback patterns proven on mobile so flows respect thumb reach, network variance, and platform conventions.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Designing or auditing a mobile-first or mobile-primary interface.
- Touch targets, gestures, or transitions are inconsistent across screens.
- Bug reports include mis-taps, lost state on rotation, or unreachable controls.
- Native iOS and Android conventions need to be honoured by the same design system.
- Performance budget requires sub-2s screen transitions on a mid-range device.

## Skip If (ANY kills it)

- Desktop-only or kiosk product — apply web/desktop heuristics instead.
- Pure WebView wrapper with no native gestures — patterns will be inert.
- Pre-MVP wireframes — patterns assume a real interaction model exists.
- Single accessibility audit pass — use accessibility heuristics directly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current screen inventory | figma / json | Design system export |
| Analytics on mis-tap and rage-tap events | csv | Product analytics |
| Platform style guides (Apple HIG, Material) | url list | Vendor docs |
| Device matrix for QA | csv | QA team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/recognition-over-recall` | Recognition patterns ground icon and gesture choices. |
| `solo/ux/ux-researcher/usability-testing` | Real session footage exposes mobile-only issues. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + run/skip rules | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-artefact` | sonnet | Section-by-section judgement against the rubric. |
| `lint-and-validate` | haiku | Deterministic schema validation + forbidden-pattern check. |
| `final-review` | opus | Cross-section coherence and stakeholder readiness. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mobile-ux-patterns.json` | JSON skeleton conforming to the output contract schema. |
| `templates/mobile-ux-patterns.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mobile-ux-patterns.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[usability-testing]]
- [[recognition-over-recall]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
