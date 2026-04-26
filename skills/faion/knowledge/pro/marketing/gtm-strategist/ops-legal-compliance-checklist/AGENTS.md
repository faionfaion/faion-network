# Legal Compliance Checklist

## Summary

A stage-gated compliance tracker for online businesses: Day 1 (entity, EIN, bank account, core policies), Month 1 (website legal pages, data protection, payment processing, IP), Year 1 (tax compliance, employment/contractor law, marketing law, industry-specific, insurance), and Ongoing (policy update cycle, data management, audits, legal counsel). The checklist verifies presence and process — it does not verify that policy text is accurate or legally sufficient, which requires attorney review.

## Why

Most online-business legal failures come not from ignorance of what is required but from skipping the implementation step. A staged checklist forces the founder to work through obligations systematically by phase, rather than treating compliance as a one-time task. The ongoing cadence (quarterly policy review, regulatory monitoring) prevents the common failure of accurate-at-launch policies that drift from reality over time.

## When To Use

- Pre-launch: confirm all Day 1 items are in place before going live
- Post-launch (Month 1): complete data protection, payment, and IP items
- Quarterly audit: detect drift between policies and actual data flows/vendors
- After adding a new third-party integration (analytics, payments, AI provider)
- Producing compliance status snapshot for investor/acquirer due diligence

## When NOT To Use

- Drafting policy text from scratch — use a generator (Termly, Iubenda) or counsel; this checklist verifies coverage, not wording
- Industry-regulated sectors (HIPAA, FINRA, FERPA, PCI-DSS) — baseline only; need vertical-specific checklists and legal review
- M&A or fundraising legal due diligence — broader scope (cap table, IP chain, employment, contracts)
- Disputes, takedowns, demand letters — adversarial process, not checklist-driven

## Content

| File | What's inside |
|------|---------------|
| `content/01-checklist.xml` | Stage-by-stage compliance items: Day 1, Month 1, Year 1, Ongoing, Website-specific, Policy Update Process |
| `content/02-common-mistakes.xml` | Six high-frequency compliance failures with root causes and fixes |
| `content/03-agent-rules.xml` | Agent safety rules: presence vs accuracy distinction, cookie-banner UX traps, DSAR workflow, prompt patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-footer-legal.py` | Headless audit: checks /privacy, /terms, /cookies, /refund presence and cookie-banner display for EU locales |
| `templates/policy-update-notification.md` | User notification email template for material policy changes |
