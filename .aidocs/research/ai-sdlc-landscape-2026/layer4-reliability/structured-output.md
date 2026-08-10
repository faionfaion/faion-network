# Structured Output (constrained decoding + schema contracts)
**Layer:** 4 — Reliability · **Verdict:** 🟢 take — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

Take it, but demote it. Constrained decoding buys you *shape*, and only shape. Every semantic constraint in our schema — the hash regex, the 0–1 score, `maxItems: 20`, `maxLength: 240` — is silently dropped by Anthropic's grammar compiler and must be re-checked in Go. Treat structured output as a parser you no longer have to write, not as a validator.

## What it is

Two distinct things that get conflated:

1. **A format instruction in the prompt** — "reply with JSON matching this schema". Free, works everywhere, and (per the 2026 format-tax literature) is where almost all of the reasoning damage happens.
2. **Constrained/grammar-guided decoding** — the provider compiles your JSON Schema into a grammar and masks the token distribution at each step so only schema-valid continuations are sampled. This is what makes `JSON.parse` never fail. Cheap in accuracy terms; the damage was already done by (1).

The industry shipped (2) between 2024 and 2026 and then discovered that (1) was the actual problem. That reframing is the single most important thing in this dossier.

## Current state

| Provider | Parameter | Status (dated) | Schema-compliance claim | Price delta |
|---|---|---|---|---|
| Anthropic Claude API | `output_config.format` (`{"type":"json_schema","schema":{…}}`); deprecated alias `output_format` | GA, Claude 4.5 and later. Beta header `structured-outputs-2025-11-13` **no longer required** (docs read 2026-08-03) | ~99% observed; Anthropic states "always valid / type safe" for the *supported* subset | $0 for the feature. Injects an extra system preamble → input tokens slightly higher |
| Anthropic on Bedrock | same | GA: Opus 5 / 4.8 / 4.7 / 4.6 / 4.5, Sonnet 5 / 4.6 / 4.5, Haiku 4.5 (2026-08-03) | — | $0 |
| Anthropic on Vertex AI | same | GA: Fable 5, Mythos 5, Opus 5/4.8/4.7/4.6/4.5, Sonnet 5/4.6/4.5, Haiku 4.5 (2026-08-03) | — | $0 |
| Anthropic strict tool use | `strict: true` on a tool definition | GA, same models | Guarantees valid tool *name* and *input* | $0 |
| OpenAI | `response_format: {type:"json_schema", json_schema:{…, strict:true}}` | GA since 2024-08 | 100% on their supported subset | $0 |
| Gemini | `response_mime_type` + `response_schema` (OpenAPI 3.0 subset) | GA | ~98% observed | $0 |

Prior-pass figures "~99% Anthropic / 100% OpenAI / ~98% Gemini" are directionally right but are **third-party observations, not vendor SLAs** — the vendors only guarantee compliance with the subset of JSON Schema they actually compile. Treat these as folklore-grade until we measure them on our own schema.

**Grammar caching (Anthropic, 2026-08-03):** compiled grammars are cached 24 h. Cache is invalidated by a change to the schema structure or to the tool set — **not** by changing `name`/`description`. First request after a schema change pays compile latency. Changing `output_config.format` also invalidates the *prompt* cache for that thread.

