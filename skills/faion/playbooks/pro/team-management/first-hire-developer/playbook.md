---
name: first-hire-developer
description: Run the full hiring funnel for your first developer — JD, sourcing, screening, take-home, panel, references, and offer with real equity numbers.
tier: pro
group: team-management
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have made and accepted a written offer to your first developer hire, with a role-appropriate JD published on three channels, a structured 4-stage evaluation process completed, references checked, and a signed offer letter that includes base salary, equity percentage, and a 30/60/90-day plan.

## Prerequisites

- A legal entity (Ltd, UG, SAS, or similar) with a bank account — you need to issue a contract.
- Budget confirmed: at least 3 months of salary in reserve before you post the role.
- Clarity on role type: frontend, backend, full-stack, or specialist (ML, mobile). Pick one.
- Read the `structured-interview-design` methodology under `pro/comms/hr-recruiter/` before designing your panel questions.
- A GitHub org or Bitbucket workspace where you can create a disposable take-home repo.
- 1Password or Bitwarden for securely sharing any sandbox credentials with candidates.

## Steps

1. **Write the JD — 5 must-haves only.**
   Draft the job description with exactly five technical requirements. Use this structure:

   ```
   Role: Senior Full-Stack Engineer (React + Django)
   Team size: 3 (you + 1 designer + this hire)
   Location: Remote, Europe timezone (UTC+0 to UTC+3 preferred)
   Compensation: €55–65k base + 0.25% equity (4-year vest, 1-year cliff)

   Must-haves (all 5 required):
   1. 4+ years shipping production React applications
   2. Python/Django REST API experience (not just tutorials)
   3. PostgreSQL — writes migrations, understands query plans
   4. Git workflow: PR-based, with code review experience
   5. Async communication fluency (written English, B2+)

   Nice-to-haves (list max 3 — none are filters):
   - Docker / docker-compose local dev experience
   - Experience at a ≤10-person startup
   - TypeScript

   What you'll work on: [2 sentences on the product and the first 3-month mission]
   ```

   Do not add "5+ years of X" where X is any technology under 5 years old. Do not list 10 requirements — you will filter out strong candidates who self-select out of inflated lists.

