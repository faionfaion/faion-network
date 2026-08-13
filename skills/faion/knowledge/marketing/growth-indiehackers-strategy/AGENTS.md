# IndieHackers Build-in-Public Strategy

## Summary

**One-sentence:** Generates a 12-week IndieHackers strategy artefact: give-first 2-4 weeks, monthly transparent revenue + lesson updates, audience flywheel KPI, and stop-condition — turns the community into a flywheel without coming off as a self-promoter.

**One-paragraph:** IndieHackers Build-in-Public Strategy produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo indie founder who needs a 12-week IH presence plan with give-first weeks, monthly transparent updates, and KPIs — before the community labels them a self-promoter.

## Applies If (ALL must hold)

- Founder is genuinely building a product (no agency / consultancy spin)
- Commit to 12 weeks of consistent presence
- Willing to publish revenue + lesson updates transparently

## Skip If (ANY kills it)

- Pre-product hype without anything to show
- B2B enterprise sale — audience mismatch
- Cannot publish revenue numbers (e.g. paid contracts NDA)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| IH account + profile filled | account | indiehackers.com |
| Monthly revenue baseline | USD | billing |
| List of 5 lessons + 5 questions you can engage on | doc | founder log |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `growth-hacker-news-launch` | Sibling community-launch methodology. |
| `growth-cold-outreach` | Outbound complement. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-give-first-2-to-4-weeks, r2-monthly-revenue-update, r3-honest-not-hype, r4-engage-3-comments-per-post, r5-12-week-stop-condition | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-growth-indiehackers-strategy` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-growth-indiehackers-strategy` | haiku | Schema check + threshold checks; deterministic. |
| `review-growth-indiehackers-strategy` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-indiehackers-strategy.json` | JSON skeleton conforming to the output contract schema. |
| `templates/growth-indiehackers-strategy.md` | Markdown skeleton for human-readable artefact rendering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-indiehackers-strategy.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[growth-hacker-news-launch]]
- [[growth-cold-outreach]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/growth-indiehackers-strategy.json`

```json
{
  "artefact_id": "growth-indiehackers-strategy-<project>-<period>",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "ih_handle": "<ih_handle>",
  "give_first_weeks": 0,
  "monthly_update_topics": [],
  "kpis": {},
  "stop_condition": "<stop_condition>",
  "owner": "<@handle>"
}
```
