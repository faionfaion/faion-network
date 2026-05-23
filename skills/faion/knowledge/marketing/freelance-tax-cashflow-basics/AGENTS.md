# Freelance Tax Cashflow Basics

## Summary

**One-sentence:** Freelance-specific tax + cashflow checklist — quarterly self-employment-tax setoff, EU reverse-charge VAT for B2B cross-border, sole-trader vs LLC threshold math, separate-account rule, 6-month runway target.

**One-paragraph:** ops-tax-basics and ops-financial-basics under gtm-strategist are SaaS-CFO-flavored (revenue recognition, runway). Freelancers need different practice. This methodology pins 5 essentials: quarterly self-employment-tax estimated payments (USA-specific or local equivalent); EU reverse-charge VAT handling for cross-border B2B; sole-trader vs LLC threshold math (revenue + liability triggers); separate business bank account; 6-month personal-runway target before scaling. Core rules: each item has a numeric trigger; quarterly check is calendar-gated; reverse-charge captured on every EU B2B invoice; runway calculation excludes business cash; entity decision documented with revenue threshold.

**Ефективно для:**

- Solo freelancer crossing $50k revenue — entity check time.
- EU cross-border B2B work — VAT reverse-charge discipline.
- Pre-quarterly-tax deadline — estimated-tax sanity check.
- Pre-rate-jump — runway buffer math.

## Applies If (ALL must hold)

- Solo freelancer or 1-2 person micro-agency.
- Revenue ≥$20k/year (taxes start mattering).
- Authority to handle own taxes (with accountant).
- Banking infrastructure (separate accounts feasible).

## Skip If (ANY kills it)

- Employed full-time (no freelance taxes).
- Tiny side income &lt;$1k/year (de minimis).
- Jurisdictions outside the noted contexts (US/EU/UK) — consult local CPA.
- Complex multi-entity setup (consult enterprise tax counsel).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trailing-12m revenue + expense | spreadsheet | own books |
| Personal monthly burn rate | budget | self |
| Accountant relationship | contact | own ops |
| Bank capable of separate accounts | config | bank |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[freelance-pilot-pricing]] | Revenue projections feed runway math. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: quarterly-estimated-tax, eu-reverse-charge-b2b, entity-threshold-decision, separate-business-account, six-month-personal-runway | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for checklist + valid/invalid | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-checks` | haiku | Numeric extraction from books. |
| `advise-on-entity` | sonnet | Bounded judgment with accountant input. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tax-checklist.json` | JSON example of the freelance tax/cashflow checklist |
| `templates/checklist.md` | Print-friendly Markdown quarterly checklist |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelance-tax-cashflow-basics.py` | Validate one checklist JSON against the schema | After draft, before publish |

## Related

- [[freelance-pilot-pricing]]
- [[freelance-rate-jump-tactics]]
- [[late-invoice-dunning-sequence]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals to one of the rules in `01-core-rules.xml`. Use it before producing the output — picking the wrong branch is the most common failure.
