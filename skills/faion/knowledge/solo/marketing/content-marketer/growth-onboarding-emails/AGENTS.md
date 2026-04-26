# Onboarding Email Sequences

## Summary

Behavior-triggered email sequences that guide new users from signup to activation.
Each email has one CTA, fires on a specific user action (or inaction), and routes
stuck users through an escalation ladder. The core rule: behavioral triggers
outperform time-based sequences by 15-40% in activation rate.

## Why

Users who sign up and see no tailored follow-up abandon before reaching the "aha
moment." Behavior-driven sequences intercept users at the exact moment they stall,
deliver contextual nudges, and route high-value users to human outreach — all
without manual effort.

## When To Use

- SaaS or app with free trial / freemium model and measurable activation steps
- Onboarding activation rate below 50% with no behavioral trigger emails in place
- Redesigning an existing time-based sequence to add behavior-triggered branches
- New product launch where the first-week user journey has been mapped
- Product has an identifiable "aha moment" milestone (connect data, create project, invite teammate)

## When NOT To Use

- Product analytics not set up — behavioral triggers require event tracking (Segment,
  Mixpanel); without data, only time-based sequences are possible
- Transactional product with no recurring engagement cycle (one-time purchase, no return)
- User base is extremely homogeneous with a single known path — a 3-email linear
  sequence may outperform complex branching
- No ESP with automation capability — Customer.io, ActiveCampaign, or Intercom
  required; basic Mailchimp is insufficient

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Segment types, trigger taxonomy, 8-email sequence structure, escalation ladder |
| `content/02-writing-rules.xml` | Per-email writing rules, subject line format, CTA constraints, metrics targets |
| `content/03-antipatterns.xml` | Common mistakes and why they fail: multiple CTAs, time-only triggers, frequency overload |

## Templates

| File | Purpose |
|------|---------|
| `templates/email-welcome.txt` | Welcome email — first action, reply-friendly tone |
| `templates/email-nudge.txt` | Stuck-user nudge — blocker removal, Day 2 trigger |
| `templates/email-celebration.txt` | Completion celebration — milestone + next step |
| `templates/email-personal-outreach.txt` | High-value signup — personal call offer, Day 10 |
| `templates/email-trial-end.txt` | Trial ending — activated user conversion push |
| `templates/prompt-sequence-design.txt` | LLM prompt to design full trigger logic table |
| `templates/prompt-email-draft.txt` | LLM prompt to draft one email per trigger event |
