# Growth Loops

## Summary

A framework for designing self-reinforcing acquisition and engagement systems where the output of one cycle becomes the input for the next. Covers five loop types (viral, content, paid, network effect, supply-side), loop efficiency calculation, loop design template, and the distinction between compounding loops and linear funnels.

## Why

Linear funnels require continuous spend to maintain growth; loops compound. Each user acquired through a loop lowers the marginal cost of the next. The loop efficiency formula (product of step-conversion rates) makes the difference between viral, stable, and decaying loops mathematically explicit — so optimization targets the actual bottleneck, not the most visible step.

## When To Use

- Product has natural sharing moments (sending links, creating public content, inviting collaborators).
- Acquisition is linear and you want to reduce CAC over time.
- Designing a new product surface and can choose architecture that enables a loop.
- Current K-factor is measurable and you want a structured path to improve it.

## When NOT To Use

- Pre-PMF: designing loops before core value is validated produces loops that compound the wrong behavior.
- Products with no trackable sharing or referral events — loop metrics cannot be measured.
- When the loop mechanism requires deceptive or spam-adjacent behavior — brand damage exceeds the acquisition gain.
- LTV:CAC &lt; 3:1 for paid loops — the economics don't support reinvestment.

## Content

| File | What's inside |
|------|---------------|
| `content/01-loop-types.xml` | Five loop types with flow diagrams, key mechanics, examples, and key metrics for each. |
| `content/02-loop-design-and-measurement.xml` | Loop efficiency formula, loop-vs-funnel comparison, loop stack pattern, implementation phases. |
| `content/03-examples-and-antipatterns.xml` | SaaS content loop, marketplace viral loop, paid acquisition loop calculations; common mistakes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-loop-design.md` | Loop design canvas: type, steps, conversion per step, bottleneck, optimization plan. |
