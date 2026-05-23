# Flexibility and Efficiency of Use

## Summary

**One-sentence:** Layer accelerators — keyboard shortcuts, saved views, command palettes, batch operations — over the default path so novices and experts both move quickly.

**One-paragraph:** Layer accelerators — keyboard shortcuts, saved views, command palettes, batch operations — over the default path so novices and experts both move quickly.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Product has a clear novice-to-expert continuum among current users.
- Power users report repetitive tasks that cannot be parallelised in the UI.
- Analytics show heavy use of a single flow that could be templated or scripted.
- Engineering can ship keyboard maps, command-K, or saved-view primitives.
- Discoverability of shortcuts can be designed without cluttering the UI.

## Skip If (ANY kills it)

- Single-task utility used once per session — shortcuts have nowhere to live.
- Pre-MVP product without a stable IA yet.
- Audience strictly novice (e.g., one-off government form).
- Accessibility constraints make some shortcuts unreachable — solve baseline first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Power-user interview notes | markdown | Research team |
| Repetitive-task analytics | csv | Product analytics |
| Existing shortcut inventory | markdown | Design ops |
| Command-palette pattern reference | url | Design system |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/recognition-over-recall` | Discoverability of shortcuts ties back to recognition. |
| `solo/ux/ux-ui-designer/consistency-standards` | Shortcuts must match platform conventions. |

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
| `templates/flexibility-efficiency.json` | JSON skeleton conforming to the output contract schema. |
| `templates/flexibility-efficiency.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-flexibility-efficiency.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[recognition-over-recall]]
- [[consistency-standards]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
