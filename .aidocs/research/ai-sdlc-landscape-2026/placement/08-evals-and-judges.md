# Placement — Evals & Judges
**Slice:** three-tier ladder, Promptfoo, DeepEval/Braintrust/LangSmith, LLM-as-judge, golden sets · **Author pass:** 8 of 10 · **Date:** 2026-08-04

## Already covered — do not duplicate

| Topic | Existing slug(s) | Gap remaining |
|---|---|---|
| Golden-set curation, stratification, incident growth | `golden-set-curation-and-maintenance`, `agent-eval-test-set-curation`, `eval-set-stratified-sampling-recipe`, `ai-feature-eval-set-design`, `verbatim-to-eval-row-recipe` | **None.** Five leaves |
| nDCG@k / Recall@k / MRR | `rag-eval-retrieval-metrics`, `evaluation-metrics` | Formulas present, RAG-chunk framing. Refresh: label the relevant **set**, binary relevance first |
| Harness → CI gate | `agent-eval-harness-bootstrap-recipe`, `rag-bench-harness-template` | Both assume the SUT is a Python/TS **function** to wrap. Nothing covers a shipped **binary/CLI** via subprocess |
| Judge rubric design | `llm-judge-rubric-evidence-first` | **Omits style bias, leads with position (≤0.04).** Refresh |
| Judge calibration, κ | `judge-calibration-protocol` | Ships at κ ≥ 0.7 — the best debiased 2026 judge (κ=0.549) never clears it. Refresh: pairwise triage instead |
| Pairwise / champion-challenger | `champion-challenger-pattern-rag`, `prompt-engineering-evaluation` | Covered |
| Cost cadence, control bands, drift | `agent-eval-cost-budget-policy`, `ci-eval-gate-config`, `model-eval-control-bands`, `eval-driven-development-tdd-for-ai`, `eval-in-prod-sampling-policy`, `agent-drift-detection-statistical` | Covered. One line into `ci-eval-gate-config`: 14-day cache TTL → `--no-cache` in CI |
| Lint floor / autofix-vs-flag / staged-only | `lint-precommit-floor`, `lint-autofix-vs-flag-decision-rule`, `lint-staged-only-not-whole-tree` | Refresh `lint-precommit-floor`: no model-calling gate in the hook |
| Broken refs in AI-written docs | `ai-orphan-link-detection` (classifies `methodology-slug-unknown`) | Crawls link bodies, not **frontmatter ref fields against a manifest**. Extend it; no new slug |
| Tool/vendor selection | `technology-evaluation-rubric`, `vendor-eval-pilot-template` | Covered. Prices go stale in a quarter — keep them out |
| Gate levels L1–L6 | `sdd/quality-gates-confidence` | **Phase-promotion** gates. No per-check instrument routing, no fail-closed rule, no rung H |

**Honest answer: the placement rule and the fail-closed rule are the only genuine gaps.** The rest is refresh.

## Verdict summary

| Approach | Verdict | Placement | Target path | Tier |
|---|---|---|---|---|
| Three-tier ladder (placement rule) | 🟢 | new methodology + 4 workflow edits | `knowledge/sdlc-ai/verification-rung-placement-rule` | **solo** |
| Fail-open vs fail-closed gates | 🟢 | new methodology (one rule) | `knowledge/sdlc-ai/gate-fail-closed-rule` | **free** |
| Rung H — manual review, honestly | 🟢 | folded into the ladder | — | solo |
| Promptfoo via `exec:` | 🟢 | new playbook | `playbooks/optimize-tune/wire-a-trigger-eval-suite-around-a-cli` | **pro** |
| DeepEval / Braintrust / LangSmith | 🔴 | one shape-comparison line in the playbook, **no prices** | — | — |
| LLM-as-judge (style bias, κ) | 🟡 | refresh 2 slugs | `llm-judge-rubric-evidence-first`, `judge-calibration-protocol` | stays geek |
| Golden sets, nDCG/recall | 🟢 | refresh 1 slug | `rag-eval-retrieval-metrics` | stays geek |

## Workflow changes

