# Technical Debt Management

## Summary

Systematic process for making technical debt visible, quantifying its interest cost, prioritizing paydown against the roadmap, and allocating 15-20% of sprint capacity continuously. Classifies debt into 6 types (deliberate, accidental, bit-rot, design, documentation, test), scores each on Interest/Contagion/Effort/Alignment, and sequences paydown aligned with planned feature work to minimize marginal cost.

## Why

Technical debt is invisible to non-technical stakeholders and never systematically addressed until it causes a crisis. The interest metaphor makes the cost concrete: debt slows delivery by a measurable fraction of sprint velocity, compounds over time, and blocks future features. Making it visible with a register and quantifying it in dev-days-per-quarter creates the business case needed to allocate capacity consistently.

## When To Use

- Codebase has aging dependencies, fragmented patterns, and "fear zones" engineers avoid.
- Onboarding: agent surveys repo for hot-spots and surfaces undocumented assumptions.
- Quarterly debt-paydown planning: scoring and sequencing the register against upcoming roadmap.
- Pre-acquisition or pre-investment due diligence: producing defensible debt inventory.
- Migration planning (lib upgrade, framework jump, monolith decomposition).

## When NOT To Use

- One-person codebase under 6 months old — debt is rounding error, ship features.
- Debt that is actually a missing feature — do not classify "we never built X" as "we built X badly".
- Production incident response — debt management is a planning activity, not firefighting.
- Code-quality theater — do not run an agent to generate a debt list nobody will fund.

## Content

| File | What's inside |
|------|---------------|
| `content/01-debt-types-and-scoring.xml` | 6 debt types, prudent/reckless quadrant, scoring formula (Interest × Alignment / Effort), and allocation approaches. |
| `content/02-debt-process.xml` | 6-step process: make visible, quantify, prioritize, allocate, pay down strategically, prevent new debt. Includes agent workflow and gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/debt-register.md` | Per-item register: type, location, description, impact (time tax + risk), fix effort, priority, related work. |
| `templates/debt-prioritization-matrix.md` | Quarterly scoring table with Interest/Contagion/Effort/Alignment columns, sprint plan, and deferred list. |
| `templates/sprint-debt-budget.md` | Sprint-level debt work log: budget, items, effort, owners, outcomes. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/debt-survey.sh` | Quarterly repo survey: git churn, radon complexity, TODO/FIXME, outdated deps, coverage gaps → feeds debt-classifier agent. |
