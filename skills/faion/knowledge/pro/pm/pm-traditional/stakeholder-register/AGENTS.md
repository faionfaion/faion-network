# Stakeholder Register

## Summary

A stakeholder register is a structured, version-controlled catalog of everyone who affects or is affected by a project — with power, interest, impact, attitude, and engagement strategy documented for each entry. Attitude assertions must be backed by observable evidence, not assumptions. The register is maintained continuously, not written once at kickoff.

## Why

Hidden stakeholders block projects at the worst possible moments. A register built from authoritative directory data (org chart, CRM) rather than the PM's memory surfaces gatekeepers (infosec, procurement, works council) who are systematically missed. Attitude documented with evidence enables targeted engagement; attitude assumed from seniority misleads. The register is the source of truth for all engagement planning and communications.

## When To Use

- Any project with more than five stakeholders where "who has authority over what" is not obvious.
- Programs spanning departments, organizations, or jurisdictions.
- Pre-RFP / vendor selection where the buying committee includes hidden influencers.
- Post-merger or post-reorg projects where lines of authority are still being redrawn.
- Compliance-driven projects requiring a documented record of consulted stakeholders.

## When NOT To Use

- Solo founders or one-person projects.
- Single co-located product squads where everyone is in one channel — a MAINTAINERS.md suffices.
- Throwaway internal scripts or hotfixes with no business stakeholder.
- Crisis response with pre-assigned incident command structure.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Register fields, Power/Interest grid, hidden-stakeholder checklist |
| `content/02-rules.xml` | Rules for evidence-backed attitudes, freshness, PII handling, and agentic workflow |

## Templates

| File | Purpose |
|------|---------|
| `templates/register-entry.yaml` | YAML template for a single stakeholder entry |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/register_audit.py` | Audits register completeness and evidence coverage; exits non-zero on issues |
