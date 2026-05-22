        ---
        slug: agents-production-deployment
        tier: geek
        group: ai
        domain: ml-engineering
        version: 1.1.0
        status: active
        last_reviewed: 2026-05-22
        maintainers: [faion-network]
        summary: Five production gates for shipping an agent: typed tool base, YAML config with env subst, structured JSON logs, retry/circuit breaker, repeatable eval harness.
        content_id: "f234a444999f2aac"
        complexity: deep
        produces: config
        est_tokens: 4200
        tags: [agents, production, deployment, logging, evaluation]
        ---
        # Agents Production Deployment

        ## Summary

        **One-sentence:** Five production gates for shipping an agent: typed tool base, YAML config with env subst, structured JSON logs, retry/circuit breaker, repeatable eval harness.

        **One-paragraph:** Production autonomous agents require five components beyond the core loop: (1) typed tool base with shared registry, (2) YAML config with env-var substitution, (3) structured JSON logs for every LLM and tool call, (4) exponential backoff retry + circuit breaker for external services, (5) eval harness measuring success rate, latency, iterations, token cost. Each is a gate; passing all five = «agent is production-ready».

        **Ефективно для:** DevOps + ML eng, що готують агента до боя і не хочуть «прод-ready без логів і еволю».

        ## Applies If (ALL must hold)

        - agent has passed prototype phase and is ≤ 2 weeks from production
- real customer traffic is in scope
- SLOs (latency_p95, success_rate, $/task) are defined
- an on-call rotation exists
- you have a CI/CD pipeline that can run the eval harness

        ## Skip If (ANY kills it)

        - still in prototype — these gates are overkill before customer traffic
- internal-only tooling with no SLO — light logging is enough
- single-team owner who is also the user — feedback loop is the gate
- regulated environment requires extra gates — these five are necessary but not sufficient

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
| `content/02-output-contract.xml` | essential | JSON Schema for produces=config + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/05-examples.xml` | medium | End-to-end worked example | ~500 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

        ## Task Routing

        | Sub-task | Model | Rationale |
        |----------|-------|-----------|
        | `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=config`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-agents-production-deployment.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

        ## Templates

        | File | Purpose |
        |------|---------|
        | `templates/base-tool.py` | Typed BaseTool + ToolRegistry skeleton |
| `templates/agent-config.yaml` | YAML config with env-var substitution |
| `templates/structured-logging.py` | structlog setup emitting the 6 required fields |
| `templates/retry-circuit.py` | tenacity + pybreaker integration |
| `templates/eval-harness.py` | Eval harness skeleton with CI hook |

        ## Scripts

        | File | Purpose | When to call |
        |------|---------|--------------|
        | `scripts/validate-agents-production-deployment.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

        ## Related

        - [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
        - [[agents-production-deployment]] — production gates this methodology feeds into.
        - external: rule rationales cite the sources in `content/01-core-rules.xml`.

        ## Decision tree

        The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-typed-tools`, `r2-config-via-yaml`, `r3-structured-logs`, `r4-retry-circuit`, `r5-eval-harness` from `content/01-core-rules.xml`.