**W1 — `improver/content/02-phases.xml`, Phase 5 (Log).** New `<rule>`: every `ERR-NNN` records `rung:` — the cheapest instrument that could have caught it (1 lint / 2 trigger eval / 3 judge / H manual) — plus, when rung ≤ 2, a `check:` naming the validator to write. Manual review is where checks are *discovered*; without the field the same defect is re-discovered every session. Worked example: 528 broken `methodology_refs`/`playbook_refs` across 5,744 MDX files (18,107 refs, 69 phantom slugs) caught by a phase-B/C **agent** — rung-3 prices for a defect a ~20-line validator catches free.

**W2 — `improver/content/05-anti-patterns.xml`, new section "Rung inflation".** NEVER dispatch a subagent to decide something readable from an artefact's bytes. NEVER let a rung-1 check *block* on a heuristic — heuristics FLAG, exact rules block (`check-structural.py`'s HARD/FLAG split); a blocking check with false positives trains the operator to bypass the gate.

**W3 — `improver/content/03-decision-tree.xml`, Routing rules.** For `"audit X"` / `"fix the issues"`, run available rung-1 validators **before** dispatching any investigation subagent, and treat their output as Phase 1 findings. Replaces the implicit "Phase 1 = subagents".

**W4 — `idea-to-prod/content/20-phases.xml`, Phase 6 (Validate)** — names no instrument today. Add an ordered, stop-at-first-failure sequence: rung 1 (lint + hooks, 0 tokens) → rung 2 (labelled trigger cases, only if the project ships LLM-backed selection) → rung H (operator reads) → rung 3 only if the operator would re-read that scenario before every release anyway. Bound it: **5–15 rung-3 scenarios, ever.** One `decisions.xml` entry, 2026-08-04, `topic="validate-by-cheapest-instrument-first"`.

**On `success_criteria` frontmatter across all six workflows — no.** They assert workflow *completion* ("outputs land on disk") and are rung-1-shaped already; the ladder there touches six files for zero behaviour change. One note instead: `improver`'s "Phase 0 runs on every invocation" is not checkable from bytes and is therefore not a gate.

## New content proposed

**1. `verification-rung-placement-rule`** — `sdlc-ai`, **solo**. Produces a Rung Placement Record: each check classified by the three-question rule (bytes only → 1; real system, mechanically-comparable answer → 2; judgement without ground truth → 3; else H), plus the corollary *a check may live on a rung only if it cannot live on the rung below*, HARD/FLAG discipline, the healthy mix (~85% rung 1 by count), and rung H stated straight — highest judgement ceiling, zero repeatability, cost in founder-hours; a manual review gate is valid, "deterministic" is the wrong word for it. Ships `scripts/validate-verification-rung-placement-rule.py`. Distinct from `quality-gates-confidence` (phase promotion), `lint-autofix-vs-flag-decision-rule` (what to do with a finding, not which instrument found it), `eval-driven-development-tdd-for-ai` (when to write an eval, not whether an eval is the right tool), `agent-eval-cost-budget-policy` (cadence inside rungs 2–3), `model-eval-control-bands` (thresholds).

**2. `gate-fail-closed-rule`** — `sdlc-ai`, **free**. One rule: *a gate that cannot evaluate must not report pass.* Failure taxonomy (parse error, refusal, truncation, rate-limit prose, empty result) and the fix — emit a synthetic high-severity `judge-parse-failure` finding so the existing threshold trips, rather than raising and changing every caller. Live examples: `llm-judge.py:175` returns `[]` on `JSONDecodeError` → exit 0, so a dead judge and a clean article are indistinguishable; `scripts/f066-validate-all.sh` always exits 0 and Vale is configured but never invoked. `fail-closed` appears in the corpus only in `ml-engineering/guardrails-*`, about runtime requests — never eval gates.

**3. Playbook `wire-a-trigger-eval-suite-around-a-cli`** — `playbooks/optimize-tune/`, **pro**. Done = labelled `queries.yaml` in git, `promptfooconfig.yaml` with an `exec:` provider around the shipped binary, deterministic asserts only, `--no-cache` in CI, baseline recorded. Covers why the harness must run the shipped artefact, not a re-implementation — a replica suite goes green while the product is broken, and our 14 `internal/search/*_test.go` files are all plumbing with the mock's answer authored by the test, so ranking cannot regress-fail today; the `exec:` three-argv contract; the 14-day cache foot-gun; one line on DeepEval/Braintrust/LangSmith — library- and SaaS-shaped, cannot test a compiled binary, out regardless of price. Promptfoo is MIT and local-only; note the OpenAI acquisition and the mitigation — use it only as a subprocess runner, never as a provider wrapper, and provider drift cannot reach you. Checked all 23 `optimize-tune` playbooks; none stands up an LLM-output eval suite.

