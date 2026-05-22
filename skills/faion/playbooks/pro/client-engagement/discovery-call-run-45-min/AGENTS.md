---
slug: discovery-call-run-45-min
tier: pro
group: client-engagement
persona: P5
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Qualified lead to 45-min discovery call yielding qualified-or-disqualified verdict + pain map + budget signal + proposal go/no-go.
content_id: c0cf3fc3c0a38ca8
methodology_refs:
  - active-listening
  - elicitation-techniques
  - stakeholder-analysis
  - mom-test
  - growth-gtm-strategy
  - competitive-intelligence
  - selling-ideas
---

# Discovery call run (45 min)

**Playbook slug:** `discovery-call-run-45-min`
**Tier:** pro
**Complexity:** medium
**Persona:** P5 -- Micro-agency founder

## Intent

Qualified lead to 45-min discovery call yielding qualified-or-disqualified verdict + pain map + budget signal + proposal go/no-go.

## Scope

Founder runs a structured first call with a qualified lead. Output: qualified-or-disqualified decision, pain map, budget signal, proposal go/no-go. Exit artifact: discovery notes + verdict + next action booked.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Full requirements elicitation - happens post-signature
- Demo / pitch deck - distinct call type

### Prerequisites

- Lead passed triage with ICP fit signal
- Pre-call form returned with 3 baseline questions

## Success criteria

The playbook is done when:
- 45-min run-of-show followed
- Pain map captured in 3 layers (symptom, cause, cost)
- Budget signal explicit (not 'depends')
- Decision-maker + signoff path identified
- Verdict written: proposal / kill / clarify

## Stages

### Stage 1: Open + frame

**Intent:** 5 min - set the agenda, the rules, the time.

**Tasks:**
- State call objective + time
- Confirm decision context
- Ask what success looks like at end of call

**Methodologies in chain:**
- `active-listening` -> `solo/comms/communicator/active-listening`

**Outputs:**
- Confirmed agenda

**Decision gate:**
> Advance once lead confirms agenda and timing.

### Stage 2: Pain map

**Intent:** 25 min - symptom, cause, cost, history.

**Tasks:**
- Use Mom-Test framing
- Map symptom to cause to cost
- Surface workarounds + prior attempts

**Methodologies in chain:**
- `elicitation-techniques` -> `pro/ba/business-analyst/elicitation-techniques`
- `stakeholder-analysis` -> `pro/ba/business-analyst/stakeholder-analysis`
- `mom-test` -> `solo/comms/communicator/mom-test`

**Outputs:**
- Pain map notes

**Decision gate:**
> Advance if dominant pain is clearly articulated with cost.

### Stage 3: Budget + decision

**Intent:** 10 min - concrete budget + signoff path.

**Tasks:**
- Ask budget range explicitly
- Identify decision-maker + influencers
- Surface alternative solutions considered

**Methodologies in chain:**
- `growth-gtm-strategy` -> `pro/marketing/gtm-strategist/growth-gtm-strategy`
- `competitive-intelligence` -> `pro/research/market-researcher/competitive-intelligence`
- `selling-ideas` -> `solo/comms/communicator/selling-ideas`

**Outputs:**
- Budget signal
- Decision-maker map

**Decision gate:**
> Advance only with explicit budget range AND signoff path.

### Stage 4: Verdict + next step

**Intent:** 5 min - propose / kill / clarify, in writing same day.

**Tasks:**
- Score against qualification rubric
- Book next step OR send polite decline
- Log verdict in pipeline

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Verdict doc
- Next step booked

**Decision gate:**
> Required: written verdict + sent follow-up within same day.

## Common pitfalls

- Pitching during discovery - converts learning into selling and breaks rapport
- Skipping budget because 'it is awkward' - bites at proposal time
- Not writing the verdict same day - memory degrades fast

## Quality checklist (self-review)

- Did I learn or did I sell?
- Is the pain map sourced from the lead's words, not my framing?
- Did I write a verdict before opening Slack?

## Related playbooks

- `proposal-customization-from-base-template`
- `inbound-lead-to-signed-retainer`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **agency-discovery-call-scorecard** (tier `pro`, blocks stage 4) -- Verdict stage needs a scorecard for proposal/kill decision
- **founder-led-qualification-rubric** (tier `pro`, blocks stage 4) -- Verdict stage needs an explicit qualification rubric
- **discovery-call-structure** (tier `pro`, blocks stage 2) -- Pain-map stage references discovery-call-structure playbook not yet ported to v2 manifest

## CLI usage

```
faion get-content discovery-call-run-45-min --format md       # human-readable rendering
faion get-content discovery-call-run-45-min --format context  # agent-optimised context bundle
faion get-content discovery-call-run-45-min --format json     # raw structured form
```
