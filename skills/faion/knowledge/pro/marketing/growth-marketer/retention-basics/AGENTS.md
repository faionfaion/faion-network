# Retention Basics

## Summary

A retention loop is a self-reinforcing cycle where using the product creates internal reasons to return. The Hook model (Nir Eyal) structures this as four components: Trigger → Action → Variable Reward → Investment. The goal is migrating users from external triggers (push notifications) to internal triggers (habit), because internal triggers do not decay like paid re-engagement.

## Why

Acquiring users without retaining them is filling a leaky bucket. Retention compounds: improving D30 from 10% to 15% directly lifts LTV. The Hook model provides a concrete design checklist that maps each product flow to missing trigger/reward/investment components — giving teams actionable gap analysis rather than vague "engage users" advice.

## When To Use

- Post-acquisition drop-off with no single dominant cause; Hook audit is the correct first step.
- New feature evaluation as a retention driver (does it create a trigger, variable reward, or investment?).
- Onboarding redesign — need explicit framing of which loop type the product depends on.
- Companion to `cohort-basics` (measurement) and `retention-strategies` (tactics) — this is the framing layer.

## When NOT To Use

- Pre-PMF: no habitual user yet; chase value, not loops.
- One-off/transactional products (tax filing, event ticketing) — "retention" means repeat-purchase next cycle, not daily return.
- Enterprise compliance tools where engagement is procurement-driven, not user-driven.
- B2B tools with small DAU but high session value — DAU/MAU misleads; measure feature-completion retention.

## Content

| File | What's inside |
|------|---------------|
| `content/01-hook-model.xml` | Four Hook components, retention loop types, design rules, antipatterns |
| `content/02-checklist.xml` | Measurement, analysis, strategy, and monitoring steps |

## Templates

| File | Purpose |
|------|---------|
| `templates/retention-curves.py` | DAU/MAU ratio + 8-week cohort retention curve from events CSV |
| `templates/hook-loop.txt` | Fill-in-the-blank Hook sentence template per product flow |
