---
slug: usability-test-cycle-end-to-end-3-weeks
tier: solo
group: role-ux-ui-designer
persona: Designer running a focused usability cycle on a defined feature
goal: discover-validate
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Single round of moderated + unmoderated usability testing on a defined feature -> severity-ranked findings + design fixes scoped + follow-up validation plan."
content_id: 066234ac486ace97
methodology_refs:
  - ai-interview-analysis
  - audience-segmentation
  - persona-building
  - success-metrics-definition
  - user-interviews-methods
  - ab-testing
  - heuristic-evaluation
  - usability-testing
  - user-interviews
---

# Usability test cycle, end-to-end (3 weeks)

## Context

Designer runs one usability cycle across 3 weeks. Includes script + recruit, moderated + unmoderated sessions (5-6 each), AI-assisted analysis, severity-ranked findings, and a scoped fix list with follow-up plan. Done when fixes are queued with engineering and a follow-up test is planned for the next iteration.

## Outcome

Open usability question on a feature -> severity-ranked findings + scoped fixes + follow-up plan. Single round of moderated + unmoderated usability testing on a defined feature -> severity-ranked findings + design fixes scoped + follow-up validation plan.

## Steps

1. **Plan.** Lock the test plan before recruiting. Tasks: Define test goals + success metrics; Build screener from audience segments + personas; Write test scripts per flow.
2. **Recruit.** Recruit the right participants in time. Tasks: Recruit 5-6 moderated participants; Launch unmoderated study with 8-10 panel users; Confirm consent + compensation.
3. **Moderated sessions.** Talk-aloud sessions for depth. Tasks: Run 5-6 moderated sessions; Capture task success/fail + observations; Same-day hot-take note per session.
4. **Unmoderated study.** Volume + behavior data. Tasks: Run unmoderated study with timed tasks; Optional A/B on a contested decision; Cross-reference with heuristic evaluation.
5. **AI-assisted analysis.** Speed up coding without losing signal. Tasks: Run AI transcript analysis; Human-validate codes; Apply severity rubric to findings.
6. **Scope fixes.** Decide what gets fixed now vs later. Tasks: Pair with engineering on fix scoping; Queue critical fixes in the backlog; Park lower-severity items with rationale.
7. **Follow-up plan.** Close the loop with a next test. Tasks: Define the follow-up validation plan; Schedule the next test post-fix; Communicate findings to stakeholders.

## Decision points

- **After Plan:** Advance when plan + script are reviewed.
- **After Recruit:** Advance when target sample is locked.
- **After Moderated sessions:** Advance only when sessions are completed.
- **After Unmoderated study:** Advance once unmoderated study is complete.
- **After AI-assisted analysis:** Advance only when severities are validated by a second eye.
- **After Scope fixes:** Advance only when criticals are queued with engineering.
- **After Follow-up plan:** Done when next test is on the calendar.

## References

- `faion/knowledge/geek/ux/user-researcher/ai-interview-analysis`
- `faion/knowledge/pro/ux/user-researcher/audience-segmentation`
- `faion/knowledge/pro/ux/user-researcher/persona-building`
- `faion/knowledge/solo/ux/user-researcher/success-metrics-definition`
- `faion/knowledge/solo/ux/user-researcher/user-interviews-methods`
- `faion/knowledge/solo/ux/ux-ui-designer/ab-testing`
- `faion/knowledge/solo/ux/ux-ui-designer/heuristic-evaluation`
- `faion/knowledge/solo/ux/ux-ui-designer/usability-testing`
- `faion/knowledge/solo/ux/ux-ui-designer/user-interviews`
- Related: `usability-test-moderation-single-session`, `heuristic-evaluation-on-a-new-screen-1hr`
