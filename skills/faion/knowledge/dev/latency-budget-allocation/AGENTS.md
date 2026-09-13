# Latency Budget Allocation

## Summary

**One-sentence:** Allocates end-to-end p95 latency across hops; emits a per-hop SLO + a CI gate spec.

**One-paragraph:** Allocates end-to-end p95 latency across hops; emits a per-hop SLO + a CI gate spec. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness without re-deriving the rationale.

**Ефективно для:**

- Pro-tier dev workflow, де потрібен auditable artefact замість ad-hoc decision.
- Команди, де ≥2 stakeholders читають один артефакт і повинні дійти однакового висновку.
- Cases where input must be cited (no fabrication) і decision-trail зберігається для review.
- Recurring trigger, що з'являється ≥1 раз на cycle і виправдовує methodology overhead.

## Applies If (ALL must hold)

- A user-facing latency SLO exists as percentile + threshold + measurement point + window, or can be written before allocation starts.
- The request's critical path can be traced hop by hop and each hop has, or can get, a caller-side latency histogram with an owning team.
- Client timeout and retry settings per hop are readable in config.
- A perf environment and a load tool exist that can produce at least 200 requests per gate run.
- The owning team has a named reviewer who can approve thresholds before a gate blocks merges.

## Skip If (ANY kills it)

- No end-to-end SLO is stated; a budget cannot be allocated from a total that does not exist.
- The path is a single hop with no downstream calls; set the SLO on that hop's histogram directly.
- Hops cannot be instrumented caller-side (opaque vendor SDK with no client timing); allocate only after a wrapper exposes the timing.
- The latency concern is throughput or saturation rather than request latency; capacity planning applies, not a per-hop budget.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| User-facing latency SLO: metric, percentile, threshold, measurement point, window | SLO document | product / SRE |
| Critical-path trace of the request naming every hop | distributed trace or sequence diagram | tracing backend |
| Caller-side latency histogram per hop with bucket boundaries | metric names, labels, bucket config | metrics catalogue |
| Measured p95 per hop and end to end over the SLO window, with request counts | dashboard export | metrics backend |
| Client timeout, retry count and backoff per hop; deadline-propagation setting | service config | repositories |
| Fan-out stages: N parallel calls and how the stage waits | code or trace | owning teams |
| Perf environment description and load tool (k6, Locust, Gatling, wrk) | environment doc + script | platform |
| Named reviewer on the owning team | roster | team lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/dev/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: total is the user-facing SLO, percentiles do not add, fan-out tightens child percentile, every hop measured, timeouts and retries fit the hop, histogram buckets at thresholds, executable CI gate, budget reconciled with measured p95 | 1800 |
| `content/02-output-contract.xml` | essential | Draft-07 schema: SLO with percentile, threshold, measurement point and window; composition verified against the end-to-end histogram (>= 1000 requests), never by adding percentiles; hops with caller-side histogram, owner, budget beside measured p95 with underwater tickets and slack justification, bucket at threshold, timeout x attempts within budget, deadline propagation, fan-out N with stricter child percentile; reserve line; percentile-only CI gate with command, environment, >= 200 requests, failure action; no agent-enabled blocking; valid + invalid examples, forbidden patterns | ~4900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 1200 |
| `content/04-procedure.xml` | essential | 8 steps: pin the SLO and measurement point, instrument every hop caller-side, record fan-out and tighten the child percentile, allocate beside measured p95 with a reserve, fit timeouts and retries and propagate deadlines, bucket at each threshold, verify against the end-to-end histogram, write the gate and hand to the reviewer | ~1850 |
| `content/05-examples.xml` | recommended | Complete allocation of an 800 ms p95 checkout SLO across five hops (12-shard fan-out, underwater pricing hop, justified slack, 100 ms reserve, k6 gate), a note per non-obvious value, and a bad allocation with the validator output | ~2850 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/output.md.j2` | Spec skeleton matching the schema in 02-output-contract.xml |
| `templates/output.md` | Spec skeleton matching the schema in 02-output-contract.xml Generated from `templates/output.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in canonical example for calibration |
| `templates/_smoke-test.md` | Filled-in canonical example for calibration Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-latency-budget-allocation.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[performance-budget-design]]
- [[perf-budget-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
