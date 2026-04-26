# Customer Success Basics

## Summary

A proactive framework for ensuring customers achieve their goals with your product before they churn. Five stages: Define (one north-star success metric per product), Measure (per-account health score from usage + sentiment + billing), Engage (event-triggered lifecycle touchpoints, not calendar dates), Enable (knowledge base + self-serve resources built before lifecycle emails), Expand (upgrade signals → expansion prompts). Core rule: trigger touchpoints on behavior events, cap automated re-engagements at one per week per account, and never let an agent issue refunds, downgrades, or credits autonomously.

## Why

Reactive support addresses problems after they cause churn. Customer success cuts churn by catching low-usage, low-adoption, and low-sentiment signals before the cancellation decision is made. For SaaS, reducing monthly churn from 5% to 3% doubles LTV. Expansion (net revenue retention above 100%) is only reachable when customers are genuinely successful — expansion motions fail on unsuccessful accounts.

## When To Use

- Defining success metrics for the first time on a SaaS, course, membership, or service product
- Building lifecycle email sequences (Day 1/3/7/14/30) with product-event triggers
- Computing customer health scores and routing at-risk accounts
- Designing self-serve enablement: knowledge base, onboarding guides, video library
- Building expansion playbooks: detect upgrade signals, trigger relevant offers

## When NOT To Use

- Reactive support tickets — use ops-customer-support
- Detailed health-score modeling and CS KPIs — use ops-customer-success-metrics
- Churn-prevention forensics on already-churning customers — different, deeper diagnostic
- Enterprise named-account QBRs — framework covers structure; agents should not drive strategic conversations
- Pre-sales / SDR motion — use gtm-strategy or growth-cold-outreach

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Success definition by product type, touchpoint cadence table, high-touch vs tech-touch model, expansion trigger signals |
| `content/02-playbooks.xml` | Onboarding playbook, at-risk intervention, expansion path template |
| `content/03-agent-rules.xml` | Agent safety rules: re-engagement caps, billing autonomy prohibition, sentiment brittleness, PII handling |

## Templates

| File | Purpose |
|------|---------|
| `templates/health-score.py` | Minimal health score: usage (40), adoption (30), sentiment (20), billing (10) → score + band |
| `templates/cs-playbook.md` | Customer success playbook: onboarding table, ongoing triggers, at-risk intervention |
