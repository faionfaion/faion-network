# PLG Implementation Guide

## Summary

A 5-phase sequential implementation roadmap for operationalizing a PLG model: (1) Foundation — define Aha moment and measure TTV; (2) Free Tier Design — limits, upgrade triggers, self-serve checkout; (3) Activation Optimization — onboarding, templates, TTV under 5 minutes; (4) Monetization — PQL scoring, upgrade prompts, automated playbooks; (5) Expansion — seat/usage triggers, expansion revenue tracking. Run phases in order — each depends on prior instrumentation.

## Why

PLG strategy without an implementation plan produces incomplete funnels: Aha moment defined but not instrumented, upgrade triggers built without PQL scoring, expansion playbooks running before activation is optimized. This guide maps the strategy (plg-basics) and tactics (plg-optimization-tactics) to engineering tickets across 5 sequential phases with concrete playbooks for freemium-to-paid, trial-to-paid, and expansion.

## When To Use

- Operationalizing a PLG model after plg-basics selected one.
- Producing a phased rollout plan that maps to engineering tickets.
- Running freemium-to-paid, trial-to-paid, or expansion playbooks as deterministic Day-N sequences.
- Selecting and justifying the PLG tech stack (analytics, onboarding, billing, PQL scoring).

## When NOT To Use

- High-level PLG model choice — route to `plg-basics`.
- Stage-specific tactic catalog — route to `plg-optimization-tactics`.
- Metric definitions and PQL math — route to `plg-metrics`.
- Pre-PMF teams without an Aha-moment hypothesis — running this checklist before PMF wastes engineering cycles.

## Content

| File | What's inside |
|------|---------------|
| `content/01-phases-and-aha.xml` | Aha moment discovery method, TTV reduction tactics, 5-phase implementation checklist, in-product upgrade trigger types and copy rules. |
| `content/02-playbooks.xml` | Freemium-to-paid, trial-to-paid, and expansion (seat growth) playbooks as Day-N state machines; human approval gates; implementation rules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/day-n-playbook.py` | Python scheduler: generates freemium-to-paid Day-N message queue with approved=False flag for human review before send. |
