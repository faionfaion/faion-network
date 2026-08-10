# The Three-Tier Verification Ladder
**Layer:** 4 — Reliability · **Verdict:** 🟢 take — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

The whole of Layer 4 collapses into one operational question: *for this specific failure, what is the cheapest instrument that can detect it?* The ladder answers it. Its value is not that the rungs are novel — it is that it forbids the expensive mistake everyone makes, which is reaching for a model to catch a defect a regex would have caught for free.

For a non-technical solopreneur the ladder is also the only affordable shape: rung 1 costs nothing and runs forever; rung 2 costs a few dollars a month; rung 3 costs attention, which is the scarcest thing they have.

## What it is

Three rungs, ordered by cost, run in order, each one only handling what the rung below provably cannot:

| Rung | Name | Instrument | Tokens | Wall-clock | Determinism |
|---|---|---|---|---|---|
| **1** | Static artefact lint | Code reading bytes | **0** | ms–seconds | Exact. Same input → same verdict, forever |
| **2** | Trigger evals | One model call per case, mechanically-checkable answer | ~1–6k in / ~200–800 out per case | seconds–minutes (parallel) | Stochastic input, **exact scoring** |
| **3** | Behavioural evals with an LLM judge | Model call + judge call per case | ~4–12k per case | minutes | Stochastic input, **stochastic scoring** |
| **(H)** | Human review gate | A person, reading | 0 | minutes–hours of *your* time | Exact-ish, unrepeatable, unscalable |

The rungs are not a maturity model. You do not "graduate" from rung 1 to rung 3. A healthy system is ~85% rung 1 by check count, ~14% rung 2, and a handful of rung 3 cases you could name from memory.

## Mechanics

---

### Rung 1 — Static artefact lint

**Definition.** A check expressible as a total function `artefact_bytes → {pass, fail, finding[]}` with no reference to a model, a network, or a human's opinion.

**What it catches.** Empirically, most of what actually breaks in a knowledge-artefact system:

- Required sections missing; forbidden sections present
- Unfilled placeholders — `TBD`, `TODO`, `<slug>`, `XXX`, `Lorem`
- ID format violations — hash not `^[a-f0-9]{16}$`, slug not kebab-case
- **Referential integrity — a `methodology_refs` / `playbook_refs` entry pointing at a slug that does not exist.** This is our single most frequent real defect class (see the recorded `phantom-methodology-slug` scar: A-writers invent non-existent slugs; nothing validated existence).
- Schema/frontmatter violations: field present, type right, length within bounds, enum member valid
- Tier-manifest consistency: every path gated, no path gated twice, no orphan
- Cross-artefact invariants: every INDEX entry resolves to a file; every file appears in exactly one INDEX
- Range violations a grammar cannot express: `score ∈ [0,1]`, `len(why) ≤ 240`
- Mechanical prose defects: quote-pair balance, duplicate parentheticals, description length outside 140–160 chars

**What it cannot catch.** Anything requiring meaning. A methodology that is well-formed, correctly cross-referenced, tier-gated, and *wrong*. A ranking that returns 20 valid IDs, none of them useful. Prose that is grammatical and vacuous. Rung 1 verifies the artefact is *shaped* like a good one.

**Cost.** 0 tokens. `check-structural.py` on an article: sub-second. A full corpus sweep across 2,622 methodologies: seconds to low minutes, entirely I/O-bound. Marginal cost of an extra check: near zero. **This is the only rung whose cost does not scale with how often you run it**, which is why it belongs in the pre-commit hook.

**Implementation sketch for our stack.**

*We already have this rung and have not noticed.* `faion-network/scripts/` holds **20** deterministic validators: `validate-methodology-v2.py`, `-xml`, `-scripts`, `-templates`, `-decision-tree`, `validate-playbook-v2/v3`, `validate-playbook-taxonomy.py`, `validate-tier-playbook.py`, `validate-workflow-v2.py`, `validate-domain-index.py`, `validate-domains-index.py`, `audit-index-coverage.py`, `f066-validate-all.sh`, `check-review-tools.sh`, plus the `build-*`/`regen-*` scripts that fail on malformed input. `faion-net-fe/scripts/` adds `check-structural.py`, `check-ai-tells.py`, `check-glossary-coverage.py`, `check-languagetool.py`, `.vale.ini`.

Three concrete moves:

