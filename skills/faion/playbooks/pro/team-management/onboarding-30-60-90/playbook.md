---
name: onboarding-30-60-90
description: Run a structured 30/60/90-day onboarding plan for a new backend developer hire — from day-1 setup through independent feature delivery.
tier: pro
group: team-management
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a backend developer onboarded through three phases — Learn (days 1–30), Contribute (days 31–60), Execute (days 61–90) — with written milestones, three formal reviews anchored to observable code artifacts, and a documented development plan for quarter 2.

## Prerequisites

- A job offer signed and start date confirmed.
- Laptop ordered and arriving on or before day 1 (standard spec: 16 GB RAM, SSD, Ubuntu 22.04 or macOS 13+).
- Accounts pre-created: GitHub org invite, AWS IAM user (read-only dev), Linear workspace, Slack workspace, 1Password team vault, Google Workspace email.
- A `new-hire` Linear project created with the day-1 checklist as issues (template in `pro/comms/hr-recruiter/` under `onboarding-30-day`).
- Hiring manager blocks 2 h on day 1 for joint plan co-authoring and 30 min weekly for the first four weeks.
- At least one senior backend engineer designated as a code-review buddy for the first 30 days.

## Steps

### Phase 1: Day 1 — Setup and context

1. **Send the pre-boarding email three days before the start date.** Use the template in `pro/comms/hr-recruiter/` email sequence. Include: first-day Slack DM contact, laptop delivery status, and link to the internal `new-hire-backend-checklist` Linear project.

2. **Complete the laptop setup checklist on day 1.** The hire works through it independently; the buddy checks it is done by end of day:
   - Clone the main backend repo: `git clone git@github.com:your-org/backend.git`
   - Install Python 3.12, `pyenv`, `direnv`, `docker compose`
   - Copy `.env.example` to `.env.local`, fill the three required dev secrets from 1Password vault `dev-shared`
   - Run `make dev` — Django dev server at `http://localhost:8000`; all 312 unit tests pass with `pytest -q`
   - Install `pre-commit` hooks: `pre-commit install`
   - Verify Slack, Linear, GitHub SSO, AWS Console read-only login all work

3. **Send intro emails to the five key contacts.** Use the template from `pro/comms/hr-recruiter/` for the internal-intro email. Recipients: backend lead, product manager, QA lead, devops engineer, and one frontend peer. Subject line: `Hi from [Name] — new backend dev`.

4. **Co-author the 30/60/90 plan.** Hiring manager and new hire sit together for 90 minutes. Fill in the plan scaffold (see below) with role-specific milestones. Save the document to Notion under `Team / Onboarding / [Name]-30-60-90.md`. Both parties sign off by EOD.

   **Day-30 milestones to write into the plan:**
   - Dev environment fully operational (verified by `make dev` + passing tests).
   - First PR merged: a bug fix or doc update chosen from the `good-first-issue` label in Linear.
   - All four CI/CD workflow steps (lint, test, build, deploy-staging) completed at least once as author.
   - Met all five key contacts (verified by sent intro emails + one follow-up Slack conversation each).
   - Written a 1-pager observation on one friction point in the codebase or tooling.

### Phase 2: Days 2–30 — Learn

5. **Read the architecture document in the first week.** Path: `docs/architecture/backend-overview.md`. By end of week 1 the hire should be able to describe the Django app structure, the three main Celery queues, and the database schema for the `orders` domain in their own words (verified at the day-7 pulse check).

6. **Shadow three production incidents or code reviews.** Log each in Linear as `observation` notes. The buddy adds the hire as a reviewer on at least two PRs per week from day 3 onward.

7. **Ship the first PR by day 14.** Pick from `good-first-issue` in Linear. Typical scope: fix a flaky test, correct a stale docstring, add a missing field validation. The PR must pass CI, receive one code review approval, and be merged by the hire following the team's squash-merge convention.

8. **Day-25 review (run before day 30).** Hiring manager runs the structured check-in at day 25, not day 30, to leave a 5-day correction window. Conversation prompt:
   - "Walk me through the 1-pager you wrote. What was the friction point and what would you change?"
   - "Which part of the codebase feels least familiar?"
   - "Are the day-60 milestones still realistic as written?"
   Update the plan doc if any milestone needs re-scoping.

### Phase 3: Days 31–60 — Contribute

9. **Assign the first owned feature by day 31.** The hire picks up a scoped Linear issue labeled `starter-feature` — typical scope: a new REST endpoint with model, serializer, view, URL, and integration test. The hire writes the technical design in a Linear comment (≤1 page) before coding. Buddy reviews the design within 24 h.

10. **Ship the feature end-to-end by day 55.** "End-to-end" means: merged to main, deployed to staging, manually smoke-tested by QA, and observed in production logs for 48 h post-deploy without error spikes. The hire writes a 3-sentence post-mortem in the Linear issue: what was harder than expected, what was learned, what to do differently.

11. **Own at least 2 code reviews per sprint from day 35.** Reviews must include a substantive comment (not just approval). Buddy tracks this in the weekly 1:1.

