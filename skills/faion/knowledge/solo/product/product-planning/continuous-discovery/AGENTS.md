# Continuous Discovery

## Summary

Continuous discovery is a weekly cadence of user interviews, feedback synthesis, and opportunity-to-roadmap diffing that keeps product decisions connected to fresh user evidence. Allocate 15–20% of capacity to it, maintain a controlled vocabulary of themes (new themes need approval), and tie every roadmap change to at least one cited opportunity from the discovery repository.

## Why

Discovery treated as a one-time project-start activity produces a roadmap frozen to the assumptions of launch day. Teresa Torres' research shows teams that run weekly touchpoints with users make fundamentally different prioritization decisions than those that rely on launch-time research — because the problem space shifts and user behavior reveals what interviews cannot predict.

## When To Use

- Post-MVP product where weekly insight is needed to keep the roadmap honest.
- Team has at least one customer-touching channel (interviews, support, in-app, analytics).
- Pairing with roadmap-design so Now/Next/Later buckets keep evolving.
- Solo PM or founder who needs an automated cadence to replace a research team.

## When NOT To Use

- Pre-PMF / 0-to-1 products — use product-discovery (deep-dive) until you have customers.
- Products with fewer than 50 active users — discovery becomes anecdote-driven, not signal-driven.
- Heavily regulated environments where every customer touch needs legal review (loop is too slow to be useful).

## Content

| File | What's inside |
|------|---------------|
| `content/01-cadence.xml` | Weekly/daily/biweekly/quarterly activity cadence with rules for each frequency |
| `content/02-synthesis.xml` | Theme clustering rules, controlled vocabulary, opportunity solution tree linkage |
| `content/03-antipatterns.xml` | Discovery theater, cadence collapse, sample bias, LLM hallucination risks |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-synthesis.json` | JSON schema for weekly synthesis agent output with themes, verbatims, and roadmap links |
| `templates/discovery-cadence.py` | Emits this week's discovery checklist as JSON (daily/weekly/biweekly/quarterly tasks) |
