# Eval Harnesses
**Layer:** 4 — Reliability · **Verdict:** 🟢 take — Promptfoo, dev-time only, via the `exec:` provider · **Verified:** 2026-08-03

One harness in this market can test a **compiled binary** instead of a Python function call. That is Promptfoo, and it is the only one that fits a Go single-binary product. The rest — DeepEval, Braintrust, LangSmith — are library-shaped: they want to wrap *your call*, which means your call has to be in their language. Sub-verdicts: Promptfoo 🟢, DeepEval 🔴, Braintrust 🔴, LangSmith 🔴, "write our own Go test harness" 🟡 (probably where we end up for rung 2).

## What it is

An eval harness is three things bolted together, and the vendors differ mostly in which of the three they actually sell you:

1. **A test-case runner** — cartesian product of prompts × providers × test cases, with concurrency, caching, and retries.
2. **An assertion library** — deterministic (string/regex/JSON/script) and model-graded (rubric, factuality, faithfulness).
3. **A results store and UI** — diffs between runs, regression detection, sharing, dashboards.

(1) and (2) are commodity and open-source. (3) is the product. Every paid tier in this market is selling (3). For a solopreneur running evals on their own machine, (3) is a `git diff` on a JSON file.

## Current state (all prices/licences verified 2026-08-03)

| Tool | Licence | Free tier | Paid | Shape | Runs our Go binary? |
|---|---|---|---|---|---|
| **Promptfoo** | **MIT** | Fully functional CLI, local, unlimited | Enterprise (undisclosed on site) | CLI + YAML config; "LLM evals run 100% locally — your prompts never leave your machine"; 23.9k GitHub stars; requires Node ≥ 22.22.0 (24 LTS recommended) | **Yes — `exec:` provider runs any binary** |
| **DeepEval** (Confident AI) | Open source (Apache-2.0 family; not stated on pricing page) | OSS library free | Confident AI cloud: **Free** (2 seats, 1 project, 5 test runs/week, 1 GB-month spans) · **Starter $200/mo** (unlimited seats, 5 projects, 5 GB-months, $1/GB-month overage) · **Team $2,000/mo** (SSO, RBAC, SOC2, 75 GB-months) · Enterprise custom | pytest-native Python library | No — you call it from Python |
| **Braintrust** | Proprietary | **Starter $0**: $10 model credits/mo, 1 GB processed data/mo (+$4/GB), 10k scores/mo (+$2.50/1k), **14-day retention**, unlimited users | **Pro $249/mo**: $249 credits, 5 GB (+$3/GB), 50k scores (+$1.50/1k), 30-day retention, custom charts, RBAC. Enterprise: custom, self-hosting **Enterprise-only** | SDK + hosted platform | No |
| **LangSmith** | Proprietary | **Developer $0**: 1 seat, 5,000 base traces/mo, community support | **Plus $39/seat/mo**: 10,000 base traces/mo, unlimited seats. Overage: LCU $1.50/unit, LSU $1.00/unit. Enterprise: self-hosted/hybrid, SSO, ABAC/RBAC | SDK + hosted platform | No |

**Corrections to the prior pass:**

- **DeepEval/Confident AI is not $19.99/user/mo.** As of 2026-08-03 the ladder is Free → **$200/mo** → **$2,000/mo** → Enterprise, and it is *per-workspace with unlimited seats*, not per-seat. The pricing model changed shape, not just price. Anyone budgeting off the old number is off by 10×.
- Braintrust Pro **$249/mo — confirmed.** LangSmith Plus **$39/seat/mo — confirmed.**
- The "14-day" figure appears in *two* places and they are different things: Promptfoo's **cache TTL** is 14 days, and Braintrust's **free-tier data retention** is 14 days. Do not conflate.

### Promptfoo and OpenAI

The GitHub README states, verbatim (read 2026-08-03):

> "Promptfoo is now part of OpenAI. Promptfoo remains open source and MIT licensed."

The repo still lists OpenAI, **Anthropic (Claude)**, Azure, Bedrock, Ollama, Google (Gemini) and DeepSeek among supported providers, plus custom providers in arbitrary languages, and the marketing site still leads with "Zero vendor lock-in". The acquisition (reported ~2026-03-09, ~$86M — *this figure is press-reported, not confirmed by either party, and I could not verify it directly; treat as unsourced*) does not appear to have changed the licence or removed competitor providers.

