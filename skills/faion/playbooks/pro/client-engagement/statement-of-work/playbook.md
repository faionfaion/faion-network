---
name: statement-of-work
description: Draft, redline, and countersign a Statement of Work covering scope, deliverables, milestones, payment terms, IP ownership, change-request process, acceptance criteria, and termination — for a fixed-price client engagement.
tier: pro
group: client-engagement
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a countersigned Statement of Work for a fixed-price client engagement — including scope boundaries, a milestone payment schedule, IP assignment language, a formal change-request process, acceptance criteria, and a termination clause — ready to reference throughout delivery. The worked example is a $40,000 marketing-site rebuild for Acme Corp.

## Prerequisites

- A signed or verbal agreement on the engagement concept (you have had the discovery call).
- Scope defined at headline level: what you will build, what you will not build, who does what.
- Rate and payment split agreed verbally ($40k total; 30/40/30 or 50/50 both common for web builds).
- A contract template tool or Google Docs / Notion with version history enabled. Recommended: [Bonsai](https://www.hellobonsai.com) (auto-version, e-sign) or [Docusign](https://www.docusign.com) with a Google Docs draft.
- Familiarity with the scope-management methodology: what constitutes a deliverable vs. a feature request.
- Prior playbook recommended: `client-email-templates` (solo/comms-stakeholder) — you will use those templates to send the SOW and follow up on redlines.

## Steps

### 1. Open the SOW template and populate the header block

Create a new document titled `SOW-Acme-MarketingSiteRebuild-v1.0.docx`. Fill in the header table:

```
Statement of Work
Client:          Acme Corp (ABN / registered address)
Contractor:      Your Studio LLC (registered address)
Effective Date:  2026-06-01
SOW Reference:   ACME-2026-001
```

Never use a generic filename like `contract.docx` — version numbers and client identifiers make redline tracking unambiguous.

### 2. Write the Scope of Work section

List deliverables as numbered outputs, not activities. Each line starts with a noun.

```
Deliverables
1. Marketing website — 8 pages (Home, About, Services, Case Studies ×3, Contact, Blog index)
   built in Gatsby 5 + Tailwind CSS, deployed to Netlify, domain: acme.com.
2. Design system — shared Figma file with colour tokens, typography scale, and component library
   (20 components minimum) handed off at milestone 2.
3. CMS integration — Contentful space configured; Acme marketing team able to publish blog
   posts and update case studies without developer access.
4. Performance baseline — Lighthouse score ≥90 for Performance, Accessibility, SEO on all pages.

Out of scope:
- Copywriting or translation of any page content.
- Custom e-commerce or payment flows.
- Server-side rendering, SSR, or API back-end beyond Contentful webhooks.
- Ongoing maintenance after 30-day warranty period.
```

The out-of-scope list is the most important part — it pre-empts the most common scope disputes.

### 3. Write the Timeline and Milestones section

Tie milestones to deliverables and payment triggers, not to calendar dates alone.

```
Milestone 1 — Design system approved (Figma sign-off by Acme)
  Target: 2026-06-20
  Payment trigger: Invoice #1 — $12,000 (30%)

Milestone 2 — Staging site live with all 8 pages (URL: staging.acme.com)
  Target: 2026-07-18
  Payment trigger: Invoice #2 — $16,000 (40%)

Milestone 3 — Production launch + 30-day warranty end
  Target: 2026-09-01 (launch 2026-08-01 + 30 days)
  Payment trigger: Invoice #3 — $12,000 (30%)
```

Add an explicit dependency note: "Milestone dates assume Acme provides all copy and brand assets by 2026-06-10. Delays in asset delivery push milestone dates proportionally."

### 4. Write the Payment Terms section

```
Payment Terms
- All invoices due net-15 from invoice date.
- Late payments accrue interest at 1.5% per month after the due date.
- Work pauses automatically if an invoice is more than 10 days overdue; timeline adjusts accordingly.
- Payments via bank transfer (IBAN: <your IBAN>) or Stripe invoice link.
- Currency: USD. Tax treatment: Contractor is responsible for own tax obligations.
```

Never omit the work-pause clause — it is the primary lever for non-payment situations and courts treat it as standard contractor language.

### 5. Write the IP Ownership section

Choose one of two models and state it explicitly. For a client-paid custom build, use full assignment:

```
Intellectual Property
Upon receipt of final payment (Invoice #3), Contractor assigns to Client all right, title,
and interest in the deliverables listed in Section 2, including source code, design files,
and documentation. Contractor retains the right to display the work in their portfolio.

Third-party libraries and Contentful are licensed under their respective terms; Contractor
makes no warranty of perpetual availability of third-party services.
```

If you use a component library you also sell to others, carve it out: "Contractor retains ownership of the base Gatsby+Tailwind component library; Client receives a non-exclusive perpetual licence to use it in connection with acme.com."

### 6. Write the Change Request Process section

```
Change Requests
Any work not described in Section 2 (Scope) requires a written Change Request (CR).

CR process:
1. Client submits CR via email to studio@yourstudio.dev with description of requested change.
2. Contractor responds within 3 business days with scope impact, cost, and timeline adjustment.
3. Client approves CR in writing ("approved" reply to the CR thread).
4. No CR work begins until written approval is received.

CRs priced at $150/hr. CRs accepted during active milestones; CRs arriving after Milestone 2
sign-off that affect already-approved pages are treated as new mini-engagements.
```

### 7. Write the Acceptance Criteria section

Acceptance criteria convert "done" from subjective to measurable:

```
Acceptance Criteria
Milestone 1 (Design system): Acme signs off the Figma file via Loom video walkthrough
  or written confirmation within 5 business days of delivery. Silence beyond 5 days
  constitutes acceptance.

Milestone 2 (Staging): All 8 pages live at staging.acme.com; Lighthouse ≥90 on all pages;
  no blocker-level bugs in the shared Jira board. Acme has 7 business days to raise
  blockers. Non-blocker feedback is addressed in Milestone 3.

Milestone 3 (Launch): Production site live at acme.com; DNS propagation confirmed;
  Contentful access transferred; all Milestone 2 blockers resolved. 30-day warranty covers
  bugs reproducible on Chrome 124+, Firefox 125+, Safari 17+.
```

The "silence = acceptance" clause on Milestone 1 prevents the design phase from stalling indefinitely.

### 8. Write the Termination Clause

```
Termination
Either party may terminate this SOW with 14 days written notice.

Termination by Client:
- Invoices for all completed milestones become immediately due.
- Work-in-progress is invoiced at $150/hr for hours logged in the current milestone.
- Deliverables completed to date are transferred upon receipt of all outstanding payments.

Termination by Contractor (material breach, e.g. non-payment > 30 days):
- All work pauses immediately.
- Client owes payment for all completed milestones and WIP hours.
- Contractor retains all IP until payment is received.
```

### 9. Send for review — the review-call ritual

Send the draft SOW to the client contact with the following ritual:

1. Send via email using the Subject: `SOW draft for review — Acme Marketing Site Rebuild (ACME-2026-001)`. Attach as PDF (not editable) for the first send; offer a Google Docs link for redlining.
2. Propose a 30-minute "SOW walkthrough call" within 48 hours. Agenda: walk sections 2, 3, and 4 aloud — those are the only three sections clients ever redline substantively.
3. On the call, screen-share the doc and read the out-of-scope list together. This surfaces misaligned expectations before they become disputes.
4. Give the client a 5-business-day redline window. After 5 days without response, send a single follow-up: "Just checking — did the SOW land OK? Happy to answer any questions before you redline."

### 10. Process redlines and reach countersignature

When redlines come back (Google Docs suggestions or email markup):

1. Accept or reject each suggestion in the doc with a one-line comment explaining your decision.
2. Accept cosmetic changes (formatting, word order) without negotiation.
3. Push back in writing on: payment-term extensions beyond net-30, IP carve-outs that leave you uncompensated, removal of the work-pause clause, or acceptance-criteria language that makes "done" entirely subjective.
4. Issue a v1.1 (or v1.2 etc.) with all accepted changes incorporated. Name the file `SOW-Acme-MarketingSiteRebuild-v1.1.docx`.
5. Once both parties are satisfied, send for e-signature via Bonsai or Docusign. Both parties sign; contractor countersigns last.
6. File the countersigned PDF as `SOW-Acme-MarketingSiteRebuild-SIGNED-2026-05-28.pdf` in your contracts folder (Google Drive `Clients/Acme/Contracts/` or local encrypted vault).

## Verify

Confirm all of the following before closing this playbook:

- `grep -i "out of scope" SOW-Acme-*.pdf` returns a result (out-of-scope list present).
- PDF contains at least 3 milestone rows with explicit payment amounts that sum to $40,000.
- Both parties' signatures and signature dates appear on the final page.
- The countersigned PDF is stored in a location accessible to both you and the client (shared Drive folder or Docusign envelope).
- Send yourself a calendar event titled "SOW ACME-2026-001: Invoice #1 due" set to Milestone 1 target date + 15 days.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Client asks to remove the work-pause clause | Client has had contractors hold work hostage in the past | Reframe: "This clause protects both of us — it means I document exactly what is complete so you get compensated work even if we part ways. I cannot remove it, but I can extend the overdue window from 10 to 14 days." |
| Client wants net-45 or net-60 payment terms | Large company AP process or cash-flow hedge | Accept net-30 as maximum. Counter with: "I can do net-30 for Milestones 1 and 2; Milestone 3 can be net-45 since it is post-launch." Never accept net-60 on a first engagement. |
| Client wants to own the base component library you reuse across clients | Miscommunication about what "IP assignment" covers | Add the carve-out in Step 5: assign rights to the custom deliverables only, license the shared library. Most clients accept this once the distinction is explained. |
| Redlines arrive after the 5-day window with major changes | Client was slow to involve their legal team | Accept the redlines anyway on a first engagement (relationship > process). For repeat clients, enforce the window: "This pushes the effective date and all milestone targets by the number of days past the window." |
| Milestone acceptance stalls — client does not respond to Milestone 1 sign-off request | Stakeholder is busy or approval process is unclear | Invoke the silence-equals-acceptance clause: "Per Section 5, the design system is accepted as of [date 5 days from delivery email]. I am proceeding to Milestone 2. Please let me know if you have any blockers." |
| Client tries to add CRs verbally on the kickoff call | Enthusiasm, scope-creep reflex | "That is a great idea — let us capture it as a Change Request so it does not get lost. I will send you the CR form after this call." Never say "sure, I can squeeze that in." |

## Next

- `procurement-management` methodology under `pro/pm/project-manager/` — apply when this SOW is one of several vendor contracts on a larger programme and you need a vendor-tracking register.
- `change-control` methodology under `pro/pm/project-manager/` — operationalise the CR process from Step 6 using a formal change-control log once the engagement is live.
- `scope-management` methodology under `pro/pm/project-manager/` — use scope decomposition techniques to break the deliverables in Section 2 into a WBS for sprint planning.

## References

- [knowledge/pro/pm/project-manager/scope-management](../../../knowledge/pro/pm/project-manager/scope-management) — scope decomposition and out-of-scope definition patterns directly back Step 2's deliverable-vs-activity framing and the out-of-scope bullet list.
- [knowledge/pro/pm/project-manager/procurement-management](../../../knowledge/pro/pm/project-manager/procurement-management) — vendor contract structure (SOW sections, payment milestones, acceptance criteria) maps directly to Sections 3–5 of this playbook.
- [knowledge/pro/pm/project-manager/change-control](../../../knowledge/pro/pm/project-manager/change-control) — the formal CR workflow in Step 6 is the project-manager change-control board adapted to a two-person contractor-client relationship.
- [knowledge/solo/comms/communicator/negotiation](../../../knowledge/solo/comms/communicator/negotiation) — redline negotiation tactics in Step 10 (accept cosmetic, push back on payment and IP) apply the interest-based negotiation framework from this methodology.
- [knowledge/solo/comms/communicator/stakeholder-communication](../../../knowledge/solo/comms/communicator/stakeholder-communication) — the review-call ritual in Step 9 uses the Validation dialogue mode to surface misaligned expectations before the SOW is countersigned.
