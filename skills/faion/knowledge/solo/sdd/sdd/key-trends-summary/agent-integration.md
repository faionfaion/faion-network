# Agent Integration — Key Trends Summary 2025-2026

## When to use
- When an agent needs to orient itself on current SDD, observability, and platform-engineering tooling before advising on architecture
- When a human asks "what tools should I use for X in 2025/2026" within the SDD/documentation domain
- As a context document loaded before roadmap sessions — surfaces which trends are worth betting on vs. stabilizing
- When evaluating whether to adopt a new tool (Kiro, Tessl, MCP, etc.) — this doc provides the industry baseline

## When NOT to use
- As a replacement for methodology-specific docs (use the dedicated methodology folders for actionable guidance)
- For time-sensitive tool decisions — this is a snapshot; always verify currency of market share data before committing
- For domains not covered here (the doc focuses on SDD, ADRs, living docs, platform engineering, observability)
- When the agent already has current context from a more specific source

## Where it fails / limitations
- Market share statistics (Backstage 89%, platform team adoption rates) become stale within 6-12 months — treat as directional, not precise
- The doc predicts 2026 trends that may not materialize; tag any roadmap decisions citing this doc as "trend-based assumption"
- Coverage is breadth-first: useful for orientation but insufficient as the sole source for any single decision
- The MCP section is brief; agents building tool integrations should read the MCP spec directly

## Agentic workflow
An agent loaded with this document can answer tooling orientation questions, evaluate whether a proposed approach is aligned with industry direction, and identify gaps in a project's SDD setup. It works best as a reference document injected at the start of an architectural planning session rather than as a target for extraction or summarization. For roadmap planning, pair it with the project's constitution.md and current .aidocs/roadmap.md.

### Recommended subagents
- Sonnet-tier subagent — orientation and tooling comparison; does not require Opus reasoning depth
- Opus-tier subagent — roadmap synthesis combining this doc with project-specific context and stakeholder constraints

### Prompt pattern
```
Context: [Key Trends Summary 2025-2026 loaded]
Task: Evaluate our current SDD setup against 2025-2026 best practices.
Our setup: [describe current tooling]
Identify: (1) gaps vs. industry standard, (2) over-engineered areas, (3) high-value additions.
Return a prioritized table: Gap | Effort | Value | Recommendation.
```

```
Based on the Key Trends Summary, assess whether adopting [Tool X] aligns with
current industry direction. Consider: maturity, agent-friendliness, community,
and fit with our stack ([stack description]). Return: Aligned/Misaligned + rationale.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `otel-cli` | Send OpenTelemetry traces/spans from shell scripts and CI | `brew install otel-cli` / [docs](https://github.com/equinix-labs/otel-cli) |
| `backstage-cli` | Scaffold and manage Backstage developer portal plugins | `npx @backstage/cli` / [docs](https://backstage.io/docs/local-dev/cli-overview) |
| `spec-kit` (GitHub) | Open-source SDD toolkit from GitHub/Microsoft | `npx spec-kit` / [docs](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Amazon Kiro | SaaS (IDE) | Yes — built for agents | Full SDD workflow with hooks; only AWS-integrated |
| Tessl | SaaS | Partial | Framework + registry for spec-driven AI coding |
| Claude Code | OSS CLI | Native | Anthropic's SDD-aware CLI; used in this workflow |
| Backstage | OSS | Yes — plugin API | TechDocs integration; agent writes docs, portal serves them |
| Port | SaaS | Yes — REST API | Service catalog; agents can register services programmatically |
| Mintlify | SaaS | Yes — Git-based | llms.txt standard; Anthropic uses it for Claude docs |
| OpenTelemetry | OSS | Yes — SDK | CNCF #2 project; instrument agent pipelines for observability |

## Templates & scripts
See `templates.md` in this folder for document scaffolding templates.

No inline script needed — this methodology is a reference document, not a workflow. Use `otel-cli` to instrument agent pipelines if you want observability on agent runs:

```bash
# Trace an agent task execution with OpenTelemetry
otel-cli exec \
  --service "sdd-agent" \
  --name "task-execution" \
  --tp-required=false \
  -- bash -c "your-agent-command"
```

## Best practices
- Load this document at the start of quarterly roadmap sessions, not per-task
- When a trend cites a specific percentage (e.g., "25% of YC W25 codebases are 95%+ AI-generated"), document the source and date in your ADRs — percentages carry implied precision they don't have
- Cross-reference the LLM-first workflow patterns (context packing, spec-first) with your project's constitution.md; adopt patterns that fit your constraints, not all of them
- For observability, start with OTel traces on agent task boundaries (start/end/error) before adding metrics and logs — traces provide the most value for debugging agent failures
- Platform engineering's "golden path" concept maps directly to SDD constitution.md: define the paved road once, enforce it in quality gates

## AI-agent gotchas
- This document does not replace tool documentation; agents citing it for specific API details will hallucinate — send agents to primary sources for implementation
- Trend documents are inherently speculative; an agent treating "2026 prediction" bullets as confirmed facts will make overconfident recommendations
- "90% of Claude Code's code is written by Claude Code itself" is a marketing claim, not a benchmark — do not use it as a quality target in agent prompts
- The SDD tools table (Kiro, Spec Kit, Tessl, Claude Code) does not imply these tools are interchangeable; each has different integration points; agents need tool-specific context before recommending adoption

## References
- [Thoughtworks: SDD Key 2025 Practice](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [Martin Fowler: SDD Tools Analysis](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [Amazon Kiro](https://kiro.dev/blog/kiro-and-the-future-of-software-development/)
- [OpenTelemetry AI Agent Observability](https://opentelemetry.io/blog/2025/ai-agent-observability/)
- [Roadie: Platform Engineering 2026](https://roadie.io/blog/platform-engineering-in-2026-why-diy-is-dead/)
- [Addy Osmani: LLM Coding Workflow 2026](https://addyosmani.com/blog/ai-coding-workflow/)
