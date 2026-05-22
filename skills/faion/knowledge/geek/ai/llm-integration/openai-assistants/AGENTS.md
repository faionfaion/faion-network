        ---
        slug: openai-assistants
        tier: geek
        group: ai
        domain: ml-engineering
        version: 1.1.0
        status: active
        last_reviewed: 2026-05-22
        maintainers: [faion-network]
        summary: Stateful OpenAI Assistants integration: thread lifecycle, File Search vector store, Code Interpreter, polling vs streaming, resource cleanup.
        content_id: "88d56b700b1003e3"
        complexity: medium
        produces: code
        est_tokens: 3700
        tags: [assistants-api, stateful-llm, file-search, code-interpreter, rag]
        ---
        # OpenAI Assistants API

        ## Summary

        **One-sentence:** Stateful OpenAI Assistants integration: thread lifecycle, File Search vector store, Code Interpreter, polling vs streaming, resource cleanup.

        **One-paragraph:** Provides production patterns for the Assistants API: assistant creation as a long-lived resource (registered + versioned), thread-per-conversation lifecycle, File Search vector-store hygiene, Code Interpreter sandbox limits, and the run-polling state machine vs streaming run events. Includes a managed-resources helper that prevents the #1 Assistants bug — leaked threads and vector stores piling up at $0.10/GB/day.

        **Ефективно для:** Команд, що будують stateful чат / помічника поверх OpenAI і не хочуть платити $40/міс за забуті thread-и та векторні сховища.

        ## Applies If (ALL must hold)

        - you need a stateful conversation surface (threads survive across turns)
- you need built-in File Search OR Code Interpreter (sandboxed Python)
- you can tolerate Assistants API's polling/streaming run model
- OPENAI_API_KEY with Assistants access is provisioned
- you can clean up threads + vector stores on session end

        ## Skip If (ANY kills it)

        - stateless one-shot completion is sufficient — use chat.completions instead
- you need on-prem hosting — Assistants is hosted-only
- latency budget < 1s — Assistants polling adds 200-500ms per turn
- you need fine-grained control over the tool loop — use raw tool-use

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
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-openai-assistants.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

        ## Templates

        | File | Purpose |
        |------|---------|
        | `templates/managed-resources.py` | Context-managed assistant + thread + vector-store lifecycle |
| `templates/query-assistant.py` | Run + poll OR stream against a thread |
| `templates/vector-store-bootstrap.py` | Project-named vector store creation with TTL |
| `templates/cleanup-sweeper.py` | Nightly sweeper for orphaned threads / vector stores |

        ## Scripts

        | File | Purpose | When to call |
        |------|---------|--------------|
        | `scripts/validate-openai-assistants.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

        ## Related

        - [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
        - [[agents-production-deployment]] — production gates this methodology feeds into.
        - external: rule rationales cite the sources in `content/01-core-rules.xml`.

        ## Decision tree

        The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-assistant-as-resource`, `r2-thread-lifecycle`, `r3-vector-store-hygiene`, `r4-run-polling-bounded`, `r5-cost-meter` from `content/01-core-rules.xml`.
