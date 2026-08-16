# Lessons Learned

## Summary

**One-sentence:** Continuous capture, structured categorisation, and mandatory retrieval of project knowledge so the same mistakes are not repeated; produces a searchable lesson database.

**One-paragraph:** Continuous capture, structured categorisation, and mandatory retrieval of project knowledge so the same mistakes are not repeated; produces a searchable lesson database. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-lessons-learned.py` enforces the output contract.

**Ефективно для:**

- Programs delivering >3 phases or releases per year.
- Org with project portfolio across multiple PMs.
- Recurring vendor relationships where pattern recognition matters.
- Compliance regimes requiring documented learning loops.

## Applies If (ALL must hold)

- A lesson repository exists (Notion / Confluence / Markdown repo).
- Lessons can be tagged with category (process, technical, vendor, comms, risk).
- Retrieval is mandatory at planning + at risk identification on new work.

## Skip If (ANY kills it)

- Single-project team with no future projects.
- Lessons captured but never read — fix retrieval first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Lesson repository | Markdown/Notion | PMO |
| Category taxonomy | list of tags | PMO |
| Retrieval triggers | list (planning, risk-id, retro) | PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[scrum-ceremonies]] | retro is the source of agile-side lessons |
| [[project-closure]] | closure is the source of waterfall lessons |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | optional | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-lesson` | sonnet | Judgement: extract reusable lesson vs project-specific note. |
| `validate-lesson` | haiku | Mechanical schema check. |
| `retrieve-for-planning` | haiku | Tag-based query into repository. |

## Templates

| File | Purpose |
|------|---------|
| `templates/lesson-validator.py` | Validator script: required fields, category in taxonomy, retrievability check |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[scrum-ceremonies]]
- [[project-closure]]
- [[communications-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/lesson-validator.py`

```python
"""lesson_validator.py — validate a lesson dict against required schema.

Usage:
  lesson = {
      "title": "New framework without training budget",
      "category": "technical",
      "impact_level": "high",
      "situation": "Chose new framework with no team experience.",
      "impact": "Development took 40% longer than estimated.",
      "root_cause": "Training time not estimated; excitement over new tech.",
      "lesson": "New technology requires explicit ramp time.",
      "recommendation": "Add 25% buffer when introducing a framework new to the team.",
  }
  ok, msg = validate(lesson)
"""

REQUIRED = ["situation", "impact", "root_cause", "lesson", "recommendation"]
VALID_CATEGORIES = {
    "planning", "execution", "technical", "team", "vendor", "stakeholder", "other"
}
ACTION_VERBS = {
    "add", "remove", "change", "require", "reject", "schedule", "train",
    "document", "review", "escalate", "measure", "tag", "automate",
    "budget", "allocate", "enforce", "update", "introduce", "define",
}


def validate(lesson: dict) -> tuple[bool, str]:
    missing = [k for k in REQUIRED if not lesson.get(k)]
    if missing:
        return False, f"missing fields: {missing}"

    cat = lesson.get("category", "")
    if cat not in VALID_CATEGORIES:
        return False, f"category must be one of {sorted(VALID_CATEGORIES)}, got '{cat}'"

    if lesson.get("impact_level") not in ("high", "medium", "low"):
        return False, "impact_level must be high | medium | low"

    rec = lesson["recommendation"].lower()
    if not any(v in rec for v in ACTION_VERBS):
        return False, "recommendation lacks an action verb (add/remove/change/...)"

    if len(lesson["recommendation"].split()) < 6:
        return False, "recommendation too vague (< 6 words)"

    return True, "ok"
```
