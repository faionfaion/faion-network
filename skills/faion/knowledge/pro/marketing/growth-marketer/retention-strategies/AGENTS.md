# Retention Strategies

## Summary

A catalogue of retention loop patterns (content, social, progress, stored-value, workflow, network-effect) paired with engagement mechanics (streaks, achievements, variable rewards, commitment devices) and a re-engagement campaign playbook. Each loop type includes a flow diagram, key mechanics, and real-product examples.

## Why

Without a deliberate retention loop, users return only when externally reminded. Self-reinforcing loops create internal triggers that reduce dependence on push/email and compound DAU/MAU over time. Matching the right loop type to the product context is essential — content loops fail on workflow tools; gamification fails on B2B multi-stakeholder products.

## When To Use

- D1/D7/D30 retention is below target and PMF is established (paying users exist but don't return).
- Designing a new product surface where loop type can be chosen during architecture.
- Refactoring lifecycle messaging when re-engagement campaigns show decaying open rates.
- Adding gamification (streaks, achievements) to consumer SaaS or learning products.

## When NOT To Use

- Pre-PMF: improving retention on a non-resonating product is rearranging deck chairs; fix activation first.
- B2B enterprise multi-stakeholder products — streaks and gamification feel out of place.
- One-shot transactional products (single-purchase courses, e-commerce) — lifecycle email is more appropriate.
- No stable event-tracking foundation — designing loops on unreliable data produces phantom wins.

## Content

| File | What's inside |
|------|---------------|
| `content/01-retention-loop-patterns.xml` | Six loop patterns with flow diagrams, key mechanics, and product examples. |
| `content/02-engagement-hooks.xml` | Streaks (with Python impl), achievements, variable rewards, commitment devices. |
| `content/03-reengagement-and-examples.xml` | Re-engagement email sequence, push notification strategy, Duolingo/Slack/TikTok/Notion examples, antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cohort-retention.py` | D-N retention by signup week using pandas event dataframe. |
