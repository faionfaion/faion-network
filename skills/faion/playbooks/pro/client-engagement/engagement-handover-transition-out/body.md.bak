# Engagement handover / transition out

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** medium · **Angle:** synthesis

## Why this playbook exists

End-of-engagement transition → client team (or another vendor) takes over → no Slack call to the outgoing dev for 30 days, AI agent on the receiving side answers correctly using the handover pack.

Synthesis playbook for a clean transition out. Covers a hand-off where the client team OR another vendor takes over. Output: 30-day silent period from the outgoing dev's calendar, an AGENTS.md the receiving team's AI agent can use, a decision-log reconstructed from git where docs trailed, signed transition-out paperwork.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Closure + lessons

**Intent:** Inhale lessons before the engagement memory fades.

**Tasks**
- Walk knowledge-areas detail with the receiving party
- Project closure ceremony
- Lessons-learned retro for the engagement
- Comms plan for the next 30 days

**Outputs**
- Closure deck
- Lessons-learned doc
- 30-day comms plan

**Decision gate**

Advance only when closure deck is countersigned.

### Stage 2 — Decision log + AGENTS.md

**Intent:** Hand over not just code, but reasoning.

**Tasks**
- Reconstruct decision log from git history where docs trailed
- Build AGENTS.md for the receiving team's AI agent
- Capture engagement-specific gotchas
- Pair with receiving party on one walkthrough

**Outputs**
- Decision log
- AGENTS.md handed to receiving team
- Pair-walkthrough log

**Decision gate**

Advance when receiving team's AI agent answers 'why X' from the handover pack alone.

### Stage 3 — Cutover + silence

**Intent:** Sign the transition-out paperwork; respect the 30-day silence.

**Tasks**
- Run transition-out sign-off ceremony
- Decommission outgoing access (laptops, accounts, VPN)
- Set out-of-engagement comms expectations
- Hold the 30-day silence — escalate via formal channels if needed

**Outputs**
- Signed transition-out doc
- Access decommissioned
- Silence period log

**Decision gate**

Done when 30-day silence holds AND no critical escalation hits the outgoing dev.

## Common pitfalls

- Leaving the outgoing dev on Slack 'just in case' — kills the silence period
- Skipping decision-log reconstruction — receiving team rebuilds the wheel
- AGENTS.md written for humans but ignored by AI agents — defeats the purpose

## Quality checklist

- Did the receiving team merge a PR using only the handover pack?
- Did we hit 30 days with zero Slack pings to the outgoing dev?
- Was the transition-out doc signed, not just acknowledged?

## Related playbooks

- `handover-to-client-in-house-team`
- `pre-handover-documentation-pack`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `engagement-handover-playbook` (blocks stage 2)
- `decision-log-reconstruction-from-git` (blocks stage 2)
- `agents-md-for-receiving-team` (blocks stage 2)
- `transition-out-signoff-template` (blocks stage 3)
