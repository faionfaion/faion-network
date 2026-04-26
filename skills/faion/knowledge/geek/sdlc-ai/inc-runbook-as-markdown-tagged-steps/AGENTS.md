# Runbook-as-Markdown with Agent Step Tags

## Summary

Author every alert runbook as a Markdown file in the project repo (`runbooks/<alert-name>.md`) with a fixed section spine — `Symptoms / Diagnose / Remediate / Escalate` — and machine-parseable HTML-comment tags on each remediation step: `<!-- agent:auto -->` for steps the SRE agent may run unattended and `<!-- agent:approval -->` for steps that must wait for a signed human approval. The agent fetches the runbook keyed by the firing alert name, parses the spine, executes only `agent:auto` steps, and refuses (with a structured request to a human) on any `agent:approval` step. Markdown stays human-readable; the tags are the agent's contract.

## Why

Free-form runbooks force the agent to "interpret" prose, which is the leading cause of unsafe actions during incidents (incident.io, PagerDuty, FireHydrant 2025-2026 retros). Tagging each step turns the runbook into a deterministic decision table: any step without `agent:auto` is implicitly forbidden for the agent, eliminating ambiguity. Markdown remains the format SREs already author, so adoption is friction-free, while the comment tags survive every renderer (GitHub, Slack unfurls, Notion). Published case studies report MTTR drops up to 50% once runbooks are agent-consumable, and the `agent:approval` boundary is what AWS Kiro-style "auto-deletion" incidents exploit when missing.

## When To Use

- Teams with more than 10 distinct alert types and a stable service catalog.
- Any oncall workflow where the SRE agent should diagnose unattended but never delete or failover without human consent.
- Migrating from PDF / Confluence runbooks to a repo-versioned, code-reviewed format.
- Multi-tool environments (PagerDuty, incident.io, FireHydrant) where one source of truth must drive every agent.

## When NOT To Use

- Prototype services with <5 alerts — runbook authoring overhead exceeds the win.
- Highly conditional remediations that need real branching logic — write a Python operator instead.
- One-shot diagnostics during an active incident — write the playbook into the postmortem afterward, not now.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tagged-step-rule.xml` | Mandatory section spine and the closed `agent:auto` / `agent:approval` tag set; agent execution rule. |
| `content/02-runbook-loader.xml` | How the agent resolves alert → runbook path and rejects unmatched alerts. |

## Templates

| File | Purpose |
|------|---------|
| `templates/runbook-template.md` | Skeleton runbook with the four-section spine and example tagged steps. |
| `templates/parse_runbook.py` | Reference parser that returns `(diagnose_steps[], auto_remediate[], approval_remediate[])`. |
