        ---
        slug: openai-api-integration
        tier: geek
        group: ai
        domain: ml-engineering
        version: 1.1.0
        status: active
        last_reviewed: 2026-05-22
        maintainers: [faion-network]
        summary: Production-grade OpenAI Chat Completions integration: client init, model selection, streaming, async batches, structured output, retries, token accounting.
        content_id: "5b76a9a00da7640c"
        complexity: medium
        produces: code
        est_tokens: 3700
        tags: [openai, gpt-4, api-integration, llm, async]
        ---
        # OpenAI API Integration

        ## Summary

        **One-sentence:** Production-grade OpenAI Chat Completions integration: client init, model selection, streaming, async batches, structured output, retries, token accounting.

        **One-paragraph:** Provides a small but opinionated wrapper over the official `openai` SDK so an agent shipping OpenAI-backed code never trips on auth, model-name drift, untyped responses, or rate-limit storms. Covers gpt-4o / gpt-4o-mini / gpt-4-turbo selection, AsyncOpenAI batching, JSON mode + structured outputs (beta.parse), exponential-backoff retries on RateLimitError/APIConnectionError, and tiktoken-driven cost tracking.

        **Ефективно для:** Backend devs, що тільки що отримали «приліпи GPT до нашого API» і не хочуть наступного дня ловити 429 + parsing-помилки в проді.

        ## Applies If (ALL must hold)

        - you are building or extending a production code path that calls OpenAI Chat Completions
- the official `openai` Python SDK is available (>=1.0)
- OPENAI_API_KEY (or AZURE_OPENAI_API_KEY) is provisioned in the runtime environment
- you have a defined quality bar for the task and a model-selection budget
- concurrency / batch needs are known up front (sync vs async)

        ## Skip If (ANY kills it)

        - task fits a smaller / cheaper provider (Claude Haiku, Gemini Flash, local Ollama)
- you need >128K context — Gemini 1.5 Pro is the right tool
- policy requires on-prem / self-hosted inference
- response format is genuinely unknown — design a schema first or use a different methodology

        ## Prerequisites

        | Input artifact | Format | Source |
        |---|---|---|
        | Use-case brief | text | Author / owner |
        | Tier-manifest entry | JSON | `skills/tier-manifest.json` |
        | Eval / fixture data (when applicable) | jsonl | Repo `tests/fixtures/` |
        | Named approver | role:person | Org RACI |

        ## Assumes Loaded

        | Methodology | Why |
        |-------------|-----|
        | `geek/ai/llm-integration/semantic-xml-content` | Authoring shape for `content/*.xml`. |
        | `geek/ai/ml-engineer/ai-agent-patterns` | Pattern catalogue for agent loops referenced from this methodology. |

        ## Content (load on demand)

        | File | Depth | What's inside | Est. tokens |
        |------|-------|---------------|-------------|
        | `content/01-core-rules.xml` | essential | 5 testable rules with statement + rationale + source | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for produces=code + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

        ## Task Routing

        | Sub-task | Model | Rationale |
        |----------|-------|-----------|
        | `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=code`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-openai-api-integration.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

        ## Templates

        | File | Purpose |
        |------|---------|
        | `templates/client.py` | Singleton OpenAI client + AsyncOpenAI factory |
| `templates/retry-policy.py` | tenacity decorator wired for RateLimitError / APIConnectionError |
| `templates/typed-call.py` | Pydantic-typed chat completion call example |
| `templates/cost-tracker.py` | Cost accounting helper using tiktoken |

        ## Scripts

        | File | Purpose | When to call |
        |------|---------|--------------|
        | `scripts/validate-openai-api-integration.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

        ## Related

        - [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
        - [[agents-production-deployment]] — production gates this methodology feeds into.
        - external: rule rationales cite the sources in `content/01-core-rules.xml`.

        ## Decision tree

        The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-model-by-task`, `r2-typed-responses`, `r3-retry-policy`, `r4-async-batch`, `r5-cost-accounting` from `content/01-core-rules.xml`.