12. **Day-45 skip-level check-in.** The hire meets the engineering manager (hiring manager's manager) for 30 minutes. This removes the reporting-chain blind spot. Standard questions from EM: "What's working well in the team?", "What would help you move faster?". EM shares observations upward; nothing punitive.

13. **Day-60 review.** Hiring manager runs the structured 60-day check-in:
    - "Show me the feature you shipped. Walk me through one tricky decision you made."
    - "Which process or tool in the team should we improve, and what's your proposed solution?"
    - "Here are your day-90 milestones — anything that needs adjusting?"
    Update the plan doc. If the feature is not yet merged, document the blocker and reset the day-90 milestone accordingly.

### Phase 4: Days 61–90 — Execute

14. **Start the first medium-complexity feature independently by day 62.** "Medium-complexity" means: involves two or more domains (e.g., `orders` + `notifications`), requires a migration, and has an external dependency (third-party API or async Celery task). The hire writes the design doc, presents it in the weekly backend sync, incorporates feedback, and starts implementation — without the buddy's day-to-day involvement.

15. **Lead or present in one team sync by day 80.** Options: present the feature design, run the sprint retrospective, or demo a merged feature to the broader team. Hiring manager introduces them; the hire does the talking.

16. **Peer feedback collection at day 85.** Hiring manager collects written feedback from the buddy and one other engineer who reviewed the hire's PRs. Three questions: "What has this person done well in the past 60 days?", "What is one area where they could grow?", "Would you want them on your next project?" Feedback goes into the day-90 review.

17. **Day-90 formal review.** Hiring manager runs the structured 90-day performance review:
    - "Walk me through what you shipped over 90 days."
    - "What do you want to own in Q2?"
    - "Based on peer feedback, here is one growth area — let's build a development plan around it."
    Output: a written development plan for Q2 saved to Notion under `Team / Dev Plans / [Name]-Q2.md`. If autonomy on 80%+ of tasks is not yet achieved, open a formal performance conversation — do not extend the onboarding frame.

## Verify

At the end of each phase, run this observable check:

**Day 30:**
```
gh pr list --author <github-username> --state merged --repo your-org/backend
```
At least 1 merged PR. The `good-first-issue` Linear ticket is `Done`.

**Day 60:**
```
gh pr list --author <github-username> --state merged --repo your-org/backend
```
At least 3 merged PRs including the `starter-feature` ticket. Linear issue status is `Done`, and the QA smoke-test note is present in the issue comments.

**Day 90:**
The Notion doc `Team / Dev Plans / [Name]-Q2.md` exists and has at least one specific growth goal. The medium-complexity feature PR is open or merged. Peer feedback doc is saved.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Hire's first PR is still in draft at day 20 | `good-first-issue` scope was too large, or environment problems blocked progress | Buddy pairs with hire for 2 h to unblock; re-scope the issue to ≤4 hours of work if needed |
| Day-30 plan milestones were written by HR alone; hire treats them as a checklist, not a commitment | Co-authoring step (Step 4) was skipped | Redo a 45-minute co-author session at day 5 at the latest; rewrite vague milestones with the hire present |
| Hire misses the day-55 ship target for the starter feature | Scope crept or technical dependencies were underestimated | Hold a scope-cutting session (see `pro/delivery-ops/` scope-cutting playbook); drop non-essential sub-tasks; re-target merge for day 60 |
| Day-45 skip-level meeting creates anxiety ("am I in trouble?") | Hire was not told the purpose | Explain in advance: "This is a standard step in our onboarding. EM wants to hear how the team feels from your perspective — nothing punitive." |
| Peer feedback at day 85 is vague ("great communicator, friendly") | Reviewers were not given structured questions | Re-send the three-question prompt; allow 24 h for resubmission before the day-90 review |
| Hire achieves <80% autonomy at day 90 | Under-qualified for the role, or the starter-feature scope was too large to complete in the ramp window | Open a formal performance conversation immediately; set a 30-day PIP with two specific measurable goals; do not extend onboarding framing |

## Next

- Run the `first-hire-developer` playbook if this is the first engineering hire and you need to set up the role architecture before Day 1.
- Review `pro/comms/hr-recruiter/` structured-interview-design methodology to calibrate the day-90 review scoring against the original hire criteria.
- In Q2, use the development plan produced at day 90 as input for the quarterly OKR-setting conversation.

## References

- [knowledge/pro/comms/hr-recruiter/30-60-90-day-plan](../../../knowledge/pro/comms/hr-recruiter/30-60-90-day-plan) — three-phase Learn/Contribute/Execute cadence, observable-artifact milestone rule, co-authoring on Day 1, and the day-25 early-review pattern used throughout Steps 4, 8, 13, and 17.
- [knowledge/pro/comms/hr-recruiter/onboarding](../../../knowledge/pro/comms/hr-recruiter/onboarding) — preboarding-to-day-1 flow, intro-email sequence, and buddy assignment pattern backing Steps 1, 3, and 6.
- [knowledge/pro/comms/hr-recruiter/onboarding-30-day](../../../knowledge/pro/comms/hr-recruiter/onboarding-30-day) — specific day-1 checklist items, `good-first-issue` PR target, and week-1 architecture-read milestone used in Steps 2, 5, and 7.
