# Technical Debt

## Summary

Methodology for identifying, tracking, prioritizing, and incrementally paying down technical debt using a register with explicit severity, interest (cost/week), and fix-cost fields. Uses Fowler's quadrant to categorize debt type (deliberate/inadvertent × reckless/prudent). Debt items require measurable business impact to enter the register.

## Why

Invisible debt silently slows feature velocity. Making it visible and measurable allows stakeholder communication, sprint capacity allocation, and ROI-driven prioritization. The "interest" metaphor (cost/week of not fixing) enables ranking by impact rather than subjective severity. Hotspot analysis from git history targets paydown where it matters most.

## When To Use

- Auditing a legacy codebase before a refactor cycle
- Sprint capacity planning to allocate a fixed % to debt paydown vs features
- After a quarter of fast shipping to reconcile "we'll fix later" promises
- Architecture reviews needing Fowler quadrant categorization
- Stakeholder communication requiring concrete cost/interest framing

## When NOT To Use

- Greenfield projects in the first sprint — no code exists yet; tracking is overhead
- As a substitute for actual refactoring — a register that never gets paid down is shelfware
- For code-style nits that linters/formatters fix automatically — those are hygiene, not debt
- For "I don't like this design" disagreements without measurable impact — keep it evidence-based

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Debt register requirements, severity rubric, interest-first ranking, hotspot targeting |
| `content/02-types-and-metrics.xml` | Fowler quadrant, debt category taxonomy, complexity metrics, automated detection approach |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-debt.sh` | Surfaces unresolved TODO/HACK/FIXME with git blame metadata and age |
