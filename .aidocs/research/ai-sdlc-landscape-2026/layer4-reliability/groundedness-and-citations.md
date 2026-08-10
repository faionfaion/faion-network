# Groundedness and Citations
**Layer:** 4 — Reliability · **Verdict:** 🟡 take the idea, not the tool — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

The idea — *every claim carries a machine-checkable pointer back into a source you supplied* — is the strongest reliability primitive in the 2026 stack, and it is nearly free for us because `faion search` already returns pointers (hash IDs) rather than prose. The tool — Anthropic's Citations API — we cannot use in our hot path, because it is a hard 400 against structured outputs. That is not a workaround-able conflict; it is a design fork.

## What it is

Three distinguishable things, usually sold as one:

1. **Forced citation at the decoder** — the provider emits, alongside each text block, an explicit reference into the source material with exact offsets. The model cannot "cite" something you did not give it, because the citation is an index, not a string. Anthropic Citations API; `search_result` content blocks.
2. **Post-hoc groundedness scoring** — take a generated answer and a context, decompose the answer into atomic claims, and check each claim for entailment against the context. Score = supported/total. RAGAS faithfulness, Vectara HHEM, Bespoke-MiniCheck.
3. **Retrieval-side grounding** — never let the model author an identifier at all; make it *select* from a supplied set, then validate the selection against that set. Zero-token, exact, no false positives. This is what our CLI already does, and it is strictly stronger than (1) or (2) for the ID-emitting part of our output.

Most of the RAG-reliability literature is about (1) and (2) because most RAG systems generate prose. We mostly generate a ranked list of IDs. Our exposure to hallucination is therefore *structurally smaller* than a chatbot's — but it is not zero, and it is currently unmeasured.

## Current state

### Anthropic Citations API (2026-08-03)

| Property | Value |
|---|---|
| Status | GA on the standard Messages API. **No beta header.** |
| Model support | All active models support citations. `search_result` blocks: all active models **except Claude Haiku 3**. |
| Clouds | Claude API; Vertex AI; Bedrock (per model availability) |
| Enablement | `citations: {"enabled": true}` set **per content block** (per `document` / per `search_result`), not globally per request |
| Cost | `cited_text` is **not counted toward output tokens**. You pay input tokens for the documents you supply, as normal. |
| Compatible with | prompt caching, token counting, batch processing |
| **Incompatible with** | **structured outputs — hard 400** |

**The incompatibility, verbatim from the official docs (fetched 2026-08-03, `platform.claude.com/docs/en/build-with-claude/citations`, "Warning" block):**

> **Citations and structured outputs are incompatible**
>
> Citations cannot be used together with [structured outputs](/docs/en/build-with-claude/structured-outputs). If you enable citations on any user-provided document (`document` blocks or `search_result` blocks) and also include the `output_config.format` parameter (or the deprecated `output_format` parameter), the API returns a 400 error.
>
> This is because citations require interleaving citation blocks with text output, which is incompatible with the strict JSON schema constraints of structured outputs.

**Confirmed, not refuted.** Provenance note: this warning was *added* to the Citations guide as a result of GitHub issue anthropics/claude-code#19417 (filed 2026-01-20, requesting the missing notice; the issue is closed and labelled `invalid`/`documentation`). The Structured Outputs guide as fetched on 2026-08-03 still does **not** carry the reciprocal warning — so if you only read that page, you will not learn this. It is documented in exactly one direction.

The mechanism explains why no workaround exists at the API level: citations are emitted as a `citations` array attached to *interleaved text blocks*. A grammar-constrained JSON output has no text blocks to attach to. Any "both" design must be two calls.

### Local groundedness scorers (2026-08-03)

| Tool | License | Size / cost | Speed | Reported accuracy |
|---|---|---|---|---|
| **Vectara HHEM-2.1-Open** | **Apache 2.0** | 0.1B params, ~600 MB RAM at fp32 | **~1.5 s per 2k-token input on a modern x86 CPU** | Balanced accuracy: AggreFact-SOTA **76.55%**, RAGTruth-Summ **64.42%**, RAGTruth-QA **74.28%**. Unlimited context (HHEM-1.0 was capped at 512 tokens). Released 2024. |
| Vectara HHEM-2.3 (commercial) | Proprietary, Vectara platform only | API | — | Higher accuracy, 10+ languages, not self-hostable |
| **Bespoke-MiniCheck-7B** (Llama-3.1-Bespoke-MiniCheck-7B) | **CC BY-NC 4.0 — NON-COMMERCIAL** (commercial licence available on request) | 7B BF16 | >500 docs/min on a single A6000 | SOTA on LLM-AggreFact (29k instances, 11 datasets). EMNLP 2024, Tang et al. |
| MiniCheck-Flan-T5-Large | (same family) | 0.8B | CPU-feasible | Below the 7B, above the DeBERTa variant |
| MiniCheck-DeBERTa-v3-Large / RoBERTa-Large | (same family) | 0.4B | CPU-feasible | Lowest of the family |
| RAGAS `Faithfulness` | Apache 2.0 (library) | LLM calls | seconds + $ per sample | Metric, not a model — cost is whatever judge you point it at |
| RAGAS `FaithfulnesswithHHEM` | Apache 2.0 | wraps HHEM-2.1-Open | CPU | Local, no judge cost |

