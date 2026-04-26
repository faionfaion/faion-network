# Agent Integration — Product Manager Agents

## When to use
- Defining MVP scope for a new product where competitor analysis is needed to determine the minimum feature set
- Upgrading an MVP to an MLP (Minimum Lovable Product) by identifying the "WOW" features that differentiate the product from functional but forgettable alternatives
- Running a structured gap analysis between current product state and MLP targets before a roadmap planning session
- Updating spec files with MLP requirements after a gap analysis or discovery session
- Sequencing MLP feature implementation when multiple WOW features are identified and need to be prioritized

## When NOT to use
- Product is at ideation stage only — no existing specs or MVP definition to analyze; start with discovery methodology instead
- Competitor landscape is entirely novel and no comparable products exist; the MVP scope analyzer needs comparables to work from
- Team is not ready to act on spec updates (e.g., mid-sprint, code freeze); run mode: analyze and mode: find-gaps for prep, defer mode: update until the team is ready
- The product is B2B enterprise with highly custom requirements; cookie-cutter MLP dimensions (Delight, Ease, Speed, Trust, Personality) may not apply without modification

## Where it fails / limitations
- `faion-mvp-scope-analyzer-agent` relies on competitor analysis that may be outdated if the tool's training data is not current; validate outputs against live competitor research
- MLP dimensions are product-agnostic heuristics — they do not replace user research; WOW features proposed without user validation may miss actual delight drivers
- mode: update modifies spec files; if specs are not version-controlled, changes are hard to review and roll back
- mode: plan produces an implementation order but does not account for team capacity, technical debt, or infrastructure constraints — treat as input to sprint planning, not as a sprint plan
- Five-mode design (analyze → find-gaps → propose → update → plan) assumes sequential execution; skipping steps produces lower-quality outputs in later modes

## Agentic workflow
Run `faion-mlp-agent` sequentially across its five modes, using the output of each mode as context for the next. A supervisor subagent coordinates the pipeline: passes the project path and mode outputs, catches errors (missing spec files, malformed JSON), and writes a session summary. For MVP scope definition on a new product, run `faion-mvp-scope-analyzer-agent` first, then hand its output to `faion-mlp-agent` starting at mode: propose (since there is no existing MVP to analyze).

### Recommended subagents
- `faion-mvp-scope-analyzer-agent` — competitor feature analysis → MVP scope recommendation for new products
- `faion-mlp-agent` (mode: analyze) — extract current MVP feature state from existing spec files
- `faion-mlp-agent` (mode: find-gaps) — identify gaps between current MVP and MLP across 5 dimensions
- `faion-mlp-agent` (mode: propose) — generate WOW feature candidates for each MLP dimension
- `faion-mlp-agent` (mode: update) — write MLP requirements back to spec files
- `faion-mlp-agent` (mode: plan) — produce implementation sequence for MLP features

### Prompt pattern
```python
# Full MLP pipeline (sequential)
from anthropic import Anthropic

project_path = "/path/to/project"
product_type = "SaaS project management tool"

tasks = [
    {"subagent_type": "faion-mlp-agent", "prompt": f"mode: analyze\nproject_path: {project_path}"},
    {"subagent_type": "faion-mlp-agent", "prompt": f"mode: find-gaps\nproject_path: {project_path}"},
    {"subagent_type": "faion-mlp-agent", "prompt": f"mode: propose\nproject_path: {project_path}\nproduct_type: {product_type}"},
    {"subagent_type": "faion-mlp-agent", "prompt": f"mode: update\nproject_path: {project_path}"},
    {"subagent_type": "faion-mlp-agent", "prompt": f"mode: plan\nproject_path: {project_path}"},
]
```

```
Use faion-mvp-scope-analyzer-agent to define MVP scope:

subagent_type: faion-mvp-scope-analyzer-agent
prompt: |
  Analyze {product_type} tools for MVP scope.
  Target: {target_segment}
  Focus: {core_differentiator}
  Output: competitor feature matrix + minimum feature set for MVP
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` | Claude Agent SDK — runtime for both PM agents | `pip install anthropic` / https://docs.anthropic.com/en/docs/agents |
| `linear` (API) | Sync MLP feature proposals to the roadmap | https://linear.app/docs/graphql |
| `notion-client` | Read/write spec documents if stored in Notion | `pip install notion-client` / https://developers.notion.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API | SaaS | Yes | Claude as the reasoning engine for both PM agents |
| Linear | SaaS | Yes (API) | Roadmap management; MLP implementation plan syncs here |
| Notion | SaaS | Yes (API) | Spec documentation; agents read/write spec files via API |
| Confluence | SaaS | Partial | Spec storage; API exists but writing structured content is cumbersome |
| Perplexity / Tavily | SaaS | Yes | Grounded competitor research for `faion-mvp-scope-analyzer-agent` |

## Templates & scripts
See `templates.md` for MLP scope canvas and MVI definition templates.

Mode pipeline coordinator (error handling):
```python
def run_mlp_pipeline(project_path: str, product_type: str) -> list[dict]:
    """Run all 5 MLP modes sequentially; return results per mode."""
    modes = ["analyze", "find-gaps", "propose", "update", "plan"]
    results = []
    for mode in modes:
        prompt = f"mode: {mode}\nproject_path: {project_path}"
        if mode == "propose":
            prompt += f"\nproduct_type: {product_type}"
        # invoke faion-mlp-agent with prompt
        # store result; pass to next mode as context if needed
        results.append({"mode": mode, "status": "ok", "output": "..."})
    return results
```

## Best practices
- Always run mode: analyze before mode: find-gaps — the gap analysis is meaningless without a baseline of current MVP features
- Treat WOW feature proposals from mode: propose as hypotheses, not decisions — validate at least 2–3 candidates with real users before writing them to specs via mode: update
- When running mode: update, ensure spec files are committed to version control first — the agent modifies files in place and changes should be reviewable as a diff
- Use the MLP dimensions (Delight, Ease, Speed, Trust, Personality) as a structured brainstorm framework, not a rigid checklist — not every dimension applies to every product
- For B2B products, weight Trust and Ease higher than Delight and Personality — enterprise buyers optimize for reliability and onboarding speed, not emotional resonance

## AI-agent gotchas
- mode: update writes to spec files autonomously — if the agent misinterprets a gap or proposes an incorrect MLP feature, the spec is modified without a review step; always require human review of the diff before merging
- Human-in-the-loop checkpoint: after mode: propose, a product manager must review and select which WOW features to accept before running mode: update — do not chain propose → update without human approval
- `faion-mvp-scope-analyzer-agent` performs competitor analysis based on training data; for fast-moving markets (AI tooling, fintech), supplement with a live web search tool call before passing outputs to the MLP pipeline
- mode: plan produces an implementation sequence but does not validate technical feasibility — engineering review is required before treating the plan as a sprint backlog

## References
- Faion MLP agent documentation: see `agents/` directory in this skill
- https://docs.anthropic.com/en/docs/agents (Claude Agent SDK)
- https://linear.app/docs/graphql (roadmap integration)
- https://developers.notion.com (spec storage integration)
- MLP concept origin: https://medium.com/the-happy-startup-school/beyond-mvp-10-steps-to-make-your-product-minimum-loveable-51800164ae0c
