# AGENT-06: Structured Output Methodologies

**Summary line 1:** Schemas are prompts: field order, names, descriptions, and enums steer autoregressive generation more than the prompt body itself.
**Summary line 2:** 14 production-grade tricks covering CoT-in-schema, title-after-content ordering, refusal fields, discriminated unions, grammar modes, and numeric/decimal reliability.

---

## so-01: Reasoning-First Field Order (CoT-in-Schema)

**Rule:** When the schema contains both reasoning and a final answer, place the reasoning field FIRST. The model is autoregressive — it can only condition the answer on tokens that already exist, so a `reasoning` field appearing before `answer` literally becomes the model's chain of thought.

**Empirical data:** Castillo (2025) ran LiveBench questions through two Pydantic models that differed only in field order. `reasoning → answer` scored 46.67% accuracy; `answer → reasoning` scored 33.33% (p < 0.01). The 13 pp gap came purely from field order — same prompt, same model.

**When to use:** Any non-trivial decision: classification with edge cases, math, multi-criteria scoring, ambiguous extraction.

**When NOT to use:** Pure transformation tasks where reasoning adds latency without accuracy (e.g., "uppercase this string", "extract all emails by regex"). Also skip when you bill by token and the upstream model is already a reasoning model (Opus thinking, o-series) — you'd be paying twice.

**Example:**
```python
# GOOD: reasoning first
class Verdict(BaseModel):
    reasoning: str = Field(description="Step-by-step analysis of evidence")
    confidence: Literal["low", "medium", "high"]
    decision: Literal["approve", "reject"]

# BAD: decision first — model commits before thinking
class VerdictBad(BaseModel):
    decision: Literal["approve", "reject"]
    reasoning: str  # post-hoc rationalization, not CoT
```

