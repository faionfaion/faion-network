# Placement — Structured Output & Grounding
**Slice:** constrained decoding, format tax, forced citations, groundedness scorers, guardrails · **Author pass:** 7 of 10 · **Date:** 2026-08-04

## Already covered — do not duplicate

| Topic | Existing slug | Gap remaining |
|---|---|---|
| Mode picking (json / SO strict / tool-call / grammar) | `ai-agents/structured-output-mode-picker` | No `output_config.format`; no supported/unsupported keyword table |
| Provider-native SO + safe parse | `ml-engineering/structured-output`, `structured-output-basics` | `output_format` alias deprecated; no wire-vs-validation split |
| SO service, SLO, failover | `ml-engineering/structured-output-patterns` | No compliance ≠ value accuracy (83.0% text, arXiv:2604.25359) |
| Reason freeform, then extract | `ai-agents/two-pass-reason-then-extract` — **brief missed this one** | Causally **wrong**: blames the grammar mask. Format tax: 92% of degradations sit in the prompt instruction, before any decoder constraint |
| Schema hygiene | `strict-mode-required-fields`, `schema-field-order`, `enum-closed-vocabulary`, `regex-patterned-string-fields` | Adequate; the last misleads on Anthropic — `pattern` unsupported |
| Guardrails runtime | 7 `guardrails-*` slugs | Saturated. One caveat: a grammar constraint is not a validator |
| Forced citation | `sdlc-ai/citation-contract-back-to-source` (pro) | Faion-internal format only. No Citations API, no `search_result_location`, no 400 fork |
| Groundedness scoring | `ai-core/hallucination-*`, `ml-engineering/rag-eval-*` | No HHEM specs; no MiniCheck licence bar; no closed-set variant |

**Uncovered, all three:** the Citations × structured-outputs 400; the semantic-constraint gap; closed-set validation. The format tax is a **correction to an existing slug**, not a fifth slug.

## Verdict summary

| Approach | Verdict | Placement | Target path | Tier |
|---|---|---|---|---|
| Semantic-constraint gap | 🟢 take | New methodology | `knowledge/ai-agents/schema-semantic-constraint-gap` | **pro** |
| Closed-set output validation | 🟢 take | New methodology | `knowledge/ai-core/closed-set-output-validation` | **solo** |
| Citations API + 400 | 🟡 idea not tool | Rewrite existing | `knowledge/sdlc-ai/citation-contract-back-to-source` | pro (keep) |
| Format tax (arXiv:2604.03616) | 🟢 take | Correct + retier | `knowledge/ai-agents/two-pass-reason-then-extract` | geek → **pro** |
| HHEM / MiniCheck / RAGAS | 🟡 idea not tool | Amend existing | `knowledge/ai-core/hallucination-detection-online` | geek (keep) |
| Guardrails AI / NeMo | 🔴 skip | One caveat line each | `ml-engineering/guardrails-{basics,implementation,custom-pipeline}` | geek (keep) |
| Subagent output contracts | 🟢 take | Workflows ×5 | `workflows/` | n/a |

## Workflow changes

**W1 — `sdd-batch-orchestrator/templates/prompt-skeleton.md`, `## Output`.** Today: three equal options, "Pick exactly one". Replace with a ranked rule — **default = freeform report body + a machine-parsed last line**; whole-message JSON only for mechanical phases (RECAPTURE, file lists), never REVIEW, PLAN, or merge resolution. The existing `verdict=PASS|FAIL-WITH-NITS|FAIL` and `done=<id> commit=<sha>` markers are already the researched-correct shape; this makes that a rule with a reason instead of an accident.

**W2 — new `sdd-batch-orchestrator/content/11-subagent-output-contracts.xml`.** (a) *Reason before you format* — the contract lives in the tail `## Output` section, never the mission statement; an early format instruction compresses the visible reasoning channel (92% / +6.8 pp / arXiv:2604.03616). (b) *Post-validate in code* — markers regex-checked (`^done=[a-z0-9-]+ commit=[0-9a-f]{7,40}$`), verdicts enum-checked, never trusted for looking right. Register: row in `AGENTS.md` Content table; `catalog.json` → `content_files: 10 → 11` + version bump.

**W3 — `brainstorm/content/02-phases.xml`.** Phase 1 demands 30 recs in `state → problem → solution → impact` — a rigid format instruction on our most reasoning-heavy task, peak format-tax exposure. Add: personas think freeform, emit the four-field shape as a terminal pass. Phase 2's "consensus count MUST be an integer in [1, 10]" is exactly what no grammar compiles — orchestrator range-checks it.

**W4 — `poll-agents/content/03-state-shape.xml`, *Append patterns*.** Before writing `done=<slug>`, the parent MUST verify `slug ∈ popped-batch set`. Closed-set membership grounding, zero token cost — the workflow-native instance of N2.

