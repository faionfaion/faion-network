# Problem Validation

## Summary

A methodology for confirming that a problem is real, painful, and worth solving before writing code. Core rule: use The Mom Test — ask about the user's life and past behavior, never about your idea. Rank evidence on a 5-level hierarchy (payment > commitment > prototype engagement > stated interest > stated problem). Only declare a problem validated when ≥3 tier-1 or tier-2 signals come from non-network respondents.

## Why

Most failed products were built for problems that exist but are not urgent or worth paying to solve. Asking "would you use this?" produces compliments, not data. The Mom Test protocol and the evidence hierarchy prevent founders from self-deceiving with flattering but useless feedback. Continuous re-validation catches market drift after launch.

## When To Use

- After idea-generation, before MVP build — confirm the problem is real and painful.
- When growth has stalled and product-problem fit is suspect.
- Before adding a major feature: validate that the underlying job-to-be-done exists.
- During pivots, to test the new problem hypothesis cheaply before writing code.

## When NOT To Use

- Post-launch with strong revenue and retention — switch to feature prioritization frameworks.
- High-velocity B2C consumer products where behavior trumps stated preference — run a paid-ads landing-page test instead.
- Regulated or specialized B2B (healthcare, finance) where interviews carry compliance overhead — use expert calls and analyst frameworks.
- When the purpose is validation theatre to feel safe rather than genuine disproof.

## Content

| File | What's inside |
|------|---------------|
| `content/01-validation-hierarchy.xml` | Evidence hierarchy (5 levels), commitment signal types, red flags to detect, and interview opener framework. |
| `content/02-interview-method.xml` | Mom Test question patterns, bad-question antipatterns, 3-agent agentic workflow, and best practices. |

## Templates

| File | Purpose |
|------|---------|
| `templates/transcript-tagger.py` | Python script using Anthropic SDK: tags each interview turn as compliment/hypothetical/generic/commitment and returns hierarchy-level score. |
