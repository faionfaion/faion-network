---
name: stakeholder-elicitation
description: Identify stakeholders via RACI matrix, run structured 30/60min interviews, and synthesize verbatim quotes into a requirements traceability matrix.
tier: pro
group: business-analysis
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a complete stakeholder register with RACI roles, structured interview transcripts with verbatim quotes, and a requirements traceability matrix (RTM) that links each quote to a stated need and a numbered functional requirement — ready to hand off to a developer or feed into a spec document.

## Prerequisites

- A defined project scope statement (even one paragraph is enough to start).
- Access to at least 3 stakeholders from different functions (sponsor, user, ops).
- A note-taking tool that lets you timestamp or tag quotes (Notion, Obsidian, or a plain `.md` file).
- Familiarity with MoSCoW or similar prioritization vocabulary (Must/Should/Could/Won't).
- Prior playbook: none required, but reading `requirements-documentation` methodology helps frame the output.

## Steps

1. **Draft the stakeholder register.** List every person or role that can affect or be affected by the project. For the billing dashboard example: `CFO`, `Accounts Receivable Manager`, `Finance Ops Analyst`, `Engineering Lead`, `Customer Success Rep`, `External Auditor (read-only)`.

2. **Assign RACI codes.** For each stakeholder, mark their role on the core deliverable (dashboard goes live):

   | Stakeholder | Responsible | Accountable | Consulted | Informed |
   |-------------|-------------|-------------|-----------|----------|
   | CFO | | X | X | |
   | AR Manager | X | | X | |
   | Finance Ops Analyst | X | | | |
   | Engineering Lead | X | | X | |
   | Customer Success Rep | | | X | X |
   | External Auditor | | | | X |

   Rule: exactly one `A` per deliverable. If you find two, escalate before scheduling interviews.

3. **Schedule interviews.** Book 30 min for Informed/Consulted stakeholders, 60 min for Responsible/Accountable. Send a one-paragraph brief: "We're building a billing dashboard. I want to understand your current workflow and what success looks like for you." No agenda attachment — it primes answers.

4. **Prepare your question arc.** Open with context-setting, move to pain discovery, close with validation:

   - **Open (first 10 min):** "Walk me through your current billing review process, end to end." / "What breaks most often?"
   - **Discover (middle 15–40 min):** "When you say 'slow', what does that mean in practice — how long does X take today?" / "What would you do with the data if you had it in real time?"
   - **Close (last 5–10 min):** "If you could only have three things from this dashboard, what would they be?" / "What would make you say this project failed?"
   - Closed questions for validation only: "Would daily refresh be enough, or do you need sub-hourly?" / "Is CSV export a blocker or a nice-to-have?"

5. **Capture verbatim quotes.** During the interview, paste exact words into a `quotes.md` file with tags:

   ```
   [CFO, 2026-04-10] "I have to pull three separate Excel files every Monday morning
   just to see what invoices are 30-days overdue. It takes two hours and I'm always
   looking at last week's data."
   Tags: #pain #data-freshness #manual-process

   [AR Manager, 2026-04-11] "The biggest risk is when a large customer goes silent —
   we only find out at month-end that they haven't paid invoice #4412."
   Tags: #risk #alerting #large-accounts
   ```

   Do not paraphrase during the session. Paraphrase in Step 7.

6. **Debrief within 24 hours.** After each interview, annotate your quotes with a `Need` field — the underlying job-to-be-done:

   ```
   Quote: "I have to pull three separate Excel files every Monday morning..."
   Need: Finance leadership needs consolidated overdue invoice data refreshed at least daily.
   ```

7. **Build the Requirements Traceability Matrix.** Create a table that connects quote → need → functional requirement (F-REQ):

   | Quote ID | Stakeholder | Verbatim (excerpt) | Need | F-REQ | Priority |
   |----------|-----------|--------------------|------|-------|----------|
   | Q-001 | CFO | "pull three separate Excel files…two hours" | Consolidated overdue invoice view, daily refresh | F-001: Dashboard shall display all invoices overdue by ≥30 days, refreshed every 24h | Must |
   | Q-002 | AR Manager | "only find out at month-end…invoice #4412" | Real-time alert when large-account invoice goes 7 days unpaid | F-002: System shall send email alert when invoice >$10 000 is unpaid for 7 days | Must |
   | Q-003 | CFO | "I need to export this for the board deck" | CSV/PDF export of filtered invoice list | F-003: Dashboard shall support CSV export of any filtered view | Should |
   | Q-004 | Finance Ops | "I need to filter by entity — we have 12 subsidiaries" | Multi-entity filter | F-004: Dashboard shall allow filtering by legal entity | Must |
   | Q-005 | External Auditor | "read-only access, no edits" | Auditor access with zero write permissions | F-005: Auditor role shall have read-only access; no create/update/delete permissions | Must |

   Assign sequential `F-REQ` IDs. A single quote may produce more than one F-REQ; a single F-REQ may be supported by multiple quotes — add both Quote IDs in that row.

8. **Validate the RTM with stakeholders.** Send each stakeholder only their rows plus any rows where they're Consulted. Ask: "Does F-001 capture what you described?" One async round of comments (Notion comment or email reply) is enough; do not schedule a second interview for validation unless a major gap surfaces.

9. **Freeze the baseline.** Once stakeholders have signed off (email "LGTM" counts), timestamp the RTM version in the filename: `rtm-billing-dashboard-v1.0-2026-04-18.md`. This is your change-control baseline.

## Verify

Open the RTM and run this checklist:

```
grep -c "^| Q-" rtm-billing-dashboard-v1.0-2026-04-18.md
```

The count should equal the number of non-header, non-separator rows. Then confirm:

- Every F-REQ maps to ≥1 Quote ID (no orphan requirements).
- Every Must-priority F-REQ has an Accountable or Responsible stakeholder as its quote source.
- The RACI table has exactly one `A` per deliverable row.
- At least one stakeholder has replied "LGTM" or equivalent in writing.

If any F-REQ has no quote source, it was invented — either find the stakeholder who said it or remove it.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Stakeholder says everything is Must priority | Anchoring to seniority or fear of missing out | Ask: "If budget were cut by 50% tomorrow, which three items survive?" — forces real prioritization |
| Two Accountable owners for the same deliverable | Unclear org governance | Escalate to project sponsor before proceeding; document the ambiguity in a `decisions.md` |
| Quote contradicts a requirement already approved by another stakeholder | Conflicting needs across roles | Log the conflict in RTM as a `CONFLICT` flag; schedule a 15-min three-way call to resolve before freezing baseline |
| Stakeholder goes silent after interview, won't validate | No perceived urgency | Send the specific rows where their name appears, with a 48h reply deadline; default to "approved as written" if no response |
| Verbatim quotes feel thin — stakeholder only gave high-level statements | Interview moved too fast to discovery | Follow up with one async question: "You mentioned X — can you give me a specific recent example?" |
| RTM grows beyond 40 rows for a single sprint scope | Scope creep captured during elicitation | Apply MoSCoW cut: move all Could/Won't rows to a `backlog-rtm.md`; keep only Must/Should in the active RTM |

## Next

- Run `requirements-prioritization` playbook to apply weighted scoring across all Must/Should F-REQs before handing off to engineering.
- Author a `spec.md` using the frozen RTM as input: each F-REQ becomes a `## Functional Requirements` bullet.
- If stakeholder count exceeds 8, consider a focus-group session using the `ba-planning` methodology for workshop facilitation.

## References

- [knowledge/pro/ba/ba-core/stakeholder-analysis](../../../knowledge/pro/ba/ba-core/stakeholder-analysis) — provides the RACI matrix structure and stakeholder register schema used in Steps 1–2; this playbook operationalizes the register into a scheduled interview sequence.
- [knowledge/pro/ba/ba-core/elicitation-techniques](../../../knowledge/pro/ba/ba-core/elicitation-techniques) — covers open-then-closed interview arc, verbatim quote capture protocol, and the 24h debrief discipline applied in Steps 4–6.
- [knowledge/pro/ba/ba-core/requirements-traceability](../../../knowledge/pro/ba/ba-core/requirements-traceability) — defines the Quote → Need → F-REQ traceability chain and change-control baseline pattern applied in Steps 7–9.
