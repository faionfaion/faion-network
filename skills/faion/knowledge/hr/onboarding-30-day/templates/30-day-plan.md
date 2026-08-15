<!--
purpose: 30-day onboarding plan skeleton — week-by-week checklist with one named milestone
consumes: role definition + team roster + tooling access list
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~400-900 tokens when loaded as context
variables:
  - name: new_hire_name
    type: string
    required: true
    description: The new starter's name as they want to be called at work. This document is the first thing they read from you - the wrong form of their name is the first impression you get to make once.
  - name: role_title
    type: string
    required: true
    description: The role as it appears in their offer letter. If the plan below is not obviously the plan for that role, the mismatch is what they will notice in week one.
  - name: manager_name
    type: string
    required: true
    description: The manager who owns the day-7, day-14 and day-30 check-ins. One person - onboarding delegated to "the team" is onboarding delegated to nobody.
  - name: buddy_name
    type: string
    required: true
    description: A peer who joined 6 to 12 months ago. Recent enough to remember what was confusing, settled enough to answer - not the most senior person with free calendar space.
  - name: start_date
    type: string
    required: true
    description: First working day, ISO. Every day number below counts from here, and day 1 has a hard requirement - a working laptop by 10am - that has to be ordered against this date.
  - name: thirty_day_milestone
    type: text
    required: true
    description: ONE specific contribution they will have shipped by day 30 - "first PR merged to production". Not a feeling or a list; a thing that either happened or did not.
-->
# 30-Day Onboarding Plan: {{new_hire_name}} — {{role_title}}

**Manager:** {{manager_name}}
**Buddy:** {{buddy_name}}
**Start date:** {{start_date}}
**30-Day Milestone:** {{thirty_day_milestone}}

---

## Week 1: Orientation (Days 1-7)

**Day 1 (non-negotiable):**
- [ ] Working laptop + all accounts configured by 10am
- [ ] IT setup verified: email, Slack, GitHub/Jira/etc.
- [ ] Meet direct team (informal, no heavy agenda)
- [ ] Lunch with {{buddy_name}}
- NO training modules on Day 1

**Days 2-5:**
- [ ] 1:1 with {{manager_name}}: role expectations, success at 30/60/90 days
- [ ] Review onboarding doc [link]
- [ ] Complete HR paperwork and benefits enrollment
- [ ] Review company handbook and code of conduct [link]
- [ ] Meet [3-5 key stakeholders — list names]

**Day 7 check-in:** 1:1 with {{manager_name}} (agenda: first week experience, blockers, questions)

---

## Week 2: Foundation (Days 8-14)

- [ ] Complete required training: [list specific modules with links]
- [ ] Shadow [key workflow or process] with [person]
- [ ] Meet cross-functional partners: [list names + roles]
- [ ] Understand team goals and current sprint/quarter priorities
- [ ] Start learning primary tools: [list tools]

**Day 14 check-in:** Buddy check with {{buddy_name}} (navigation, culture, questions)

---

## Weeks 3-4: Deep Dive (Days 15-30)

- [ ] Understand current projects: [list 2-3 with context]
- [ ] Review past work examples: [where to find them]
- [ ] Identify top 3 knowledge gaps (write them down)
- [ ] Begin first task toward the 30-day milestone (guided)
- [ ] Complete 30-day milestone: {{thirty_day_milestone}}

**Day 30 check-in:** Manager review (milestone assessment, 60-day goals, satisfaction rating)

---

## 30-Day Success Criteria

- [ ] Can explain company mission and team's contribution to it
- [ ] Knows all direct team members by name and role
- [ ] Understands key processes and daily tools
- [ ] Has documented 60-day goals (co-created with {{manager_name}})
- [ ] Completed all required training modules
- [ ] **30-Day Milestone achieved:** {{thirty_day_milestone}}

---

## Resources

| Resource | Link | Owner |
|----------|------|-------|
| Onboarding wiki | | |
| Team runbook | | |
| Architecture overview | | |
| Org chart | | |
| PTO / benefits guide | | |