1. **One entry point.** `make lint` in faion-network running all 20 in sequence with a single exit code. Today the knowledge of which validators exist and in what order lives in a human's head and in `f066-validate-all.sh`, which is not obviously canonical. A non-technical operator cannot run 20 scripts; they can run one.
2. **Add the missing referential-integrity check** — every `methodology_refs`/`playbook_refs` slug must resolve against `tier-manifest.json`. This is the phantom-slug defect and it is currently caught by an *agent* in phase B/C, i.e. at rung 3 prices, for a rung-1 defect. Moving it down one rung is the highest-leverage single change available.
3. **Port the artefact-shape checks that guard the binary into Go** so they run in `go test` and in CI without Python: score range, `why` rune-length, ID format, tier-gate zero-leak, `maxItems`. Python stays for the corpus; Go owns anything that protects the shipped binary.

Sketch:

```go
// internal/search/validate.go — rung 1, zero tokens
func ValidateResult(r Result, cands map[string]Entry, userTier Tier) []Finding {
    var f []Finding
    for i, h := range r.Hits {
        if _, ok := cands[h.ID]; !ok {
            f = append(f, Finding{Sev: High, Rule: "hallucinated-id", At: i, ID: h.ID})
        }
        if h.Score < 0 || h.Score > 1 {
            f = append(f, Finding{Sev: High, Rule: "score-out-of-range", At: i})
        }
        if len([]rune(h.Why)) > 240 {
            f = append(f, Finding{Sev: Med, Rule: "why-overflow", At: i})
        }
    }
    for _, p := range r.Playbooks {
        if !TierAllows(userTier, p.Tier) {
            f = append(f, Finding{Sev: Critical, Rule: "tier-leak", ID: p.ID})
        }
    }
    return f
}
```

---

### Rung 2 — Trigger evals

**Definition.** Run the real system on a realistic request and assert **mechanically** on what it selected. The model is in the loop; the *scoring* is not. The answer is an ID, a set, a boolean, a rank — something comparable with `==`.

**The question it answers:** *does the right thing fire at all?* Not "is the output good" — "did the system reach for the correct methodology / skill / workflow when a real user asked a real question".

**What it catches.**

- Retrieval regressions: a prompt edit, a corpus addition, or a model version bump silently drops the correct methodology out of the top-5
- Trigger failures: a query that should surface `spec-structure` surfaces nothing, or surfaces `perf-test-basics`
- Hallucinated IDs at a measurable *rate* rather than as a log line
- Tier leaks under realistic load (rung 1 catches the shape; rung 2 catches it happening on real queries)
- Transport divergence: the same query returning materially different rankings on `claude` vs `codex` vs `gemini` vs HTTP
- Empty-result regressions on queries that used to work

**What it cannot catch.** Whether the methodology it correctly retrieved is any *good*. Whether the `why` explanation is honest. Whether the ranking *order* within a correct set is sensible beyond what your labels encode. Rung 2 is only as smart as the labels, and the labels are binary.

**Cost.** One model call per case. For `faion search`, the payload is the query plus the candidate list — call it **2–6k input tokens** and **200–800 output tokens** per case. A 50-case suite ≈ 150–300k input tokens ≈ **single-digit dollars at Sonnet-class rates, ~10× that at Opus-class**. Wall-clock at concurrency 8: **1–3 minutes**. Cheap enough for a nightly run and for every prompt change; too slow and too costly for a pre-commit hook.

**Implementation sketch for our stack.**

Asset first, harness second. `evals/queries.yaml`, hand-labelled, in git:

```yaml
- id: q001
  query: "how do I write a spec before coding"
  tier: solo
  relevant: [a3f2c1b9d8e7f0a1, 5f01aa2b3c4d5e6f]   # hash IDs, binary relevance
  must_not_return: []
- id: q002
  query: "мій RAG галюцинує, як зловити"
  tier: pro
  relevant: [9c1d...]        # non-English trigger coverage
```

Runner — Promptfoo `exec:` around the real binary (see `eval-harnesses.md`), or plain `go test`:

```yaml
# evals/promptfooconfig.yaml
providers:
  - id: faion-cli
    exec: ./evals/run-search.sh      # $1=prompt, $2=options JSON, $3=context JSON
tests: file://queries.yaml
defaultTest:
  assert:
    - type: python                    # deterministic scorer, no judge
      value: file://score.py          # returns {pass, score, reason}
```