**Correction to the prior pass:** Bespoke-MiniCheck-7B is **CC BY-NC 4.0**. The "~100× cheaper than a GPT-4-class factuality judge" claim comes from the MiniCheck paper's cost analysis and is credible on compute grounds, but the licence makes it **unusable in a commercial product** without a negotiated licence from Bespoke Labs. For Faion — a paid CLI — that is disqualifying for anything shipped, and legally murky even for a dev-time gate that informs a commercial product. HHEM-2.1-Open (Apache 2.0) has no such problem and should be the default choice.

## Mechanics

### Citations request shape (`document`, exact)

```jsonc
{
  "model": "claude-opus-5",
  "max_tokens": 1024,
  "messages": [{
    "role": "user",
    "content": [
      {
        "type": "document",
        "source": { "type": "text", "media_type": "text/plain",
                    "data": "The grass is green. The sky is blue." },
        "title": "My Document",
        "context": "This is a trustworthy document.",
        "citations": { "enabled": true }
      },
      { "type": "text", "text": "What color is the grass and sky?" }
    ]
  }]
}
```

### `search_result` content block (the RAG-native form)

```jsonc
{
  "type": "search_result",
  "source": "https://example.com/article",   // REQUIRED — URL or any identifier
  "title": "Article Title",                  // REQUIRED
  "content": [                               // REQUIRED — array of text blocks
    { "type": "text", "text": "…" }
  ],
  "citations": { "enabled": true }           // optional, per-block
}
```

Placeable in two positions: (a) returned from a **custom tool call**, for dynamic RAG; (b) directly as **top-level content in a user message**, for pre-fetched content. No special prompting required — ask the question and citations appear.

### Citation object returned (`search_result_location`)

```jsonc
{
  "type": "search_result_location",
  "cited_text": "All API requests must include an API key…",
  "source": "https://docs.company.com/api-reference",
  "title": "API Reference - Authentication",
  "search_result_index": 0,
  "start_block_index": 0,
  "end_block_index": 1
}
```

| Field | Type | Meaning |
|---|---|---|
| `type` | string | always `"search_result_location"` |
| `source` | string | echoed from the search result |
| `title` | string \| null | echoed from the search result |
| `cited_text` | string | full text of `content[start_block_index:end_block_index]` joined. **Not counted toward output tokens.** |
| `search_result_index` | int | 0-based index among *all* `search_result` blocks in the request, in appearance order across all messages and tool results |
| `start_block_index` | int | 0-based index of first cited block within that result's `content` |
| `end_block_index` | int | exclusive end index; always > `start_block_index` |

**Granularity rule — the design lever nobody notices:** *the text block is the minimal citable unit.* Claude cites whole blocks, never substrings. To get finer-grained citations you must **split your `content` array into smaller blocks**. Chunking strategy *is* citation precision. A single 4,000-word block yields one useless citation covering everything.

(For plain `document` blocks the citation type is `char_location` with `start_char_index`/`end_char_index` for text, `page_location` with `start_page_number` for PDFs, and `content_block_location` for custom content — the offsets the prior pass described. `search_result` uses block indices, not char offsets.)

### Metric formulas — implementable in Go

**Faithfulness (RAGAS definition, verified 2026-08-03):**

```
Decompose the response into atomic claims c_1 … c_n.
For each c_i, decide entail(c_i, retrieved_context) ∈ {0,1}.

Faithfulness = |{ i : entail(c_i, ctx) = 1 }| / n          ∈ [0,1]
```

Example from the docs: a response with 2 claims of which 1 is supported → 0.5. `FaithfulnesswithHHEM(device="cpu", batch_size=10)` substitutes HHEM-2.1-Open for the entailment step, removing the judge cost.

**HHEM score:** `model.predict(pairs)` where `pairs: List[Tuple[premise, hypothesis]]`. Returns a scalar in [0,1] per pair; 0 = hypothesis unsupported by premise, 1 = fully factually consistent. It is a *classifier probability*, not a calibrated probability of truth — thresholds must be chosen on your own data.

