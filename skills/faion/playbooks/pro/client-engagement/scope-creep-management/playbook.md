---
name: scope-creep-management
description: Detect out-of-SOW requests, document them via change-request form, and charge via contract amendment or refuse with a professional no.
tier: pro
group: client-engagement
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a repeatable scope-control system: a signed SOW as the detection baseline, a change-request (CR) form that captures impact and cost, a tiered approval path (PM → Sponsor → CCB), and a professional refusal script — so every out-of-scope ask either generates an amendment invoice or is declined with a documented reason.

## Prerequisites

- A signed Statement of Work (SOW) or contract with explicit deliverables, exclusions, and acceptance criteria. If none exists, baseline scope first (see `scope-cutting` playbook in `solo/sdd-workflow/`).
- A change register (GitHub Issues, Jira, Notion table, or a CSV in the project repo) where all CRs are tracked.
- Client contacts identified: who submits requests, who signs off on budget changes (the approver is often not the day-to-day contact).
- Project communication channels documented: email thread, Slack workspace, or PM tool where informal asks arrive.
- One billing mechanism in place: either a T&M line item or a contract amendment clause.

## Steps

1. **Establish the detection boundary at kickoff.** In the kickoff call, read the SOW exclusions section aloud. Confirm the client understands that anything not in the signed document goes through change control. Send a follow-up email summarising what is in scope, what is explicitly out of scope, and the CR process. This conversation creates the reference point you cite in every future deflection.

2. **Identify an incoming request as in-scope or out-of-scope.** When a new ask arrives — via email, Slack, a call, or a ticket — compare it against the SOW deliverables table. Signal phrases that indicate out-of-scope:
   - "While you're at it, can you also…"
   - "It should only take a few minutes…"
   - "We just need a small change to…"
   - "The stakeholder mentioned they'd like…" (especially when the stakeholder is not the signatory)
   Any new feature, integration, redesign, or non-trivial revision not listed in the SOW is a scope event regardless of perceived size.

3. **Open a Change Request using the CR form below.** Do this within 24 hours of the ask — delay signals tacit acceptance. Fill every field:

   ```
   ## Change Request — CR-[NNN]

   **Date:** YYYY-MM-DD
   **Requester:** [Name, Role]
   **Project:** [Project name]
   **SOW reference:** [Section / deliverable the request departs from]

   ### Description
   [One paragraph: what the client wants and how it differs from signed scope.]

   ### Impact Analysis
   | Dimension   | Delta                                      |
   |-------------|--------------------------------------------|
   | Scope        | [New deliverable or modification required] |
   | Effort       | [X developer-days]                         |
   | Cost         | [+$X at $Y/day rate]                       |
   | Timeline     | [+X calendar days; revised delivery date]  |
   | Risk         | [Any new dependencies, unknowns, third-party APIs] |

   ### Options
   A. Implement as described — cost and timeline above.
   B. Implement a reduced version — [describe] — cost $X, +Y days.
   C. Defer to Phase 2 — no cost now; added to next SOW.
   D. Decline — rationale: [brief reason].

   ### Decision (client to complete)
   [ ] Option selected: ___
   [ ] Authorised by (name + signature): ___
   [ ] Date authorised: ___
   ```

4. **Route the CR to the correct decision tier.** Send the completed CR to the client within 24 hours and explain which option you recommend. Do not start any work until written authorisation is received — a "sounds good" in Slack is not authorisation.
   - Minor (≤1 day, ≤$500): PM approves; confirm by email.
   - Medium (1–5 days, ≤$5,000): client sponsor approves; send CR PDF via DocuSign or email with explicit reply sign-off.
   - Major (>5 days or >$5,000): formal contract amendment required before work starts.