`--no-cache` in CI, always: Promptfoo's disk cache has a **14-day TTL** and keys on the provider call, so a rebuilt binary would otherwise be scored against a fortnight-old response.

Scoring, computed in Go so it is shippable and assertable (formulas from `groundedness-and-citations.md`):

```
Recall@5  = |Rel ∩ Top5| / |Rel|
nDCG@10   = DCG@10 / IDCG@10,  DCG@k = Σ (2^rel_i − 1)/log2(i+1)
MRR       = mean over queries of 1/rank(first relevant)
hallucinated_id_rate = Σ|Emitted \ Candidates| / Σ|Emitted|
tier_leak_rate       = must be exactly 0
```

**Prerequisite that blocks everything:** `internal/search/agent.go:270` currently discards hallucinated IDs into `logger.Warn`. Nothing counts them, so no assertion can exist. Surface a counter on `Result` first; the eval suite is unbuildable until then.

**Baseline reality check:** all 14 test files in `internal/search/` (2,868 lines) are plumbing. `regression_test.go` tests XML marshalling. `agent_test.go` drives a mock whose answer the test itself authored. **A ranking-quality regression cannot fail our suite today.** Rung 2 is not an enhancement; it is the missing floor.

---

### Rung 3 — Behavioural evals with an LLM judge

**Definition.** Run the system, then have a model judge whether the output still does what it did. Stochastic scoring of stochastic output.

**What it catches.** Only things with no mechanical ground truth: has the *character* of the output degraded — is the `why` still explanatory rather than tautological; does a workflow body still read as executable steps; did a prompt refactor quietly make output verbose, hedging, or generic.

**What it cannot catch — reliably.** Anything, at absolute scale. Per arXiv:2604.23178 (TMLR 2026), the best debiased configuration tested reaches **71.0% agreement with humans, κ = 0.549** — "moderate" on Landis–Koch, *below* any sane gating threshold. Style bias runs **0.10–0.76** (judges prefer markdown), while position bias is only **≤0.04**. Claude judges prefer *concise* output (−0.12), which flatters our house style — a comfortable bias is the dangerous kind.

**Cost.** System call + judge call: **~4–12k tokens per case**, plus the human cost of writing and calibrating the rubric, plus **50 hand-labelled pairs** before any number it produces means anything. Wall-clock: minutes. The real cost is not tokens; it is that each rung-3 case is a small ongoing maintenance obligation. **Realistic budget: 5–15 scenarios total, ever.** If you have 40, you have not built a rung-3 suite, you have built a slow rung-2 suite with a random number generator in it.

**Implementation sketch for our stack.**

Pairwise, never absolute. Champion/challenger on a prompt change:

```
for each of ~10 canonical queries:
    A = search(query, prompt=champion)
    B = search(query, prompt=challenger)
    normalise_formatting(A); normalise_formatting(B)   # style bias is the big one
    verdict_1 = judge(query, A, B)
    verdict_2 = judge(query, B, A)                      # order swap, cheap
    if verdict_1 != mirror(verdict_2): record as UNDECIDED, do not count
report: win / loss / undecided counts + the judge's stated reasons
```

Ship rule: report the *distribution*, never a mean. A challenger that wins 7, loses 1, and is undecided on 2 is a promotion. A challenger with "average score 4.2 vs 4.0" is noise with a decimal point.

Borrow the rubric shape from `faion-net-fe/scripts/rubrics/uk-quality.yaml` — enumerated criteria, per-finding severity, `--max-high 0`. **Do not borrow the fail-open**: `llm-judge.py:175` returns `[]` on `JSONDecodeError`, converting every judge malfunction (refusal, truncation, rate-limit prose) into a clean pass. Any rung-3 check we write must emit a synthetic high-severity `judge-parse-failure` finding instead.

---

### Rung H — Human validation gates, honestly

The user's point deserves a straight answer rather than a knowing smile.

**A person reading the output with their eyes is a legitimate verification instrument.** For a solopreneur it is often the *best* one: it has the highest ceiling on judgement quality of anything in this document, it needs no infrastructure, and it is the only instrument that can notice a problem you did not think to check for. Every rung above is an attempt to *buy back* human attention, not to replace human judgement.

But the word has to be used precisely. When we say a check is **deterministic**, we mean: same input → same verdict, repeatable by a machine, at any hour, at zero marginal cost, in CI, on a branch nobody is watching. Human review is:

