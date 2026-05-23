# PCI-DSS Vendor Evidence Pack

## Summary

**One-sentence:** Audit-ready evidence pack template for PCI-DSS vendor assessments: scope statement, SAQ type, AoC, network diagrams, key-management proof, quarterly ASV scan, pen-test summary.

**One-paragraph:** Audit-ready evidence pack template for PCI-DSS vendor assessments: scope statement, SAQ type, AoC, network diagrams, key-management proof, quarterly ASV scan, pen-test summary. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Вендор обробляє CHD або токени — без evidence pack QSA розгортає аудит.
- Аудит у наступні 12 місяців — pack має бути готовий за 30 днів, а не за тиждень до due date.
- QSA вже відмовив у попередньому pack за неповноту scope statement — треба структурований template.
- Power-user не хоче переробляти діаграми мережі кожні 6 місяців — потрібен живий evidence ledger.

## Applies If (ALL must hold)

- Vendor handles, stores, or processes cardholder data
- PCI-DSS audit (QSA or self-assessment SAQ) is required within next 12 months
- Evidence pack must be assembled in a defensible, auditor-ready form
- Owner of evidence pack is named + accountable

## Skip If (ANY kills it)

- Org does not handle cardholder data (CHD) and is not in PCI scope
- Vendor is fully outside CDE and there's a contractual carve-out
- QSA already has a current evidence pack covering this scope

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
| `templates/report.md` | working skeleton matching the `produces=report` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pci-dss-vendor-evidence-pack.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Does the vendor handle CHD + need an auditor-ready PCI-DSS evidence pack within 12 months?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
