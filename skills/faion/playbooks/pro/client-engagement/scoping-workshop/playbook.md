---
name: scoping-workshop
description: Run a 2-hour client scoping workshop and produce a signed scope.md covering user stories, prioritized features, risks, and budget alignment.
tier: pro
group: client-engagement
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have conducted a structured 2-hour workshop with your client and produced a `scope.md` document — covering context, user stories, MoSCoW-prioritized features, a risk register, and budget/timeline calibration — that both parties sign off on before any design or development begins.

## Prerequisites

- A signed engagement letter or NDA with the client.
- A shared calendar invite (Google Meet / Zoom link ready) for the 2-hour slot.
- A shared doc workspace (Notion, Google Docs, or Confluence) where the client can see the document being drafted in real time.
- The `scope.md` template from this playbook's `templates.md` (or copy the inline template in Step 6 below).
- At least one client stakeholder with budget authority on the call.
- Familiarity with MoSCoW prioritization (`must`, `should`, `could`, `won't`) — see References.

## Steps

### Block 1 — Context Check (0:00–0:15)

1. Open the shared doc and paste the template header: project name, date, attendees, version `0.1-draft`.
2. Ask the client to confirm the business trigger in one sentence: *"What problem disappears when this project ships?"* Record verbatim in the `## Context` section.
3. Ask: *"Who loses money or time today because this problem exists?"* — this surfaces the primary user persona.
4. Confirm the client's internal decision-maker for scope changes (name + role). Record in `## Stakeholders`.
5. Set the timer for Block 2. If the context discussion runs long, park deeper explanations in a `## Parking Lot` section and move on.

### Block 2 — User Story Mapping (0:15–0:45)

6. Open a virtual whiteboard (Miro or FigJam) or share your screen with a table:

   | Story ID | As a… | I want to… | So that… |
   |----------|--------|------------|----------|
   | US-01 | returning customer | reset my password via SMS | I can log in without contacting support |

7. Ask the client: *"Walk me through a day in the life of your primary user. What do they do first?"* Write each action as a user story (`US-01`, `US-02`, …).
8. Aim for 8–15 user stories. Stop at 15 — anything beyond that signals scope creep.
9. Group stories into 3–5 epics (e.g., `Auth`, `Dashboard`, `Notifications`). Label each story with its epic tag.
10. Copy the full story table into the `## User Stories` section of `scope.md`.

### Block 3 — MoSCoW Prioritization (0:45–1:15)

11. For each user story, ask: *"If we skip this entirely, does the product still solve the core problem?"*
    - No → `must`
    - Yes, but it hurts UX → `should`
    - Nice to have → `could`
    - Explicitly out of scope → `won't`
12. Record priority in the `Priority` column of the user story table.
13. Count `must` stories. If there are more than 7, push back: *"We have 9 musts — that's a full product, not an MVP. Which 3 would you cut if budget halved?"* Force a ranking of the `must` list (1 = highest).
14. Paste the final prioritized table into `## Features (MoSCoW)` in `scope.md`.

### Block 4 — Risk Register (1:15–1:30)

15. Create a three-column table in `scope.md` under `## Risks`:

    | Risk | Likelihood (H/M/L) | Mitigation |
    |------|-------------------|------------|
    | Third-party payment API changes pricing | M | Abstract payment layer; switch provider in 1 sprint if needed |
    | Client content (copy, images) delayed ≥2 weeks | H | Content freeze date in contract; placeholder assets used until then |
    | Key client stakeholder unavailable for review | M | Designate a backup approver now (name: _______) |

16. Ask the client: *"What external systems do we depend on?"* Add each as a risk row.
17. Ask: *"What has blocked similar projects at your company before?"* Add those too.
18. Assign Likelihood together. Agree on mitigations you both own (yours vs. theirs).

### Block 5 — Budget and Timeline Calibration (1:30–1:45)

19. Share your ballpark estimate range (do NOT give a single number yet): *"Based on the 6 must stories, I estimate X–Y weeks and $A–$B."*
20. Ask: *"What is your hard budget ceiling?"* If the ceiling is below your lower bound, go back to the `must` list and cut.
21. Ask: *"Is there a date that, if we miss it, causes real business pain?"* Record it as the `hard deadline` vs. `soft deadline`.
22. Document the agreed budget range and both deadlines in `## Budget + Timeline` in `scope.md`.
23. Note any scope items explicitly deferred to a Phase 2 in `## Out of Scope`.

### Block 6 — Next Steps (1:45–2:00)

