# Micro-MVPs

## Summary

Micro-MVPs are extremely small, high-signal experiments (hours to days) that validate one specific assumption before committing engineering time. The rule: pre-register the success criterion as a number before launching; if a "micro" MVP takes longer than one week to build, it is not micro.

## Why

Traditional MVPs take weeks or months to build, wasting runway when the core assumption is wrong. Micro-MVPs isolate the riskiest assumption and test it at minimal cost — a landing page tests demand, a Stripe Payment Link tests willingness-to-pay, a Wizard-of-Oz tests workflow fit — each costing hours rather than weeks.

## When To Use

- Validating one specific assumption (demand, willingness-to-pay, workflow fit) before committing engineering time
- Pre-PMF stage where every shipped feature is a learning bet, not a delivery
- Validating a new segment for an existing product (fake-door, smoke-test)
- Solo or 2-person team with limited capacity — micro-MVPs preserve runway
- Founder is "in love with a feature" — a micro-MVP is the cheapest way to disprove the hypothesis

## When NOT To Use

- Post-PMF feature work for an established product where users expect polish — fake-door damages trust
- Compliance, security, or infrastructure work — there is no demand to validate
- Teams with no monitoring/instrumentation — you cannot learn from the experiment without measurement
- Brand-sensitive launches where being seen running an experiment is reputational risk
- B2B enterprise sales cycles where a "video demo" is table stakes, not a validation experiment

## Content

| File | What's inside |
|------|---------------|
| `content/01-experiment-types.xml` | Six micro-MVP types with effort, what each validates, and classic examples |
| `content/02-process.xml` | 6-step process from identifying the riskiest assumption to pivot/persevere decision |
| `content/03-antipatterns.xml` | Validation theatre, compound experiments, post-hoc threshold setting |

## Templates

| File | Purpose |
|------|---------|
| `templates/experiment-preregistration.yaml` | Pre-registration card: hypothesis, type, success criterion, ethical unwind, decision rule |
