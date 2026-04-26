# Risk Register

## Summary

A structured log of identified threats and opportunities, each scored by probability x impact (1-25 scale), assigned a response strategy (Avoid/Transfer/Mitigate/Accept for threats; Exploit/Share/Enhance/Accept for opportunities), and owned by a named individual. Every Accept entry requires a contingency plan or amount. The register is a living artefact: reviewed weekly, updated on new signals, closed when risks pass or materialise.

## Why

Unmanaged risks derail projects through surprise: scramble mode erodes stakeholder confidence and recovery is reactive. A scored register converts vague worry into trackable work items, forces explicit ownership, and surfaces near-certain high-impact risks before they hit. Risk-driven contingency (sum of probability x cost-exposure per open risk) beats flat 15% reserves because it calibrates to actual exposure.

## When To Use

- Standing up the uncertainty domain at project kickoff
- Weekly risk review cycles (diffing register against issue tracker and schedule)
- Pre-gate and steering-committee snapshots (top-N risks with response status)
- Vendor/supplier onboarding (category=External, contract clauses as triggers)
- Any milestone where "what could kill this?" deserves a written answer

## When NOT To Use

- Pure-Scrum teams already tracking risks as backlog impediments — duplicate tracking splits attention
- Tasks under 1 week with a single owner — a standup question suffices
- Pre-discovery R&D where uncertainty is the work — use a learning log instead
- Risks already covered by a separate risk system (GDPR, security) — avoid reinventing

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Identify → Analyse → Score → Respond → Own → Monitor cycle; probability/impact scales; response strategies for threats and opportunities |
| `content/02-rules.xml` | Concrete rules: one named owner per risk, observable triggers, Accept requires contingency, opportunity quota, score validation |
| `content/03-examples.xml` | Software project register example; opportunity risks example; common antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-register.md` | Register table (ID, description, category, P, I, score, strategy, response, owner, status) |
| `templates/risk-card.md` | Single risk deep-dive card with trigger, contingency, and ownership fields |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/validate-register.py` | Validate risk YAML: score integrity, Accept+contingency rule, heatmap output |
