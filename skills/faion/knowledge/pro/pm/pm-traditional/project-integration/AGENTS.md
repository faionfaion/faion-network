# Project Integration Management

## Summary

The PM as integrator ensures that decisions in scope, schedule, cost, quality, risk, resources, communications, and procurement are consistent and mutually reinforcing. All component plans live as typed YAML/JSON artifacts in git; status RAG is computed from measurable variance thresholds, never from opinion; and every baseline change goes through a documented change-control PR. Agents propose; sponsors approve baseline changes.

## Why

Silo management — optimising each knowledge area independently — routinely produces locally good and globally bad outcomes: a scope addition that is "free" for engineering adds cost and schedule risk that the PM discovers two weeks later. Integration is the discipline that catches cross-area effects before they become surprises. Without an integration view, status reports reflect the best news from each silo rather than the worst constraint across them.

## When To Use

- Multi-team / multi-vendor programs where decisions in one area routinely affect another
- Regulated programs where the Project Charter is a contractual artifact requiring version control
- Hybrid agile+waterfall environments with component plans in different tools needing a single source of truth
- Portfolio PMO reporting where dozens of projects feed the same status rollup
- Integrated Change Control when a change request affects more than one baseline

## When NOT To Use

- Solo or duo teams — overhead exceeds value; a one-page README and a kanban board cover integration
- Pure agile single-team with one product backlog — Scrum already integrates work; bolting on PMBoK integration creates conflict
- Pre-charter exploratory spikes — formalising integration too early kills learning
- Portfolios where project owners refuse to share artifacts in a common format — fix governance first

## Content

| File | What's inside |
|------|---------------|
| `content/01-charter.xml` | Charter elements, SMART criteria, success metrics, version control rules |
| `content/02-status-and-change.xml` | RAG computation rules, change control workflow, integration antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/status-rag.py` | Deterministic RAG computation from EVM and risk YAML baselines |
