# 1:1 Question Bank by Tenure

## Summary

**One-sentence:** Tenure-indexed question bank for 1:1s: 30-60-90 day questions, 6-month, 1-year, 2-year+ — different inputs need different questions.

**One-paragraph:** Pins a 5-bucket question bank (30d / 60d / 90d / 6mo / 1yr+) of ≥10 pre-tested 1:1 questions each. Output is a versioned spec the PM consults before each 1:1 so questions match tenure. Pairs with `pm-1on1-template-engineering-design` (the 5-section template).

**Ефективно для:**

- Solo PM running 1:1s with contractors at different tenures who keeps asking 'how's it going' to everyone. Tenure-bucketed questions surface different signals at each stage.

## Applies If (ALL must hold)

- Running 1:1s with ≥1 teammate
- Teammates span ≥2 tenure brackets (30d / 60d / 90d / 6mo / 1yr+)
- Default 1:1 template exists (or being adopted alongside)

## Skip If (ANY kills it)

- Only one teammate, one tenure — bank is overkill
- No 1:1 cadence at all — adopt cadence first
- Tenure data unavailable / irrelevant (e.g. one-off contractors)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| List of teammates with start dates | table | people doc |
| Standard 1:1 template (5 sections) | doc | pm-1on1-template-engineering-design |
| Rolling notes per teammate | doc | notes store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/pm-1on1-template-engineering-design` | Peer methodology — bank questions fill the 5-section template. |
| `solo/pm/project-manager/freelancer-personal-crm-minimal` | Peer methodology — tenure data sourced from the CRM. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules incl. skip-this-methodology + run-the-checklist | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-1-1-question-bank-by-tenure` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-1-1-question-bank-by-tenure` | haiku | Schema check + threshold checks; deterministic. |
| `review-1-1-question-bank-by-tenure` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/1-1-question-bank-by-tenure.json` | JSON skeleton conforming to the output contract schema. |
| `templates/1-1-question-bank-by-tenure.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-1-1-question-bank-by-tenure.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[pm-1on1-template-engineering-design]]
- [[freelancer-personal-crm-minimal]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
