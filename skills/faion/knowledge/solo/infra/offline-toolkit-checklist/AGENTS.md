---
slug: offline-toolkit-checklist
tier: solo
group: infra
domain: infra
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Offline-ready laptop checklist for indie hackers on travel days: pre-synced Notion, repo clones, env vars, Stripe CSV exports, and a deterministic restore drill before flight."
content_id: "6f4fd7231b5fe145"
complexity: medium
produces: checklist
est_tokens: 5500
tags: [offline, travel, checklist, indie-hacker, preflight]
---
# Offline Toolkit Checklist

## Summary

**One-sentence:** Offline-ready laptop checklist for indie hackers on travel days: pre-synced Notion, repo clones, env vars, Stripe CSV exports, and a deterministic restore drill before flight.

**One-paragraph:** Indie hackers lose half a travel-day to broken offline access — Notion empty, repo not cloned, env vars missing, payments dashboard inaccessible. This methodology hands them a binary, dated checklist that turns 'I think I'm offline-ready' into a verified, named-owner artefact: every required artefact has a verify command, every verify command has an expected output, and the checklist is signed off by the operator before departure. The output is a `checklist` shaped artefact that downstream agents can replay in CI to catch dotfile drift.

## Applies If (ALL must hold)

- Operator will work offline for ≥4 hours within the next 24 hours.
- Operator's primary work is repo-based (code + content + notes) and not pure browser SaaS.
- Operator can run a deterministic verify command per checklist row before departure.

## Skip If (ANY kills it)

- Trip is < 1 hour and reliable mobile tethering is available.
- Operator uses managed cloud workstation (Codespaces, Gitpod) that has no offline mode.
- Operator is on a shared / hot-desk laptop where dotfiles cannot be pre-synced.

**Ефективно для:**

- Соло-фаундери що часто літають та витрачають 2-4 години аеропорту на відновлення робочого середовища.
- Indie hackers на digital-nomad режимі з flaky-Wi-Fi реальністю.
- Конференції / off-site: pre-flight check замість panic-debug у залі прильоту.
- Команди де один розробник — це і ops, і product, і support; downtime = lost revenue.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Laptop with last-30-day usage history | macOS / Linux laptop | operator |
| Dotfiles repo (chezmoi / stow) | Git repo | operator dotfiles |
| Secrets vault export | 1Password / Bitwarden CLI | vault manager |
| List of revenue-critical dashboards | Markdown list with CSV export commands | owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft/dotfiles-management` | Dotfiles sync is the first checklist row. |
| `solo/infra/server-craft/secrets-management` | Secrets export procedure is row two. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 900 |
| `content/04-procedure.xml` | essential | Step-by-step pre-flight procedure | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-checklist` | haiku | Template fill from operator inventory. |
| `populate-verify-commands` | sonnet | Per-row verify command + expected output. |
| `review-completeness` | opus | Cross-row coverage check (no critical category missed). |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton for the pre-flight checklist. |
| `templates/_smoke-test.md` | Minimum viable filled-in checklist for one travel day. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-offline-toolkit-checklist.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | Pre-departure: after filling the checklist. |

## Related

- [[dotfiles-management]]
- [[secrets-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
