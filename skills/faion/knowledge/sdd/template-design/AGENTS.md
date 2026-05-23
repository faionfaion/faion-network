# Template Design

## Summary

**One-sentence:** Maintain the canonical design.md template as a versioned, lintable Markdown skeleton so every team-authored design doc starts from the same shape.

**One-paragraph:** Without a canonical design.md template, every doc invents its own layout and depth. This methodology owns the design.md template: section headers, placeholder copy, lint rules, and quarterly review cycle. The template is versioned semver; downstream methodologies (design-doc-structure, design-doc-writing-process) reference it by path; agents copy it as the starting skeleton.

**Ефективно для:**

- Team standardising design docs — needs one template to point at.
- Solo founder onboarding collaborators; template anchors expectations.
- Agent generating design.md from spec; template is the target shape.
- Refactor projects where design.md drift hurts review velocity.

## Applies If (ALL must hold)

- Design-doc-structure methodology is in use.
- Template lives in a shared location (this methodology's templates/).
- Template is version-controlled and lint-checked.
- Quarterly review cycle is in place.

## Skip If (ANY kills it)

- Team uses external design-doc tool (Notion, Confluence) — different template.
- Single-author scrap project — no shared template needed.
- Pre-SDD adoption — no design docs yet.
- Template superseded by an external standard — defer.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| design-doc-structure spec | markdown | design-doc-structure |
| templates/design-doc.md | markdown | This methodology |
| Lint rules | yaml | Repo config |
| Quarterly review schedule | calendar | Team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/design-doc-structure` | Layout the template implements. |
| `solo/sdd/sdd-planning/design-doc-writing-process` | Flow the template anchors. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `update-template` | sonnet | Per-change reasoning on template fields. |
| `lint-pass` | haiku | Deterministic lint check. |
| `quarterly-review` | opus | Cross-doc review against current architecture. |

## Templates

| File | Purpose |
|------|---------|
| `templates/template-design.json` | JSON skeleton conforming to the output contract schema. |
| `templates/template-design.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-template-design.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[design-doc-structure]]
- [[template-spec]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
