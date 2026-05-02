---
name: weekly-status-report
description: Write and send a 6-section Friday status email that keeps clients informed, prevents escalation calls, and documents project health for week 4 of a 12-week engagement.
tier: pro
group: client-engagement
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a repeatable Friday ritual: a 6-section status email sent by 5 pm that covers TL;DR, done this week, doing next week, blockers/risks, decisions needed, and budget/timeline status — so clients stay informed without calling you, and you have a written paper trail of every week's progress and decisions.

## Prerequisites

- A signed SOW or contract with a delivery schedule (week number, milestones, budget line items).
- Access to your project's task tracker (GitHub Projects, Linear, Jira, or equivalent) to pull "done" items.
- Client primary contact email and the CC list established at kickoff (sponsor + any stakeholders who want visibility).
- A sent-mail folder or shared drive folder named `status-reports/` to archive each report for reference.
- The project budget figure and hours-to-date (from your time tracker: Toggl, Harvest, or a spreadsheet).

## Steps

1. **Open your task tracker on Friday at 4:30 pm and filter closed items for the current week.** Pull every ticket moved to "Done" or "Closed" between Monday 00:00 and Friday 17:00. Copy the ticket titles and IDs. This takes 5 minutes and gives you the raw material for sections 2 and 3.

2. **Write the TL;DR section — 2 lines maximum.** State the project health (Green / Amber / Red) and one sentence on the week's headline result and next milestone.

   ```
   Health: Green
   Week 4/12 complete — hero section, navigation, and CMS schema are live in staging.
   Next milestone: content migration review with client (Tue 6 May).
   ```

   Green = on track. Amber = at risk, mitigable. Red = blocked or over budget — if Red, call first, then send the email.

3. **Write "Done this week" as a bullet list, grouped by area.** Use task tracker ticket titles verbatim or lightly edited. Include the ticket ID in brackets so the client can cross-reference if needed.

   ```
   Design
   - Hero section responsive layout (MKT-41)
   - Navigation mega-menu collapsed states (MKT-44)

   Backend / CMS
   - Contentful content model: 8 content types defined (MKT-47)
   - Staging deploy pipeline via GitHub Actions (MKT-49)

   Client actions completed
   - Brand asset pack received and organised in /brand-assets/
   ```

4. **Write "Doing next week" as a numbered priority list.** List 3–5 items in order of priority. This primes the client for the next check-in and pre-empts "where are things?" emails.

   ```
   1. Content migration: import 12 hero/feature pages from old site into Contentful (MKT-52)
   2. Forms integration: contact + quote request forms wired to HubSpot (MKT-53)
   3. Performance audit: Lighthouse scores baseline on staging (MKT-55)
   4. Client review: walkthrough of staging environment (async Loom or live call per client preference)
   ```

5. **Write "Blockers / Risks".** If none, write "None this week." If present, use a 3-column format: item, impact, action needed by whom.

   ```
   | Item | Impact | Action |
   |------|--------|--------|
   | Final copy for Services page not received | Blocks MKT-52; may push content migration to Week 6 | Client team to send copy by Mon 5 May 17:00 |
   | HubSpot API key not yet provisioned | Blocks MKT-53 | Client to create a Private App key in HubSpot portal and share via 1Password (see SOW §4.3) |
   ```

6. **Write "Decisions needed".** List items that require client input before next Friday. Assign each a deadline. This replaces ad-hoc email threads with a structured queue.

   ```
   1. Approve or reject staging homepage layout by Wed 7 May → required before mobile QA begins
   2. Confirm preferred analytics platform (GA4 vs. Plausible) by Fri 9 May → affects sprint 5 scope
   ```

   If no decisions are outstanding, write "None — you're all set until next Friday."

7. **Write "Budget / Timeline status".** Include three numbers: budget spent to date, budget remaining, and weeks elapsed vs. total. Add one sentence of commentary if the project is drifting.

   ```
   Budget: $12,400 of $28,000 spent (44%) — tracking slightly ahead of midpoint spend for Week 4.
   Timeline: Week 4 of 12 — on track for 15 May content-freeze milestone.
   ```

   If spend exceeds 50% before the midpoint, flag Amber and note which scope areas drove the overage.