- **Reliable** — a good reviewer catches things no rung catches
- **Not repeatable** — the same person reading the same artefact twice, tired, produces different verdicts
- **Not scalable** — it costs the scarcest resource the business has
- **Not automatable** — it cannot gate a 3 a.m. CI run
- **Not a regression test** — it cannot tell you that something *changed*, only whether the thing in front of you is acceptable

So: **"human validation gate" is a valid gate and an invalid substitute for the word "deterministic."** Calling manual review deterministic is not wrong about its *value*, it is wrong about its *properties* — and the property that matters operationally is repeatability without you. The honest formulation for our docs: *"manual review gate — highest judgement quality, zero repeatability, cost measured in founder-hours."* State the cost in the same breath as the value and the tradeoff becomes obvious rather than contentious.

**The rule that makes human review compound instead of repeat:** every time human review catches something, ask *"which rung could have caught this?"* and push it down. A slug that does not exist → rung 1 validator. A wrong methodology surfaced → a new labelled row in `queries.yaml`, rung 2. A vaguer tone after a prompt edit → a rung-3 scenario, or accept that you will re-read it. Human review is where new checks are *discovered*; it should not be where the same check is *repeated*.

---

## The placement rule

For any check you want to add, ask three questions in order and stop at the first "yes".

> **Q1. Can this be decided by reading the artefact's bytes, with no model and no reference to what a reasonable person would have wanted?**
> → **Rung 1.** Write it as code. No exceptions, no "but a model would be easier to write" — a model is never easier to *maintain*.
>
> **Q2. Does it need the real system to run, but the correct answer is mechanically comparable — an ID, a set, a rank, a boolean, a count?**
> → **Rung 2.** Write a labelled case. The label is the asset; the harness is replaceable.
>
> **Q3. Does it need a judgement about quality with no mechanical ground truth?**
> → **Rung 3 — but only if you would personally re-read this scenario before every release anyway.** If you would not, it is not important enough to pay for a judge. Delete it or accept the risk explicitly.
>
> **Anything left over is Rung H.** Read it yourself, and when it catches something, push a new check down to Q1 or Q2.

**The corollary, which is the actual discipline:** a check may only live on a rung if it *cannot* live on the rung below. Every check on rung 2 that a regex could do is a check that runs 1000× less often than it should, for money. Every check on rung 3 that an `==` could do is a coin flip you are paying for.

**Two anti-patterns to name explicitly:**

- **Rung inflation** — reaching for the fanciest available instrument because it is the most interesting to build. The phantom-slug defect is our live example: caught by an agent at rung 3, when a 20-line `validate-refs.py` at rung 1 would catch it every time, for free, in the pre-commit hook.
- **Rung deflation** — writing an elaborate deterministic check for something that genuinely requires judgement, then watching it produce false positives until everyone learns to ignore it. `check-structural.py` handles this correctly and is worth copying: it separates **HARD** findings (block, some auto-fixable) from **FLAG** findings (report, do not block — "heuristics with false-positive risk"). A rung-1 check that must guess should *flag*, never block.

## Cadence