**The vendor-neutrality question, honestly:** MIT is irrevocable for the code that exists today, so the downside risk is not "they take it away" — it is **drift**. New assertion types, new provider features, and bug-fix priority will plausibly favour the OpenAI stack over time, and Anthropic-specific features (e.g. `output_config.format` semantics, citation blocks) may lag. Our mitigation is structural and costs nothing: **we use Promptfoo only as a runner around our own binary via `exec:`.** We never let it wrap a provider call. In that configuration Promptfoo does not know or care which model we use — it sees a subprocess and a string — so provider drift cannot reach us, and if the project ever goes bad we can replace the runner with ~200 lines of Go and keep the YAML.

## Mechanics

### `promptfooconfig.yaml` — exact top-level shape

```yaml
description: string                 # optional
prompts:  <string | array | object> # REQUIRED
providers: <array>                  # REQUIRED (or `targets:`)
tests: <path | inline array | generator>   # optional
defaultTest: <test-case>            # optional — merged into every test
scenarios: <array>                  # optional — groupings of tests + data
outputPath: <path>                  # optional
sharing: <bool | object>            # optional
env: <map>                          # optional — env var overrides
evaluateOptions:                    # optional
  cache: true                       # default true
  # concurrency, timeouts
extensions: <array>                 # optional — lifecycle hook files
metadata: <map>                     # optional
```

### Test case shape

```yaml
tests:
  - description: string
    vars:            # substituted into prompts; string | array | file path
      query: "how do I ship a feature"
    assert: [ <assertion>, … ]
    threshold: 0.8   # aggregate score threshold for pass/fail
    provider: …      # per-test provider override
    options:
      transform: <fn|script>      # mutate output before assertions
      transformVars: <fn|script>  # mutate vars before substitution
      prefix: / suffix: <string>
      disableVarExpansion: bool
```

### Assertion shape

```yaml
- type: <string>     # REQUIRED
  value: <string | array | number | object | function>
  threshold: <number>
  weight: <number>   # default 1
  metric: <string>   # label for aggregation across tests
  transform: <fn>    # mutate output for this assertion only
  provider: <string> # grader model, for model-graded types only
```

**Deterministic assertion types (no model call, free, instant):** `contains`, `equals`, `regex`, `is-json`, `javascript`, `python`, `cost`, `latency` — plus a `not-` prefix on any of them for negation.

**Model-graded types (cost a call, need `provider`):** `llm-rubric`, `factuality`, `answer-relevance`, `context-faithfulness`, `g-eval`.

The split matters: **model-graded assertions are opt-in per assertion.** A config with only deterministic asserts spends $0 and finishes in the time it takes your binary to run. This is what makes Promptfoo suitable for rungs 1–2 of the ladder.

### The `exec:` provider — why this tool and not the others

```yaml
providers:
  - 'exec: python chain.py'
  # or
  - id: faion-search
    exec: ./bin/faion search --json
```

Also usable from the CLI: `promptfoo eval -p prompt1.txt -r 'exec: python chain.py'`.

The script receives **three command-line arguments, in order**:

1. `prompt` — the rendered prompt string
2. `options` — JSON string of provider configuration
3. `context` — JSON string with test-case vars, metadata, evaluation info

Arguments, not stdin. It returns the API-call result on stdout. (The docs page fetched 2026-08-03 does not pin down whether the return must be a raw string or a JSON envelope with `output`/`tokenUsage`/`error`; the Python-provider page has the precise contract. **Open item — verify before writing the wrapper.**)

For us this means a ~15-line shell or Node shim: take `$1` as the query, call `./bin/faion search "$1" --json --tier "$TIER"`, echo stdout. The harness never touches an API key. It never sees a model name. It tests the artefact users actually run.

### Caching

