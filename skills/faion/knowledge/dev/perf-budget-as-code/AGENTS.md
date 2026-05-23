# Perf Budget As Code

## Summary

**One-sentence:** Codifies a performance budget as a CI-checked config (lighthouse-budget.json, web-vitals thresholds, k6 SLO).

**One-paragraph:** Codifies a performance budget as a CI-checked config (lighthouse-budget.json, web-vitals thresholds, k6 SLO). Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness without re-deriving the rationale.

**Ефективно для:**

- Pro-tier dev workflow, де потрібен auditable artefact замість ad-hoc decision.
- Команди, де ≥2 stakeholders читають один артефакт і повинні дійти однакового висновку.
- Cases where input must be cited (no fabrication) і decision-trail зберігається для review.
- Recurring trigger, що з'являється ≥1 раз на cycle і виправдовує methodology overhead.

## Applies If (ALL must hold)

- The triggering case shows up in the user's workload at least once per cycle.
- A named consumer (human reviewer or downstream agent) exists for the output.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Operator has authority to act on the artefact (write access, sign-off rights).

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — the artefact will be orphaned regardless of quality.
- Cannot access input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trigger event / brief | markdown / ticket | team owner |
| Input source-of-truth (system, dashboard, transcript) | varies | platform / product |
| Prior cycle's artefact (if any) | this methodology's `produces` shape | artefact store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 1000 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/output.json` | Config template (JSON) matching the schema in 02-output-contract.xml |
| `templates/_smoke-test.md` | Filled-in canonical example for calibration |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-perf-budget-as-code.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[perf-budget-pr-policy]]
- [[performance-budget-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