| Rung | When it runs | Who can run it |
|---|---|---|
| 1 | Pre-commit hook + every CI run + `make lint` on demand | Anyone, including a non-technical operator |
| 2 | Nightly, and on every change to a prompt / the corpus / a model pin | CI, or `make eval` |
| 3 | Before a release; on a champion/challenger prompt decision | You, deliberately, with the token bill in view |
| H | On anything new, and on anything rung 1–3 flagged as ambiguous | You |

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | Judging the Judges (arXiv:2604.23178, TMLR 2026) | https://arxiv.org/abs/2604.23178 | 71.0% agreement / κ=0.549 ceiling; style bias 0.10–0.76 vs position ≤0.04; Claude verbosity −0.12 — the empirical basis for rung 3's low ceiling | 2026-08-03 |
| 2 | The Format Tax (arXiv:2604.03616) | https://arxiv.org/html/2604.03616 | 92% of degradation from the prompt instruction, not the decoder; two-pass recovers +6.8 pp — why rung-2 scoring must stay outside the model | 2026-08-03 |
| 3 | The Structured Output Benchmark (arXiv:2604.25359) | https://arxiv.org/abs/2604.25359 | Near-perfect schema compliance vs **83.0%** value accuracy on text — the gap rung 1 cannot see and rung 2 exists to measure | 2026-08-03 |
| 4 | Promptfoo — Configuration reference | https://www.promptfoo.dev/docs/configuration/reference/ | Deterministic vs model-graded assertion split; test-case and assertion shapes — the rung 1/2 vs rung 3 boundary, in YAML | 2026-08-03 |
| 5 | Promptfoo — Custom script provider | https://www.promptfoo.dev/docs/providers/custom-script/ | `exec:` provider, three argv args — how a Go binary becomes testable | 2026-08-03 |
| 6 | Promptfoo — Caching | https://www.promptfoo.dev/docs/configuration/caching/ | 14-day TTL, `~/.promptfoo/cache`, `--no-cache` — the CI foot-gun | 2026-08-03 |
| 7 | Citations — Claude Platform Docs | https://platform.claude.com/docs/en/build-with-claude/citations | Verbatim citations × structured-outputs 400 — a rung-1-detectable API constraint | 2026-08-03 |
| 8 | `faion-network/scripts/` (local, 20 validators) | — | Rung 1, already built: `validate-methodology-*`, `validate-playbook-*`, `validate-domain*`, `audit-index-coverage.py`, `f066-validate-all.sh` | 2026-08-03 |
| 9 | `faion-net-fe/scripts/check-structural.py` (local) | — | The reference rung-1 implementation: HARD-vs-FLAG severity split; docstring states it runs before any LLM review "so the model never burns an iteration on a mechanically-detectable defect" | 2026-08-03 |
| 10 | `faion-cli/internal/search/` (local, 14 test files, 2,868 lines) | — | The baseline: all plumbing, zero ranking regression; `agent.go:270` `logger.Warn` on hallucinated IDs | 2026-08-03 |

## What to borrow for faion

Ordered by leverage, highest first:

1. **Count hallucinated IDs instead of logging them** (`agent.go:270`). One field on `Result`. Unblocks every rung-2 assertion. Nothing else on this list is possible first.
2. **`validate-refs.py`** — every `methodology_refs`/`playbook_refs` slug resolves against `tier-manifest.json`. Rung 1, ~20 lines, catches our most frequent live defect, currently paid for at rung-3 prices.
3. **`make lint` in faion-network** — one entry point over all 20 validators. Makes rung 1 operable by a non-technical person, which is the actual product thesis.
4. **`evals/queries.yaml`** — 30 hand-labelled queries with binary relevance, covering EN + UA, all four tiers, and at least one query per knowledge domain. The labels are the durable asset; the harness is not.
5. **`internal/search/validate.go`** — the Go rung-1 checks the JSON Schema grammar cannot express (score range, `why` rune-length, tier leak). See sketch above.
6. **HARD vs FLAG severity, copied from `check-structural.py`** — a rung-1 check that must guess flags, never blocks. This is the discipline that keeps a lint suite trusted.
7. **Fail closed everywhere.** Codify: *a gate that cannot evaluate must not report pass.* Fix `llm-judge.py:175` as the first instance.
8. **The placement rule itself**, written into the corpus as a decision leaf. It is the most transferable thing in Layer 4 and it is not a tool — it is exactly the kind of thing Faion sells.

## What NOT to borrow — and why

- **Do not build rung 3 first.** It is the most interesting and the least valuable. With no rung 1 referential-integrity check and no rung 2 at all, a judge suite would be an expensive opinion about a system whose basic invariants are unverified.
- **Do not put rung 2 or 3 in the pre-commit hook.** Costs money and minutes per commit; you will disable it within a week and then you have nothing.
- **Do not ship any rung's machinery inside the binary.** No runtime Python, no runtime judge, no runtime eval. All three rungs are dev-time. The user's machine runs `faion search`, full stop.
- **Do not let rung 1 block on heuristics.** Diacritic-density, em-dash density, register-mixing — these are FLAG-tier in `check-structural.py` for good reason. A blocking check with false positives trains you to bypass the gate, which costs more than the check ever saved.
- **Do not gate on any rung-3 absolute score.** κ ≈ 0.55. Pairwise win/loss/undecided, or nothing.
- **Do not call manual review "deterministic."** Call it a manual review gate, state that it costs founder-hours and does not repeat, and let the tradeoff be visible.
- **Do not let the eval suite grow without a budget.** Every rung-2 case is a recurring token cost and a label to maintain; every rung-3 case is a rubric to recalibrate. A 200-case suite nobody runs is worth less than a 30-case suite that runs nightly.

