# Hire + onboard a new product-team dev in 2 weeks

**Playbook slug:** `hire-onboard-product-dev-2-weeks`
**Tier:** geek
**Complexity:** medium
**Persona:** P6 — Product-Dev Team

## Intent

Signed offer → first merged PR + first on-call shadow within 14 days.

## Scope

A new product-dev hire walks in on day 1 and walks out of day 14 with a merged PR, an on-call shadow under their belt, a 30/60/90-day plan filed, and a buddy. Their CLAUDE.md/AGENTS.md context pyramid is set up; they have run the dev loop locally; they know the incident protocol; the team has a written retro of how week-1 went.

### What this playbook covers

A four-stage chain that begins before day 1 and closes at day 14 with a retro. The point is to compress the typical 30-60 day ramp by treating onboarding as a feature delivery: pre-work, scoped first PR, shadowed incident exposure, retro. The methodologies are pulled from `pro/comms/hr-recruiter/` for the people-side and `geek/sdlc-ai/` for the engineering surface that the hire must absorb (CLAUDE.md pyramid, incident defaults, conventional commits floor).

### Non-goals

- Sourcing + screening — covered by `hiring-screen-take-home-review` and `hire-to-productive-60-days-in-house`
- Long-term performance reviews — out of scope for 14-day window
- Company-wide HR compliance training — handled by HR centrally

### Prerequisites

- Signed offer with start date
- Laptop + accounts provisioned before day 1
- Buddy assigned at offer-signature time, not day 1
- Repos have CLAUDE.md + AGENTS.md context pyramid in place

## Success criteria

The playbook is done when:
- 30/60/90-day plan filed by end of day 3
- Local dev loop running by end of day 2
- First PR merged by day 10
- First on-call shadow completed by day 14
- Day-14 retro between hire + manager + buddy
- Hire has read and acknowledged incident-runbook + secrets policy

## Stages

### Stage 1: Pre-arrival prep

**Intent:** Accounts, repo access, buddy, 30/60/90 skeleton ready before day 1.

**Tasks:**
- Provision laptop + accounts using secrets-management protocol
- Assign a buddy and a manager 1:1 cadence
- Pre-fill 30/60/90 skeleton tied to a small first owned ticket
- Confirm EVP messaging on day-1 welcome packet

**Methodologies in chain:**
- `employee-value-proposition` → `pro/comms/hr-recruiter/employee-value-proposition`
- `30-60-90-day-plan` → `pro/comms/hr-recruiter/30-60-90-day-plan`
- `secrets-management` → `pro/infra/cicd-engineer/secrets-management`

**Decision gate:**
> Advance when laptop boots, repo clones, buddy and manager are calendared. Otherwise day 1 burns on logistics.

### Stage 2: Week 1 — orient + first PR

**Intent:** Hire understands repo layout, runs dev loop, ships a small first PR.

**Tasks:**
- Walk the AGENTS.md context pyramid
- Pair with buddy on dev loop locally
- Pick a starter ticket with clear AC
- Open and merge a small PR with conventional commits

**Methodologies in chain:**
- `onboarding-30-day` → `pro/comms/hr-recruiter/onboarding-30-day`
- `onboarding` → `pro/comms/hr-recruiter/onboarding`
- `claude-md-creation` → `geek/dev/code-quality/claude-md-creation`
- `llm-friendly-architecture` → `geek/dev/code-quality/llm-friendly-architecture`
- `kb-agents-md-context-pyramid` → `geek/sdlc-ai/kb-agents-md-context-pyramid`
- `claude-code` → `geek/ai/claude-code`
- `gov-conventional-commits-enforced` → `geek/sdlc-ai/gov-conventional-commits-enforced`
- `lint-precommit-floor` → `geek/sdlc-ai/lint-precommit-floor`
- `task-plan-mode-locked-execution` → `geek/sdlc-ai/task-plan-mode-locked-execution`
- `task-spec-kit-three-step` → `geek/sdlc-ai/task-spec-kit-three-step`
- `task-worktree-runtime-isolation` → `geek/sdlc-ai/task-worktree-runtime-isolation`

**Decision gate:**
> Advance when the hire has merged a PR they understand and can explain back to their buddy.

### Stage 3: Week 2 — incident protocol + on-call shadow

**Intent:** Hire is incident-literate and has shadowed at least one on-call rotation slot.

**Tasks:**
- Walk the incident runbook + read-only-investigation default
- Walk the tool-tier approval gate
- Shadow an on-call slot with the buddy
- Dry-run a postmortem auto-draft on a synthetic incident

**Methodologies in chain:**
- `onboarding-60-90-day` → `pro/comms/hr-recruiter/onboarding-60-90-day`
- `inc-runbook-as-markdown-tagged-steps` → `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `inc-read-only-investigation-default` → `geek/sdlc-ai/inc-read-only-investigation-default`
- `inc-tool-tier-approval-gate` → `geek/sdlc-ai/inc-tool-tier-approval-gate`
- `inc-postmortem-auto-draft-no-publish` → `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish`

**Decision gate:**
> Advance when hire can articulate the read-only-investigation default and the approval-gate boundary unaided.

### Stage 4: Day-14 retro + retention loop

**Intent:** Capture what worked, what didn't, what to keep — wire to retention.

**Tasks:**
- Retro between hire + manager + buddy
- Update mistake-memory / patterns-memory with onboarding lessons
- Confirm 30/60/90 plan still fits or rewrite
- Set retention checkpoint at day 60

**Methodologies in chain:**
- `retention-compliance` → `pro/comms/hr-recruiter/retention-compliance`
- `lessons-learned` → `pro/pm/pm-traditional/lessons-learned`

**Decision gate:**
> Required output: written retro. If the hire stops at week 14 with no retro, the next hire repeats the same friction.

## Common pitfalls

- Buddy assigned on day 1, not before — wastes the first 48h
- Starter ticket too ambitious — kills momentum
- Skipping the incident protocol walkthrough — first page becomes the lesson
- Treating onboarding as "HR's job" — engineering owns ramp

## Quality checklist (self-review)

- Can the hire explain CLAUDE.md context pyramid back to me?
- Did the first PR pass our normal gates with no special exceptions?
- Did the hire ask at least one good repo-shaped question that surfaced a real gap?

## Related playbooks

- `hire-to-productive-60-days-in-house`
- `hiring-screen-take-home-review`
- `adopt-faion-org-wide-overrides`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **ai-pair-onboarding-script** (tier `geek`, blocks stage 2) — Week-1 stage needs an AI-pair script for guided first-PR sessions
- **ramp-task-difficulty-ladder** (tier `geek`, blocks stage 2) — Starter ticket selection needs a written difficulty ladder so picks aren't ad-hoc

## CLI usage

```
faion get-content hire-onboard-product-dev-2-weeks --format md       # human-readable rendering
faion get-content hire-onboard-product-dev-2-weeks --format context  # agent-optimised context bundle
faion get-content hire-onboard-product-dev-2-weeks --format json     # raw structured form
```
