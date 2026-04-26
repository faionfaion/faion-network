# Viral Loops and Growth Mechanics

## Summary

Viral loops are self-reinforcing growth cycles where a user action creates an artifact that is shared or exposed, motivating new users to join and repeat the action. The K-factor (K = i * c, invites-per-user times conversion rate) quantifies loop strength. Seven loop types exist: inherent, word-of-mouth, incentivized, social, collaborative, content, and embedded. Select one primary loop type matched to your product before engineering, then instrument it and iterate via viral-optimization.

## Why

Linear growth (spend money → get users, stop → growth stops) caps the business at acquisition budget. A viral loop with K = 0.3 reduces effective CAC by 30% permanently and compounds over time. Even K well below 1 is valuable; K = 1+ is rare and unstable. Cycle time is as important as K: K = 0.4 with a 3-day cycle outcompounds K = 0.7 with a 60-day cycle over a quarter.

## When To Use

- Designing a growth loop for a new product or vertical (strategic design layer).
- Choosing among loop types: which fits product DNA, ICP, and current PMF stage?
- Planning measurement infrastructure (events, K-funnel, cycle-time tracker) before engineering.
- Companion to viral-optimization (the iterating layer) and ops-churn-prevention (retention side).

## When NOT To Use

- Pre-PMF: weak product value → weak inviter motivation → loop fizzles regardless of mechanics.
- Pure sales-led businesses where unit economics already work — adding viral complexity gives marginal lift.
- Regulated categories (finance, health, gambling) where unsolicited referrals violate FTC/MiFID II/HIPAA.
- Products where sharing imposes social cost on the inviter (sensitive niches) — virality is anti-loyalty.

## Content

| File | What's inside |
|------|---------------|
| `content/01-loop-types.xml` | Seven loop types, match-to-product-type guide, loop anatomy (action/artifact/distribution/motivation/friction) |
| `content/02-design-rules.xml` | Loop design rules: single primary loop, cycle time lever, friction reduction, invitee landing page priority |
| `content/03-examples.xml` | Three case studies: Dropbox referral, Spotify Wrapped social loop, Notion templates content loop |

## Templates

| File | Purpose |
|------|---------|
| `templates/loop-anatomy.md` | Loop design template: name, type, action/artifact/distribution/motivation/friction, K-factor targets |
| `templates/referral-program.md` | Referral program design: value proposition, mechanics, sharing options, tracking, fraud rules |
| `templates/loop-projection.py` | Naive compounding model: project user count from K + cycle time over N days |
