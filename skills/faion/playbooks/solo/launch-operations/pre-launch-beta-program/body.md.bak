# Pre-launch beta program

**Playbook slug:** `pre-launch-beta-program`  
**Tier:** solo  
**Complexity:** medium  
**Persona:** P1 — Solo SaaS Builder

## Intent

Working MVP → public-ready v1 with testimonials and waitlist after a closed beta.

## Scope

Solo founder runs a closed beta of 10–30 hand-picked users that produces a buyable v1, testimonials, and a launch-day waitlist. End state is a rehearsed public launch, not improvised. Exit artifact is a launch-day runbook with confirmed waitlist count.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Public open beta — closed, hand-picked only
- Pricing experiments — done after launch

### Prerequisites

- MVP completes end-to-end workflow on staging
- List of 50+ prospects to invite from prior discovery

## Success criteria

The playbook is done when:
- 10-30 beta users active for at least 2 weeks
- ≥5 written testimonials with permission to publish
- ≥3 high-severity issues found and resolved before launch
- Launch-day runbook with hour-by-hour plan
- Waitlist with ≥100 confirmed signups

## Stages

### Stage 1: Charter

**Intent:** Define what the beta is FOR, who's in, what's measured.

**Tasks:**
- Write beta charter (purpose + success criteria)
- Pick 10-30 invitees by ICP fit
- Set beta exit date

**Methodologies in chain:**
- `feature-prioritization-moscow` → `solo/product/product-manager/feature-prioritization-moscow`
- `success-metrics-definition` → `solo/research/researcher/success-metrics-definition`
- `use-case-mapping` → `solo/research/researcher/use-case-mapping`

**Outputs:**
- Beta charter doc
- Invitee list

**Decision gate:**
> Advance once charter is signed off. Refuse to run beta without explicit success criteria.

### Stage 2: Onboard

**Intent:** Hand-hold each beta user through first value moment.

**Tasks:**
- Personal welcome email per invitee
- Schedule kick-off calls
- Document onboarding gaps

**Methodologies in chain:**
- `active-listening` → `solo/comms/communicator/active-listening`
- `growth-landing-page-design` → `solo/marketing/conversion-optimizer/growth-landing-page-design`

**Outputs:**
- Welcome sequence
- Per-user kickoff notes

**Decision gate:**
> Advance when ≥80% of invitees complete first value moment. Stay if <50%.

### Stage 3: Observe

**Intent:** Watch how they use it under real conditions without explaining.

**Tasks:**
- Set up session replays / logs
- Run 5 follow-up interviews
- Tag confusion + bug events

**Methodologies in chain:**
- `heuristic-evaluation` → `solo/ux/ux-ui-designer/heuristic-evaluation`
- `usability-testing` → `solo/ux/ux-ui-designer/usability-testing`
- `user-interviews` → `solo/research/researcher/user-interviews`
- `feedback-management` → `solo/product/product-operations/feedback-management`
- `product-analytics` → `solo/product/product-operations/product-analytics`

**Outputs:**
- Confusion + bug log
- Usage analytics snapshot

**Decision gate:**
> Advance when ≥3 themes emerge. Loop if signal is too noisy.

### Stage 4: Iterate

**Intent:** Ship fixes for blocking issues only — resist scope creep.

**Tasks:**
- Cut iteration list to launch-blockers
- Ship fixes
- Re-test with beta cohort

**Methodologies in chain:**
- `technical-debt` → `solo/dev/software-developer/technical-debt`
- `technical-debt-management` → `solo/product/product-operations/technical-debt-management`

**Outputs:**
- Iteration changelog
- Tech debt log for post-launch

**Decision gate:**
> Advance when zero launch-blockers remain. If new blockers appear, repeat Observe.

### Stage 5: Harvest

**Intent:** Collect testimonials, build the waitlist, lock the launch date.

**Tasks:**
- Request testimonials with permission
- Open public waitlist
- Pick launch date + channels

**Methodologies in chain:**
- `growth-customer-testimonials` → `solo/marketing/content-marketer/growth-customer-testimonials`
- `growth-reddit-marketing` → `solo/marketing/content-marketer/growth-reddit-marketing`
- `growth-indiehackers-strategy` → `solo/marketing/gtm-strategist/growth-indiehackers-strategy`
- `product-launch` → `solo/product/product-manager/product-launch`

**Outputs:**
- ≥5 testimonials
- Waitlist page live
- Launch date

**Decision gate:**
> Required output: launch-day runbook + waitlist count. Move to public launch.

## Common pitfalls

- Inviting friends who won't churn-test the product — pick real prospects
- Treating beta as private demo — must run unattended for real signal

## Quality checklist (self-review)

- Did the beta surface bugs I didn't know about, or just confirm what I built?
- Are the testimonials specific (named outcomes) or generic ('great tool')?

## Related playbooks

- `solo-idea-to-validated-mvp`
- `pmf-hunt-post-mvp`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **beta-charter-template** (tier `solo`, blocks stage 1) — Charter stage needs ready-to-fill template with success criteria slots
- **solo-launch-day-runbook** (tier `solo`, blocks stage 5) — Harvest stage outputs a runbook but template doesn't yet exist

## CLI usage

```
faion get-content pre-launch-beta-program --format md       # human-readable rendering
faion get-content pre-launch-beta-program --format context  # agent-optimised context bundle
faion get-content pre-launch-beta-program --format json     # raw structured form
```
