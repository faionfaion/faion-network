# Product Operations (Product Ops)

## Summary

A dedicated Product Ops function removes operational drag — process docs, tool plumbing, status
updates, metric rollups, stakeholder comms — so PMs spend more time on discovery and strategy.
96% of orgs now have this function; 50% report to CPO. Maturity runs from Level 1 (process docs)
to Level 3 (AI automation). Agents are a near-perfect fit because Product Ops work is repetitive,
system-of-record-driven, and benefits from deterministic automation.

## Why

Product teams spend 30–40% of time on operational tasks instead of discovery and strategy.
A structured ops function (or an agent-driven equivalent) recaptures that capacity. Without it,
every PM re-invents status updates, templates, and metric definitions — creating artifact drift
and decision latency. With it, PMs can focus on the work only humans can do.

## When To Use

- Solopreneur or small team where a human Product Ops hire isn't justified but the weekly
  operational tax (status updates, roadmap snapshots, metric rollups) still needs to be paid
- Multi-product / multi-team setup with 3+ PMs working in different tools causing artifact drift
- Migrating from ad-hoc PM workflows to a documented system
- Pre-fundraise / board-prep cycles requiring recurring "state of product" packs from 5–10 sources
- Org-wide release calendars, dependency maps, capacity planning across squads

## When NOT To Use

- A team with one PM and one product — the operational tax is too small; agent flows add more
  maintenance overhead than they save
- During the first 30 days of a new product where workflows haven't stabilized
- Strategic product decisions (pricing, positioning, kill/scale) — Product Ops enables those
  decisions, it does not make them
- Heavily regulated environments where every status update has compliance implications
- When PM tools have no public API — no API means no agents

## Content

| File | What's inside |
|------|---------------|
| `content/01-responsibilities.xml` | Ops areas, maturity model, AI-native ops patterns, 2026 stats |
| `content/02-agent-usage.xml` | Agentic layers, subagents, prompt patterns, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/ops-rollup.sh` | Weekly rollup from Linear + PostHog, outputs Markdown to stdout |
| `templates/ops-schema.sql` | Canonical ops-store schema: feature, release, risk, metric_kpi tables |
