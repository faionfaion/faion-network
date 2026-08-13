# Business Storytelling (Pyramid / SCQA / Pixar)

## Summary

**One-sentence:** Generates a Pyramid / SCQA / Pixar structured business narrative (case study, exec memo, or presentation outline) that leads with conclusion and passes the so-what test.

**One-paragraph:** People remember stories 22x better than facts alone. Business storytelling uses three complementary frameworks — Pyramid Principle for logic-driven decisions, SCQA for narrative tension, Pixar for case studies — to lead with conclusions and support with evidence. Every claim must pass the 'so what' test: a fact without an implication is incomplete. This methodology emits a case study, executive memo, or presentation outline depending on the goal, each with mandatory answer-first ordering.

**Ефективно для:**

- Case study lead summary that must fit in 3 sentences.
- Pixar-arc story for a customer-success narrative.
- Presentation outline that needs a tension arc.
- Memo that must persuade in a 30-second skim.

## Applies If (ALL must hold)

- Narrative arc is appropriate (vs. raw data dump).
- Audience is busy; 30s skim is the default.
- There is a single central claim or outcome.
- Evidence is available to back the claim.

## Skip If (ANY kills it)

- Pure technical doc — reference structure beats narrative.
- Status report without a decision — bullet list is fine.
- Internal Slack < 3 sentences — over-engineered.
- Reactive support reply — wrong context.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Central claim | one sentence | author |
| Audience profile | role + time budget | session owner |
| Evidence | facts + numbers + sources | research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[business-storytelling]] | sister methodology focused on Pyramid for executive comms |
| [[selling-ideas]] | pitch-flavored applications |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `framework-selection` | sonnet | Judgment on goal fit. |
| `draft-causal-chain` | sonnet | Pixar arc needs craft. |
| `so-what-pass` | haiku | Mechanical: append implications. |

## Templates

| File | Purpose |
|------|---------|
| `templates/case-study.md` | Pixar case-study skeleton |
| `templates/executive-summary.md` | Pyramid executive memo skeleton |
| `templates/presentation-outline.md` | SCQA presentation outline skeleton |
| `templates/prompt-case-study.txt` | Prompt to generate a Pixar case study |
| `templates/prompt-pyramid.txt` | Prompt to generate a Pyramid executive memo |
| `templates/scqa.md` | SCQA worksheet |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-storytelling.py` | Validate storytelling artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[business-storytelling]]
- [[selling-ideas]]
- [[stakeholder-communication]]

## Decision tree

See `content/06-decision-tree.xml`. Routes by narrative goal (decision / tension / outcome-story) to one of the three frameworks.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-case-study.txt`

```text
Write a case study using the Pixar framework.
Situation: <who the customer is and their baseline state>
Change event: <what was implemented or what decision was made>
Consequence chain: <what happened as a result, in sequence (at least 2 "Because of that" steps)>
Resolution: <final outcome with specific metrics — numbers required>
Add a 1-sentence customer or stakeholder quote at the end.
Keep to 150 words maximum.
Every result must pass the so-what test: include the implication, not just the metric.
```

### `templates/prompt-pyramid.txt`

```text
Apply the Pyramid Principle to write an executive summary.
Recommendation (1 sentence): <recommendation>
Data/evidence available: <bullet list of facts with numbers>
Audience: <role, e.g. C-suite with 5 min to read>
Output format:
1. Recommendation — 1 sentence, leads with the conclusion
2. Argument 1 + evidence (2-3 bullets)
3. Argument 2 + evidence (2-3 bullets)
4. Argument 3 + evidence (2-3 bullets)
5. Next steps — 2-3 specific actions with owners
MECE check: flag any overlapping arguments before finalizing.
Every data point must include a "so what" implication for the audience.
```
