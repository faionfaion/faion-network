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