- Enabled by default. Disk-based at `~/.promptfoo/cache`. Memory-backed when `NODE_ENV=test`.
- **Default TTL: 14 days.**
- Env vars: `PROMPTFOO_CACHE_ENABLED`, `PROMPTFOO_CACHE_TYPE` (`disk`|`memory`), `PROMPTFOO_CACHE_PATH`, `PROMPTFOO_CACHE_TTL` (seconds).
- CLI: `--no-cache` on `promptfoo eval`; `promptfoo cache clear`.
- Caveat for us: caching keys on the provider call. With an `exec:` provider the cache will happily serve a stale result after we rebuild the binary. **Always `--no-cache` in CI, or clear the cache in the build step.** This is a real foot-gun and not documented as one.

### Metric formulas the harness must compute (we implement these, not Promptfoo)

For a query *q* with a hand-labelled relevant set `Rel(q)` and our returned top-*k* ID list:

```
Recall@k    = |Rel(q) ∩ TopK(q)| / |Rel(q)|
Precision@k = |Rel(q) ∩ TopK(q)| / k
MRR         = (1/|Q|) · Σ_q  1 / rank_q(first relevant)

DCG@k  = Σ_{i=1..k} (2^{rel_i} − 1) / log2(i + 1)
IDCG@k = DCG@k of the relevance-descending ideal ordering
nDCG@k = DCG@k / IDCG@k                                  ∈ [0,1]
```

With binary relevance the DCG numerator is just `rel_i`. **Start binary.** Graded relevance needs a labelling protocol (what is a "2" vs a "1"?) that we do not have and would get wrong.

Two more that are specific to us and cost nothing:

```
hallucinated_id_rate = Σ_q |Emitted(q) \ Candidates(q)| / Σ_q |Emitted(q)|
tier_leak_rate       = Σ_q |{hits above user tier}| / Σ_q |Emitted(q)|     # must be exactly 0
```

`tier_leak_rate` is a **security** metric wearing an eval costume. It should be a Go unit test with a hard zero, not a harness metric — but it belongs in the same eval set because the eval set is where realistic queries live.

## Our current state — the honest baseline

`~/workspace/projects/faion-net/faion-cli/internal/search/` has **14 test files, 2,868 lines**, and **zero ranking regression tests**:

- `regression_test.go` (135 lines) is named for regression but tests `MarshalXML` round-tripping of the `Result` envelope — structural, not behavioural.
- `agent_test.go` (562 lines) drives the agent through a mock dispatcher. The mock's response is authored by the test, so the assertions confirm that our *plumbing* forwards and filters what we told it to forward and filter. That is worth having. It cannot fail when ranking quality degrades.
- `testdata/` holds `golden_search.xml` and `golden_search_workflow.xml` — golden *renderings*, not golden *rankings*.
- Consequence: **a change to the ranking prompt, the candidate-selection logic, or the model version cannot fail our test suite.** The suite is green by construction on exactly the axis that matters to a user.

Existing deterministic validators in `faion-network/scripts/` — **20 of them** (the prior estimate of ~15 was low), all dev-time Python:

`validate-methodology-v2.py`, `validate-methodology-xml.py`, `validate-methodology-scripts.py`, `validate-methodology-templates.py`, `validate-methodology-decision-tree.py`, `validate-playbook-v2.py`, `validate-playbook-v3.py`, `validate-playbook-taxonomy.py`, `validate-tier-playbook.py`, `validate-workflow-v2.py`, `validate-domain-index.py`, `validate-domains-index.py`, `audit-index-coverage.py`, `f066-validate-all.sh`, `check-review-tools.sh` + the `build-*`/`regen-*` scripts that fail on malformed input.

**This is already rung 1 of the ladder, built and running.** We do not need to invent static artefact linting — we need to notice we have it, point it at the *right* artefacts, and give it a single entry point.