**W5 — `media-ops/content/05-scaffold-structure.xml`.** `json_repair.py` defends a failure class constrained decoding removes. Keep it; add: the residual risk is *value* accuracy, not parse failure — spend review budget there.

## New content proposed

**N1 `ai-agents/schema-semantic-constraint-gap`** — **pro**. Produces a two-file schema pair: wire schema (Anthropic-supported keywords only) + validation schema (full Draft-7), with the post-validation checklist for every dropped keyword (`minimum`, `maximum`, `minLength`, `maxLength`, `pattern`, `maxItems`) and the transport-divergence note (Gemini's OpenAPI subset accepts `pattern`; Claude does not). Checked against all five SO slugs plus `strict-mode-required-fields`, `regex-patterned-string-fields` — none carries the table or the split. Registration: `AGENTS.md` + `CLAUDE.md` + `meta.json` + `content/{01-core-rules,02-output-contract,03-failure-modes,06-decision-tree}.xml` + `scripts/validate-*.py`, mirroring `ai-agents/context-graph-engineering/`; `scripts/regen-tier-manifest.py --diff` then write; hand-add the `<methodology slug=… tier="pro" path=…>` block to `ai-agents/INDEX.xml` alphabetically, bump `<index count="103">` → `104`; `scripts/validate-domain-index.py`; CHANGELOG under `## [Unreleased]`.

**N2 `ai-core/closed-set-output-validation`** — **solo**. Produces a validation contract: when the output space is enumerable, replace the groundedness stack with set membership — `grounding_rate = |E ∩ C| / |E|`, exact, zero tokens, no threshold. Includes the "is my space actually closed?" test and the anti-pattern of claim-decomposing a 240-char justification. Grep for `closed-set` / `candidate set` / `grounding_rate` across the four relevant domain INDEX files returns zero. Same registration steps against `ai-core/INDEX.xml`.

## Tier convention — follow or break

**Break it for the two new slugs.** All five SO slugs are geek; the reliability cluster is 42 geek / 9 pro / 6 solo; INDEX.md defect #6 already names this skew as inverted against our advantage. Reliability is the layer where competitors are empty — pricing our only empty-market content at $99 means nobody reads it.

Not "cheaper everywhere" but **scars low, engineering high**. N2 is one page, no code, and spares a solo user a RAGAS pipeline they never needed: solo. N1 turns a green schema check into a known-false signal — cheap to consume, expensive to discover, and it makes the geek content above it legible: pro. `structured-output-patterns`, `-mode-picker`, and the guardrails slugs stay geek. N4 follows: corrected and citable, "decouple reasoning from formatting" is a design rule, not an implementation.

## Rejected

- **A fifth SO slug** — five exist; everything new is a correction or a different shape.
- **New Guardrails AI / NeMo content** — seven slugs already, both runtime Python, irrelevant to a Go binary.
- **Bespoke MiniCheck** — CC BY-NC 4.0 against a commercial CLI; appears only as a licence warning.
- **Any groundedness scorer as a gate** — HHEM's 64–77% balanced accuracy is triage, not pass/fail.
- **A new playbook** — methodology-shaped concern. Cross-link from `build-ship`.
- **RAGAS faithfulness on our search output** — we emit a ranked ID list, not prose.

## Risks / conflicts with other slices

- **Pass 8 owns eval harnesses and LLM-as-judge.** `groundedness-and-citations.md` defines nDCG@k / Recall@k / MRR and the RAGAS formula, but those land in `knowledge/ml-engineering/rag-eval-retrieval-metrics` and `rag-eval-generation-metrics` — **their placement, not mine.** I claim only the HHEM/MiniCheck licence facts in `knowledge/ai-core/hallucination-detection-online`.
- **`knowledge/ai-core/llm-hallucination-test-patterns` (pro) is a live collision** — its `citation_verification` / `grounding_required` patterns are the natural home for `grounding_rate`, which N2 also defines. Split: N2 defines the metric, pass 8 packages the CI test class.
- **`knowledge/sdlc-ai/citation-contract-back-to-source`** may also be claimed by `layer5-domain/desk-research-with-citations.md`. Same file, different reasons — sequence the edits.
- **Tier moves** in N1/N2/N4 all shift `skills/tier-manifest.json`; a concurrent rebalance against defect #6 would conflict. One regen, one commit.
- **Existing drift:** `sdd-batch-orchestrator/AGENTS.md` says `version: 2.0.0`, `workflows/catalog.json` says `1.0.0`. W2 touches the catalog — reconcile both in one commit.
- **`scripts/build-domain-index-v2.py` must not be run** by anyone touching these INDEX.xml files; every step above is hand-edit + `validate-domain-index.py`.