2. **Post on three channels in one day.**
   - **LinkedIn Jobs**: Post directly at https://www.linkedin.com/jobs/post/. Select "Remote" as location. Budget €5–15/day for 7 days of promotion. Expected reach: 200–600 impressions per day.
   - **Otta** (https://otta.com/post-a-job): Free for companies hiring fewer than 5 people. Strong signal-to-noise — candidates are actively looking. Fills in 2–4 weeks for a well-written JD.
   - **AngelList / Wellfound** (https://wellfound.com/recruit): Create a company profile, post the role. Startup-oriented candidates expect equity detail here — always publish the percentage.

   Do not post on all boards simultaneously. Three focused channels beat ten diluted ones.

3. **Screen applications: apply a binary filter in under 10 minutes per CV.**
   Your only filter at this stage is the 5 must-haves from the JD. Create a spreadsheet with columns:
   `Name | Source | React prod? | Django prod? | PG? | Git PR? | English? | Notes | Decision`

   Assign Y/N per criterion. Advance anyone with 5/5. Consider 4/5 only if the missing criterion is learnable in 2 weeks (e.g., PostgreSQL for a strong MySQL engineer).

   Target: advance 8–12 candidates to phone screen per 100 applications.

4. **Run a 30-minute phone screen: 3 calibration questions.**
   Book via Calendly (free plan). Send a Google Meet or Whereby link. Record only with consent.

   Ask these three questions exactly as written — they are calibrated for signal, not trick answers:

   ```
   Q1 (past project): "Tell me about the most complex backend system you personally
   designed or changed in the last 2 years. What was hard, and what would you do
   differently now?"
   → Listen for: concrete technical details, self-awareness, ownership language.
      Red flags: vague "we" answers, inability to describe tradeoffs.

   Q2 (values): "Describe a time a technical decision you made turned out to be wrong.
   How did you find out, and what did you do?"
   → Listen for: takes ownership, describes a real failure, shows learning.
      Red flags: blames others, minimizes, says it hasn't happened.

   Q3 (alignment): "What does your ideal working setup look like — team size,
   communication cadence, how you prefer to receive feedback?"
   → Listen for: compatibility with your actual environment (remote async? small team?).
      Red flags: describes something structurally incompatible with your setup.
   ```

   After the call, score each question 1–3. Advance candidates scoring ≥7/9 total.

   Target: advance 4–6 to take-home.

5. **Send a take-home assessment: max 3 hours, paid.**
   Pay €75–150 per completed assessment (wire or Wise transfer within 5 days of submission). This filters serious candidates in, not casual applicants out. Candidates who decline are often not a fit for async work.

   Create a **private GitHub repo** in your org (name: `hiring-[role]-[year]-[initials]`) and grant read access to the candidate. Include a `README.md` with:

   ```markdown
   # Take-home Assessment

   Estimated scope: 2–3 hours. Treat this as real work, not a demo.

   Task: [One concrete, scoped task relevant to your actual codebase]

   Example for a Django + React role:
   "Add a `/api/items/` endpoint that returns paginated items with optional
   `?category=` filter. Write one test. Add a minimal React component that
   fetches and displays the first page. No styling required."

   Criteria we evaluate:
   - Code structure and naming
   - Error handling
   - Test coverage of the happy path
   - README with setup instructions (must run in 5 minutes with docker-compose)

   Submission: Open a PR against this repo's main branch within 5 business days.
   ```

   Review the PR as you would a real one: leave inline comments, note what you liked and what you'd ask about.

6. **Run the final technical panel (3 people, 90 minutes).**
   Panel composition: you (founder/product), one engineer (part-time contractor or advisor), one domain expert (optional, async video review acceptable).

   Structure (use the `structured-interview-design` methodology for question anchors):

   | Slot | Duration | Owner | Content |
   |------|----------|-------|---------|
   | Architecture deep-dive | 30 min | Engineer | Walk us through a system you designed; whiteboard on Miro |
   | Code review live | 20 min | You | Candidate reviews a real (anonymized) PR from your codebase |
   | Values + growth | 20 min | You | 2 STAR behavioral questions from the methodology |
   | Candidate Q&A | 20 min | All | Candidate's questions — take notes on what they ask |

   Score each section independently (1–5) before debrief. Do not share scores during the panel.
   Debrief protocol: each panelist states their score + one sentence rationale. Discussion follows. Consensus required to advance to offer.

7. **Check two references: former manager + former peer.**
   Email template (adapt and send the day after the panel):

   ```
   Subject: Reference check for [Name] — [Role]

   Hi [Reference name],

   [Candidate] applied for a Senior Engineer role at [Your company]. They listed you
   as a reference. This takes 15 minutes by phone or async — whichever you prefer.

   Three questions I'd like to cover:
   1. How did [Name] handle a technically ambiguous situation?
   2. What would you say is their biggest area for growth?
   3. Would you hire them again if the role fit? (Yes / No / Depends — tell me the depends)

   If async works: just reply to this email.
   If you prefer a call: here's my Calendly — [link]

   Thanks,
   [Your name]
   ```

   A reference who won't answer question 3 directly is telling you something. Proceed to offer only with two positive references that include a direct "yes" to question 3.

8. **Send the offer letter with concrete numbers.**
   Deliver verbally first (30-min call), then follow up with a written letter within 24 hours.

   Concrete benchmark numbers for a Senior Full-Stack Engineer (remote, European market, May 2026):

   | Level | Base (gross) | Equity | Cliff | Vest |
   |-------|--------------|--------|-------|------|
   | Mid (3–5 yr) | €50–60k | 0.15–0.20% | 12 months | 4 years |
   | Senior (5–8 yr) | €60–75k | 0.20–0.30% | 12 months | 4 years |
   | Lead / Staff | €75–95k | 0.30–0.50% | 12 months | 4 years |

   Written offer must include:
   - Base salary (annual gross, currency, payment cycle)
   - Equity: exact percentage, vesting schedule (4-year, 1-year cliff standard), valuation basis or cap table share count
   - Start date
   - Notice period (2–4 weeks standard for remote roles in EU)
   - Equipment policy (provided or BYOD + monthly stipend €50–100)
   - 30/60/90-day plan: attach the plan document as a PDF

   Give 5 business days to decide. Do not retract the offer before day 5 unless there is a material change.

## Verify

After the offer is signed, confirm all of the following are true:

1. `git log --oneline -5` on the take-home repo shows the candidate's PR was merged — you have a concrete code artifact from the hire.
2. Your spreadsheet has 8 columns completed for all screened candidates (audit trail for any future diversity review).
3. Your lawyer or legal tool (Deel, Remote, or local counsel) has issued a contract matching the offer letter numbers exactly.
4. The 30/60/90-day plan is in your shared task manager with the hire's first milestone set for day 30.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Fewer than 20 applications after 2 weeks | JD too restrictive or channels wrong | Remove 1 must-have (usually years-of-experience), repost on Wellfound with equity visible |
| Strong candidates drop at phone screen | Screen feels like an interrogation | Open with 2-minute product pitch first; candidates self-select into mission before you evaluate |
| Take-home submissions are low quality | Task too open-ended or unpaid | Pay immediately after submission; narrow the task to one endpoint + one test |
| Panel disagreement — no consensus | Interviewers evaluated different competencies | Re-run independent scoring; if still split, default to No for first hire (cost of a bad first hire is severe) |
| Offer rejected on equity percentage | Candidate has competing offers with higher equity | Counter with accelerated cliff (6 months instead of 12) rather than raising percentage — preserves cap table |
| Reference says "depends" on re-hire question | Usually a performance or conduct issue | Ask one follow-up: "What context would change your answer?" If vague, treat as a soft no |
| Contractor availability for panel | You have no engineer to interview with | Hire a senior engineer on Toptal for 2 hours ($200–400) for panel only — still cheaper than a bad hire |

## Next

- Run the `onboarding-30-day` playbook immediately after signing — first-30-day failure is the most common cause of early attrition.
- Set up a structured 1-on-1 cadence (weekly, 30 min) in the first 90 days using the `30-60-90-day-plan` methodology.
- After 3 months, calibrate your hiring rubric: compare panel scores against actual performance to improve future screen accuracy.

## References

- [knowledge/pro/comms/hr-recruiter/recruiting-process](../../../knowledge/pro/comms/hr-recruiter/recruiting-process) — full-cycle talent acquisition framework that backs the 8-stage funnel in this playbook (JD → sourcing → screen → take-home → panel → references → offer → onboard).
- [knowledge/pro/comms/hr-recruiter/structured-interview-design](../../../knowledge/pro/comms/hr-recruiter/structured-interview-design) — six-step structured interview process used directly in Step 6's panel design: competency mapping, behavioral anchors, independent scoring, and debrief protocol.
- [knowledge/pro/comms/hr-recruiter/recruitment-funnel-optimization](../../../knowledge/pro/comms/hr-recruiter/recruitment-funnel-optimization) — stage-by-stage conversion benchmarks (application → screen → take-home → offer) used to set the target numbers in Steps 3 and 4.
