# Match Between System and Real World

## Summary

**One-sentence:** Nielsen Heuristic #2 applied: speak the user's language, not the system's — use words, phrases, icons, and ordering that match the target audience's real-world conventions rather than internal data-model terms.

**One-paragraph:** Nielsen Heuristic #2 applied: speak the user's language, not the system's — use words, phrases, icons, and ordering that match the target audience's real-world conventions rather than internal data-model terms. The methodology pins the artefact: a glossary mapping each UI string to (audience term, system term, source) and a rubric scoring the UI on jargon, ordering, and localisation fidelity.

**Ефективно для:**

- Multi-audience products where internal terminology leaks to UI.
- Localised products mapping to non-English conventions (date formats, currency).
- Reviewers catching jargon during copy review.
- Audit surface: rubric score per screen.

## Applies If (ALL must hold)

- Product copy is user-visible.
- Target audience uses distinct terminology from the system internals.
- Localisation matters (≥1 non-English market).

## Skip If (ANY kills it)

- Internal admin tool used only by engineers.
- Pure-code surface (CLI for developers) where system terms are correct.
- Audience is the system maintainer.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| UI copy inventory | list | Frontend |
| Audience glossary | csv | Research |
| Localisation files | json | i18n |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `none` | This methodology has no upstream dependency. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-match-real-world` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-match-real-world` | haiku | Schema check + threshold checks; deterministic. |
| `review-match-real-world` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/match-real-world.json` | JSON skeleton conforming to the output contract schema. |
| `templates/match-real-world.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/match-real-world.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/match-real-world.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[recognition-over-recall]]
- [[flexibility-efficiency]]
- [[help-documentation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/match-real-world.json`

```json
{
  "artefact_id": "match-real-world-example",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "owner": "@solo-founder",
  "subject": "subject under review",
  "criteria": [
    {
      "id": "c1",
      "score": 4,
      "weight": 1.0
    },
    {
      "id": "c2",
      "score": 3,
      "weight": 1.0
    }
  ],
  "overall": 0.75
}
```
