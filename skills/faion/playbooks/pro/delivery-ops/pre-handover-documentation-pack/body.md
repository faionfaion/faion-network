# Pre-handover documentation pack

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** deep · **Angle:** atomic

## Why this playbook exists

Senior rotating off a project → produces a self-contained pack that lets the next person ship within a week.

Doc sprint produced when a senior is rotating off (vacation, next engagement, or full handoff). Output: a self-contained pack — ADRs, design docs, onboarding plan, dark-knowledge notes, shadow-session runbook — so the next person ships within a week. Used independently of the 3-week formal client handover.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Inventory

**Intent:** Audit what exists vs what's only in your head.

**Tasks**
- List active modules, services, integrations
- Walk through 30-day onboarding plan structure
- Identify gaps where docs trail reality
- Plan the project-closure-adjacent steps from existing methodology

**Outputs**
- Module inventory
- Doc-gap list

**Decision gate**

Advance only after every active module is listed.

### Stage 2 — Refresh docs

**Intent:** Close the gap between docs and reality.

**Tasks**
- Backfill ADRs for last 3 months of decisions
- Apply design-docs patterns to refresh stale docs
- Adopt living-documentation conventions per module
- Document scope boundaries (what was NOT built)
- Write design docs for any module without one

**Outputs**
- Refreshed ADRs
- Refreshed design docs
- Living-documentation conventions in place

**Decision gate**

Advance when a stranger can read the docs and answer top-10 questions unaided.

### Stage 3 — Dark knowledge + shadow

**Intent:** Capture the things never written down and arrange one shadow session.

**Tasks**
- Run dark-knowledge extraction interview with yourself (or a peer)
- Document gotchas: cron quirks, vendor flakes, weird ports
- Sketch shadow-session runbook for the rotation
- Compile the handover pack URL

**Outputs**
- Dark-knowledge doc
- Shadow-session plan
- Handover pack URL

**Decision gate**

Done when the pack is single-link shareable AND a peer has spot-checked it.

## Common pitfalls

- Treating handover as 'I'll write up next week' — never happens
- Documenting code but not the calendar quirks (vendor freezes, cron windows)
- No shadow session — the successor learns the bug list the hard way

## Quality checklist

- Could a new joiner ship a PR by day 5 using only this pack?
- Did I write down the things I'd whisper if I were on the phone?
- Did a peer spot-check the pack before I rotated?

## Related playbooks

- `handover-to-client-in-house-team`
- `engagement-handover-transition-out`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `handover-pack-template-outsource` (blocks stage 3)
- `dark-knowledge-extraction-protocol` (blocks stage 3)
- `shadow-handover-session-runbook` (blocks stage 3)
