---
slug: multi-machine-offline-cache
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Spec for faion CLI per-machine cache, deterministic offline fallback, license-aware re-activation across laptop + workstation + client-issued device.
content_id: "0a064cb86a7d9dca"
complexity: medium
produces: spec
est_tokens: 4300
tags: [faion-cli, offline, cache, multi-machine, infra]
---
# Multi-Machine Offline Cache

## Summary

**One-sentence:** Spec for faion CLI per-machine cache, deterministic offline fallback, license-aware re-activation across laptop + workstation + client-issued device.

**One-paragraph:** Spec for faion CLI per-machine cache, deterministic offline fallback, license-aware re-activation across laptop + workstation + client-issued device. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Спеціаліст працює з laptop + desktop + іноді client-issued machine — без єдиної схеми cache синхронізації.
- Літак / no-internet client site трапляються частіше ніж раз на місяць — потрібен offline-first fallback.
- License-модель з per-machine activation count — без правил re-activation легко вилетіти за ліміт.
- Команда переходить між робочими сесіями — стан cache має бути deterministic, не 'latest wins'.

## Applies If (ALL must hold)

- User works on >=2 machines (laptop + workstation + occasional client laptop)
- User expects CLI to function offline (flights, no-internet client site)
- License model includes per-machine activation count
- Refresh token + license token storage spec exists

## Skip If (ANY kills it)

- Single-machine user — out of scope
- Fully cloud-hosted dev environment (Codespaces, Devbox) — different sync model
- License is unlimited devices — no activation logic needed

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trigger context | Markdown / ticket / transcript | upstream task |
| Named owner | string (handle, email, role) | team roster |
| Storage location | URL / repo path | artefact store |
| Prior cycle artefact (if any) | this methodology's output | last run |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/AGENTS.md` | parent group context (vocabulary, neighbouring methodologies) |
| `solo/sdd/sdd` | SDD discipline for artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + run-the-checklist + skip-this-methodology conclusions | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid + invalid + forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom / root-cause / fix | ~700 |
| `content/04-procedure.xml` | essential | step-by-step procedure (input/action/output/decision-gate) | ~700 |
| `content/05-examples.xml` | essential | one worked end-to-end example with inputs and final artefact | ~700 |
| `content/06-decision-tree.xml` | essential | root-question + branches + conclusion refs to 01-core-rules | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment over bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high or evidence chain is required |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | working skeleton matching the `produces=spec` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-machine-offline-cache.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Does the user work on >=2 machines with a license that counts activations + needs offline mode?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
