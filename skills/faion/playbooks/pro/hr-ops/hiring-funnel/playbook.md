---
name: hiring-funnel
description: Run a repeatable ATS-style hiring funnel from JD publish to signed offer, hitting ≤30-day time-to-hire with per-stage conversion tracking.
tier: pro
group: hr-ops
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a documented, repeatable hiring funnel covering six stages (sourced → screened → technical → onsite → offer → signed), a conversion-rate spreadsheet that flags where candidates drop, a compliant offer letter template with salary, equity, start date, and contingencies filled in, and a completed onboarding handoff packet ready for day one.

## Prerequisites

- Legal entity with payroll capability (Ltd, SAS, GmbH, or equivalent) — offers cannot be made without it.
- Hiring budget confirmed: base salary × 1.3 to cover employer taxes and onboarding costs.
- A designated hiring manager and at least one technical interviewer committed to the panel.
- An ATS or lightweight substitute set up: Ashby (free trial), Notion hiring board, or a Google Sheet with the six-stage columns defined before sourcing begins.
- Role clarity: title, seniority level, remote/hybrid/onsite, and the three non-negotiable skills documented.
- Read the `recruiting-process` methodology under `pro/comms/hr-recruiter/` before configuring stage gates.
- Completed `first-hire-developer` playbook if this is your first-ever hire — that playbook covers the one-off founding-hire context; this playbook assumes the ops layer is already understood.

## Steps

### Stage 1 — Source (target: 40 qualified applicants in 7 days)

1. **Publish the JD on three channels simultaneously.**
   - LinkedIn Jobs: budget $150 for a 7-day sponsored post.
   - RemoteOK or We Work Remotely for remote roles ($299 flat fee, 30-day post).
   - Your own careers page or a pinned tweet/LinkedIn post if you have >1k relevant followers.
   JD must include: title, seniority, 3–5 hard requirements (no wish lists), salary band (e.g. $65k–$85k base), remote policy, and equity range (0.1%–0.5% for senior IC).

2. **Set up the sourcing tracker in your ATS.**
   Add columns: `Name | Source channel | Applied date | Stage | Last action | Notes`. Tag every inbound lead with its source channel so you can calculate cost-per-hire per channel after the cohort closes.

3. **Activate warm outreach in parallel.**
   Message 10 past colleagues or referral candidates on LinkedIn with a personalised 3-line note. Referral hires convert at 3× the rate of job-board applicants and typically have 40% shorter time-to-hire.

### Stage 2 — Screen (target: 12 screened from 40 applicants; conversion ≈ 30%)

4. **Apply the CV filter in ≤48h.**
   Hard-filter on: years relevant experience, required skills, red flags (3+ jobs in 18 months without explanation). Move rejects to `Archived` immediately to keep the pipeline clean.

5. **Send a 5-question async screen to all shortlisted applicants.**
   Use Loom or a 200-word written form. Cover: motivation for the role, one relevant past project, availability, expected salary, and one role-specific technical question (e.g. "describe your approach to database migrations in a live system"). Turnaround deadline: 48h. No response = auto-archive.

6. **Score screens using a 1–3 rubric.**
   3 = meets all criteria; 2 = meets most, one concern; 1 = clear gap. Only 2s and 3s advance. Document scores in the ATS. This creates an audit trail if candidates later challenge the process.

### Stage 3 — Technical (target: 6 from 12 screened; conversion ≈ 50%)

7. **Send the take-home task within 24h of async screen approval.**
   Time-box: 2–3 hours of genuine effort. Use a disposable GitHub repo with a README that states the task, input/output contract, and evaluation criteria. For backend roles: build a REST endpoint with tests. For frontend: implement a component from a Figma spec. Return deadline: 5 business days.

8. **Review submissions within 48h using the structured rubric.**
   Evaluate on: correctness, code quality, test coverage, and README clarity. Score each dimension 1–3. Minimum passing score: 9/12. Borderline submissions (7–8) go to a 15-minute clarification call before deciding.

### Stage 4 — Onsite (target: 4 from 6 technical passers; conversion ≈ 67%)

9. **Schedule the panel interview as a single 90-minute block.**
   Structure: 15 min culture/motivation (hiring manager), 45 min technical deep-dive (tech lead), 30 min role-play scenario or architecture discussion. Single block reduces candidate fatigue and speeds scheduling by 3–5 days vs. separate rounds.

10. **Use structured scoring with a shared scorecard.**
    Each interviewer scores independently before the debrief. Dimensions: technical depth, problem-solving approach, communication, and culture add. Debrief the same day. Consensus required; lone veto by one interviewer must be documented with specific observable evidence.

11. **Run reference checks on final 2 candidates before extending any offer.**
    Call two references per candidate (not just email). Ask: "What would this person need to improve to be ready for a senior role?" and "How did they handle a project that went wrong?" Weak references are a disqualifier; document answers verbatim.

### Stage 5 — Offer (target: ≤30 days from Stage 1 start; conversion: 80%+ of offers accepted)

12. **Extend the verbal offer within 24h of panel debrief.**
    State: base salary, equity (% + vesting schedule), start date, remote/hybrid policy, and any contingencies (background check, reference check completion). Give 48h to respond verbally before issuing written terms.

