# Churn Prevention

## Summary

Churn prevention is an operational playbook for reducing involuntary and voluntary cancellations through three phases: early intervention (re-engagement before the user decides to leave), save offers (at the cancellation flow), and win-back campaigns (after churn). Each phase uses tiered actions matched to churn-reason segment, not a generic discount. Agent role: score health, draft segmented copy, stage campaigns — humans approve send.

## Why

Unchecked churn compounds: a 7% monthly churn destroys ~57% of ARR per year. Intervention ROI is highest before the cancellation decision is made; save offers and win-backs are progressively more expensive. Reason-matched playbooks outperform generic discounts and avoid training customers to threaten cancellation for extraction.

## When To Use

- Monthly churn is at or above 3% on a paid SaaS or subscription product.
- Churn analysis (ops-churn-basics) is done: root causes segmented by reason (price / value / feature gap / involuntary).
- Engagement events (login, feature use) and payment events are tracked and accessible.
- A lifecycle email tool (Customer.io, Intercom, Braze) is owned and writable.
- Cancellation flow is in your product (you can ship a save-offer page, dunning UI).

## When NOT To Use

- B2C apps with no recurring revenue and no contact channel — there is nobody to save.
- Pre-product-market-fit: churn is a symptom of weak value, not weak retention ops.
- Enterprise contracts with manual renewal — handled by AE/CS humans, not this playbook.
- Free tier with zero LTV — saving free users wastes intervention budget.

## Content

| File | What's inside |
|------|---------------|
| `content/01-intervention-playbook.xml` | Signal-to-action table, re-engagement email structure, save offer at cancellation |
| `content/02-win-back.xml` | Win-back timing, email structure, success metrics, anti-patterns |
| `content/03-agent-rules.xml` | Agent workflow rules: draft-only mode, offer constraints, health-score SQL |

## Templates

| File | Purpose |
|------|---------|
| `templates/churn-prevention-playbook.md` | Early-warning triggers, save offers, win-back campaigns table |
| `templates/health-score.sql` | Weekly health-score snapshot SQL (login, feature, support, tenure) |
