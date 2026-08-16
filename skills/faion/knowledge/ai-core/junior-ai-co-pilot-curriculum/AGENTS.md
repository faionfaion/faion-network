# Junior AI Co-Pilot Curriculum

## Summary

**One-sentence:** Produces a 6-week onboarding curriculum that brings a junior engineer to safe-and-useful daily AI co-pilot usage — modules, exercises, gating rubric, mentor checklist.

**One-paragraph:** Juniors thrown at AI co-pilots either over-trust (commit hallucinated APIs that fail in prod) or under-trust (still write everything by hand, lose the productivity edge). A 6-week curriculum with explicit modules — prompt anatomy, hallucination check, scoped edits, test-first AI, security boundaries, mentor review — paired with weekly exercises and a gating rubric (junior cannot graduate to unsupervised co-pilot use without passing all rubric items) turns AI usage into a learned skill rather than a folklore practice. Mentor checklist makes review consistent across teams.

**Ефективно для:** dev teams onboarding 1-5 juniors per quarter, agencies standardising AI usage across consultants, bootcamps adding AI module to existing curriculum.

## Applies If (ALL must hold)

- At least one junior engineer (≤2 years professional experience) joins the team in the next quarter.
- The team has settled on a primary AI co-pilot (Claude Code, Cursor, Copilot, etc.) — curriculum mentions tool specifics.
- A named mentor with ≥1 year of AI-augmented dev experience exists.
- A safe sandbox / staging environment is available for junior exercises.

## Skip If (ANY kills it)

- Solo founder with no juniors — content overhead with no audience.
- Team has no AI co-pilot in use — curriculum has nothing to anchor on.
- Junior already passed an equivalent program at prior employer — sit-the-rubric instead of repeat the curriculum.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tech stack | inventory | engineering wiki |
| Primary AI co-pilot tool name | string | team standard |
| Codebase access (read + sandbox write) | git creds | onboarding script |
| Mentor calendar slot | weekly 30-min | mentor's calendar |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[ai-failure-mode-taxonomy]]` | Junior must recognise the 6 base failure modes. |
| `[[indirect-prompt-injection-defense]]` | Security module references this directly. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: 6-week schedule, ≥6 modules, weekly exercise, mentor 30-min review, gating rubric, no-grad-without-pass | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for curriculum.json: modules, exercises, rubric, mentor checklist | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: vibes-only training, no rubric, no mentor, single-tool tunnel, no security module | ~600 |
| `content/04-procedure.xml` | medium | 6-step procedure: assess junior → tailor modules → assign exercises → review weekly → score rubric → graduate | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "is there an incoming junior + AI co-pilot in the team?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Tailor module list to stack | sonnet | Mechanical from tech-stack inventory. |
| Generate exercises | opus | Creative + level-appropriate. |
| Score rubric attempt | sonnet | Bounded comparison against rubric. |
| Author mentor talking points | sonnet | Template-filled. |

## Templates

| File | Purpose |
|---|---|
| `templates/curriculum.schema.json` | JSON Schema for curriculum.json. |
| `templates/curriculum-skeleton.md` | 6-week skeleton with module headers. |
| `templates/rubric.md.j2` | Gating rubric (binary pass/fail per item). |
| `templates/rubric.md` | Gating rubric (binary pass/fail per item). Generated from `templates/rubric.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/mentor-checklist.md.j2` | Weekly review checklist for mentors. |
| `templates/mentor-checklist.md` | Weekly review checklist for mentors. Generated from `templates/mentor-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum curriculum.json that passes the validator. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-junior-ai-co-pilot-curriculum.py` | Validates curriculum.json against the schema; asserts ≥6 modules, ≥1 exercise per module, rubric with ≥10 items. | Pre-commit on curriculum; before sharing with new hires. |

## Related

- parent skill: `geek/ai/`
- `[[ai-failure-mode-taxonomy]]` — referenced in the hallucination-check module
- `[[indirect-prompt-injection-defense]]` — referenced in the security module

## Decision tree