13. **Issue the written offer letter within 24h of verbal acceptance.**
    Required elements:
    - **Role title and reporting line** — e.g. "Senior Backend Engineer, reporting to CTO."
    - **Compensation** — base salary (monthly gross), currency, pay cadence (bi-weekly or monthly).
    - **Equity** — exact percentage (e.g. 0.3%), cliff (12 months), total vest (48 months), exercise window (90 days post-termination standard; negotiate 5 years for senior hires).
    - **Start date** — specific calendar date, not "ASAP."
    - **Contingencies** — background check passing, I-9 or equivalent right-to-work verification, any IP assignment agreement.
    - **Expiry** — offer valid for 5 business days from issue date.
    Use DocuSign or HelloSign for e-signature. Save the countersigned PDF to your HR folder before the start date.

14. **Negotiate scope, not salary range.**
    If the candidate counters above your band ceiling, offer accelerated review at 6 months, additional PTO days, or a signing bonus (one-time, non-recurring cost) before re-opening base salary.

### Stage 6 — Onboarding Handoff (complete before day one)

15. **Send the pre-boarding packet 5 business days before start date.**
    Contents: equipment shipping confirmation or office access instructions, accounts to be provisioned (GitHub org, Slack, 1Password), day-one agenda (first meeting at 10:00 local, with whom, where), and the 30/60/90-day plan document.

16. **Complete the internal handoff to the manager and team.**
    Manager delivers: completed onboarding checklist, access to team wiki, first sprint assignment or project brief, and intro to the two closest colleagues. Mark the task "Signed + Onboarding Initiated" in your ATS.

### Conversion tracking

Record actuals in your tracking sheet after each cohort closes:

| Stage | Target in | Target out | Target CVR | Actual CVR |
|-------|-----------|------------|------------|------------|
| Sourced | — | 40 | 100% | |
| Screened | 40 | 12 | 30% | |
| Technical | 12 | 6 | 50% | |
| Onsite | 6 | 4 | 67% | |
| Offer | 4 | 1 | 25% | |
| Signed | 1 | 1 | 80%+ | |

If actual CVR is >20% below target at any stage, run a root-cause review before the next cohort.

## Verify

Open your ATS and confirm:
- All six stages have at least one entry (even if archived).
- A countersigned offer PDF exists in your HR folder with the candidate's full name and start date.
- The 30/60/90-day plan document is accessible to the hiring manager.
- Time-to-hire (applied date → signed date) is ≤30 calendar days.

If time-to-hire exceeded 30 days, identify which stage held longest and whether it exceeded its target window.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| <10 qualified applicants after 7 days | JD too restrictive or salary band too low for the market | Remove 1–2 requirements from hard filter; check Glassdoor/Levels.fyi for local market rates and adjust band by 10–15% |
| Async screen response rate <40% | Long form, wrong channel, or candidate already placed | Shorten to 3 questions; switch from email form to Loom video prompt; re-source from a different channel |
| Take-home submissions miss the rubric entirely | Task is ambiguous or too open-ended | Rewrite README: add concrete input/output examples and a sample passing test so candidates understand expectations |
| Offer declined after verbal acceptance | Counter-offer from current employer or competing offer | Ask why immediately; if compensation, evaluate one-time signing bonus (not base bump); if role scope, discuss title or responsibilities; do not extend window beyond 2 extra days |
| Reference check reveals a serious concern | Reference describes a dismissal or interpersonal pattern | Do not proceed; archive with full notes; if only one reference flags it, conduct a third reference call before deciding |
| Onboarding handoff incomplete on day one | Manager not briefed or accounts not provisioned | Assign an "onboarding owner" (not the hiring manager) who owns the checklist; set a calendar reminder 5 business days before start |

## Next

- `pro/comms/hr-recruiter/onboarding-30-day` — structure the new hire's first 30 days with measurable check-ins and a formal 30-day review.
- `pro/comms/hr-recruiter/structured-interview-design` — deepen panel interview design with bias-reduction techniques and scoring calibration across multiple interviewers.
- `pro/team-management/first-hire-developer` — if this is your first ever hire, read this playbook for the founding-hire context before running this funnel.

## References

- [knowledge/pro/comms/hr-recruiter/recruiting-process](../../../knowledge/pro/comms/hr-recruiter/recruiting-process) — defines the six-stage gate model this playbook operationalises, including qualification criteria for each stage transition.
- [knowledge/pro/comms/hr-recruiter/recruitment-funnel-optimization](../../../knowledge/pro/comms/hr-recruiter/recruitment-funnel-optimization) — conversion benchmarks (30% screen rate, 50% technical pass rate) used in the Stage conversion targets and the tracking table.
- [knowledge/pro/comms/hr-recruiter/structured-interview-design](../../../knowledge/pro/comms/hr-recruiter/structured-interview-design) — shared scorecard design and independent scoring before debrief, referenced in Step 10 to prevent anchoring bias.
- [knowledge/pro/comms/hr-recruiter/onboarding](../../../knowledge/pro/comms/hr-recruiter/onboarding) — pre-boarding packet structure and day-one agenda components referenced in Step 15 for the onboarding handoff.