The prose gate at `~/workspace/projects/faion-net/faion-net-fe/scripts/` (`check-structural.py`, `check-ai-tells.py`, `check-glossary-coverage.py`, `check-languagetool.py`, `.vale.ini`, `llm-judge.py` + `rubrics/`) is excellent and **is not an agent eval**. It scores MDX prose for an editorial pipeline. Reusing its *architecture* (deterministic step 0 before any LLM step — `check-structural.py`'s own docstring says it "Runs as step-0 of phase D / phase G BEFORE any LLM review, so the model never burns an iteration on a mechanically-detectable defect") is the borrow. Reusing its *code* would be a category error.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | Promptfoo — GitHub | https://github.com/promptfoo/promptfoo | "Promptfoo is now part of OpenAI. Promptfoo remains open source and MIT licensed."; provider list incl. Anthropic; "evals run 100% locally"; Node ≥22.22.0; 23.9k stars | 2026-08-03 |
| 2 | Promptfoo — Configuration reference | https://www.promptfoo.dev/docs/configuration/reference/ | Full YAML key list, test-case shape, assertion object shape, deterministic vs model-graded assertion type lists | 2026-08-03 |
| 3 | Promptfoo — Custom script provider | https://www.promptfoo.dev/docs/providers/custom-script/ | `exec:` declaration forms; the three argv arguments (prompt, options JSON, context JSON) | 2026-08-03 |
| 4 | Promptfoo — Caching | https://www.promptfoo.dev/docs/configuration/caching/ | Default on; `~/.promptfoo/cache`; **14-day TTL**; `PROMPTFOO_CACHE_*` env vars; `--no-cache`, `promptfoo cache clear` | 2026-08-03 |
| 5 | Promptfoo homepage | https://www.promptfoo.dev/ | "Zero vendor lock-in", 300,000+ developers, on-prem/cloud, CI/CD integrations | 2026-08-03 |
| 6 | Confident AI pricing | https://www.confident-ai.com/pricing | Free / **$200** / **$2,000** / Enterprise; seat and GB-month limits; overage $1/GB-month | 2026-08-03 |
| 7 | Braintrust pricing | https://www.braintrust.dev/pricing | Starter $0 (14-day retention) / **Pro $249/mo** / Enterprise; score and GB overage rates; self-hosting Enterprise-only | 2026-08-03 |
| 8 | LangSmith pricing | https://www.langchain.com/pricing-langsmith | Developer $0 (5k traces, 1 seat) / **Plus $39/seat/mo** (10k traces) / Enterprise; LCU $1.50, LSU $1.00 | 2026-08-03 |

## What to borrow for faion

1. **Promptfoo as a dev-time runner around `./bin/faion` via `exec:`.** Never as a provider wrapper. This keeps us model-agnostic, keeps API keys out of the harness, and tests the shipped artefact. Node is a dev dependency, which the mandate explicitly permits; nothing enters the binary.
2. **Deterministic-first assertion discipline, copied from our own `check-structural.py`.** A test case's `assert` list should be ordered cheapest-first, and the model-graded assertions should be a separate config file that runs on a different cadence. Promptfoo makes this natural because model-graded types are opt-in.
3. **A single `evals/` directory in faion-cli** holding: `queries.yaml` (query → expected relevant IDs, hand-labelled), `promptfooconfig.yaml` (deterministic asserts via the `python`/`javascript` assert types calling a scorer), and a `Makefile` target. Version the labels in git; the label set *is* the asset, and it survives any harness we later replace.
4. **Compute nDCG@k / Recall@k / `hallucinated_id_rate` in Go**, exposed by a `faion eval` hidden subcommand or a `go test` in `internal/search/eval`. Promptfoo orchestrates; we own the metric. Metrics implemented in someone else's Python are metrics we cannot ship, cannot assert on in `go test`, and cannot explain.
5. **Borrow Braintrust's and LangSmith's *free* tiers as a comparison harness only** if we ever want a UI for a specific investigation. Never as infrastructure. Both free tiers are generous enough for a one-off.
6. **Borrow the pytest-native idea from DeepEval without the library:** eval cases should be `go test` cases, runnable with `go test ./internal/search/eval/...`, so they run in the same command as everything else and fail the same way.

## What NOT to borrow — and why

- **DeepEval / Braintrust / LangSmith as our harness — skip all three.** They are library- and SaaS-shaped: to use them, our call must be a Python or TypeScript function they can wrap. Ours is a Go binary. Wrapping it would mean reimplementing `faion search` in Python for the eval, which tests a replica and not the product — the worst possible outcome, because it can be green while the shipped binary is broken.
- **Do not pay for any of them at current scale.** $200/mo (Confident AI Starter) or $249/mo (Braintrust Pro) buys dashboards and retention for an eval suite that will run maybe weekly and produce a few hundred rows. `git` retains it for free, forever, with better diffs.
- **Do not let Promptfoo make the model calls.** The moment `providers:` contains `anthropic:claude-opus-5`, we have (a) put our API key in a Node process, (b) coupled our eval to Promptfoo's Anthropic client rather than our own four transports, and (c) exposed ourselves to exactly the vendor-drift risk the OpenAI acquisition creates. The `exec:` provider avoids all three.
- **Do not trust the Promptfoo cache in CI.** 14-day TTL + `exec:` provider = a rebuilt binary silently evaluated against a fortnight-old response. `--no-cache` in CI, always.
- **Do not reuse `faion-net-fe/scripts/llm-judge.py` as an agent eval.** It scores MDX prose against editorial rubrics. Different artefact, different failure modes, and it has a fail-open bug (`llm-judge.py:175` returns `[]` on `JSONDecodeError`) — see `llm-as-judge.md`.
- **Do not build a results UI.** It is the thing every vendor is selling and the thing a solopreneur needs least. A JSON file in git and `jq` covers it.
- **Do not add Node to the runtime.** Dev-time only, declared in a `devDependencies`-equivalent, never invoked by the binary.

## Mapping to our corpus

| Slug | Domain | Action |
|---|---|---|
| `rag-bench-harness-template` | ai-core | **Primary target.** Add the Promptfoo `exec:` pattern as a concrete template; add the nDCG/Recall formulas |
| `ci-eval-gate-config` | sdlc-ai | Add the `--no-cache` foot-gun; add deterministic-vs-model-graded cadence split |
| `eval-driven-development-tdd-for-ai` | ai-core | Cross-link the ladder; state the "plumbing tests are green by construction" failure mode |
| `ai-feature-eval-set-design` | ai-core | Add: label the *relevant set*, not the ranking; start binary-relevance |
| `eval-set-stratified-sampling-recipe` | ai-core | Reusable as-is for building `queries.yaml` |
| `eval-contract-template` | ai-core | Add `hallucinated_id_rate` and `tier_leak_rate` as contract terms |
| `rag-eval-retrieval-metrics` | ml-engineering | Add explicit formulas (currently unverified whether they are present) |
| `rag-eval-pipeline`, `rag-eval-strategy`, `rag-eval-test-set-generation` | ml-engineering | Reconcile — three overlapping leaves; this dossier is a chance to dedupe |
| `regression-eval-before-fix-rule` | sdlc-ai | Directly applicable to the `agent.go:270` counter work |
| `model-eval-control-bands` | ai-core | Where the threshold discipline lives (don't gate on a metric with no baseline) |
| `champion-challenger-pattern-rag` | ai-core | The pattern for evaluating a prompt change against the current prompt |

Gap — nothing covers **"evaluating a compiled binary rather than a library call"**, which is the whole reason Promptfoo wins for us. New leaf.

## Open questions / staleness risk

- **Unverified: the exact return contract of the `exec:` provider** (raw stdout string vs JSON envelope with `output`/`tokenUsage`/`error`). Must be pinned before writing the shim. Check `promptfoo.dev/docs/providers/python/` for the sibling contract.
- **Unverified: the reported ~$86M Promptfoo acquisition price and the 2026-03-09 date.** The acquisition itself is confirmed by the repo README; the terms are press-reported and I could not reach a primary source. Do not cite the number.
- **Medium staleness on all four price tables.** SaaS eval pricing has moved repeatedly (Confident AI's model changed shape entirely since the prior pass). Re-verify before any purchase decision; assume anything older than a quarter is wrong.
- Promptfoo's Node ≥22.22.0 floor will drift. It is a dev dependency so the blast radius is a `.nvmrc`, but it does mean the harness has an independent upgrade cadence from the Go toolchain.
- Open design question: should `faion eval` be a hidden subcommand of the shipped binary (simplest for the `exec:` shim, but adds eval code to the product) or a separate `cmd/faion-eval` binary (cleaner, but two build targets)? Leaning separate binary — the shipped artefact should not contain its own grader.
- We have **no labelled query set at all**. Everything above is scaffolding around an asset that does not yet exist. The first 30 labelled queries are worth more than any harness choice.