**Known operational failure:** "compiled grammar is too large" (anthropic-sdk-python issue #1185) for complex schemas. Our `search.json` is small; a future playbook-body schema might not be.

## Mechanics

### Anthropic request shape (exact, 2026-08-03)

```jsonc
{
  "model": "claude-opus-5",
  "max_tokens": 1024,
  "messages": [ /* … */ ],
  "output_config": {
    "format": {
      "type": "json_schema",
      "schema": { /* JSON Schema, supported subset only */ }
    }
  }
}
```

Go SDK:

```go
client.Messages.New(ctx, anthropic.MessageNewParams{
    Model:     anthropic.ModelClaudeOpus5,
    MaxTokens: 1024,
    OutputConfig: anthropic.OutputConfigParam{
        Format: anthropic.JSONOutputFormatParam{
            Schema: schema, // map[string]any
        },
    },
})
```

### JSON Schema subset — the part that decides our design

**Supported** (Anthropic, 2026-08-03): `object`, `array`, `string`, `integer`, `number`, `boolean`, `null`; `enum` (scalars only); `const`; `anyOf`; `allOf` (not with `$ref`); internal `$ref` / `$defs` / `definitions`; `required`; `additionalProperties: false` (must be `false`); `default`; string `format` ∈ {date-time, time, date, duration, email, hostname, uri, ipv4, ipv6, uuid}; `minItems` ∈ {0, 1}.

**NOT supported:**

- `minimum`, `maximum`, `multipleOf`
- `minLength`, `maxLength`, `pattern`
- `maxItems`; `minItems` other than 0 or 1
- recursive schemas; external `$ref`; complex types inside `enum`
- `additionalProperties` set to anything but `false`

The official SDKs (Pydantic/Zod helpers) *strip* unsupported keywords from the wire schema, fold them into the field `description` as prose, and re-enforce them client-side after parsing. That is exactly the behaviour we must replicate in Go by hand — the Go SDK will not validate for us.

**Consequence for `internal/search/schemas/search.json`:** every constraint that actually protects us is in the unsupported list.

| Constraint in our schema | Compiled into the grammar? | Must be enforced in Go |
|---|---|---|
| `id.pattern: ^[a-f0-9]{16}$` | ❌ | yes — and we already do, structurally (see below) |
| `score.minimum: 0` / `maximum: 1` | ❌ | **yes — currently NOT enforced** |
| `hits.maxItems: 20` | ❌ | yes — we clamp via `opts.Top` |
| `why.maxLength: 240` | ❌ | **yes — currently NOT enforced** |
| `additionalProperties: false` | ✅ | free |
| `required: [id, score, why]` | ✅ | free |
| `tier.enum: [free,solo,pro,geek]` | ✅ | free |

`agent.go` drops any hit whose `id` is not a key in `candByID`, which is a *stronger* check than the regex — an ID that is well-formed but not in the candidate set is still rejected. Good. Score range and `why` length are unguarded.

### The format tax — measured, dated, and decisive

**arXiv:2604.03616, "The Format Tax", Ivan Yee Lee, Loris D'Antoni, Taylor Berg-Kirkpatrick (UC San Diego), 2026-04-04.**

Design: separate the *format-requesting instruction* (call it `GET·`) from the *grammar-constrained decode* (`GETC`), and measure each independently across MATH-500 (500 competition-math problems), GPQA-Diamond (198 graduate science questions), ZebraLogic (500 constraint-satisfaction puzzles), WritingBench (500 open-ended writing tasks), over 6 open-weight models (Qwen, OLMo, SLM, Nemotron families) and 4 closed APIs.

Findings:

- **92% of statistically significant degradations (McNemar test) are already present in `GET·` — the prompt instruction alone, before any decoder constraint.** The grammar adds little further harm.
- Open-weight models: **−3.9 pp** average without GCD, **−5.8 pp** averaged across formats. Worst on MATH-500 and ZebraLogic.
- Closed-weight models: near-zero or *positive* deltas for Claude Haiku, Grok, GPT-5.4-nano. Older GPT-5-nano still −5.2 pp. **Frontier closed models have largely absorbed the tax.**
- Mitigation — **decoupled two-pass**: turn 1 answers freeform with no format instruction; turn 2 reformats. Recovers **+6.8 pp** on average, improving 42 of 72 model×task×format combinations.
- Alternative — **extended thinking** (hidden scratchpad, then format): **+9.2 pp** average, but a **15% worsening rate**; higher variance.

Mechanism the authors propose: a format instruction compresses the *visible* reasoning channel before the model has finished solving, so the model commits early.

**arXiv:2604.25359 is a different paper than the prior pass assumed.** It is *"The Structured Output Benchmark: A Multi-Source Benchmark for Evaluating Structured Output Quality in Large Language Models"*, Singh, Khurdula, Khemlani, Agarwal, submitted 2026-04-28. It is nonetheless the second-most important citation here, because it separates **schema compliance** from **value accuracy** (exact leaf-value match) across 21 frontier and open-weight models:

| Source domain | Value accuracy |
|---|---|
| Text (5,000 eval records from a 25,091-record corpus) | **83.0%** |
| Image (209 records, OCR'd PDFs) | 67.2% |
| Audio (115 records, conversation transcripts) | 23.7% |

Models achieve *near-perfect schema compliance* while getting one leaf value in six wrong on plain text. Longer context makes extraction substantially harder.

**This is the number to put on a slide.** "Valid JSON" and "correct JSON" differ by ~17 points on the easiest modality. A green schema check is not a green correctness check.

### Assessing our own scar tissue

Recorded observation: Anthropic Agent SDK with `output_format=json_schema` on Sonnet 4.5 omitted **required** fields roughly 30% of the time; production fix was plain text parsed into Pydantic.

Verdict on the prior pass's argument that the 2026 format-tax research retroactively makes text→parse the *correct* design rather than a workaround: **half right, and the half that is wrong matters.**

- **Right:** the format tax says the *instruction* is the cost, so "reason in prose, then structure" is a genuinely better shape than "structure while reasoning". Text→parse is a degenerate one-pass version of the recommended two-pass. Our production choice is defensible on principle, not just on superstition.
- **Wrong:** the format tax explains *accuracy* loss, not *required-field omission*. Under true constrained decoding a required field cannot be omitted — the grammar makes the closing brace unreachable until the field is emitted. A 30% omission rate is therefore evidence that the Agent SDK path was **not** applying grammar constraints (schema passed as a prompt instruction, or a soft/JSON-mode path), or that the request errored into a fallback. Blaming the format tax for it lets a real integration bug hide behind a paper.
- **Practical upshot:** do not generalise "SDK structured output is unreliable" into "the API's `output_config.format` is unreliable". They are different code paths. Measure ours; do not inherit the scar.

### Metric formulas we will implement in Go

Structured-output health, computed over an eval run of *N* search calls:

```
schema_valid_rate      = n_responses_parsing_and_validating / N
hallucinated_id_rate   = Σ ids_not_in_candidate_set / Σ ids_emitted
range_violation_rate   = Σ hits with score<0 or score>1 / Σ hits
overflow_rate          = Σ hits with len(why)>240 runes / Σ hits
empty_result_rate      = n_responses with len(hits)==0 / N
```

`hallucinated_id_rate` is the one that matters and the one we currently throw away into a `logger.Warn`.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | Structured outputs — Claude Platform Docs | https://platform.claude.com/docs/en/build-with-claude/structured-outputs | `output_config.format` shape, GA model list per cloud, supported/unsupported JSON Schema keyword lists, 24 h grammar cache, strict tool use, SDK snippets incl. Go | 2026-08-03 |
| 2 | Citations — Claude Platform Docs | https://platform.claude.com/docs/en/build-with-claude/citations | Verbatim warning that citations + `output_config.format` → 400 | 2026-08-03 |
| 3 | The Format Tax (arXiv:2604.03616) | https://arxiv.org/html/2604.03616 | Prompt-vs-decoder decomposition, 92% McNemar figure, per-family pp deltas, two-pass +6.8 pp / thinking +9.2 pp | 2026-08-03 |
| 4 | The Structured Output Benchmark (arXiv:2604.25359) | https://arxiv.org/abs/2604.25359 | Schema compliance vs value accuracy: 83.0 / 67.2 / 23.7% text/image/audio, 21 models | 2026-08-03 |
| 5 | Capacity, Not Format (arXiv:2606.09410) | https://arxiv.org/abs/2606.09410 | Reframes format cost as a capacity demand strong models absorb; delayed-structure ablation recovers most loss | 2026-08-03 (title/abstract only) |
| 6 | Decoupling Task-Solving and Output Formatting (arXiv:2510.03595) | https://arxiv.org/abs/2510.03595 | Earlier statement of the two-pass mitigation | 2026-08-03 (title only) |
| 7 | anthropic-sdk-python issue #1185 | https://github.com/anthropics/anthropic-sdk-python/issues/1185 | "compiled grammar is too large" for complex schemas | 2026-08-03 |
| 8 | vercel/ai issue #14342 | https://github.com/vercel/ai/issues/14342 | Third-party confirmation that Zod schemas with `minimum`/`maximum`/`exclusiveMinimum`/`not` break Anthropic structured outputs | 2026-08-03 |
| 9 | Instructor | https://python.useinstructor.com/ | MIT; Pydantic-validate-then-reask pattern; `max_retries`; **has a Go implementation** | 2026-08-03 |

## What to borrow for faion

1. **Keep structured output on all four transports; stop treating the schema as a contract.** Split `search.json` conceptually into a *wire schema* (only Anthropic-supported keywords — this is what we send) and a *validation schema* (the full Draft-7 file — this is what Go enforces after parse). Today we ship one file that pretends to be both.
2. **Add the three missing Go post-validations**: score ∈ [0,1], `len([]rune(why)) ≤ 240`, and a runes-not-bytes length check. Cheap, deterministic, zero tokens.
3. **Count hallucinations, don't log them.** `agent.go:270` should increment a counter on `Result` (e.g. `Result.Dropped []DroppedID` or at minimum `Result.HallucinatedCount int`) so an eval harness can assert on it. A `logger.Warn` is invisible to a test. This is the single highest-value one-line-ish change in this whole layer.
4. **Adopt the two-pass shape only where reasoning is hard.** For `faion search` — a ranking task over a supplied candidate list — the reasoning is shallow and the closed-weight models we target show ~zero format tax. One-pass constrained decoding is correct here. If we ever add a task with real reasoning depth (e.g. "compose a plan across N methodologies"), use turn-1-freeform / turn-2-format.
5. **Pin `additionalProperties: false` and `required` everywhere** — these two *are* compiled, so they are free reliability.
6. **Instrument grammar-cache behaviour.** Any change to `search.json` costs a compile on first call and invalidates the prompt cache. Version the schema and avoid churning it.

## What NOT to borrow — and why

- **Do not ship a runtime validation library.** Instructor exists in Go, and it is still a no: it wants to own the call and the retry loop. Our post-validation is ~30 lines of Go against a struct we already have. Adding a dependency to do less than we already do is negative value.
- **Do not adopt reask/retry loops on schema failure as a default.** With grammar-constrained decoding the schema failure mode largely disappears; what remains is *semantic* failure, which a reask cannot fix because the model has no signal about what was wrong. Retry costs a whole call and hides the defect from metrics.
- **Do not add `pattern`/`minimum`/`maxItems` to the wire schema expecting enforcement.** At best they are stripped; at worst (per vercel/ai #14342) the request 400s.
- **Do not chase 100% schema compliance as a quality goal.** The Structured Output Benchmark says compliance is already near-perfect while value accuracy is 83%. Optimising the metric that is already saturated is theatre.
- **Do not use structured output on any request that also needs citations.** Hard 400. See `groundedness-and-citations.md`.
- **No runtime Python.** Pydantic, Instructor-Python, Guardrails AI are dev-time-only tools at best, and we do not need them at all.

## Mapping to our corpus

Existing methodologies that this dossier updates or contradicts:

| Slug | Domain | Action |
|---|---|---|
| `structured-output` | ml-engineering | Rewrite: add the supported/unsupported keyword table and the "wire schema vs validation schema" split |
| `structured-output-basics` | ml-engineering | Add `output_config.format` (current) and mark `output_format` deprecated |
| `structured-output-patterns` | ml-engineering | Add the two-pass decoupled pattern with the +6.8 pp figure; add "schema compliance ≠ value accuracy" with the 83.0% number |
| `test-property-based-llm-invariants` | sdlc-ai | Natural home for "post-validate what the grammar cannot express" as a property list |
| `quality-gates-confidence` | sdd | Cross-link: a passing schema check is a *low*-confidence signal |
| `guardrails-basics`, `guardrails-implementation`, `guardrails-custom-pipeline` | ml-engineering | Add the caveat that grammar constraints are not validators |

Gap — no methodology currently exists for: **"format tax and when to decouple reasoning from formatting"**. That is a new leaf, and it is the most quotable finding in Layer 4.

## Open questions / staleness risk

- **High staleness.** Anthropic's supported-keyword list has moved twice in ~9 months (beta header dropped, `output_format` → `output_config.format`). Re-verify the unsupported list before any release that depends on it. Concretely: if `pattern` ever becomes supported, our ID-validation story simplifies.
- We have **not** measured Anthropic's compliance rate on *our* schema. The ~99% figure is inherited. First eval run should produce our own number.
- Unresolved: was the Sonnet 4.5 / Agent SDK 30% omission a grammar-off path or a genuine constrained-decoding bug? Worth one afternoon of reproduction, because the answer decides whether we can trust `output_config.format` at all.
- Gemini and Codex transports enforce different subsets (Gemini uses an OpenAPI 3.0 subset, which *does* support `pattern` and numeric ranges). Our four transports therefore have **four different effective validation levels**. Go post-validation is the only way to make them agree; until it exists, the same query can pass on Gemini and fail on Claude for reasons invisible to us.
- `maxItems: 20` on `hits` is unenforced on the Anthropic path; a pathological response could be large. `opts.Top` clamps the output but the parse happens first — worth a defensive cap on decoded length.
