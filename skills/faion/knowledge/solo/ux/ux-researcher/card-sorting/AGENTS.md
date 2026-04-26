# Card Sorting

## Summary

A research method that asks users to organize topic cards into groups they define (open sort),
into predefined categories (closed sort), or a hybrid. Results reveal users' mental models for
content organization. Use 30-60 cards, recruit 15-20 participants for open sorts (30+ for
statistical closed sorts), and analyze via similarity matrix and standardization score.

## Why

Navigation categories that make sense internally often fail users because they mirror org charts
or product taxonomies rather than user mental models. Card sorting surfaces the actual groupings
users expect before IA decisions are locked in, preventing expensive post-launch navigation
redesigns. Similarity matrices (items grouped together >70% of the time) provide objective
evidence for structural decisions.

## When To Use

- Designing or redesigning primary navigation — validate category labels and groupings.
- When analytics show high search use and low nav use — users cannot find content in current IA.
- Before tree testing — generate the structure that tree testing will then validate.
- When migrating content to a new IA — ensure the new structure matches user expectations.

## When NOT To Use

- When the IA is already validated and stable — card sorting is generative; use tree testing
  to validate an existing structure instead.
- With fewer than 15 participants for open sort — below that threshold, patterns are unreliable.
- When cards exceed 60 items — cognitive fatigue degrades result quality; split into multiple
  focused sorts by content area.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | 6-step procedure: goals, card prep, format choice, recruiting, conducting, analysis metrics |
| `content/02-examples.xml` | Open sort e-commerce example, closed sort placement results, analysis thresholds |

## Templates

| File | Purpose |
|------|---------|
| `templates/card-sort-plan.md` | Plan skeleton: objectives, method, participants, card list, categories (closed), timeline |
| `templates/results-report.md` | Results report: user-created categories, agreement matrix, placement %, recommendations |
