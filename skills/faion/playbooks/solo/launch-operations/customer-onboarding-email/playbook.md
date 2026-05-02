---
name: customer-onboarding-email
description: Build a 7-email drip sequence that moves new signups from welcome to activated within the first week.
tier: solo
group: launch-operations
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a live 7-email onboarding sequence configured in Loops, Resend, or Mailchimp that sends Day 0 through Day 7 messages automatically for every new signup — guiding each user from welcome to first value, social proof, power-feature discovery, and a direct feedback ask.

## Prerequisites

- A product with a working signup flow and at least 10 test users.
- An ESP account: [Loops](https://loops.so) (recommended for SaaS), [Resend](https://resend.com) (developer-first transactional), or [Mailchimp](https://mailchimp.com) (content creators / newsletters).
- A verified sending domain (SPF + DKIM records in DNS). Loops and Resend provide guided setup; Mailchimp requires manual DNS entry.
- New-user events firing from your app or a webhook you can trigger on signup.
- A `<product-name>`, `<founder-name>`, and `<product-url>` to replace in subject/body templates below.

## Steps

1. **Connect your signup source to the ESP.**

   - Loops: Add the Loops SDK or call `POST https://app.loops.so/api/v1/contacts/create` with `email`, `firstName`, and any custom properties (plan, source). Enable the "New Contact" trigger for your loop.
   - Resend: Use `resend.emails.send()` from your signup handler. For a sequence, install `resend-sequences` or build a queue (Redis + BullMQ / cron) that schedules delayed sends.
   - Mailchimp: Add contacts to a list via the Mailchimp API or Zapier webhook. Use "Customer Journey" to build the 7-step sequence.

2. **Create the Day 0 welcome email (send immediately on signup).**

   Subject: `Welcome to <product-name> — your first step is here`

   Body excerpt:
   ```
   Hi <first_name>,

   You're in. Here's exactly what to do next:

   → [<CTA: Complete your profile / Connect your first X / Create your first Y>](<product-url>/onboarding)

   Takes 2 minutes. Once done, you'll unlock <specific benefit>.

   — <founder-name>
   P.S. Hit reply if anything looks off.
   ```

   One CTA only. Plain text or minimal HTML. Send from `<founder-name>@<product-domain>`, not `noreply@`.

3. **Create the Day 1 first-value tutorial email (send ~24h after signup).**

   Subject: `The one thing that unlocks <product-name>`

   Body excerpt:
   ```
   Hi <first_name>,

   Most users who get value from <product-name> do one thing first: <specific action>.

   Here's how in 3 steps:
   1. Go to <product-url>/dashboard
   2. Click "<Feature Name>"
   3. <Complete action>

   That's the aha moment. Takes under 5 minutes.

   → [Do it now](<product-url>/dashboard)
   ```

   Keep the tutorial to a single task. Link to a help doc if more context is needed — do not inline it.

4. **Create the Day 3 social proof email.**

   Subject: `How <real-customer-name> used <product-name> to <outcome>`

   Body excerpt:
   ```
   Hi <first_name>,

   <real-customer-name> runs a <niche> and had the same question you might have:
   "<specific doubt or pain point>."

   After using <product-name> for two weeks: <concrete result — numbers preferred>.

   "Quote from the customer." — <real-customer-name>, <title/company>

   → [See how they did it](<product-url>/case-studies/<slug>)
   ```

   Use a real customer name and real outcome. If no case study exists yet, use a usage stat (`"137 teams use this workflow"`).

5. **Create the Day 5 power-feature email.**

   Subject: `Most people miss this in <product-name>`

   Body excerpt:
   ```
   Hi <first_name>,

   There's a feature most users discover too late: <Power Feature Name>.

   It lets you <specific outcome> without <common manual workaround>.

   Quick demo: <product-url>/demo/<feature-slug>

   → [Try <Power Feature Name>](<product-url>/feature/<feature-slug>)
   ```

   Choose a feature that separates retained users from churned ones in your analytics.

6. **Create the Day 7 feedback ask email.**

   Subject: `One question for you, <first_name>`

   Body excerpt:
   ```
   Hi <first_name>,

   You've had <product-name> for a week. I have one question:

   What's the one thing that's still unclear or frustrating?

   Hit reply — I read every response personally.

   — <founder-name>
   ```

   No CTA link. Pure reply-based response. Segment anyone who replies into a "high-intent" list for follow-up.

7. **Configure delays and set exit conditions.**

   - Loops: Set delays between emails in the loop editor. Add exit condition: "User completed onboarding" (custom property `onboarded: true`). This stops the sequence for already-activated users.
   - Resend / queue: Schedule jobs at `+1d`, `+3d`, `+5d`, `+7d` from signup timestamp. Cancel remaining jobs when your app fires the activation event.
   - Mailchimp: In Customer Journey, set "Time delay" steps and add a "Goal" step (tag `activated`) that exits users who complete onboarding.

8. **Verify deliverability before going live.**

   Send all 7 emails to a test address at [mail-tester.com](https://www.mail-tester.com). Score must be ≥8/10. Common failures: missing DKIM, SPF softfail, or `Reply-To` header mismatch. Fix in your ESP's domain settings before enabling the sequence for real users.

## Verify

Send a test signup through your flow and confirm all 7 emails land in the inbox (not spam) by checking mail delivery status in your ESP dashboard. In Loops: go to Metrics → Loop runs and verify the contact is progressing through steps. In Resend: check the Events tab for each `emails.send()` call. In Mailchimp: Customer Journey → View journey activity → confirm step timestamps.

Minimum check: subject lines appear exactly as authored, sender is `<founder-name>@<product-domain>`, and Day 0 email arrives within 60 seconds of signup.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Day 0 email lands in spam | Sending domain not verified (missing DKIM) | Add DKIM TXT record from your ESP's domain settings; re-check at [mail-tester.com](https://www.mail-tester.com) |
| Sequence stops after Day 1 with no errors | Exit condition triggered too early (activation event fires on any login, not on completing onboarding) | Narrow the activation event to the real aha-moment action (e.g., "project created", not "signed in") |
| Reply-to goes to `noreply@` and founder never sees responses | ESP defaults to the sending address for Reply-To | Set `Reply-To: <founder-name>@<product-domain>` explicitly in each email template |
| Open rates below 20% by Day 3 | Subject lines are generic or preview text missing | A/B test subject lines in Loops/Mailchimp; add preview text (first 90 chars after greeting) |
| Loops contact not entering the loop | Contact created without the trigger property | Confirm the loop trigger field (e.g., `userGroup: "onboarding"`) is sent in the API call at signup |

## Next

- `stripe-integration-basics` — add a Day 7 upgrade CTA once the feedback ask confirms intent, wired to a Stripe checkout link.
- `churn-intervention` — build a follow-up sequence for users who never completed Day 1's CTA; triggers at Day 14 inactivity.
- Review the `growth-onboarding-emails` methodology for behavioral-trigger upgrades once your ESP supports event-based branching.

## References

- [knowledge/solo/marketing/content-marketer/growth-onboarding-emails](../../../knowledge/solo/marketing/content-marketer/growth-onboarding-emails) — behavioral-trigger pattern behind Day 1 and Day 5 emails: one CTA per email, fires on action/inaction, escalation ladder for stuck users; directly informs Steps 3, 5, and 7 exit conditions.
- [knowledge/solo/marketing/content-marketer/growth-email-marketing](../../../knowledge/solo/marketing/content-marketer/growth-email-marketing) — welcome sequence structure, 80/20 value-to-pitch ratio, and deliverability rules (SPF/DKIM, <0.1% complaint threshold) that underpin Step 2 and Step 8 of this playbook.