**Balanced accuracy** (the metric HHEM and MiniCheck report — use it, not raw accuracy, because groundedness datasets are class-imbalanced):

```
BA = ½ · ( TP/(TP+FN) + TN/(TN+FP) )
```

**Our actual groundedness metric — ID grounding rate.** For a search response with emitted IDs `E` and candidate set `C`:

```
grounding_rate      = |E ∩ C| / |E|            (1.0 = perfect)
hallucinated_id_rate = 1 − grounding_rate
```

Zero tokens, zero model, exact, no false positives, no threshold to tune. Every RAG groundedness paper is an approximation of this check; we get the exact version for free because our output space is a closed set.

**Retrieval quality (needed for `eval-harnesses.md`, defined once here).** With graded relevance `rel_i` of the item at rank *i*:

```
DCG@k  = Σ_{i=1..k} (2^{rel_i} − 1) / log2(i + 1)
IDCG@k = DCG@k of the ideal (relevance-descending) ordering
nDCG@k = DCG@k / IDCG@k                        ∈ [0,1]

Recall@k    = |Rel ∩ TopK| / |Rel|
Precision@k = |Rel ∩ TopK| / k
MRR         = (1/|Q|) · Σ_q 1 / rank_q(first relevant)
```

For binary relevance `rel_i ∈ {0,1}` the DCG numerator collapses to `rel_i`, i.e. `DCG@k = Σ rel_i / log2(i+1)`. Use binary relevance for our first eval set — graded relevance requires a labelling protocol we do not have.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | Citations — Claude Platform Docs | https://platform.claude.com/docs/en/build-with-claude/citations | Full request/response shape for text/PDF/custom-content documents; per-block `citations.enabled`; **verbatim structured-outputs 400 warning**; prompt-caching interaction | 2026-08-03 |
| 2 | Search results — Claude Platform Docs | https://platform.claude.com/docs/en/build-with-claude/search-results | `search_result` block schema; two placement modes; `search_result_location` field table; "text block is the minimal citable unit"; `cited_text` not billed as output; all active models except Haiku 3 | 2026-08-03 |
| 3 | anthropics/claude-code issue #19417 | https://github.com/anthropics/claude-code/issues/19417 | Origin of the incompatibility warning; filed 2026-01-20; proposed text now shipped in doc #1 | 2026-08-03 |
| 4 | Vectara HHEM-2.1-Open model card | https://huggingface.co/vectara/hallucination_evaluation_model | Apache 2.0, 0.1B/600 MB, 1.5 s per 2k tokens on CPU, unlimited context, `predict()` API, AggreFact/RAGTruth balanced accuracy | 2026-08-03 |
| 5 | Bespoke-MiniCheck-7B model card | https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B | **CC BY-NC 4.0**, InternLM2.5-7B-Chat base, 35k training examples, LLM-AggreFact SOTA, >500 docs/min on A6000, smaller Flan-T5/DeBERTa/RoBERTa variants | 2026-08-03 |
| 6 | RAGAS Faithfulness | https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/ | Claim-decompose → entail → ratio formula; `FaithfulnesswithHHEM(device, batch_size)` | 2026-08-03 |

## What to borrow for faion

1. **Name what we already have.** `agent.go` validating every returned ID against `candByID` *is* a forced-citation mechanism with a 100%-precision verifier. Document it as `grounding_rate`, expose it on `Result`, and assert on it in tests. This is the borrow with the best cost/benefit ratio in Layer 4.
2. **Make `hallucinated_id_rate` a first-class metric, not a log line.** `internal/search/agent.go:270` currently does `logger.Warn("search: dropping hallucinated id", …)` and continues. Nothing counts it, so no test can fail on it and no user can see it. Minimum change: a counter on `Result`; better: `Result.Dropped []string` plus a `--verbose` line. Then a threshold assertion in the eval harness (`hallucinated_id_rate ≤ 0.02`).
3. **Borrow the chunking-is-citation-granularity insight for `get-content`.** If we ever surface *excerpts* of a methodology (a summary, a "why this one" quote), the unit we chunk at is the unit a user can verify at. Methodology bodies should be addressable at section granularity, not file granularity.
4. **Borrow the `search_result` shape as our own internal envelope**, even though we do not call the Citations API. `{source, title, content[]}` with a stable index is a good serialisation for the candidate list we already build — and if we ever *do* run a cited-prose feature, the payload is already in the right shape.
5. **If a cited-prose feature is ever wanted (e.g. `faion explain`), design it as two calls from day one:** call 1 = structured output → IDs (no citations); call 2 = citations-enabled prose over the bodies of those IDs (no `output_config.format`). The 400 forces this and it is a better design anyway — the ID selection stays machine-checkable, and the prose stays citable.
6. **HHEM-2.1-Open as a dev-time-only spot-checker** for any prose we generate about the corpus (marketing copy, methodology summaries). Apache 2.0, CPU, no cloud, no per-call cost. Run it in the faion-net-fe quality gate, never in the CLI.

