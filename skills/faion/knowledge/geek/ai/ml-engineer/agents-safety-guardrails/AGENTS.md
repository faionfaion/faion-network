        ---
        slug: agents-safety-guardrails
        tier: geek
        group: ai
        domain: ml-engineering
        version: 1.1.0
        status: active
        last_reviewed: 2026-05-22
        maintainers: [faion-network]
        summary: Five guardrail categories for production agents: execution, content, financial, action, human-in-loop. Each carries trip-conditions and a recovery path.
        content_id: "801330a8dce3344d"
        complexity: deep
        produces: config
        est_tokens: 4200
        tags: [agents, safety, guardrails, human-in-loop, sandboxing]
        ---
        # Agents Safety Guardrails

        ## Summary

        **One-sentence:** Five guardrail categories for production agents: execution, content, financial, action, human-in-loop. Each carries trip-conditions and a recovery path.

        **One-paragraph:** Autonomous agents require five categories of guardrail before production deployment: execution safety (iteration limits, timeouts), content safety (input validation, PII handling), financial safety (cost caps, rate limiting), action safety (sandboxed execution, blocked patterns), and human-in-loop gates for irreversible actions. Each guardrail has explicit trip conditions and a documented recovery path.

        **Ефективно для:** Команд, що готують агента до production traffic і знають, що без guardrail-ів він зробить три нерозворотні дії в першу годину.

        ## Applies If (ALL must hold)

        - agent has at least one tool with real-world side-effects
- production traffic is in scope
- cost budget is finite
- regulatory / safety reviewers exist
- there are irreversible actions in the tool list (payments, hires, deletes)

        ## Skip If (ANY kills it)

        - agent is read-only (no side-effect tools)
- sandbox is fully isolated (no escape possible)
- internal-only with single-user trust model
- prototype phase — guardrails defer to step before launch

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
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-agents-safety-guardrails.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

        ## Templates

        | File | Purpose |
        |------|---------|
        | `templates/guardrails.yaml` | Five-category guardrail config skeleton |
| `templates/human-loop-gate.py` | Slack-based approval gate for irreversible actions |
| `templates/pii-scrubber.py` | Input + log PII scrubber |
| `templates/trip-handler.py` | Recovery-path dispatch helper |

        ## Scripts

        | File | Purpose | When to call |
        |------|---------|--------------|
        | `scripts/validate-agents-safety-guardrails.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

        ## Related

        - [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
        - [[agents-production-deployment]] — production gates this methodology feeds into.
        - external: rule rationales cite the sources in `content/01-core-rules.xml`.

        ## Decision tree

        The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-five-categories`, `r2-trip-conditions`, `r3-recovery-path`, `r4-human-loop-irreversible`, `r5-cost-cap` from `content/01-core-rules.xml`.
