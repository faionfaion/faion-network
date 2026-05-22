---
slug: mcp-servers
tier: geek
group: ai
domain: claude-code
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Curated, audited catalog of public MCP servers organized by category (marketing, analytics, dev, design, PM), with install commands + auth + tool-count + risk score.
content_id: "ec6215f1c092cf9e"
complexity: medium
produces: report
est_tokens: 4400
tags: [mcp, claude-code, integration, api, tools]
---
# MCP Server Catalog

## Summary

**One-sentence:** Curated, audited catalog of public MCP servers organized by category (marketing, analytics, dev, design, PM), with install commands + auth + tool-count + risk score.

**One-paragraph:** Many teams rebuild MCP servers because they didn't know a public one exists. This methodology codifies a catalog audit: every candidate server scored on category, install command shape, auth model, tool-count, security posture (gitleaks-scanned, minimum-scope creds), maintenance signal (last release &lt; 90 days). Output is a Markdown + JSON catalog the team queries before considering a build-vs-buy decision.

**Ефективно для:**

- Build-vs-buy decision: глянути в catalog перед написанням свого MCP сервера.
- Onboarding new team members: catalog показує які integrations доступні з коробки.
- Security audit: server-level scoring (gitleaks + scope-min + maintenance) фільтрує ризикові пакети.
- Marketing/PM/Dev — кожен тип ролі бачить релевантні tools у своїй категорії.

## Applies If (ALL must hold)

- Team uses Claude Code with MCP enabled.
- Multiple integrations are in scope (≥ 3 services).
- Quarterly review owner exists to refresh the catalog.

## Skip If (ANY kills it)

- Single MCP integration with no plans to add more.
- Air-gapped environment where public servers cannot be used at all.
- Catalog maintained centrally upstream by the platform team — link to it instead of forking.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service inventory | list of services agents integrate with | team survey |
| MCP registry | modelcontextprotocol.io listing | public |
| Security scorecard rubric | gitleaks + scope-min + maintenance | security team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology is self-contained; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: per-server-scorecard, category-required, maintenance-signal-90d, scope-min-required, quarterly-refresh-cadence | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for report + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `search-mcp-registry` | haiku | Mechanical lookup. |
| `score-each-candidate` | sonnet | Light judgment on recommendation. |
| `publish-catalog` | haiku | Markdown render. |

## Templates

| File | Purpose |
|------|---------|
| `templates/catalog.md` | Catalog Markdown template (per-category sections) |
| `templates/catalog.json` | Machine-readable catalog JSON |
| `templates/scorecard.md` | Per-server scorecard template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mcp-servers.py` | Validate the report artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[mcp]]
- [[mcp-basics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
