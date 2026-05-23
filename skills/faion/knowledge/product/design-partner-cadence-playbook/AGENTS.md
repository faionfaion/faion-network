# Design Partner Cadence Playbook

## Summary

**One-sentence:** Design Partner Cadence Playbook delivers a concrete, testable methodology that turns the recurring task of 'Customer demo / sneak-peek session' into an auditable artefact, addressing the gap: Pro/geek-tier B2B PMs need a methodology for running an ongoing design-partner cohort (cadence, incentives, NDAs, escalation path).

**One-paragraph:** Pro/geek-tier B2B PMs need a methodology for running an ongoing design-partner cohort (cadence, incentives, NDAs, escalation path). Design Partner Cadence Playbook closes this gap with a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. The methodology is anchored to the triggering work 'Customer demo / sneak-peek session' (role-product-manager, pro tier). It produces a structured artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

**Ефективно для:**

- Pro/geek B2B PM веде design-partner cohort (3-8 customers) з регулярним cadence.
- Customer demo / sneak-peek session перетворюється на auditable cycle.
- PM хоче знати, коли promote partner до paying customer чи graduate з програми.

## Applies If (ALL must hold)

- The triggering activity 'Customer demo / sneak-peek session' (role: role-product-manager) is in your current workload at least once per cycle.
- You have authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the artefact — human reviewer OR downstream agent.
- An auditable source-of-truth is available for the inputs the methodology needs.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems / dashboards / docs that feed the methodology's inputs.
- A storage location for the produced artefact (git repo, doc, ticket) where the consumer can read it.
- Prior cycle's artefact (if any) accessible for carry-forward and trend comparison.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounded in the cited gap | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design_partner_cadence_playbook_template_fill` | haiku | Template fill, no judgment |
| `design_partner_cadence_playbook_evidence_check` | sonnet | Bounded comparison + judgment |
| `design_partner_cadence_playbook_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-partner-cadence-playbook.md` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/design-partner-cadence-playbook.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-design-partner-cadence-playbook.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-partner-cadence-playbook.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/product/` (see neighbouring methodologies)
- triggering activity: `role-product-manager/Customer demo / sneak-peek session`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.
