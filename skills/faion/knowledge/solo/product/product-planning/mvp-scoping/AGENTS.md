# MVP Scoping

## Summary

Define the smallest product version that validates a hypothesis: one core problem, one user, one measurable learning goal, a kill criterion, and Must-Have features capped at 60% of build capacity. If you cannot state what you will learn and when you will stop, it is not an MVP.

## Why

Founders over-scope to cover edge cases and under-scope by accident when they mistake "minimum" for "thin." The MoSCoW + capacity guard combination forces an explicit budget split — Must ≤ 60%, Should ≤ 20%, buffer 20% — and the kill criterion prevents the MVP from becoming a permanent v1 when metrics miss.

## When To Use

- Starting a new product or major feature where the goal is hypothesis validation, not final UX.
- Founder has 30+ "obvious" features and needs to cut to 3–5 buildable in one timebox.
- An agent is converting an idea description into an implementation plan and needs explicit scope before SDD/spec writing.
- Following up with mlp-planning, micro-mvps, or product-discovery — MVP scoping is the entry gate.

## When NOT To Use

- Post-PMF feature work — use roadmap-design + RICE instead.
- Compliance-driven products where "minimum" is dictated by regulation (the floor is fixed).
- B2B enterprise sales where the "MVP" must include integrations and SLAs — that is an MMP, not an MVP.
- When you already know the answer and need to ship — skip ceremony, write the spec directly.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | MVP definition, MVP vs MLP distinction, MoSCoW priority table, 6-step scoping process |
| `content/02-examples.xml` | Time-tracking app and course platform MVP examples with Must/Won't tables |
| `content/03-antipatterns.xml` | Common scoping failures: over-scoped Musts, missing kill criterion, fake MVP |

## Templates

| File | Purpose |
|------|---------|
| `templates/mvp-scope-doc.md` | Full MVP scope document with problem, feature table, learning goals, kill criterion |
| `templates/mvp-quick-check.md` | 5-question validator for fast scope review |
| `templates/mvp-capacity.py` | CLI script: reads scope JSON, fails if Must-Have days exceed 60% budget or kill criterion is missing |
