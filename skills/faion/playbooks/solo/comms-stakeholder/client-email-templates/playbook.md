---
name: client-email-templates
description: Send project proposals, weekly status updates, scope-change confirmations, polite refusals, and closure invoices using five ready-to-paste email templates.
tier: solo
group: comms-stakeholder
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have five ready-to-paste email templates covering the full freelance client lifecycle — proposal, weekly status, scope change, polite refusal, and project closure — each with a real subject line and body you can send immediately after filling in `<bracketed>` variables.

## Prerequisites

- An active client relationship or a prospect you are proposing to.
- Your project scope, rate, and timeline defined (even roughly — the templates expose what you still need to finalize).
- A personal email address at your own domain (e.g., `alex@yourstudio.dev`), not a free-tier Gmail. Clients judge professionalism from the sending address.
- Familiarity with the five dialogue modes from the `stakeholder-communication` methodology: you will be using the Validation and Clarification modes in Templates 3 and 4.

## Steps

### 1. Send a project proposal (Template 1)

Use when: you have had an initial call and want to convert interest into a signed agreement.

**Subject:** `Proposal: <Project Name> — scope, price, and timeline`

```
Hi <First Name>,

Thank you for the call on <date>. Here is what I propose.

SCOPE
<2–4 bullet points of deliverables, each starting with a verb>
- Design and build a 5-page Gatsby site with Tailwind CSS
- Integrate Stripe checkout for a single product
- Deploy to Netlify with a custom domain and SSL

OUT OF SCOPE (to avoid surprises)
- Ongoing content updates after handoff
- SEO copywriting
- Third-party API integrations not listed above

PRICE
<Project rate>: €<amount> fixed, or €<hourly rate>/hr estimated at <N> hours.
50% due on signing, 50% on delivery.
Payment via bank transfer or Stripe invoice.

TIMELINE
Kickoff: <date>
First draft: <date, typically 2 weeks out>
Final delivery: <date>
Assumes feedback within 48 hours at each review stage.

NEXT STEP
Reply "yes" and I will send the contract and first invoice within 24 hours.
Or let me know what you would like to adjust.

— <Your Name>
<your-domain.com>
```

Do not embed a PDF. Inline text closes faster. Keep scope bullets to 6 or fewer — more scope means a longer negotiation.

### 2. Send a Friday weekly status (Template 2)

Use when: a project is in active delivery and the client has not asked for updates. Send every Friday at the same time to prevent "where are we?" emails.

**Subject:** `<Project Name> — week of <Mon DD Mon>: status update`

```
Hi <First Name>,

Week <N> update.

DONE THIS WEEK
- <Completed item 1 — link to staging URL or screenshot if relevant>
- <Completed item 2>

IN PROGRESS
- <Current work item> — on track for <target date>

BLOCKERS / NEEDS FROM YOU
- <Specific ask, if any> — needed by <date> to stay on schedule
- (none this week — just keeping you informed)

OVERALL STATUS: on track / at risk / delayed
<One sentence explanation if not "on track">

Next update: Friday <date>.

— <Your Name>
```

Keep it under 150 words. If there are no blockers, say so explicitly ("none this week") — silence reads as avoidance. The staging URL is the most valuable thing you can include.

### 3. Confirm a scope change (Template 3)

Use when: the client asks for something outside the original scope, either verbally or in writing. Send within 2 hours of the request.

**Subject:** `Scope change confirmation: <brief description> — <Project Name>`

```
Hi <First Name>,

Thanks for the note about <new request>.

To confirm my understanding:

YOU ARE ASKING FOR
<One precise sentence describing the new work>

IMPACT
- Additional cost: €<amount> (or: included, no charge)
- Timeline: <adds N days / no change>
- What shifts: <what gets pushed or dropped to fit this in>

To proceed, please reply "confirmed" and I will add this to the project scope and send an updated invoice if applicable.

If I have misunderstood the request, reply with corrections and I will re-confirm.

— <Your Name>
```

Never start new work before receiving "confirmed". The Validation dialogue mode applies here: you are confirming your understanding, not negotiating — keep the tone neutral and factual.

### 4. Decline a request politely (Template 4)

