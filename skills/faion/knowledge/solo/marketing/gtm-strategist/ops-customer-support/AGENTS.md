# Customer Support

## Summary

A self-serve-first support hierarchy for solopreneurs: build FAQ and knowledge base before
adding any async channel, define SLA tiers by plan (Free = 24-48h, Paid = 4-24h, Enterprise
= 1-4h), and use weekly ticket pattern reviews to feed product improvements. The rule:
if the same question is asked 5+ times, add it to the FAQ; if the same bug is reported
repeatedly, prioritize the fix.

## Why

70-85% of support volume can be deflected by a well-built FAQ and knowledge base.
Responding to the first ticket from any paying customer within 4 hours — regardless of SLA
tier — reduces churn risk at the critical early-adoption stage. Ticket category patterns
are a direct product signal: if how-to tickets for a specific feature exceed 20% of volume,
that feature needs UX work, not more documentation. Agents must never promise specific
fixes or timelines without human confirmation.

## When To Use

- Setting up the first support system (self-serve docs, email SLAs, templates)
- Drafting or updating a support policy document
- Conducting a weekly support review: pattern extraction, FAQ gap identification
- Mining ticket export for product insight (recurring pain points → roadmap)
- Drafting template responses for the top recurring question types

## When NOT To Use

- Real-time live chat or voice support — requires a human in the loop, not an agent
- Legal or financial issues raised via support — escalate immediately
- Incidents affecting all users (outages, data loss) — use incident response process
- Sensitive topics (account termination, fraud) — human judgment required
- Sending any response that includes a refund, credit, or plan change without human approval

## Content

| File | What's inside |
|------|---------------|
| `content/01-support-hierarchy.xml` | Self-serve → async → live → proactive levels, SLA by tier, escalation path |
| `content/02-processes-and-patterns.xml` | Ticket categorization, resolution tracking metrics, product feedback loop, communication tips |

## Templates

| File | Purpose |
|------|---------|
| `templates/support-policy.md` | Support policy doc: channels, SLA by plan, escalation contacts |
| `templates/weekly-review.md` | Weekly support review: volume, performance, top issues, action items |
| `templates/email-acknowledgment.md` | First-response acknowledgment email template |
| `templates/email-resolution.md` | Resolution email template with step-by-step fix format |
| `templates/ticket-patterns.py` | Count tickets by category from CSV export; output weekly summary |
