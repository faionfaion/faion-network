# Design Docs at Big Tech Companies

## Summary

Reference survey of design-document practices at Google, Amazon, Uber, Spotify, Stripe, Netflix, Microsoft, Airbnb, Shopify, and Atlassian. Covers document names (RFC, ERD, 6-Pager, ADR), review formats, and the trigger rules for when a doc is required vs. optional. The core rule: write before coding; match document weight to change scope; always include "do nothing" as an alternative.

## Why

Design docs serve four purposes: early issue identification (cheap to fix on paper), consensus building, knowledge sharing, and onboarding. Without them, architecture decisions are re-litigated repeatedly and new engineers cannot reconstruct intent. LLMs excel at generating doc outlines and alternatives sections but cannot supply organizational history or system-specific context — those require human authorship.

## When To Use

- Choosing a design doc format before starting a cross-team feature or architecture change
- Adapting an RFC/ERD process to your team's async culture and scale
- Using an LLM to draft initial structure from requirements (outlines and alternatives)
- Onboarding new engineers via existing design docs as primary reference material
- Deciding whether a change needs a 1-pager, full RFC, or no doc at all

## When NOT To Use

- Bug fixes and features under 2 days — skip the doc, write code
- Purely internal team decisions with no cross-team impact
- When organizational context, team politics, or proprietary system details are critical — LLMs cannot supply these
- Post-implementation documentation — design docs must precede coding to be useful

## Content

| File | What's inside |
|------|---------------|
| `content/01-company-practices.xml` | Company comparison table; Google, Amazon, Uber, Spotify, Stripe, Meta, Microsoft detailed practices |
| `content/02-when-and-patterns.xml` | Trigger table (change type → doc needed), LLM assistance guidance, common mistakes |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-design-doc.txt` | Prompts for generating initial doc skeleton and reviewing for issues |
