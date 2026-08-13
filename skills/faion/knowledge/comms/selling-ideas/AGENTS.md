# Selling Ideas

## Summary

**One-sentence:** Generates an SPIN-Challenger pitch artefact (elevator pitch / executive pitch / one-pager) that amplifies pain before presenting a solution, with LAER objection handling.

**One-paragraph:** A persuasion framework for pitching technical or business ideas to different audiences. Combines SPIN Selling (uncover and amplify pain via Situation → Problem → Implication → Need-payoff), Challenger Sale (teach a new insight, tailor, take control), the elevator pitch template, and LAER objection-handling (Listen, Acknowledge, Explore, Respond). Core rule: never pitch until the audience feels the problem.

**Ефективно для:**

- 30-second elevator pitch at a networking event.
- Executive briefing where the audience won't read past page 1.
- Sales conversation transitioning from discovery to proposal.
- Internal idea sale (engineer pitching adoption to PM).

## Applies If (ALL must hold)

- Audience has a real pain that the idea addresses.
- Author has time to ask 2-3 SPIN questions before pitching.
- Audience has decision authority on at least one next step.
- The idea has a concrete differentiator (Challenger insight).

## Skip If (ANY kills it)

- Audience is in evaluation-only mode (RFP) — different format.
- Pain has not been validated — go back to mom-test first.
- Pure information sharing, no decision sought — use storytelling.
- Author is hostile to the audience — selling is a relationship act.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Idea + differentiator | 1-sentence insight | author |
| Audience profile | role + likely pain + decision power | research |
| Proof points | evidence the solution works | case studies / metrics |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[mom-test]] | discovery before pitching |
| [[business-storytelling]] | frame the pitch with Pyramid / SCQA |

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
| `challenger-insight-draft` | sonnet | Synthesis of insight from data. |
| `spin-composition` | sonnet | Tone + order-sensitive. |
| `laer-objection-prep` | sonnet | Empathy + bounded judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/elevator-pitch.txt` | 30s elevator pitch skeleton (insight + 1-line SPIN + CTA) |
| `templates/executive-pitch.txt` | Executive pitch skeleton (insight + full SPIN + CTA) |
| `templates/one-pager.txt` | One-pager skeleton (Pyramid + SPIN + CTA box) |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-selling-ideas.py` | Validate selling-ideas artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[mom-test]]
- [[business-storytelling]]
- [[stakeholder-communication]]
- [[negotiation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on pain validation first; without it the methodology refuses to apply. Otherwise it routes by format to the matching structure rule.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/elevator-pitch.txt`

```text
# Elevator Pitch Template (7-line)

For [TARGET CUSTOMER]
Who [HAS THIS PROBLEM]
Our [PRODUCT/IDEA]
Is a [CATEGORY]
That [KEY BENEFIT]
Unlike [COMPETITORS/CURRENT APPROACH]
We [UNIQUE DIFFERENTIATOR]

---

# Example: CI/CD Pipeline

For engineering teams
Who waste hours on manual deployments
Our CI/CD pipeline
Is an automation platform
That deploys code in minutes with confidence
Unlike Jenkins or manual scripts
We require zero maintenance and integrate in 30 minutes

---

# 10-Second Version

"We help [WHO] [DO WHAT] [BETTER/FASTER/CHEAPER]."

Example: "We help engineering teams deploy daily instead of weekly."
```

### `templates/executive-pitch.txt`

```text
# Executive Pitch Structure (4 blocks, 30 seconds each)

## Block 1: Problem (30s)
[Business pain stated with a number]
Example: "We spend $200K/year on manual QA that could be automated."

## Block 2: Solution (30s)
[High-level approach — no technical depth]
Example: "We implement automated test coverage that catches bugs before production."

## Block 3: Impact (30s)
[Expected outcomes with numbers]
Example: "Based on industry benchmarks, 80% coverage reduces production incidents by 60%."

## Block 4: Ask (30s)
[Specific decision + timeline]
Example: "I'm asking for $30K and 6 weeks to implement a pilot. Can we schedule a review of the proposal?"
```

### `templates/one-pager.txt`

```text
# [IDEA NAME]

## Problem
[1-2 sentences describing the pain with numbers if possible]

## Solution
[1-2 sentences describing the approach — what it does, not how]

## Benefits
- [Benefit 1 with number: e.g., "40% reduction in deployment time"]
- [Benefit 2 with number]
- [Benefit 3 with number]

## Cost/Effort
[Time, money, and resources required — be specific]

## Risk
[What could go wrong + mitigation for each]

## Ask
[Specific decision needed: budget approval / resource allocation / go/no-go]
```