5. **Draft and attach a contract amendment for approved medium and major CRs.** Use your standard amendment template:

   ```
   Amendment No. [N] to SOW dated [original date]

   Project: [Name]
   Parties: [Your company] and [Client company]

   This Amendment adds the following to the SOW:

   1. New deliverable: [description]
   2. Additional effort: [X days at $Y/day = $Z]
   3. Revised delivery date: [date]
   4. Payment terms: [50% on approval, 50% on delivery / net-30 invoice]

   All other terms of the original SOW remain in effect.

   Signatures:
   [Your name, date]          [Client name, date]
   ```

   Do not begin implementation until both signatures (or email confirmations from an authorised representative) are on file.

6. **Log the CR outcome in the change register.** Record the CR id, description, option chosen, authorised by, date, and billing reference. Update CR status to one of: `Submitted`, `Under Review`, `Approved`, `Rejected`, `Deferred`, `Implemented`. Keep rejected CRs permanently — they are evidence if the same request resurfaces under a different title.

7. **Close the loop on implemented CRs.** Once the work is delivered and accepted, mark the CR `Implemented`, update the SOW deliverables table (or attach the amendment), and issue the invoice. Reference the CR id on the invoice line item: `Development per CR-007 — [description] — $X`.

## Verify

After the first CR cycle, confirm the system is working:

```bash
# If your register is a CSV in the project repo:
grep -c "Approved\|Rejected\|Deferred" project-docs/change-register.csv
# Should return ≥1 — every past request has a status, not just "open"

grep -c "Implemented" project-docs/change-register.csv
# Cross-check: every Implemented CR should have an invoice number in column 8
```

For a Jira or GitHub Issues register, verify:
- Every CR issue has a label from: `cr/approved`, `cr/rejected`, `cr/deferred`, `cr/implemented`.
- Every `cr/approved` issue has a linked invoice or amendment reference in its description.
- No CR is older than 5 business days without a decision status (i.e., no one is sitting on a pending request).

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| **Free-feature creep**: client says "this is just a bug fix" but it requires new development | Scope-by-stealth framing — fixing a behaviour that was never scoped as a requirement is new work, not a defect | Open a CR immediately. Reply: "The SOW specifies [X]. The requested behaviour [Y] was not part of the agreed deliverable. I'm raising a CR so we can price it correctly." |
| **"While you're at it" requests**: small asks arrive verbally or in passing, accumulate silently | The client (and sometimes the team) assumes small items are absorbed | Enforce the 24-hour CR rule regardless of size. A 2-hour task at $150/hr is still a CR. Pattern of small asks = budget erosion. Log each one; after 3 minor approved CRs, review whether a retainer is more appropriate. |
| **Scope-by-stealth from the client team**: junior stakeholders, developers on the client side, or non-signatory managers add requirements directly to the backlog or Slack channel | The approver is not the person submitting requests; team members assume their asks are pre-approved | At kickoff, communicate clearly: only named authorised approvers can approve scope changes. When a non-authorised person submits an ask, acknowledge receipt, route it via CR, and cc the approver. Do not act on it until the approver signs off. |
| **Client refuses to sign amendment**: "just start and we'll sort the paperwork later" | Client is used to informal agencies that absorb scope; or genuine urgency | Hold the line: "I'm ready to start as soon as the amendment is countersigned — I can turn it around same-day." If the client continues pressing, escalate to your own management. Starting without written authorisation removes your ability to invoice for the work. |

## Next

- Review `change-control` methodology under `pro/pm/project-manager/` to set up tiered CR routing for larger engagements with a CCB.
- If scope requests are recurring from the same project, open a retainer conversation: `client-retainer-setup` (when authored) under `pro/client-engagement/`.
- Use `scope-management` methodology under `pro/pm/project-manager/` to write explicit exclusion sections into future SOWs — prevention reduces the CR volume.

## References

- [knowledge/pro/pm/project-manager/change-control](../../../knowledge/pro/pm/project-manager/change-control) — provides the tiered decision authority model (PM/Sponsor/CCB) and CR register status values used directly in Steps 4 and 6 of this playbook.
- [knowledge/pro/pm/project-manager/scope-management](../../../knowledge/pro/pm/project-manager/scope-management) — the "write exclusions before inclusions" rule and the MoSCoW traceability approach underpin Step 1's SOW baseline and the detection logic in Step 2.