8. **Assemble the email.** Use the template below, paste your six sections, and send at 5 pm Friday from your project-management email address (not personal). CC the stakeholders established at kickoff. Subject line includes project name and week number.

   ```
   Subject: [Rebuild Marketing Site] Week 4/12 Status — Green

   Hi Sarah,

   Here is the Week 4 update.

   ── TL;DR ──────────────────────────────────────────────
   Health: Green
   Week 4/12 complete — hero section, navigation, and CMS schema are live in staging.
   Next milestone: content migration review with client (Tue 6 May).

   ── Done this week ─────────────────────────────────────
   Design
   - Hero section responsive layout (MKT-41)
   - Navigation mega-menu collapsed states (MKT-44)

   Backend / CMS
   - Contentful content model: 8 content types defined (MKT-47)
   - Staging deploy pipeline via GitHub Actions (MKT-49)

   Client actions completed
   - Brand asset pack received and organised in /brand-assets/

   ── Doing next week ────────────────────────────────────
   1. Content migration: import 12 hero/feature pages (MKT-52)
   2. Forms integration: HubSpot wired to contact + quote forms (MKT-53)
   3. Performance audit: Lighthouse baseline on staging (MKT-55)
   4. Client review: staging walkthrough (async Loom or live)

   ── Blockers / Risks ───────────────────────────────────
   | Item | Impact | Action |
   |------|--------|--------|
   | Final Services copy missing | Blocks MKT-52 | Client to send by Mon 5 May 17:00 |
   | HubSpot API key not provisioned | Blocks MKT-53 | Client to create Private App key (SOW §4.3) |

   ── Decisions needed ───────────────────────────────────
   1. Approve staging homepage layout by Wed 7 May
   2. Confirm analytics platform (GA4 vs. Plausible) by Fri 9 May

   ── Budget / Timeline ──────────────────────────────────
   Budget: $12,400 of $28,000 spent (44%) — on track.
   Timeline: Week 4 of 12 — on track for 15 May content-freeze milestone.

   Let me know if you have questions. Next update: Friday 9 May.

   Ruslan
   ```

9. **Archive the sent email.** Save a copy to `status-reports/week-04.md` (or export as PDF) in the project shared drive. When disputes arise, the archived reports are your first line of evidence for what was communicated, when, and what client responses were received.

## Verify

Check that the ritual is working after 3 consecutive weeks:

- Open your `status-reports/` folder and confirm `week-02.md`, `week-03.md`, `week-04.md` exist with sent timestamps.
- Search your email sent folder for the project name: `subject:"Rebuild Marketing Site" after:2026-04-01` — confirm 3–4 results, all sent between 16:00 and 18:00 on Fridays.
- Review the "Decisions needed" column in your task tracker. Every decision raised in a status report should have either a client reply or a follow-up entry in the next week's report. Zero open decisions older than 2 weeks with no response = the ritual is working.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Client replies with new requirements inside the status email thread | Status email doubles as a request channel | Add a footer: "This report is for visibility only. For new requests, please raise a ticket at [project-board-url] or reply to the project Slack channel." Route the request to your change-control process (see `scope-creep-management`). |
| Client stops reading the email after Week 3 | Report is too long or too technical | Cut "Done this week" to 5 bullets max. Lead with business outcomes, not ticket IDs. Replace "Contentful content model defined" with "CMS ready: your team can start entering copy on Monday." |
| Sponsor escalates mid-week despite getting the report | TL;DR health status is too vague | Make health status explicit and honest. If a risk is real, name it in the TL;DR — do not bury it in the blockers section. Surprises cause escalation; a pre-named Amber risk rarely does. |
| Budget column shows >55% spend at Week 4 of 12 | Scope or estimation drift | Raise Amber immediately. Break out the budget by area in that week's report. Open a scope conversation: "We have used 55% of budget at 33% of timeline. I'd like 30 minutes this week to review scope against remaining budget." Do not wait for Week 8. |
| You miss a Friday send | Calendar conflict or travel | Send Saturday morning with subject `[Late] Week N/12 Status`. Acknowledge the delay in one sentence. Do not skip entirely — a missing report triggers more anxiety than a late one. |

## Next

- Set up `scope-creep-management` to handle the requests that arrive inside status email threads.
- When the project enters its final 3 weeks, switch to a bi-weekly cadence and add a "Remaining work vs. time" burn-down paragraph referencing `pro/pm/project-manager/` earned-value-management methodology.
- For clients who want more structure, author a project dashboard in Linear or Notion and link it from the TL;DR line — clients can self-serve between Fridays.

## References

- [knowledge/pro/pm/project-manager/communications-management](../../../knowledge/pro/pm/project-manager/communications-management) — the Communications Management Plan pattern that defines audience, cadence, and format fields; the 6-section email structure in this playbook maps directly onto the plan's required output artifacts.
- [knowledge/pro/pm/project-manager/stakeholder-engagement](../../../knowledge/pro/pm/project-manager/stakeholder-engagement) — the stakeholder information-need matrix and engagement level tracking model that backs the health-status (Green/Amber/Red) system and the "Decisions needed" section in Steps 2 and 6.
- [knowledge/solo/comms/communicator/stakeholder-communication](../../../knowledge/solo/comms/communicator/stakeholder-communication) — the plain-language framing rules and audience-aware editing principles applied in Step 3's outcome-first bullet rewrites and in the "client stops reading" troubleshooting entry.