24. Read the `## Next Steps` template aloud and fill in together:

    ```
    - [ ] Agency: deliver scope.md v1.0 (signed) within 24h
    - [ ] Client: confirm content freeze date by YYYY-MM-DD
    - [ ] Agency: send design proposal within 5 business days of scope sign-off
    - [ ] Client: introduce technical lead (if separate from stakeholder) by YYYY-MM-DD
    ```

25. Confirm that the client will sign off via email reply or a digital signature on the doc (DocuSign / native Google Doc approval).
26. Close the call. Send the completed `scope.md` via email within 24 hours of the session.

### Produce scope.md (post-call, within 24h)

27. Clean up the draft: remove `[Parking Lot]` items that were resolved, fix typos, add the version header `v1.0 — pending sign-off`.
28. Send to the client with subject line: `[ProjectName] Scope v1.0 — please sign off by YYYY-MM-DD`.
29. On sign-off: update version to `v1.0-signed`, record the sign-off date and approver name in the header.
30. File `scope.md` in your project folder (e.g., `projects/clientname-2026-q3/docs/scope.md`).

## Verify

Open `scope.md` and confirm all five sections are filled:

```bash
grep -c "^## " projects/clientname-2026-q3/docs/scope.md
```

Expected output: `7` (Context, Stakeholders, User Stories, Features (MoSCoW), Risks, Budget + Timeline, Next Steps + Out of Scope).

Additionally, confirm the client's sign-off reply email is in your inbox before starting any design or development work. If the count is less than 7 or no sign-off email exists, the workshop is incomplete.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Client lists 20+ user stories with no agreement on priorities | Stakeholder has not thought about scope before the call | Enforce the time-box hard. Stop story mapping at 15 items. Tell the client: "We'll prioritize now and park the rest in Phase 2." |
| Budget ceiling is 40% below estimate after must-story count | Client has unrealistic expectations | Do not negotiate the rate. Instead, cut scope: present 3 must stories that could move to should and show the resulting estimate range. |
| Key decision-maker joins 20 minutes late | Scheduling failure | Restart Block 1 (5 minutes) for the late joiner. Do not skip context check — wrong assumptions at this stage cost weeks later. |
| Client insists every story is a "must" | Fear of missing features | Use the "budget halved" forcing question (Step 13). If that fails, show the delivery timeline for all-must and let the date speak. |
| Client wants to skip the risk register | Time pressure | Read the two highest-likelihood risks aloud and ask: "If this happens and we haven't agreed on mitigation, who owns it?" That usually unblocks the conversation. |
| scope.md sign-off is delayed beyond 5 business days | Internal client approval chain | Escalate to the contact you identified in Step 4. Add a clause to your engagement letter: "Scope is frozen 7 days after delivery; work begins on sign-off or day 7, whichever comes first." |

## Next

- `delivery-kickoff` (pro/delivery-ops) — run the project kickoff meeting after scope is signed.
- Review `pro/ba/ba-core/requirements-validation` methodology to verify that each `must` story maps to a measurable acceptance criterion before design starts.
- For complex integrations surfaced in the risk register, run a `pro/ba/ba-core/elicitation-techniques` deep-dive session before writing technical specs.

## References

- [knowledge/pro/ba/ba-core/elicitation-techniques](../../../knowledge/pro/ba/ba-core/elicitation-techniques) — user story mapping in Block 2 applies structured elicitation: open questions → verbatim capture → actor-goal decomposition into `As a / I want / So that` format.
- [knowledge/pro/ba/ba-core/requirements-prioritization](../../../knowledge/pro/ba/ba-core/requirements-prioritization) — MoSCoW framework used in Block 3; the "budget-halved" forcing question is drawn from the must-count ceiling technique in this methodology.
- [knowledge/pro/pm/project-manager/risk-register](../../../knowledge/pro/pm/project-manager/risk-register) — three-column risk table in Block 4 follows this methodology's Likelihood/Mitigation schema; the two default rows (API change, content delay) are the top-frequency risks from real project post-mortems.
- [knowledge/pro/pm/project-manager/scope-management](../../../knowledge/pro/pm/project-manager/scope-management) — budget/timeline calibration in Block 5 and the explicit Out-of-Scope section apply the scope boundary technique to prevent creep before the project starts.
- [knowledge/pro/ba/ba-core/stakeholder-analysis](../../../knowledge/pro/ba/ba-core/stakeholder-analysis) — Steps 3–4 (identifying primary user persona and budget-authority decision-maker) follow this methodology's stakeholder classification grid.
