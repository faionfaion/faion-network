---
slug: client-firing-protocol
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Decision-record for terminating a toxic agency client: criteria checklist, transition plan, contract clean-exit, post-mortem and ICP-refinement \u2014 a versioned ADR with named owner, not a heat-of-the-moment Slack message."
content_id: "3f0a3a734ca64c12"
complexity: medium
produces: decision-record
est_tokens: 4200
tags: [agency, client-management, termination, marketing]
---
# Client Firing Protocol

## Summary

**One-sentence:** Decision-record for terminating a toxic agency client: criteria checklist, transition plan, contract clean-exit, post-mortem and ICP-refinement — a versioned ADR with named owner, not a heat-of-the-moment Slack message.

**One-paragraph:** Decision-record for terminating a toxic agency client: criteria checklist, transition plan, contract clean-exit, post-mortem and ICP-refinement — a versioned ADR with named owner, not a heat-of-the-moment Slack message. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Client meets ≥ 2 of: payment delay > 60 days, scope abuse documented ≥ 3 times, team-burn-out signal, ICP misalignment.
- Founder is the contract signer and has authority to terminate.
- Termination clause exists in the active contract with a defined notice period.

## Skip If (ANY kills it)

- Client misalignment is < 60 days old — try one structured re-alignment conversation first.
- Termination would breach a current-quarter financial covenant — defer or restructure first.
- Solo single-client agency where firing means closure — different methodology applies.

**Ефективно для:**

- Мікро-агенція з токсичним клієнтом що з'їдає > 20% часу команди.
- Засновники що відкладали firing на 90+ днів через побоювання revenue hit.
- Команди де bad-fit клієнт демотивує senior contributors.
- Аудит-ready середовища де термінація має мати documented rationale.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/marketing-manager` | Parent role context — agency operating discipline. |
| `solo/marketing/content-marketer` | Adjacent role context — content + portfolio surface. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-adr` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-class-and-tradeoff` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-skeleton.md` | ADR skeleton with status / decision_class / context / decision / alternatives-rejected / consequences / rollback / signers. |
| `templates/_smoke-test.md` | Minimum viable filled-in ADR. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-firing-protocol.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[agency-niche-positioning]]
- [[agency-case-study-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
