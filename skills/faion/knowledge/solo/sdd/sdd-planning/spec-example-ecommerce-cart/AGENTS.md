# Spec Example: E-commerce Cart

## Summary

A fully-populated SDD spec for a shopping cart feature — covering personas, user stories,
functional and non-functional requirements, Given/When/Then acceptance criteria, out-of-scope
table, and a preliminary data model. Use as a few-shot reference when generating or reviewing
specs for similar features.

## Why

Agents writing specs without a concrete reference produce structurally incomplete documents:
missing the "Out of Scope / When" column, omitting open questions, copying story-point estimates
instead of token budgets, and writing NFRs without measurement sources. A worked example with
these sections present (and some intentionally incomplete) teaches by demonstration what a
complete spec looks like and where gaps hide.

## When To Use

- Agent or developer needs to see what a fully-populated spec looks like in practice
- Calibrating spec-writing output quality — compare agent output against this example
- Bootstrapping a new e-commerce cart-adjacent feature (persistence, guest-vs-logged-in,
  quantity limits, session merge patterns recur across cart-related features)
- Onboarding a new contributor to the SDD workflow

## When NOT To Use

- Starting a new spec by editing this file directly — use `../template-spec/` instead
- Non-e-commerce domains: guest cart, localStorage, product-catalog dependency are
  domain-specific and transfer poorly without significant reframing
- Taking NFR targets (200ms p95, 50k concurrent) as real project targets — they have
  no measurement source and must be replaced

## Content

| File | What's inside |
|------|---------------|
| `content/01-full-spec.xml` | Complete shopping cart spec: problem statement, personas, user stories, FR/NFR, AC scenarios, out-of-scope, dependencies, data model |
| `content/02-usage-guide.xml` | How to use this example as a few-shot reference; what agents commonly miss; prompt patterns |

## Templates

none

## Scripts

| File | Purpose |
|------|---------|
| `scripts/check-coverage.sh` | Print all unchecked AC coverage items from a spec file |