The decision tree at `content/06-decision-tree.xml` gates whether to spin up the curriculum: no incoming junior or no co-pilot in use → skip; junior incoming and tool standardised → run the protocol; junior with prior pass certificate → run rubric only.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/curriculum.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/junior-ai-co-pilot-curriculum",
  "_purpose": "JSON Schema for the curriculum spec consumed by the validator script.",
  "_consumes": "operator-authored curriculum.json",
  "_produces": "validation verdict",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "loaded by validator only",
  "type": "object",
  "required": [
    "junior_name",
    "mentor_name",
    "weeks",
    "modules",
    "rubric",
    "tool"
  ],
  "properties": {
    "junior_name": {
      "type": "string",
      "minLength": 1
    },
    "mentor_name": {
      "type": "string",
      "minLength": 1
    },
    "tool": {
      "type": "string"
    },
    "weeks": {
      "type": "integer",
      "minimum": 4,
      "maximum": 8
    },
    "modules": {
      "type": "array",
      "minItems": 6,
      "items": {
        "type": "object",
        "required": [
          "id",
          "title",
          "week",
          "exercise",
          "reflection_required"
        ],
        "properties": {
          "id": {
            "type": "string"
          },
          "title": {
            "type": "string"
          },
          "week": {
            "type": "integer"
          },
          "exercise": {
            "type": "string"
          },
          "reflection_required": {
            "type": "boolean",
            "const": true
          }
        }
      }
    },
    "rubric": {
      "type": "array",
      "minItems": 10,
      "items": {
        "type": "object",
        "required": [
          "id",
          "statement",
          "evidence"
        ],
        "properties": {
          "id": {
            "type": "string"
          },
          "statement": {
            "type": "string"
          },
          "evidence": {
            "type": "string"
          }
        }
      }
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "Minimum viable curriculum that passes the validator.",
  "_consumes": "validate-junior-ai-co-pilot-curriculum.py",
  "_produces": "validator decision = ok",
  "_depends_on": "templates/curriculum.schema.json",
  "_token_budget_impact": "docs-only",
  "junior_name": "Smoke Tester",
  "mentor_name": "Smoke Mentor",
  "tool": "Claude Code",
  "weeks": 6,
  "modules": [
    {
      "id": "m1",
      "title": "Prompt anatomy",
      "week": 1,
      "exercise": "refactor 3 prompts",
      "reflection_required": true
    },
    {
      "id": "m2",
      "title": "Hallucination check",
      "week": 2,
      "exercise": "review 5 outputs",
      "reflection_required": true
    },
    {
      "id": "m3",
      "title": "Scoped edits",
      "week": 3,
      "exercise": "5 small PRs",
      "reflection_required": true
    },
    {
      "id": "m4",
      "title": "Test-first AI",
      "week": 4,
      "exercise": "3 TDD tasks",
      "reflection_required": true
    },
    {
      "id": "m5",
      "title": "Security boundaries",
      "week": 5,
      "exercise": "IPI suite run",
      "reflection_required": true
    },
    {
      "id": "m6",
      "title": "Mentor review",
      "week": 6,
      "exercise": "PR walkthrough",
      "reflection_required": true
    }
  ],
  "rubric": [
    {
      "id": "r1",
      "statement": "Spots fabricated API",
      "evidence": "week 2"
    },
    {
      "id": "r2",
      "statement": "Writes contract prompts",
      "evidence": "PRs"
    },
    {
      "id": "r3",
      "statement": "Scoped edits",
      "evidence": "PR history"
    },
    {
      "id": "r4",
      "statement": "Test-first",
      "evidence": "week 4"
    },
    {
      "id": "r5",
      "statement": "IPI awareness",
      "evidence": "week 5"
    },
    {
      "id": "r6",
      "statement": "No creds in prompts",
      "evidence": "mentor"
    },
    {
      "id": "r7",
      "statement": "Approved-tool only",
      "evidence": "mentor"
    },
    {
      "id": "r8",
      "statement": "Cites sources",
      "evidence": "PRs"
    },
    {
      "id": "r9",
      "statement": "Compares co-pilots",
      "evidence": "week 1"
    },
    {
      "id": "r10",
      "statement": "Knows when not to AI",
      "evidence": "retro"
    }
  ]
}
```
