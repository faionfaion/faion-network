# Difficult Conversations

## Summary

**One-sentence:** Generates a STATE-structured live script or DESC-structured written message for high-stakes conversations, with safety signals and WWWF close.

**One-paragraph:** The Crucial Conversations framework structures high-stakes conversations (high stakes + differing opinions + strong emotions) through seven sequential skills: Start with Heart, Learn to Look, Make it Safe, Master My Stories, STATE My Path, Explore Others' Paths (AMPP), Move to Action (WWWF). The DESC script is the shorter written format. Both require separation of observable facts from interpretations. Output: a STATE opening or DESC message + a preparation checklist + a WWWF tracker.

**Ефективно для:**

- Saying no to a boss when the request crosses a hard line.
- Boundary-setting Slack message about after-hours pings.
- Performance issue conversation that needs to stay factual.
- Co-founder values disagreement on a strategic call.

## Applies If (ALL must hold)

- Stakes are high, opinions differ, emotions are strong.
- Author has time to prepare (not real-time crisis).
- Both parties remain in the working relationship after the conversation.
- Observable facts can be separated from interpretation.

## Skip If (ANY kills it)

- Real-time crisis requiring de-escalation now — different protocol.
- Formal HR disciplinary process — defer to legal language.
- Anonymous feedback context — script-driven is wrong tool.
- Power asymmetry where political context dominates — coach with mentor first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Observable facts | dates, quotes, behaviors | author |
| My story | what I tell myself it means | author |
| Other party's perspective | what they likely tell themselves | author |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[conflict-resolution]] | neighbouring methodology for ongoing peer conflict |
| [[active-listening]] | RASA discipline during the live exchange |

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
| `fact-story-separation` | haiku | Mechanical stripping of evaluation. |
| `draft-state-or-desc` | sonnet | Tone-sensitive composition. |
| `wwwf-extraction` | haiku | Mechanical extraction of decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/preparation-checklist.md` | Pre-conversation preparation checklist |
| `templates/wwwf-tracker.md` | WHO/WHAT/WHEN/Follow-up commitment tracker |
| `templates/prompt-state-script.txt` | Prompt to generate a STATE opening from fact + story |
| `templates/prompt-desc-script.txt` | Prompt to generate a DESC written boundary message |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-difficult-conversations.py` | Validate difficult-conversations artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[conflict-resolution]]
- [[active-listening]]
- [[feedback]]
- [[stakeholder-communication]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by channel (live → STATE, async → DESC) and prep time availability. Without prep time the methodology refuses to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-state-script.txt`

```text
Help me prepare for a difficult conversation using the Crucial Conversations framework.
Situation: <describe what happened with specific observable facts>
What I want: for me: <goal>; for them: <goal>; for the relationship: <goal>
Facts (not stories): <list specific observable behaviors with dates or frequencies>
My contribution: <how did I create or enable this situation>
Their likely perspective: <what might they be thinking or feeling>

Output:
1. Preparation checklist assessment — what is clear, what is missing
2. STATE-structured opening script — 3-5 sentences maximum, must end with a genuine question
3. 2-3 AMPP questions to use when they respond
4. One potential safety risk and how to restore safety if it occurs
Human review required before use: verify every factual claim; calibrate tone to the actual relationship.
```

### `templates/prompt-desc-script.txt`

```text
Write a DESC script for the following boundary situation.
Situation: <describe the specific recurring behavior and its impact>
Target outcome: <what specific change I need>
Positive consequence if resolved: <what improves for both parties>
Negative consequence if unresolved: <what I will actually do — must be realistic and proportionate>

Output: 4 clearly labeled paragraphs (D / E / S / C). Keep under 100 words total.
D must contain a specific observable behavior, not an evaluation.
E must contain a genuine emotion word, not "I feel that..."
S must be a specific positive request, not a demand or a negative.
C negative consequence must be proportionate and something you are genuinely willing to do.
```
