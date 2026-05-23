# Stat-Power Pre-Check

## Summary

**One-sentence:** Pre-flight power calculation that converts traffic, baseline conversion, and target lift into a GO / STRETCH / KILL verdict before any CRO experiment launches.

**One-paragraph:** Solopreneurs and small-team marketers run underpowered tests constantly — too little traffic, premature stops, noisy 'winners'. This methodology blocks that. Before any experiment, the marketer fills five typed inputs (weekly visitors, baseline conversion, target relative lift, alpha, power) and reads a verdict: GO (enough traffic in the window), STRETCH (need to extend the window or accept lower power), KILL (effect size uneconomic — pivot to a structural change). The check is qualitative-numerate, just enough math to refuse to run tests that cannot conclude.

**Ефективно для:** solopreneurs running CRO; growth marketers triaging hypotheses; agencies setting client expectations before launching tests.

## Applies If (ALL must hold)

- Planning a CRO experiment on a page with conversion event tracking already wired
- Weekly traffic to the test surface is measurable and stable (±20% WoW)
- Baseline conversion rate known for ≥4 weeks
- Decision authority sits with the marketer (no committee approval lag)

## Skip If (ANY kills it)

- Traffic too sparse (<~200 conversions / week at baseline) — use qualitative methods
- Change is a bug or compliance fix that MUST ship — do not gate on power
- Change is a brand / trust signal not measurable by a single conversion event
- Test is structurally underpowered AND cannot be redesigned — accept as non-experiment

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Last 4 weeks of weekly visitors + conversions on the test surface | CSV / dashboard | analytics |
| Target lift as a relative percentage (e.g. '10% lift on signup') | Note | hypothesis brief |
| Agreed maximum test window | Note | experiment ledger |
| Optional: power calculator (Evan Miller / statsmodels) | Link or Python script | tools/ |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/experiment-hypothesis-scoring` | upstream hypothesis scoring |
| `pro/marketing/experiment-ledger-discipline` | where the verdict is recorded |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema, valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom + root cause + fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `collect_inputs` | haiku | Mechanical extraction from analytics |
| `compute_power_verdict` | sonnet | Bounded math with typed inputs |
| `write_verdict_record` | sonnet | Bounded synthesis for the ledger entry |

## Templates

| File | Purpose |
|------|---------|
| `templates/stat-power-precheck.json` | JSON schema for the verdict record |
| `templates/stat-power-precheck.md` | Markdown skeleton with all five inputs and the verdict block |
| `templates/power-calc.py` | 10-line Python power calculator using statsmodels |
| `templates/_smoke-test.json` | Minimum-viable filled verdict |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stat-power-precheck.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- `pro/marketing/experiment-hypothesis-scoring`
- `pro/marketing/experiment-ledger-discipline`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether stat-power-precheck applies: root question — "Is the change a measurable CRO experiment AND traffic is stable AND baseline known?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-required-inputs, r2-no-launch-without-verdict, r3-minimum-conversions, r4-sequential-stop-guard, r5-lift-as-relative, r6-window-frozen.
