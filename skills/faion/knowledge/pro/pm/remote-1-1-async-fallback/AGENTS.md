---
slug: remote-1-1-async-fallback
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Async-doc 1:1 protocol for cross-timezone PMs who cannot meet weekly synchronously; emits typed `Async11Note` per cycle with named prompts, response window, escalation rule, and outcome review.
content_id: "8906b1d8c6697eff"
complexity: medium
produces: playbook-step
est_tokens: 3300
tags: [pm, pro, 1on1, async, remote, timezones]
---
# Remote 1:1 Async Fallback

## Summary

**One-sentence:** A structured async-doc 1:1 protocol for cross-timezone PMs who cannot meet synchronously every week; emits typed `Async11Note` per cycle with named prompts, response window, escalation rule, and outcome review.

**One-paragraph:** Synchronous weekly 1:1s break when one party is in UTC-8 and the other in UTC+10, or when one party is on parental leave / sick / on retreat. Default fallback is to skip the cycle — silently degrading PM↔IC visibility until a problem surfaces. This methodology pins an async fallback: PM posts the next-cycle Async11Note (3 named prompts: blockers, decisions-needed, morale) to a private doc, IC responds within a published response window (default 48 business hours), PM acknowledges with next-step actions, and any unresponsive cycle escalates to a synchronous call or to the IC's manager. Output is versioned, owned, and reviewed quarterly for response-rate drift.

**Ефективно для:**

- Cross-timezone PM ↔ IC pairs where synchronous weekly is structurally impossible.
- IC on temporary leave / retreat / sick where async preserves signal continuity.
- PMs covering ≥ 5 ICs whose 1:1 calendar saturates — async absorbs surge.
- Quarterly review: response-rate trend flags structural issues.

## Applies If (ALL must hold)

- PM ↔ IC pairing exists with weekly cadence baseline.
- Async response infrastructure exists (private doc / Slack DM / email).
- IC is reachable within the published response window.
- PM has authority to escalate to manager on second unresponsive cycle.

## Skip If (ANY kills it)

- Synchronous 1:1 is feasible — use it. Async is fallback, not default.
- IC is on formal disconnection leave (vacation per company policy) — pause, do not async-pursue.
- < 3 cycles per year — single doc cheaper than versioned methodology.
- No named owner.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 1:1 baseline cadence | calendar | PM |
| Private doc / DM channel | Slack / Notion / email | PM ↔ IC |
| Last quarter Async11Notes | JSON | this methodology |
| Escalation contact (IC's manager) | stakeholder register | HR |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[team-development]] | 1:1 signals feed Tuckman staging + skill matrix. |
| [[team-morale-pulse-survey]] | Morale prompt aligns with pulse axes. |
| [[rag-policy-thresholds]] | Unresponsive-cycle count is a Red signal. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: explicit trigger, bounded output, evidence-anchored, named owner, iteration loop | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `Async11Note` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: cargo-cult, ownership ambiguity, drift, leakage, no outcome review, trigger drift | ~900 |
| `content/04-procedure.xml` | medium | 5-step: post prompts → IC responds → PM ack → escalate-if-unresponsive → quarterly review | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: response window, unresponsive count, scope of issue → ack / escalate / synchronous-reschedule | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compose-prompts` | haiku | Fixed text fill. |
| `synthesise-response` | sonnet | Bounded judgment on IC reply. |
| `escalation-decision` | sonnet | Threshold-based escalation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Async11Note skeleton with 3 named prompts |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum viable filled `Async11Note` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-remote-1-1-async-fallback.py` | Validate `Async11Note`: named prompts, response window, escalation, owner | Pre-merge |
| `scripts/staleness-check.py` | Flag notes whose `last_reviewed` > 90 days | Weekly cron |

## Related

- [[team-development]]
- [[team-morale-pulse-survey]]
- [[rag-policy-thresholds]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observed response state (within window, late, missing) to ack / escalate / reschedule. Each leaf references a rule from `01-core-rules.xml`.
