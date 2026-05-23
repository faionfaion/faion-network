# Manual Override Ledger

## Summary

**One-sentence:** Decision-record ledger for every config drift override: who, what, why, time-to-revert, link to upstream PR. Turns ad-hoc out-of-band changes into auditable records.

**One-paragraph:** Decision-record ledger for every config drift override: who, what, why, time-to-revert, link to upstream PR. Turns ad-hoc out-of-band changes into auditable records. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Інцидент закрили швидким fix у консолі — потрібен запис, інакше IaC drift зростатиме.
- Audit consumer (SOC2/ISO) вимагає trail кожного manual change — ad-hoc Slack-повідомлення не йде.
- Команда планує переходити drift→IaC щотижня, але немає списку 'що треба переводити'.
- Один інженер часто робить overrides без записів — потрібен ledger + owner accountability.

## Applies If (ALL must hold)

- Operator just did an out-of-band cloud-console change to fix incident
- Override is expected to be reverted to IaC within a known window
- An audit consumer (SOC2, ISO, internal sec review) requires a written trail
- A named owner is accountable for closing the override

## Skip If (ANY kills it)

- No team owner exists — ledger becomes orphan
- Override is part of normal automation flow (e.g. autoscaling) — not 'manual'
- Org policy already forbids manual overrides — record refusal instead

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
| `templates/decision-record.md` | working skeleton matching the `produces=decision-record` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-manual-override-ledger.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Was an out-of-band manual change made that needs an auditable record with a named owner?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
