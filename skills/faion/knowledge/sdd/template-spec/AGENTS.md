# Template Spec

## Summary

**One-sentence:** Maintain the canonical spec.md template as a versioned, lintable Markdown skeleton so every team-authored spec starts from the same shape.

**One-paragraph:** Without a canonical spec.md template, every spec invents its own layout and depth. This methodology owns the spec.md template: section headers, placeholder copy, lint rules, and quarterly review cycle. The template is versioned semver; downstream methodologies (spec-structure, spec-requirements) reference it by path; agents copy it as the starting skeleton for new specs.

**Ефективно для:**

- Team standardising specs — needs one template to point at.
- Solo founder onboarding collaborators; template anchors expectations.
- Agent generating spec.md from discovery output; template is the target shape.
- Refactor projects where spec drift hurts review velocity.

## Applies If (ALL must hold)

- Spec-structure methodology is in use.
- Template lives in a shared location (this methodology's templates/).
- Template is version-controlled and lint-checked.
- Quarterly review cycle is in place.

## Skip If (ANY kills it)

- Team uses external spec tool (Notion, Confluence) — different template.
- Single-author scrap project — no shared template needed.
- Pre-SDD adoption — no specs yet.
- Template superseded by an external standard — defer.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| spec-structure spec | markdown | spec-structure |
| templates/spec.md | markdown | This methodology |
| Lint rules | yaml | Repo config |
| Quarterly review schedule | calendar | Team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/spec-structure` | Layout the template implements. |
| `solo/sdd/sdd-planning/spec-requirements` | Requirement format hosted by the template. |

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
| `quarterly-review` | opus | Cross-spec review against current conventions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/template-spec.json` | JSON skeleton conforming to the output contract schema. |
| `templates/template-spec.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-template-spec.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[spec-structure]]
- [[template-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