## What NOT to borrow — and why

- **Do not put the Citations API in the `faion search` path.** It is a hard 400 with `output_config.format`, and dropping structured output to gain citations would trade a guaranteed-parseable ID list for prose we would then have to regex. Strictly worse.
- **Do not adopt Bespoke-MiniCheck in any form.** CC BY-NC 4.0 against a commercial CLI. The accuracy edge over HHEM is not worth a licence negotiation, and "we only used it at dev time" is a position we would have to defend rather than one we would enjoy.
- **Do not ship any groundedness scorer inside the binary.** HHEM is a PyTorch model; MiniCheck is a 7B. Both are runtime Python, both violate the single-binary mandate, and neither is needed — our ID-grounding check is exact and free.
- **Do not implement RAGAS faithfulness against our search output.** It is a metric for *generated prose over retrieved context*. We generate a ranked ID list. Applying claim-decomposition to `why` strings (≤240 chars of justification) would produce noise, cost judge tokens, and measure the wrong thing. The `why` field is a UX affordance, not a claim we stand behind.
- **Do not treat HHEM's ~64–77% balanced accuracy as a gate.** A scorer that is wrong a quarter to a third of the time is a *triage aid*, not a pass/fail. Use it to rank things for human attention, never to block.
- **Do not confuse `cited_text` being free with citations being free.** You pay full input tokens for every document you attach. Attaching the corpus to get citations would be ruinous; attaching the ~3–10 bodies the user actually selected is fine.

## Mapping to our corpus

| Slug | Domain | Action |
|---|---|---|
| `citation-contract-back-to-source` | sdlc-ai | **Closest existing leaf.** Update with the `search_result_location` field table and the "minimal citable unit = text block" rule; add the structured-output 400 as a named constraint |
| `hallucination-attribution-checklist` | ai-core | Add the closed-set variant: when the output space is a supplied set, attribution is set-membership, not entailment |
| `hallucination-detection-online` | ai-core | Add HHEM-2.1-Open with its 2026-08-03 specs; add the MiniCheck licence warning |
| `llm-hallucination-test-patterns` | ai-core | Add `grounding_rate` / `hallucinated_id_rate` formulas |
| `hallucination-incident-runbook` | ai-core | Cross-link: a spike in `hallucinated_id_rate` is the trigger |
| `rag-eval-generation-metrics` | ml-engineering | Add the exact RAGAS faithfulness formula + `FaithfulnesswithHHEM` |
| `rag-eval-retrieval-metrics` | ml-engineering | Add the nDCG@k / Recall@k / MRR formulas verbatim as written above |
| `rag-failure-taxonomy` | ml-engineering | Add "well-formed but non-existent identifier" as a distinct failure class |
| `ai-iac-hallucination-detector` | sdlc-ai | Sibling pattern; cross-link |

Gap — no leaf covers: **"closed-set generation: when your output space is enumerable, validate by membership and skip the whole groundedness stack"**. That is the most Faion-shaped idea in this dossier and it is missing from 2,622 methodologies.

## Open questions / staleness risk

- **Medium-high staleness on the incompatibility.** It is a stated implementation limitation with an obvious commercial reason to fix (every RAG product wants both). If Anthropic ships citation-aware structured output, re-plan the `faion explain` design. Re-verify quarterly; the canonical location is the Warning block in doc #1.
- The Structured Outputs guide does not carry the reciprocal warning as of 2026-08-03. If we build against the Structured Outputs page alone we will rediscover this by 400 in production. Worth a comment in our transport code citing the Citations page.
- HHEM-2.1-Open's benchmark numbers are from 2024 and the model has not been refreshed in the open line (2.3 is commercial-only). Its performance on 2026-era model outputs is unknown and probably worse than reported — newer models hallucinate differently.
- Unverified: whether `search_result` blocks are billed differently from `document` blocks. Docs state `cited_text` is not billed as output; input-side billing of `search_result` content is assumed to be standard input tokens but not explicitly confirmed.
- We have **no baseline** for our own `hallucinated_id_rate`. Every recommendation in this file about thresholds (≤2%) is a guess until the first eval run. Treat the threshold as a placeholder, not a target.
