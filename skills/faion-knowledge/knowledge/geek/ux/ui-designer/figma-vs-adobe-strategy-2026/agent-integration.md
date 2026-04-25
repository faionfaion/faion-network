# Agent Integration — Figma vs Adobe Strategy 2026

## When to use
- Conducting a toolchain audit for a product team deciding which design platform to standardize on
- Evaluating whether to migrate an existing Adobe XD or Photoshop workflow to Figma (or vice versa)
- Advising a solopreneur or small team on which subscription gives the best agent-automation surface
- Documenting a multi-tool design stack decision for an AGENTS.md or architecture doc

## When NOT to use
- When the team is already fully committed to one platform — a strategy comparison adds friction, not value
- When the decision is driven purely by individual tool features rather than workflow fit — this methodology is about strategic positioning, not feature checklists
- When the client dictates tooling — tool choice is not up for internal deliberation in that context

## Where it fails / limitations
- Figma vs. Adobe comparisons go stale quickly — both platforms ship major AI features quarterly; any analysis older than 6 months may be misleading
- "Best tool" conclusions do not transfer across team types: a product team's answer differs from a creative agency's
- Pricing structures change; per-seat vs. bundle calculations depend on team size, which shifts over time
- The analysis cannot account for in-house expertise: a team fluent in Illustrator switching to Figma incurs a real productivity cost that is hard to quantify

## Agentic workflow
An agent can assist with a Figma vs. Adobe strategy decision by collecting structured inputs (team size, task types, existing tools, API requirements, budget) and mapping them against a decision rubric. The agent produces a recommendation document with scored criteria and a rationale. For toolchain audits, the agent can parse a list of design tasks the team performs and classify each as "Figma-native," "Adobe-native," or "either" based on capability maps. Human review is required before any platform migration decision is finalized — the agent produces the analysis, not the decision.

### Recommended subagents
- `faion-sdd-executor-agent` — executes a toolchain audit task from an SDD spec, generates a decision document

### Prompt pattern
```
You are a design toolchain strategist. Evaluate the following team's workflow against Figma and Adobe CC:

Team: {team_size} people, {team_type} (product team / creative agency / solo)
Primary tasks: {task_list}
Required agent-automation surface: {automation_needs}
Budget: {budget_per_seat_per_month}
Current tools: {current_tools}

Score each platform (0–5) on:
- Collaboration
- AI automation capability (agent-driveable APIs)
- Asset creation (images, vectors, video)
- Developer handoff
- Cost efficiency for this team size

Output: Markdown table of scores + 2-paragraph recommendation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| figma-export | Export Figma assets/specs via CLI for migration audit | github.com/lucaorio/figma-export |
| adobe-ccx-cli (internal) | Adobe Creative Cloud asset management (enterprise only) | developer.adobe.com/creative-cloud |
| jq | Parse and compare JSON exports from both platforms | apt install jq |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma REST API | SaaS | Yes | Full read; limited write. Best agent surface for design automation. |
| Adobe Firefly Services | SaaS (enterprise) | Yes — REST | Asset generation API. Requires Adobe enterprise plan. |
| Adobe Creative Cloud API | SaaS | Partial | UXP-based automation inside CC apps; not fully headless. |
| Zeroheight | SaaS | Partial | Design system docs that integrate with both Figma and Adobe; REST API available. |
| Brandfolder / Bynder | SaaS | Yes | DAM systems that work with both toolchains; agent-driveable via REST. |

## Templates & scripts
See templates.md for decision matrix templates.

Tool selection scoring script (Python, ~35 lines):

```python
import json

CRITERIA = ["collaboration", "agent_api", "asset_creation", "dev_handoff", "cost_efficiency"]

# Baseline scores (update quarterly as features ship)
FIGMA_SCORES = {"collaboration": 5, "agent_api": 4, "asset_creation": 2, "dev_handoff": 5, "cost_efficiency": 4}
ADOBE_SCORES = {"collaboration": 3, "agent_api": 3, "asset_creation": 5, "dev_handoff": 3, "cost_efficiency": 3}

def score(platform_scores: dict, weights: dict) -> float:
    return sum(platform_scores[c] * weights.get(c, 1) for c in CRITERIA)

def recommend(weights: dict) -> str:
    fig = score(FIGMA_SCORES, weights)
    ado = score(ADOBE_SCORES, weights)
    winner = "Figma" if fig >= ado else "Adobe CC"
    return f"Figma: {fig:.1f} | Adobe: {ado:.1f} → Recommended: {winner}"

# Example: product team weights (collaboration + dev handoff matter most)
product_weights = {"collaboration": 2, "agent_api": 1.5, "asset_creation": 0.5, "dev_handoff": 2, "cost_efficiency": 1}
print(recommend(product_weights))

# Example: creative agency weights (asset creation + cost matter most)
agency_weights = {"collaboration": 1, "agent_api": 0.5, "asset_creation": 2.5, "dev_handoff": 1, "cost_efficiency": 2}
print(recommend(agency_weights))
```

## Best practices
- The optimal 2026 stack for most product teams is Figma (design, collaboration, handoff) + Firefly via API (asset generation) — they are not mutually exclusive
- Assess agent-automation requirements explicitly: Figma REST API is the richer automation surface; Adobe CC is more limited outside enterprise plans
- For solopreneurs, Figma's free plan + Firefly free credits covers most use cases without a paid subscription
- Revisit the decision every 6 months — Figma Config and Adobe MAX both ship major capability changes annually
- When migrating from Adobe XD to Figma, use the XD plugin for Figma to import files, then audit component fidelity manually
- Document the toolchain decision in the project's AGENTS.md so agents operating on the project know which APIs to target

## AI-agent gotchas
- Agents cannot access Figma billing or plan information — team size and subscription tier must be provided as input, not discovered
- Adobe Creative Cloud API for automation (UXP) requires a human session inside a CC app; purely headless pipelines must use Firefly Services (enterprise only)
- Figma REST API write capabilities are narrower than the UI — agents cannot create new frames, only modify existing nodes; design-from-scratch automation requires a human setup step
- Pricing data in training data is stale; always fetch current pricing from official sources before including it in a recommendation
- Both platforms have changed their AI feature names multiple times since 2024; prompt patterns should reference capabilities (e.g., "text-to-vector"), not product names that may change

## References
- https://www.figma.com/blog/figma-2026/
- https://developer.adobe.com/firefly-services/docs/
- https://uxtools.co/survey-2026/
- https://www.figma.com/developers/api
- https://www.adobe.com/creativecloud/business.html
