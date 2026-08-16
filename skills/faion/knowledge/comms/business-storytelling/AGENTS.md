# Business Storytelling

## Summary

**One-sentence:** Generates a Pyramid / SCQA / Pixar structured narrative (exec summary, case study, or presentation outline) that puts the answer first and survives the 'so what' test.

**One-paragraph:** Business storytelling is the discipline of structuring persuasive communication so the audience grasps the point immediately and remembers it. Three primary frameworks: Pyramid Principle (lead with answer, support with MECE arguments), SCQA (Situation-Complication-Question-Answer for narrative tension), Pixar (causal because-of-that chain for change stories). The methodology emits one of three artefacts — an executive summary, a case study, or a presentation outline — each obeying answer-first ordering and the so-what test on every claim.

**Ефективно для:**

- Executive summaries that lose readers in the second paragraph.
- Case studies that bury the outcome below 500 words of context.
- Investor decks where the story arc collapses into a feature list.
- Internal memos pitching a strategic shift.

## Applies If (ALL must hold)

- Audience is busy (executive, investor, customer in evaluation mode).
- Message must survive being read in 30 seconds.
- There is one central claim, not a status report.
- A 'so what' implication exists for every supporting fact.

## Skip If (ANY kills it)

- Status report — use Pyramid only if a decision is implied; otherwise plain bullets work.
- Technical reference doc — engineering reference is structured by API, not narrative.
- Reactive support reply — no narrative arc needed.
- Internal Slack thread of < 3 sentences.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Audience profile | role + decision they own + time budget | session owner |
| Central claim | one sentence | author |
| Evidence list | facts + sources | research |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[selling-ideas]] | pairs with SPIN for live pitches |
| [[storytelling]] | sister methodology focused on narrative structure |

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
| `framework-selection` | sonnet | Judgement on audience + message-type fit. |
| `draft-supports` | sonnet | MECE structuring requires judgement. |
| `so-what-pass` | haiku | Mechanical: append implication to each fact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/executive-summary.txt` | Pyramid-structured executive summary skeleton |
| `templates/case-study.txt` | Pyramid case-study skeleton with outcome-first headline |
| `templates/presentation-outline.txt` | SCQA / Pixar presentation outline skeleton |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-business-storytelling.py` | Validate business-storytelling artefact against the schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[storytelling]]
- [[selling-ideas]]
- [[stakeholder-communication]]
- [[feedback]]

## Decision tree

See `content/06-decision-tree.xml`. Routes by message type (decision / change / case-study) and the presence of a causal chain to a framework, each leaf referencing a rule from 01-core-rules.xml.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/executive-summary.txt`

```text
# Executive Summary Template (Pyramid Structure)

## Recommendation
[One sentence: what you recommend doing]

## Context
[2-3 sentences: situation (what is true today) and complication (what changed or threatens)]

## Key Points
1. [Argument 1 + supporting evidence with number]
2. [Argument 2 + supporting evidence with number]
3. [Argument 3 + supporting evidence with number]

## Next Steps
[Specific actions needed, who does what, by when]

---

# Example

## Recommendation
We should migrate our infrastructure to cloud hosting by Q3.

## Context
Our on-premise setup handles current load adequately. However, projected growth of 40% over 12 months will exceed capacity, and our current setup requires 3 weeks of engineering time per year for maintenance.

## Key Points
1. Cost: Cloud TCO is 40% lower at projected scale (based on AWS pricing calculator with our usage profile)
2. Scalability: Current servers reach 80% CPU during peak; cloud auto-scaling handles 10x spikes automatically
3. Speed: Deployment time drops from 3 hours to 15 minutes with managed CI/CD

## Next Steps
- Ruslan reviews cloud provider options by May 15
- Engineering estimates migration effort by May 22
- Decision meeting scheduled for May 29
```

### `templates/case-study.txt`

```text
# Case Study Template (Pixar Causal Structure)

## Challenge
[What problem did the customer/team face? Include the scale: how long, how costly, how frequent]

## Solution
[What approach was taken? 2-3 sentences, no technical depth required]

## Results
- [Metric 1: X% improvement in Y — before vs after]
- [Metric 2: $X saved or earned]
- [Metric 3: Time or effort reduction]

## Quote
"[Customer or team member testimonial]" — [Name, Title]

---

# Example

## Challenge
Our content team spent 10 hours per week manually compiling analytics reports from 5 different tools, leaving no time for actual analysis or strategy.

## Solution
We built an automated dashboard that pulls from all sources into a single view, with weekly email digests for stakeholders.

## Results
- Reporting time: 10 hours/week → 1 hour/week (90% reduction)
- Analysis output: 0 strategic recommendations per month → 4 per month
- Stakeholder satisfaction: NPS from 20 to 65

## Quote
"I finally have time to think about what the data means instead of just collecting it." — Maria, Head of Content
```

### `templates/presentation-outline.txt`

```text
# Presentation Outline Template (4 Sections)

## 1. HOOK (1 slide)
[Surprising fact, bold contradiction, or specific story — not an agenda]

## 2. PROBLEM (2-3 slides)
Situation: [What is true today — shared context]
Complication: [What changed or what is at risk]
Impact: [Concrete consequence if not addressed — with number]

## 3. SOLUTION (3-5 slides)
Approach: [High-level how without deep technical detail]
How it works: [Just enough mechanism to build credibility]
Proof: [Case study, benchmark, or pilot result]

## 4. CALL TO ACTION (1 slide)
Ask: [Specific decision — budget / approval / next meeting]
Timeline: [When a decision is needed and why]

---

# Notes
- One key point per slide — if you have more, split
- Slides support what you say; never read from slides
- End with the ask visible on screen during discussion
```
