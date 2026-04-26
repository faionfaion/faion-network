# Technical Debt Management

## Summary

A six-step framework for making technical debt visible, quantified, and systematically paid down — covering debt registration, impact scoring (interest × contagion / effort), capacity allocation, and prevention policies. Debt is classified into six types (deliberate, accidental, bit-rot, design, documentation, test) and prioritized against product work using the same backlog cadence.

## Why

Technical debt is invisible to non-technical stakeholders and never competes fairly against features. Without a register and a scoring formula, teams default to ignoring debt until a crisis forces a disruptive rewrite. Anchoring "interest" to measurable slowdown (PR cycle time, MTTR, test flakiness) makes debt economically comparable to feature investment.

## When To Use

- Roadmap velocity visibly declining despite stable headcount — need a quantified debt register to defend capacity allocation.
- Quarterly planning where 15-20% of capacity is reserved for paydown and engineering needs a prioritized list.
- Post-P0 outage or regression cluster where the post-mortem identifies debt as root cause.
- Before a major architectural change (auth rewrite, billing migration) — surface debt on the change surface so it is eliminated, not carried forward.
- Multi-repo solopreneur portfolio where debt silently compounds in lower-traffic repos.

## When NOT To Use

- Pre-PMF prototypes where the entire codebase is deliberate prudent debt by design — track only debt that blocks the next validation experiment.
- Single-file scripts and one-shot data migrations — registration cost exceeds rewrite cost.
- When engineering has lost trust in PM prioritization — repair trust first via engineer-driven sprints, then introduce the scoring matrix.
- Bit-rot dependency upgrades that are fully automatable (Renovate / Dependabot) — automate, do not bureaucratize.
- Crisis quarters (runway &lt; 6 months, regulator deadline) — freeze the register, ship survival features, resume after.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Debt taxonomy, quadrant, six-step process, prioritization formula. |
| `content/02-examples.xml` | Legacy API debt and missing test coverage worked examples with decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/debt-register.md` | Debt register skeleton with per-item fields (type, impact, effort, priority). |
| `templates/debt-prioritization-matrix.md` | Quarterly scoring table and sprint debt budget template. |
| `templates/debt-hotspots.sh` | Bash script: churn × complexity hotspot analysis feeding a scanner subagent. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/debt-hotspots.sh` | Finds high-churn + high-complexity files; emits JSONL for triage agent. |