**Source:** [Structured outputs: don't put the cart before the horse — Dylan Castillo](https://dylancastillo.co/posts/llm-pydantic-order-matters.html)

---

## so-02: Title/Summary AFTER Content (Inverted Header Pattern)

**Rule:** When generating a piece of content with metadata about it (title, slug, summary, tags, sentiment), put the CONTENT field first and the metadata fields last. The autoregressive model can only "see" the article when generating the title if the article tokens already exist in context.

**Mechanism:** This is the reasoning-first rule in disguise. The body IS the reasoning trace for the title. Generating `title` then `body` means the title is generated blind and the body is forced to fit it; generating `body` then `title` lets the title summarize what was actually written.

**When to use:** Articles, emails, posts, summaries, code-then-explanation, image captions where you want both the long form and short metadata in one call.

**When NOT to use:** When the title is a hard constraint given as input (user-provided headline) — then it goes in the prompt, not the schema. Also skip if you stream output to a UI that needs the title first; in that case, do two calls.

**Example:**
```python
class BlogPost(BaseModel):
    body: str = Field(description="Full article, 600-800 words, markdown")
    title: str = Field(description="Compelling 6-10 word title that captures body")
    slug: str = Field(description="kebab-case URL slug derived from title")
    tags: list[str] = Field(description="3-5 lowercase tags from body topics")
```

**Source:** [Optimizing AWS Bedrock Structured Output with JSON Schema Design](https://explore.n1n.ai/blog/aws-bedrock-json-schema-structured-output-guide-2026-02-16) — "Field ordering represents a form of Chain of Thought embedded directly into your data structure."

---

## so-03: Field Descriptions as Inline Mini-Prompts

**Rule:** Treat every `description=` as a tiny CoT prompt that the model sees right before it generates that field. Be explicit about format, range, edge cases, and forbidden patterns. Cheap, dense, surgical steering signal.

**Empirical data:** PARSE research showed that optimizing field descriptions yields 60%+ improvement in extraction accuracy. Making relationships explicit in descriptions improves complex reasoning accuracy up to 40%.

**When to use:** Always. Especially for ambiguous fields, units (USD vs cents), formats (ISO-8601), and exclusions ("do NOT include retracted papers").

**When NOT to use:** When the description would duplicate enum values verbatim (the enum already constrains decoding); when bloating the schema past the model's context budget on cold-cache calls.

**Example:**
```python
class Invoice(BaseModel):
    total_cents: int = Field(
        description=(
            "Total in CENTS as an integer. "
            "$19.99 -> 1999. Never include currency symbol. "
            "If invoice shows tax separately, include it in total."
        )
    )
    issue_date: str = Field(
        description="ISO-8601 YYYY-MM-DD. If only month/year shown, use day=01."
    )
```

**Source:** [PARSE: LLM Driven Schema Optimization for Reliable Entity Extraction](https://arxiv.org/html/2510.08623v1) | [Bad Schemas could break your LLM Structured Outputs — Instructor](https://python.useinstructor.com/blog/2024/09/26/bad-schemas-could-break-your-llm-structured-outputs/)

---

## so-04: Field Names ARE Prompts (Semantic Naming)

**Rule:** Field names directly steer the model's prediction of the next tokens. Use specific, English, semantically-loaded names. Never `field1`, `val`, `data`, `output` — always `customer_age_years`, `invoice_total_usd`, `is_genuine_complaint`.

**Empirical data:** Renaming a single field from `final_choice` to `answer` raised model accuracy from 4.5% to 95% on a benchmark (Instructor blog, Sept 2024). That is a 90 point swing from changing a single token.

**When to use:** Always. Costs nothing, often the highest-leverage single change in the schema.

**When NOT to use:** Never; even legacy/protobuf-mapped schemas should add `description` to compensate for cryptic names.

**Example:**
```python
# BAD
class Out(BaseModel):
    val1: int
    val2: str
    flag: bool

# GOOD
class CustomerComplaint(BaseModel):
    severity_score_1_to_5: int
    primary_product_mentioned: str
    requires_human_escalation: bool
```

**Source:** [Bad Schemas could break your LLM Structured Outputs — Instructor](https://python.useinstructor.com/blog/2024/09/26/bad-schemas-could-break-your-llm-structured-outputs/)

---

## so-05: Embedded Scratchpad / Plan-Steps Field

**Rule:** Before any complex output, add a `plan_steps: list[str]` or `scratchpad: str` field at the top of the schema. The model writes its plan first, then executes it in subsequent fields. This is structured-output's equivalent of `<thinking>` tags but works inside strict JSON mode.

**Empirical data:** Adding a reasoning field increased GSM8k accuracy by 60% (per AWS Bedrock SO design guide). Tabular CoT (Tab-CoT) — a list of `{step, subquestion, procedure, result}` rows — is the documented Instructor pattern.

**When to use:** Multi-step calculations, multi-criteria classifications, code generation (plan -> code -> tests), data extraction where dependencies between fields matter.

**When NOT to use:** Latency-critical streaming UI; ultra-cheap classifiers where plan tokens cost more than the win.

**Example:**
```python
class ReasoningStep(BaseModel):
    step: int
    subquestion: str
    procedure: str
    result: str

class MathSolution(BaseModel):
    plan_steps: list[ReasoningStep] = Field(
        description="Decompose problem; one row per arithmetic operation"
    )
    final_answer: float
```

**Source:** [Tab-CoT — Instructor docs](https://python.useinstructor.com/prompting/thought_generation/chain_of_thought_zero_shot/tab_cot/) | [Open NotebookLM — Together AI scratchpad pattern](https://docs.together.ai/docs/open-notebooklm-pdf-to-podcast)

---

## so-06: Enum Constraints for Closed Vocabularies

**Rule:** Anywhere the answer set is finite, use a typed enum (`Literal[...]` in Pydantic, `enum` in JSON Schema). Constrained decoders mask all non-enum tokens to probability 0, making hallucinated labels mathematically impossible.

**Caveat (April 2026):** Mini/nano models still hallucinate enum values when SO is bypassed by JSON-mode-only fallback. Always pair enums with `strict: true` on OpenAI or constrained backends like XGrammar/Outlines.

**When to use:** Sentiment, intent, severity, routing labels, language codes, status states, model-of-the-day picker.

**When NOT to use:** Open vocabularies (free-text tags, user names, novel entity types). For semi-open sets, use `Literal[...] | str` and a discriminated union.

**Example:**
```python
class Ticket(BaseModel):
    category: Literal["billing", "tech_support", "refund", "spam", "other"]
    priority: Literal["P0", "P1", "P2", "P3"]
    sentiment: Literal["angry", "frustrated", "neutral", "happy"]
```

**Source:** [Structuring Enums for Flawless LLM results with Instructor](https://ohmeow.com/posts/2024-07-06-llms-and-enums.html) | [vLLM Structured Outputs](https://docs.vllm.ai/en/latest/features/structured_outputs/)

---

## so-07: Discriminated Unions for Routing & Polymorphic Output

**Rule:** When the model must choose between distinct shapes (different actions, different entity types, different intents), use a discriminated union with a `kind`/`type` literal as the discriminator. The model writes the discriminator first, which then constrains the rest of the object via grammar.

**Mechanism:** The discriminator field locks the schema branch, so the remaining fields are typed and validated correctly. Tagged unions are the JSON-schema dual of pattern matching.

**When to use:** Agent action selection, multi-shape extraction (Person vs Company vs Product), router outputs, event logs.

**When NOT to use:** When all branches share 90% of fields — flatten with optional fields and a discriminator instead.

**Example:**
```python
class SearchAction(BaseModel):
    kind: Literal["search"] = "search"
    query: str

class FetchAction(BaseModel):
    kind: Literal["fetch"] = "fetch"
    url: str

class FinishAction(BaseModel):
    kind: Literal["finish"] = "finish"
    summary: str

class AgentTurn(BaseModel):
    reasoning: str
    action: Annotated[
        SearchAction | FetchAction | FinishAction,
        Field(discriminator="kind")
    ]
```

**Source:** [Pydantic Unions docs](https://docs.pydantic.dev/latest/concepts/unions/) | [Json Schema Patterns: Discriminated Unions — endjin](https://endjin.com/blog/json-schema-patterns-dotnet-pattern-matching-and-discriminated-unions)

---

## so-08: Refusal Field for Safety-Aware Extraction

**Rule:** When the schema is strict and refusals must NOT break parsing, add an explicit `refusal: str | None` field at the top of the schema. OpenAI's strict-mode response now includes a top-level `refusal` string when the model declines; mirror it inside your own schemas for consistency across providers.

**When to use:** PII extraction, medical/legal domains, content classification with abuse cases, or any pipeline where a refusal must short-circuit downstream code without throwing JSON errors.

**When NOT to use:** Trivial transformations where refusals are not expected; in pipelines where refusals are converted to errors anyway.

**Example:**
```python
class MedicalExtract(BaseModel):
    refusal: str | None = Field(
        default=None,
        description="If you cannot/should not answer, explain here. Else null."
    )
    diagnoses: list[str] | None = None
    medications: list[str] | None = None
```

```python
# Then:
if response.refusal:
    log_refusal(response.refusal)
    return None
```

**Source:** [Introducing Structured Outputs in the API — OpenAI](https://openai.com/index/introducing-structured-outputs-in-the-api/) | [Structured model outputs — OpenAI API](https://developers.openai.com/api/docs/guides/structured-outputs)

---

## so-09: Strict Mode = required + additionalProperties: false

**Rule:** When using OpenAI/Azure/strict-mode SO, every object must (a) list every property in `required`, (b) set `additionalProperties: false`. Optional fields are simulated by `T | None` (nullable) — NOT by leaving them off `required`.

**Why:** Strict mode compiles the schema into a finite-state grammar; missing fields would create non-determinism in the FSM. Pydantic-to-OpenAI bridges (Instructor, openai-python) translate `Optional[X]` -> `{type: ["X", "null"], required: true}`.

**When to use:** Always when targeting OpenAI/Azure strict mode or Anthropic tool input schemas with required-everything.

**When NOT to use:** Local Outlines/XGrammar pipelines that support proper JSON-Schema optional fields natively.

**Example:**
```python
class User(BaseModel):
    model_config = {"extra": "forbid"}  # -> additionalProperties: false
    name: str
    email: str
    middle_name: str | None = None  # nullable, NOT optional
```

**Source:** [Schema additionalProperties must be false when strict is true — OpenAI Community](https://community.openai.com/t/schema-additionalproperties-must-be-false-when-strict-is-true/929996) | [How to Fix OpenAI Structured Outputs Breaking Pydantic Models](https://medium.com/@aviadr1/how-to-fix-openai-structured-outputs-breaking-your-pydantic-models-bdcd896d43bd)

---

## so-10: Numbers as Strings for Decimal Reliability

**Rule:** For money, prices, exact decimals, IDs, phone numbers, and anything where lossy float conversion would corrupt data — use `str` with a regex `pattern`, NOT `float`. Then parse with `Decimal()` on the receiving side.

**Why:** LLMs encode numbers as per-digit base-10 representations and frequently quote them anyway (`"79.99"` instead of `79.99`). Forcing a float field invites silent precision loss; forcing a string with regex makes the model produce a deterministic, parseable token stream.

**When to use:** Currency, scientific decimals, big integers (>2^53), credit card / phone / postal numbers, version strings.

**When NOT to use:** Counts, scores, indices — `int` is fine for those.

**Example:**
```python
class LineItem(BaseModel):
    price_usd: str = Field(
        pattern=r"^\d+\.\d{2}$",
        description="USD price as decimal string e.g. '19.99'. Two decimal places required."
    )
    quantity: int  # OK as int — small counts
```

**Source:** [Promptfoo — LLM evaluation techniques for JSON outputs](https://www.promptfoo.dev/docs/guides/evaluate-json/) | [Language Models Encode Numbers Using Digit Representations in Base 10](https://arxiv.org/html/2410.11781v1)

---

## so-11: SO vs JSON Mode vs Tool Call vs Grammar — Pick by Use Case

**Rule:** Four distinct modes, four use cases. Wrong choice = wasted tokens or silent constraint violations.

| Mode | Format guarantee | Schema guarantee | Best use |
|------|------------------|------------------|----------|
| **JSON mode** | valid JSON | none | legacy / where strict SO unsupported |
| **Structured Outputs** (`response_format: json_schema, strict: true`) | valid JSON | full | data extraction, classification |
| **Tool call** | valid JSON args | full | agent actions, function dispatch |
| **Grammar** (Outlines / XGrammar / GBNF) | grammar | grammar | local models, custom DSLs, non-JSON outputs |

**When to use which:**
- Deterministic extraction → SO with strict mode
- Agent that takes actions → tool call (Anthropic and OpenAI both)
- Custom DSL/SQL/regex output → grammar (XGrammar 100x faster than alternatives)
- Open-source model without SO support → Outlines + Pydantic

**When NOT to use:** Plain JSON mode in production after mid-2025 — every major provider ships constrained SO; `json_object` mode is now legacy.

**Example:**
```python
# OpenAI SO mode
client.responses.parse(
    model="gpt-5",
    input=msgs,
    text_format=Verdict,  # auto-emits {type: "json_schema", strict: true}
)

# Anthropic tool-call mode (preferred for SO)
client.messages.create(
    model="claude-opus-4-7",
    tools=[{"name": "submit_verdict", "input_schema": Verdict.model_json_schema()}],
    tool_choice={"type": "tool", "name": "submit_verdict"},
)
```

**Source:** [JSON Mode vs Function Calling vs Structured Output: 2026 Guide](https://www.buildmvpfast.com/blog/structured-output-llm-json-mode-function-calling-production-guide-2026) | [When should I use function calling, structured outputs or JSON mode? — Vellum](https://www.vellum.ai/blog/when-should-i-use-function-calling-structured-outputs-or-json-mode) | [XGrammar paper](https://arxiv.org/abs/2411.15100)

---

## so-12: Schema Reuse Across Pipeline Steps (Versioned Contracts)

**Rule:** Define each shape ONCE as a Pydantic model and import it across stages. Persist `schema_version` in every event/log. Schema changes are breaking changes — bump versions and keep old parsers for at least one rollback window.

**When to use:** Multi-step pipelines (extract → enrich → score → publish), agent meshes, anything with replay/backfill.

**When NOT to use:** One-shot scripts, exploratory notebooks.

**Example:**
```python
# shared/schemas.py
class ArticleDraft(BaseModel):
    schema_version: Literal["v3"] = "v3"
    body: str
    title: str
    tags: list[str]

# stage_1_extract.py
draft: ArticleDraft = client.parse(..., text_format=ArticleDraft)

# stage_2_enrich.py — receives the SAME type
def enrich(draft: ArticleDraft) -> ArticleEnriched: ...
```

**Source:** [Continuous Integration for LLM Prompts — DEV](https://dev.to/kuldeep_paul/continuous-integration-for-llm-prompts-a-step-by-step-guide-to-automated-prompt-deployment-359k) | [LLM Structured Outputs: Schema Validation for Real Pipelines (2026) — Collin Wilkins](https://collinwilkins.com/articles/structured-output)

---

## so-13: Array vs Single-Item — Always Wrap in `items`

**Rule:** When extracting N entities, never make the top-level response a bare array. Always wrap with `{items: [...]}` plus a count. This (a) keeps top-level type stable for `additionalProperties: false`, (b) lets you add metadata (e.g., `total_found`, `truncated`), (c) avoids the "is this one item or one-element list?" parse ambiguity.

**Pitfall pattern:** Asking for "extract entities" with a plain `list[Entity]` yields zero entities when the model thinks none exist, OR a single dict when it thinks there's only one. Wrap ALWAYS.

**When to use:** Any extraction with variable cardinality.

**When NOT to use:** Hard-coded N (always exactly 3 suggestions) — use `tuple[X, X, X]` or fixed array length.

**Example:**
```python
class EntityList(BaseModel):
    total_found: int = Field(description="Count of entities; 0 if none")
    truncated: bool = Field(description="True if more entities exist beyond limit")
    items: list[Entity]
```

**Source:** [Structured data extraction from unstructured content — Simon Willison](https://simonwillison.net/2025/Feb/28/llm-schemas/) (the `--schema-multi` pattern) | [End-to-End Structured Extraction with LLM — Databricks](https://medium.com/@AI-on-Databricks/end-to-end-structured-extraction-with-llm-part-1-batch-entity-extraction-876ce17b290f)

---

## so-14: Two-Pass — Free-Form Reasoning Then Structured Extraction

**Rule:** When raw reasoning quality matters more than format (math proofs, deep analysis, creative writing), DO NOT lock the model into JSON during the reasoning step. Run two passes: (1) free-form reasoning (or extended thinking), (2) cheap small-model extraction into the strict schema.

**Empirical data:** Forcing strict JSON during reasoning costs 10–15% on math and complex analysis benchmarks vs free-form-then-extract. The format constraint interferes with the reasoning trace itself.

**When to use:** Math, research synthesis, code with deep reasoning, anything where the answer is more valuable than throughput.

**When NOT to use:** Simple extraction, classification, latency-critical paths — single-pass strict SO wins on cost and latency.

**Example:**
```python
# Pass 1: free-form Opus thinking
raw = client.messages.create(
    model="claude-opus-4-7",
    thinking={"type": "enabled", "budget_tokens": 16000},
    messages=[{"role": "user", "content": question}],
).content[-1].text

# Pass 2: cheap Haiku extraction into strict schema
verdict = haiku_client.responses.parse(
    model="claude-haiku-4-7",
    input=[{"role": "user", "content": f"Extract from:\n{raw}"}],
    text_format=Verdict,
)
```

**Source:** [JSON Mode vs Function Calling vs Structured Output: 2026 Guide](https://www.buildmvpfast.com/blog/structured-output-llm-json-mode-function-calling-production-guide-2026) | [SLOT: Structuring the Output of Large Language Models](https://arxiv.org/html/2505.04016v1) | [The "think" tool — Anthropic](https://www.anthropic.com/engineering/claude-think-tool)

---

## Cross-Cutting Notes

- **Schema is a prompt.** Names, order, descriptions, enums, and patterns ALL steer generation. Treat the schema as the highest-leverage edit surface in the system.
- **Order rule of thumb:** inputs / context fields → reasoning / scratchpad → main content → metadata about content (title, tags, summary). Each later field can "see" earlier ones.
- **Combine, don't choose.** so-01 + so-03 + so-05 + so-06 stack: reasoning-first + rich descriptions + scratchpad + enums = production-grade schema.
- **Test by ablation.** When accuracy drops, try (a) reorder fields, (b) rename fields, (c) thicken descriptions BEFORE prompting harder.

## Sources Index

- [Dylan Castillo — order matters](https://dylancastillo.co/posts/llm-pydantic-order-matters.html)
- [n1n.ai — AWS Bedrock JSON schema design 2026](https://explore.n1n.ai/blog/aws-bedrock-json-schema-structured-output-guide-2026-02-16)
- [PARSE arxiv 2510.08623](https://arxiv.org/html/2510.08623v1)
- [Instructor — Tab-CoT](https://python.useinstructor.com/prompting/thought_generation/chain_of_thought_zero_shot/tab_cot/)
- [Instructor — bad schemas blog](https://python.useinstructor.com/blog/2024/09/26/bad-schemas-could-break-your-llm-structured-outputs/)
- [OpenAI — introducing Structured Outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/)
- [OpenAI structured outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs)
- [OpenAI community — strict mode + additionalProperties](https://community.openai.com/t/schema-additionalproperties-must-be-false-when-strict-is-true/929996)
- [Vellum — when to use what](https://www.vellum.ai/blog/when-should-i-use-function-calling-structured-outputs-or-json-mode)
- [BuildMVPFast — 2026 guide](https://www.buildmvpfast.com/blog/structured-output-llm-json-mode-function-calling-production-guide-2026)
- [BAML — schema-aligned parsing](https://boundaryml.com/blog/schema-aligned-parsing)
- [XGrammar paper arxiv 2411.15100](https://arxiv.org/abs/2411.15100)
- [XGrammar 2 arxiv 2601.04426](https://arxiv.org/html/2601.04426)
- [vLLM Structured Outputs docs](https://docs.vllm.ai/en/latest/features/structured_outputs/)
- [Outlines / dottxt-ai](https://github.com/dottxt-ai/outlines)
- [Anthropic — think tool](https://www.anthropic.com/engineering/claude-think-tool)
- [Anthropic — extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
- [Pydantic Unions](https://docs.pydantic.dev/latest/concepts/unions/)
- [endjin — discriminated unions](https://endjin.com/blog/json-schema-patterns-dotnet-pattern-matching-and-discriminated-unions)
- [Promptfoo — JSON eval](https://www.promptfoo.dev/docs/guides/evaluate-json/)
- [arxiv 2410.11781 — base 10 digit encoding](https://arxiv.org/html/2410.11781v1)
- [Simon Willison — schemas](https://simonwillison.net/2025/Feb/28/llm-schemas/)
- [Collin Wilkins — SO pipelines 2026](https://collinwilkins.com/articles/structured-output)
- [SLOT arxiv 2505.04016](https://arxiv.org/html/2505.04016v1)
- [ohmeow — enums with Instructor](https://ohmeow.com/posts/2024-07-06-llms-and-enums.html)
- [JSON Schema regex / pattern](https://json-schema.org/understanding-json-schema/reference/regular_expressions)
- [lm-format-enforcer](https://github.com/noamgat/lm-format-enforcer)
