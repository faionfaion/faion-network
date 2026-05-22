        ---
        slug: tool-use-basics
        tier: geek
        group: ai
        domain: ml-engineering
        version: 1.1.0
        status: active
        last_reviewed: 2026-05-22
        maintainers: [faion-network]
        summary: Minimum-viable LLM tool use: typed tool registry, provider-agnostic JSON schema, request-execute-respond loop with bounded iterations.
        content_id: "3b70988611e47c52"
        complexity: medium
        produces: code
        est_tokens: 3700
        tags: [tool-use, function-calling, agent-loop, openai, anthropic]
        ---
        # Tool Use Basics

        ## Summary

        **One-sentence:** Minimum-viable LLM tool use: typed tool registry, provider-agnostic JSON schema, request-execute-respond loop with bounded iterations.

        **One-paragraph:** Pattern for adding function-calling to an LLM-driven feature: a small tool registry (name → callable + JSON schema), provider-specific schema converters (OpenAI / Anthropic / Gemini), a request-execute-respond loop with a hard iteration cap, and audit logging of every tool call. Lays the foundation for ReAct, plan-execute, and other agent patterns without dragging in a heavyweight framework.

        **Ефективно для:** Девів, які додають перший «agent-style» цикл і не хочуть одразу хапати LangChain — щоб лишити простір для росту в свій бік.

        ## Applies If (ALL must hold)

        - the LLM needs to invoke external functions, APIs, or code
- tools have well-defined inputs (JSON schema) and outputs
- iteration cap is acceptable (≤ 10 tool calls per user request)
- audit logging requirement exists (compliance, debugging)
- you are NOT yet building a full multi-agent system

        ## Skip If (ANY kills it)

        - single-shot completion is sufficient — no tools needed
- you already use a heavyweight framework (LangGraph) — match its conventions
- tool outputs are huge (multi-MB) — design a different protocol
- tools are non-deterministic side-effects (payments, hires) — require human-in-loop layer

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
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-tool-use-basics.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

        ## Templates

        | File | Purpose |
        |------|---------|
        | `templates/tool-definition.json` | Example JSON tool definition for OpenAI / Anthropic |
| `templates/agent-loop.py` | Provider-agnostic request-execute-respond loop |
| `templates/tool-registry.py` | Typed ToolRegistry with Pydantic input models |
| `templates/audit-logger.py` | Per-call audit log helper |

        ## Scripts

        | File | Purpose | When to call |
        |------|---------|--------------|
        | `scripts/validate-tool-use-basics.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

        ## Related

        - [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
        - [[agents-production-deployment]] — production gates this methodology feeds into.
        - external: rule rationales cite the sources in `content/01-core-rules.xml`.

        ## Decision tree

        The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-typed-tool`, `r2-bounded-iterations`, `r3-audit-every-call`, `r4-deterministic-naming`, `r5-error-as-tool-result` from `content/01-core-rules.xml`.
