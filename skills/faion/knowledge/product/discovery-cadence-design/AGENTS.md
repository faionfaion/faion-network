# Discovery Cadence Design

## Summary

**One-sentence:** Designs the interview slot, OST refresh cycle, and assumption-test pipeline for a specific team — the act continuous-discovery-habits assumes already happened.

**One-paragraph:** Continuous-discovery-habits assumes the cadence exists. Nothing covers the act of designing the cadence for a specific team (interview slots, OST refresh cycle, assumption-test pipeline). PMs joining new teams hit this immediately. Output: cadence plan + interview slot policy + OST cycle + assumption-test queue.

**Ефективно для:**

- Команда вирішила робити continuous discovery — тепер треба спроектувати конкретний cadence.
- Interview slot, OST refresh cycle, assumption-test pipeline на конкретний team-context.
- PM відрізняє ritual design від ritual existence — generic methodology цього не дає.

## Applies If (ALL must hold)

- PM joining new team OR existing team without discovery cadence
- team has ≥1 PM with discovery authority
- ≥1 active product surface with paying users

## Skip If (ANY kills it)

- team already has stable Teresa-Torres-style cadence (interview/week + OST) — augment, don't re-design
- team in shutdown phase — discovery not the priority
- purely B2C consumer impulse product — qualitative discovery has limited fit

## Prerequisites

- current team size + roles
- current customer-research capacity
- current OST or assumption inventory (or willingness to start one)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | parent skill — provides operating context for this methodology |
| `pro/product/continuous-discovery-habits` | peer methodology — produces inputs or consumes outputs |
| `solo/research/user-interviews` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounded in the cited gap | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/discovery-cadence-design.md` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/discovery-cadence-design.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-discovery-cadence-design.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-discovery-cadence-design.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/product/product-manager/`
- peer methodology: `pro/product/continuous-discovery-habits`
- peer methodology: `solo/research/user-interviews`
- external: https://www.producttalk.org/ (Teresa Torres); https://www.producttalk.org/2021/08/continuous-discovery-habits/

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.
