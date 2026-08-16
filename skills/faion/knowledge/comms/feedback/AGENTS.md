# Giving and Receiving Feedback

## Summary

**One-sentence:** Generates an SBI/SBII feedback message (Situation-Behavior-Impact[-Intent]) calibrated on Radical Candor's care/challenge axes; LEARN script for receiving.

**One-paragraph:** A set of structured models for delivering and receiving feedback that is specific, behavior-focused, and actionable. SBI (Situation-Behavior-Impact) is the base format; SBII adds an Intent inquiry to avoid attribution errors. Radical Candor calibrates the care/challenge axes — Care Personally + Challenge Directly. For receiving feedback, LEARN (Listen-Empathize-Acknowledge-Respond-Next steps) prevents defensive reactions. Output: an SBI/SBII message + a LEARN response script + a Radical-Candor quadrant tag.

**Ефективно для:**

- Performance conversations that need to stay behavior-focused.
- Praising contribution without slipping into personality.
- Coaching a teammate whose habit blocks delivery.
- Receiving harsh feedback without going defensive.

## Applies If (ALL must hold)

- The behavior is recent (≤ 7 days) so memory is sharp.
- Concrete observable behavior exists, not a personality claim.
- The author cares about the recipient (Radical Candor's care axis is true).
- Time exists for a real conversation, not just a Slack zinger.

## Skip If (ANY kills it)

- Public channel — feedback delivered publicly is humiliation, not feedback.
- Author's only goal is venting — write to self, do not deliver.
- Behavior is not actually observable — coach the observation first.
- Recipient is currently in crisis — defer feedback.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Situation | where + when (specific) | author |
| Behavior | what happened, observable | author |
| Impact | consequence on you / team / outcome | author |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[active-listening]] | for receiving feedback (LEARN response) |
| [[conflict-resolution]] | when the feedback may surface deeper conflict |

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
| `strip-interpretation` | haiku | Mechanical rewrite of personality into behavior. |
| `compose-sbii` | sonnet | Tone-sensitive structuring. |
| `quadrant-check` | sonnet | Self-deception detection requires judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/constructive-feedback.txt` | SBII constructive feedback skeleton |
| `templates/positive-feedback.txt` | SBI positive recognition skeleton |
| `templates/asking-for-feedback.txt` | Prompt to invite feedback using LEARN-ready framing |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feedback.py` | Validate feedback artefact against the schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[conflict-resolution]]
- [[difficult-conversations]]
- [[active-listening]]
- [[stakeholder-communication]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by direction (giving / receiving) and, for giving, by the sign of the impact to decide SBI vs SBII and the honesty cross-check.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/constructive-feedback.txt`

```text
# Constructive Feedback Template (SBI)

"[Name], do you have 5 minutes? I have some feedback.

In [SITUATION / specific context],
when you [BEHAVIOR / observable action],
the impact was [NEGATIVE EFFECT / concrete consequence].

Going forward, could you [ALTERNATIVE BEHAVIOR]?
What do you think?"

---

# Example

"Jordan, do you have 5 minutes? I have some feedback.

In the code review yesterday,
when you approved the PR without comments,
the impact was that a bug made it to staging and QA had to work overtime.

Going forward, could you leave at least one comment noting what you checked?
What do you think?"
```

### `templates/positive-feedback.txt`

```text
# Positive Feedback Template (EEC)

"Hey [Name], quick positive feedback:

In [SITUATION / specific context],
when you [BEHAVIOR / observable action],
[POSITIVE EFFECT / concrete impact on team, project, or person].

Keep it up — [why this matters or what to repeat]."

---

# Example

"Hey Alex, quick positive feedback:

In yesterday's client demo,
when you opened with the customer problem story,
the client immediately understood why this matters and asked for a proposal.

Keep it up — that hook framing is exactly what we need in every demo."
```

### `templates/asking-for-feedback.txt`

```text
# Asking for Feedback Template

"I'm working on improving [SPECIFIC AREA].

Could you give me feedback on [SPECIFIC THING — one behavior or output]?

Specifically:
- What's working well that I should keep doing?
- What's one thing I could do differently?"

---

# Example

"I'm working on improving how I communicate technical decisions to non-technical stakeholders.

Could you give me feedback on my last architecture proposal presentation?

Specifically:
- What's working well that I should keep doing?
- What's one thing I could do differently to make it clearer?"
```