## Mapping to our corpus

| Slug | Domain | Action |
|---|---|---|
| `quality-gates-confidence` | sdd | **Primary home for the ladder.** Add the three rungs, the placement rule, the fail-closed rule, and the honest treatment of manual gates |
| `lint-autofix-vs-flag-decision-rule` | sdlc-ai | Direct sibling — HARD vs FLAG is the same decision, one rung down. Cross-link and reconcile |
| `lint-precommit-floor` | sdlc-ai | Defines what belongs in the hook: rung 1 only. Add the explicit prohibition on rungs 2–3 |
| `lint-staged-only-not-whole-tree` | sdlc-ai | Cadence detail for rung 1 at scale |
| `eval-driven-development-tdd-for-ai` | ai-core | Add the ladder as the cost model underneath EDD; add "plumbing tests are green by construction" |
| `ci-eval-gate-config` | sdlc-ai | Rung 2's CI shape; add the Promptfoo `--no-cache` foot-gun |
| `regression-eval-before-fix-rule` | sdlc-ai | Reinforces rung 2 as the floor; directly applicable to the `agent.go:270` work |
| `judge-calibration-protocol` | ai-core | Rung 3's entry requirement — no judge without κ |
| `model-eval-control-bands` | ai-core | Where rung-2 and rung-3 thresholds are defined; add "no baseline → no gate" |
| `ai-feature-eval-set-design`, `eval-set-stratified-sampling-recipe`, `verbatim-to-eval-row-recipe` | ai-core | The rung-2 labelling pipeline, already present — reuse rather than rewrite |
| `eval-contract-template` | ai-core | Add `hallucinated_id_rate` and `tier_leak_rate` as named contract terms |
| `test-property-based-llm-invariants` | sdlc-ai | Rung 1 for LLM output — natural home for the Go post-validation list |
| `rag-bench-harness-template` | ai-core | Rung 2 template; add the `exec:`-a-binary pattern |
| `mutation-testing-bootstrap`, `test-mutation-feedback-loop` | sdlc-ai | The honest way to find out whether rung 1 catches anything: mutate an artefact, see if the lint trips |
| `hallucination-attribution-checklist`, `llm-hallucination-test-patterns` | ai-core | Rung-2 metric definitions |

Gaps — no leaf covers: **(a) the cheapest-instrument placement rule itself; (b) fail-open vs fail-closed for LLM-backed gates; (c) "manual review is a gate but not a deterministic one".** All three are new leaves and all three are Faion-shaped: portable judgement, not tool trivia.

## Open questions / staleness risk

- **Low staleness.** The ladder is an economic argument about relative instrument cost, and that ordering (bytes < one model call < two model calls < human hours) is stable. The *numbers* inside rungs 2 and 3 will drift with token prices and judge quality; the ordering will not.
- **The rung-3 ceiling is the one thing that could move.** If judge–human agreement rises materially above κ ≈ 0.55, rung 3 becomes gate-worthy and the ladder's top gets cheaper. Plausible within 12 months. Re-check `judge-calibration-protocol` annually.
- **We have no baselines for anything.** Every threshold in this file — `hallucinated_id_rate ≤ 0.02`, `Recall@5 ≥ 0.8`, `κ ≥ 0.6` — is a placeholder. The first eval run replaces guesses with numbers, and only then should any of them gate.
- **Unmeasured: what fraction of our real defects rung 1 would actually catch.** The claim that it is "a large share" is inference from the recorded scar tissue (phantom slugs, dropped `methodology_refs` in translation, description overflow, quote-closer mismatches, wrapper-artifact leaks, `needs-review` status blocks) — every one of those is rung-1-shaped. That is strong circumstantial evidence, not a measurement. A mutation-testing pass over the corpus would turn it into one.
- **Open:** should `faion eval` be a hidden subcommand of the shipped binary (simplest `exec:` shim) or a separate `cmd/faion-eval`? Leaning separate — the artefact users run should not carry its own grader.
- **Open:** whether rung 2 should assert on *ranking order* or only on *set membership* in the top-k. Set membership is robust and labellable today; order requires graded relevance and a labelling protocol we would get wrong. Start with membership; revisit once we have 100+ labelled queries.
