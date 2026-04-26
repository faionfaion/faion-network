# Stakeholder Analysis

## Summary

Identify all parties affected by or influencing a change initiative, classify them by influence and impact, document their needs and concerns, and plan engagement accordingly. Uses Mendelow power-interest grid for cadence and Mitchell-Agle-Wood salience model for prioritization. Definitions (stakeholder, responsibility model, salience model) must be frozen before any classification begins.

## Why

Gathering requirements from the wrong people produces incomplete or conflicting inputs that surface late and cause rework. Formal stakeholder analysis with locked definitions and a responsibility model (RACI/RASCI/DACI/RAPID) gives every downstream artifact a traceable source of truth and satisfies BABOK 3 §3.2 audit requirements.

## When To Use

- Starting any initiative: identify stakeholders before the first interview or workshop
- Regulated / audited programs (SOX, MDR, ISO 13485, GDPR Art. 35 DPIA) needing BABOK-aligned artifacts
- Onboarding a new BA or agent to an existing program to ensure reproducible classification
- Choosing a responsibility model (RACI vs RASCI vs DACI vs RAPID) for a specific decision class
- Disambiguating "stakeholder" from "user", "persona", "actor", "customer" across Confluence/Notion pages

## When NOT To Use

- Solo / pre-PMF work where ceremony exceeds value — use direct customer discovery
- Pure code refactor with zero business-stakeholder change
- One-shot decisions with a single accountable owner — a one-line ADR is enough
- Open-source community projects with pseudonymous identities (salience axes cannot be measured)

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | 6-step process: identify, characterize, map influence/impact, capture needs, plan engagement, manage relationships; stakeholder category table |
| `content/02-models.xml` | Mendelow power-interest grid, Mitchell-Agle-Wood salience model (8 types), responsibility models (RACI/RASCI/DACI/RAPID) with limitations and selection rules |
| `content/03-agentic.xml` | Agent workflow, definition-freezing protocol, subagent patterns, RACI lint script, AI-agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholder-register.md` | Register table with ID, role, category, influence, impact, attitude, engagement columns |
| `templates/stakeholder-profile.md` | Per-stakeholder profile: characteristics, needs, concerns, communication preferences, engagement history |
| `templates/raci-lint.sh` | Bash linter: fails if any RACI row has != 1 Accountable or 0 Responsible |
