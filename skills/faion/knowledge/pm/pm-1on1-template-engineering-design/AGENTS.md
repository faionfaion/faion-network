# PM 1:1 Template (Engineering / Design)

## Summary

**One-sentence:** 30-min biweekly 1:1 template for PM↔eng/design: career / project / craft / blockers / feedback — five named sections, rolling notes log.

**One-paragraph:** Pins a 30-min biweekly 1:1 format with eng/design contractors or teammates: five named sections (career / project / craft / blockers / feedback). Output is a per-meeting artefact appended to a rolling log so trends become visible after 3+ meetings.

**Ефективно для:**

- Solo PM or founder with 1-4 eng/design contractors whose 1:1s drift into status updates. Five-section template that makes career + craft show up alongside project blockers.

## Applies If (ALL must hold)

- Working with ≥1 eng/design contractor or teammate for ≥4 weeks
- 1:1 cadence exists (weekly / biweekly) OR being established
- Founder/PM has authority to schedule recurring 30-min slot

## Skip If (ANY kills it)

- Engagement <4 weeks (too short for trend)
- Synchronous full-team standup covers 1:1 ground
- Contractor explicitly declined 1:1 cadence

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Calendar block for biweekly slot per teammate | calendar event | calendar |
| Rolling notes doc per teammate (Notion / Google Doc) | doc | notes store |
| Last 30 days of project context (PRs, designs, blockers) | log | GitHub / Figma / PM tool |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/outsource-onboarding-one-pager-template` | Peer methodology — onboarding inputs feed the first 1:1 agenda. |
| `solo/pm/async-standup-methodology` | Peer methodology — daily standup supplies project-section inputs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules incl. skip-this-methodology + run-the-checklist | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-pm-1on1-template-engineering-design` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-pm-1on1-template-engineering-design` | haiku | Schema check + threshold checks; deterministic. |
| `review-pm-1on1-template-engineering-design` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pm-1on1-template-engineering-design.json` | JSON skeleton conforming to the output contract schema. |
| `templates/pm-1on1-template-engineering-design.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pm-1on1-template-engineering-design.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[outsource-onboarding-one-pager-template]]
- [[async-standup-methodology]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
