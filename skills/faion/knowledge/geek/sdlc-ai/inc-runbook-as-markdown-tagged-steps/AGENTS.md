---
slug: inc-runbook-as-markdown-tagged-steps
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Author every alert runbook as a Markdown file in the project repo (`runbooks/<alert-name>.
content_id: "631405a186b3eeee"
tags: [incident-response, runbook, sre-agent, approval-gate, oncall]
---
# Runbook-as-Markdown with Agent Step Tags

## Summary

**One-sentence:** Author every alert runbook as a Markdown file in the project repo (`runbooks/<alert-name>.

**One-paragraph:** Author every alert runbook as a Markdown file in the project repo (`runbooks/<alert-name>.md`) with a fixed section spine — Symptoms / Diagnose / Remediate / Escalate — and machine-parseable HTML-comment tags on each remediation step: `<!-- agent:auto -->` for steps the SRE agent may run unattended and `<!-- agent:approval -->` for steps that must wait for a signed human approval. The agent fetches the runbook keyed by the firing alert name, parses the spine, executes only `agent:auto` steps, and refuses (with a structured request to a human) on any `agent:approval` step. Markdown stays human-readable; the tags are the agent's contract.

## Applies If (ALL must hold)

- Teams with more than 10 distinct alert types and a stable service catalog.
- Any oncall workflow where the SRE agent should diagnose unattended but never delete or failover without human consent.
- Migrating from PDF / Confluence runbooks to a repo-versioned, code-reviewed format.
- Multi-tool environments (PagerDuty, incident.io, FireHydrant) where one source of truth must drive every agent.

## Skip If (ANY kills it)

- Prototype services with fewer than 5 alerts — runbook authoring overhead exceeds the win.
- Highly conditional remediations that need real branching logic — write a Python operator instead.
- One-shot diagnostics during an active incident — write the playbook into the postmortem afterward, not now.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
