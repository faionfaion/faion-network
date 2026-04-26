# Stakeholder Engagement

## Summary

A structured process to identify all parties affected by or affecting a project, map each on the Power/Interest grid, assign an engagement strategy per quadrant, and execute a communication cadence — stored as a version-controlled YAML register so changes produce a diff history and evidence-backed attitudes. Engagement is continuous; the register must refresh quarterly minimum.

## Why

Projects fail when key stakeholders are ignored or mismanaged. Missed requirements from silent stakeholders, resistance from influential parties, scope creep from unmanaged expectations, and approval bottlenecks all trace back to a broken or absent engagement plan. The Power/Interest grid is the minimum viable model; the Mitchell-Agle-Wood salience overlay (power × legitimacy × urgency) is required when political risk is significant.

## When To Use

- Project kickoff for any cross-functional initiative with more than 5 named parties
- Programs with significant political risk: M&A integration, reorgs, vendor consolidation, regulated rollouts
- Multi-stakeholder transformation programs (cloud migration, ERP) with sponsors, champions, blockers, and external auditors
- Public-facing programs (government, NGO, infrastructure) with citizen/community stakeholders
- Pre-RFP or vendor-selection efforts where the buying committee has hidden influencers

## When NOT To Use

- Solo founders or very small teams (under 5 stakeholders) — direct conversation beats matrix overhead
- One-off internal hotfixes or refactors with no business stakeholder change — RACI alone is enough
- Anonymous open-source community projects — power/interest axes are meaningless without identity
- Crisis or incident response — incident command structure replaces engagement plan during P0
- When stakeholder identification is still unsolved — do BA `stakeholder-analysis/` first to get a register

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Five-step engagement process, Power/Interest grid, quadrant strategies, communication matrix |
| `content/02-workflow.xml` | Agentic register-curator pipeline, salience scoring, prompt patterns, limitations |
| `content/03-tools-and-references.xml` | CLI tools, SaaS integrations, best practices, AI-agent gotchas, references |

## Templates

| File | Purpose |
|------|---------|
| `templates/register.yaml` | Stakeholder register schema: id, power, interest, attitude, quadrant, cadence, last_engaged |
| `templates/engagement-due.py` | Script: flag stakeholders past their engagement cadence deadline |
