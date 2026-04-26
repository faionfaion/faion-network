# Stakeholder Analysis

## Summary

A six-step methodology that identifies all parties affected by or influencing a change initiative, maps them on a 2x2 influence-vs-impact matrix (Manage Closely / Keep Satisfied / Keep Informed / Monitor), documents individual needs, concerns, and communication preferences, plans engagement cadence per quadrant, and stores the register as a YAML file in git so diffs become the relationship history. The register is a living artifact refreshed at minimum quarterly.

## Why

Requirements gathered from the wrong people are incomplete or conflict-laden; missing a regulator, works council, or downstream API consumer invalidates downstream artifacts. IIBA BABOK v3 ch. 3 treats stakeholder engagement as a Knowledge Area because the cost of a missing stakeholder compounds across every subsequent BA activity. Requiring an `evidence:` field on every attitude assertion prevents the politeness-bias failure where everyone is classified as "supportive."

## When To Use

- Kickoff of any cross-functional initiative with more than five named parties (sponsor, SMEs, end users, regulator, vendor).
- Migration/replacement projects where end-user resistance is the dominant risk.
- Regulated programs (HIPAA, GDPR, SOX, MDR) — the regulator is a mandatory stakeholder.
- M&A and reorg work where the political map is unstable; rerun the matrix every 2-4 weeks.
- Pre-RFP/vendor-selection work where the buying committee has hidden influencers (security, procurement, legal).

## When NOT To Use

- Solo founder pre-PMF with fewer than three people involved — go directly to customer interviews.
- Strictly internal engineering refactors with no business stakeholder change — RACI alone is sufficient.
- Public open-source projects with anonymous community contributors — influence/impact axis is meaningless; use governance patterns.
- One-off bug fixes or hotfixes — the stakeholder map will be stale before the deploy completes.

## Content

| File | What's inside |
|------|---------------|
| `content/01-identification.xml` | Eight stakeholder categories, six-step analysis procedure, influence/impact matrix quadrants, needs/concerns template, conflict resolution techniques. |
| `content/02-agent-workflow.xml` | Git-native register pattern, recommended subagents, prompt patterns (discovery + engagement-plan), AI gotchas, best practices. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholder-register.md` | Stakeholder register table with ID, role, category, influence, impact, attitude, engagement columns. |
| `templates/stakeholder-profile.md` | Individual stakeholder profile with characteristics, needs, concerns, communication preferences, engagement history. |
| `templates/stakeholder-matrix.py` | Script: validate YAML register and emit Mermaid quadrant chart for influence-vs-impact visualization. |