**Registration, all three:** dir + `AGENTS.md` (no frontmatter) + `CLAUDE.md` + `meta.json` + `content/NN-*.xml` → `scripts/regen-tier-manifest.py` → **hand-add** the `<methodology slug= tier= path=>` / `<playbook>` entry with `<summary>` to `knowledge/sdlc-ai/INDEX.xml` (`count="91"` → 93) and `playbooks/by-goal/optimize-tune/INDEX.xml`. **Never run `build-domain-index-v2.py`** — it reads frontmatter absent from all 2,623 methodology `AGENTS.md`; `--write` wipes the index.

**Refreshes (bump `last_reviewed`, no new slugs):** `llm-judge-rubric-evidence-first` — style bias (0.10–0.76) first, position (≤0.04) last, per-family verbosity signs incl. Claude −0.12 with the warning that a bias aligned with your house style is the dangerous kind, and "normalise formatting before judging". `judge-calibration-protocol` — Landis–Koch bands, the κ=0.549 / 71.0% ceiling, below κ 0.6 a judge is triage not a gate, report win/loss/undecided never a mean. `rag-eval-retrieval-metrics` + `eval-contract-template` — `hallucinated_id_rate` and `tier_leak_rate` as contract terms. `ci-eval-gate-config` — `--no-cache`. `lint-precommit-floor` — rung 1 only in the hook. `ai-orphan-link-detection` — extend to frontmatter ref fields.

## Tier call

**Ladder solo, fail-closed free, playbook pro; refreshes stay geek.** The cluster is 42 geek / 9 pro / 6 solo and reliability is the layer where competitors are empty, so the expensive rungs stay paid. But rung 1 costs zero tokens and is the only part a non-technical operator can run on day one; pricing the judgement that *saves* money at $99 sells it to people who already own it. `gate-fail-closed-rule` is free as the hook into the paid material — the free→solo→pro shape pass 1 used. Rung 1 is the only free reliability content.

## Rejected

A "Promptfoo methodology" — tool config is playbook material. Any slug encoding DeepEval/Braintrust/LangSmith pricing — the earlier $19.99 figure was off by 10× ($200/mo), which is the argument for never encoding prices. A golden-set methodology — five exist. A judge-bias methodology — belongs in the existing rubric slug. A rung-H slug — one section of the ladder. Eval machinery inside the CLI: no runtime Python, no runtime judge, no `faion eval` in the shipped binary. `g-eval` as a default — absolute scores, the shape we say not to gate on. The Kendall τ 0.72–0.91 claim — unsourced.

**Content-sealing flag:** `queries.yaml` stores **query → expected ID list**, never methodology bodies, and the `exec:` shim echoes the CLI's own JSON. A harness that logs retrieved content into an eval artefact becomes a body-dumping side channel; IDs are also the cheaper, more durable asset.

## Risks / conflicts with other slices

- **Pass 7** owns the `output_config.format` fix for `llm-judge.py`'s `JSONDecodeError` path; I own only the fail-**open** half — a schema-valid empty array is still empty. Cross-reference, do not restate. Pass 7 also owns `hallucinated_id_rate` as a groundedness metric; I claim it only as an eval-contract term.
- **`knowledge/sdlc-ai/INDEX.xml`** — two additions here, pass 1 adds three. Merge entries, reconcile `count=` once.
- **`improver/content/{02-phases,03-decision-tree,05-anti-patterns}.xml`** — pass 1 edits `04-memory-files.xml`; different files, but both change the memory-entry shape (`rung:`/`check:` vs `confirmation:`/`unenforced`). Reconcile into one ERR/DEC schema.
- **`idea-to-prod/content/20-phases.xml` + `decisions.xml`** — passes 1–3 target this workflow too. Highest collision risk; my edit is confined to Phase 6.
- **`skills/tier-manifest.json`** — regenerated, never hand-edited; exactly one pass runs `regen-tier-manifest.py`, last.