Use when: the client asks you to do work outside your skills, capacity, or willingness, and you want to preserve the relationship.

**Subject:** `Re: <their original subject line>`

```
Hi <First Name>,

Thank you for thinking of me for <request>.

I am not the right fit for this one because <one honest sentence — capacity, skills, or scope>.

What I can do instead:
- <Alternative A: a smaller version of the request you can handle>
- <Alternative B: refer them to someone specific — "I can introduce you to <Name> who specialises in this">
- <Alternative C: push to a later date — "I have capacity from <date> if timing is flexible">

Let me know if any of those work for you.

— <Your Name>
```

Always offer at least one alternative. A plain "no" closes the relationship; an alternative keeps it open. Use the Clarification mode only if you are unsure why they are asking — one question at most before declining.

### 5. Close a project and request payment (Template 5)

Use when: deliverables are handed off and you are ready to close the engagement.

**Subject:** `<Project Name> — project complete + invoice #<NN>`

```
Hi <First Name>,

<Project Name> is complete. Here is a summary of what was delivered:

DELIVERED
- <Deliverable 1 — link>
- <Deliverable 2 — link>
- <Any credentials, repo access, or documentation handed off>

INVOICE
Invoice #<NN> for €<amount> (final 50%) is attached / sent via <Stripe / bank transfer>.
Due: <date, typically net-15>.

WHAT HAPPENS NEXT
<Any handoff notes: how to update content, who to contact for hosting issues, etc.>

It has been a pleasure working on this. If you need anything in the first 30 days, reply here. For new projects, feel free to reach out any time.

— <Your Name>
```

Attach the invoice as a PDF, or include a Stripe payment link inline. Sending the closure email and invoice together reduces the "invoice came out of nowhere" friction.

## Verify

Send Template 1 to yourself at a second email address. Confirm:

- Subject line contains both the project name and the word "Proposal".
- All `<bracketed>` variables are replaced.
- The "NEXT STEP" paragraph has exactly one call to action.
- The email renders correctly in both Gmail and Apple Mail (dark mode and light mode).

If using Superhuman, Spark, or Hey: create a snippet for each template and tag it `client-comms`. Retrieve via `/client` prefix search.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Client does not reply to proposal within 5 days | Subject line too generic or email landed in promotions | Follow up with exactly one reply to the same thread: "Quick check — did my proposal land OK? Happy to jump on a 10-minute call to walk through it." Do not resend the full email. |
| Client replies to scope-change email with "let us discuss" instead of "confirmed" | They want to negotiate the price or timeline, not just confirm | Treat the meeting as a Clarification session: ask "what specifically would you like to adjust — the cost, the timeline, or the scope itself?" and confirm in writing after. |
| Invoice goes unpaid past due date | Client is waiting for a formal reminder or forgot | Send a single-line reply to the closure email thread: "Hi <First Name> — just a note that Invoice #<NN> was due on <date>. Please let me know if there is anything holding up payment." Do not apologise. |
| Client asks to expand scope during status update | Weekly update surfaces new ideas and scope grows informally | Reply immediately with Template 3 (scope-change confirmation) before any new work starts, even if the change seems small. |

## Next

- `difficult-conversations` methodology under `solo/comms/communicator/` — apply when a client disputes the scope-change confirmation or rejects the closure invoice.
- `negotiation` methodology under `solo/comms/communicator/` — use when the proposal negotiation extends beyond two back-and-forth emails.
- Consider the `stakeholder-communication` methodology's Validation protocol for high-stakes proposals: run a Clarification session before writing Template 1 to confirm power/interest level and avoid misaligned scope.

## References

- [knowledge/solo/comms/communicator/stakeholder-communication](../../../knowledge/solo/comms/communicator/stakeholder-communication) — the Validation dialogue mode backs Template 3's "confirm before proceeding" pattern, and the Power/Interest grid informs when to send Template 2 proactively versus reactively.
- [knowledge/solo/comms/communicator/difficult-conversations](../../../knowledge/solo/comms/communicator/difficult-conversations) — the "name the issue neutrally" rule is the basis for Template 4's single-sentence reason and the Troubleshooting entry on unpaid invoices.
