# Agent Integration — AI-Native Product Development (Product Manager)

## When to use
- Writing roadmap strategy for a product where AI is not a feature but the delivery mechanism (AI-first architecture)
- Deciding which AI capabilities to build vs. buy for a given product; structuring the build-vs-buy decision for a stakeholder presentation
- Onboarding a product team to the "AI-native" development pattern: define intent → AI generates → human refines → test
- Framing EU AI Act obligations for a product — which AI components require documentation, explainability, and bias testing
- Identifying which product layers (research, design, dev, test, analytics, support) are highest-priority candidates for AI integration
- Transitioning a traditional product roadmap to an AI-native one where inference cost, model versioning, and explainability are first-class concerns

## When NOT to use
- The product has no AI components and none are planned — standard product management methodologies apply
- Team is exploring whether to use AI at all; this methodology assumes the decision to go AI-native is already made
- Product operates in a domain where current AI models cannot achieve acceptable quality (e.g., domain-specific medical diagnosis without specialized fine-tuning)
- Sprint/quarter planning without a strategic product context — this methodology operates at the strategy layer, not at the task execution layer

## Where it fails / limitations
- The "AI-native MVP pattern" (define intent → AI generates → human refines) works well for content and code generation products but maps poorly onto data pipelines, infrastructure tools, and B2B workflow automation
- EU AI Act compliance is a moving target; specific implementing acts change the obligations for high-risk AI systems — legal review is required, not just an agent-generated checklist
- Build-vs-buy decisions have a 12–18 month shelf life; the vendor landscape for AI APIs changes rapidly and the analysis should be revisited at each planning cycle
- Explainability requirements vary by jurisdiction and user expectation; what satisfies a regulator may not satisfy a user, and vice versa
- Bias testing in the development phase requires a structured evaluation dataset; most teams do not have one at MVP stage and skip the step, accumulating technical debt

## Agentic workflow
Use a product-strategy subagent to apply the AI integration layer map across the product stack and produce a scored opportunity table. A second subagent applies the build-vs-buy framework to each AI feature candidate, outputting a decision matrix. A compliance subagent generates an EU AI Act obligation checklist for the product's AI components by risk tier. The outputs feed into a roadmap document that a product manager reviews and edits before sharing with the team.

### Recommended subagents
- `faion-mlp-agent` (mode: analyze) — baseline the current product's AI integration level before proposing expansions
- `ai-layer-mapper` — scores AI integration opportunities per product layer (research/design/dev/test/analytics/support) by impact and feasibility
- `build-vs-buy-evaluator` — applies build/buy heuristics to AI feature candidates and outputs a decision table for stakeholder review
- `eu-ai-act-classifier` — classifies AI components by risk tier and generates the applicable compliance obligation list

### Prompt pattern
```
You are a product manager creating an AI-native product strategy.

Product description: {product_description}
Target users: {target_users}
Current AI integration level: {current_level}  # none / partial / core

For each layer below, identify the top AI integration opportunity, rate it
(Impact 1-5, Effort 1-5), and recommend Build or Buy:

Layers: Research, Design, Development, Testing, Analytics, Support

Then apply the EU AI Act framework: classify each AI component by risk tier
(unacceptable / high / limited / minimal) and list the key obligations.
```

```
Make a build-vs-buy recommendation for these AI features:
{feature_list}

For each feature, evaluate:
1. Is this a core differentiator (unique to our product)?
2. Do we have a unique data advantage?
3. Is speed-to-market the priority over long-term control?

Output a decision table: Feature | Build/Buy | Rationale | Review Date
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` | Claude as the AI engine for AI-native product features | `pip install anthropic` / https://docs.anthropic.com |
| `langfuse` | Track AI feature quality, cost, and usage as product metrics | `pip install langfuse` / https://langfuse.com |
| `linear` (API) | Roadmap management; AI-native features tracked here | https://linear.app/docs/graphql |
| `mlflow` | Version and track AI models used in built features | `pip install mlflow` / https://mlflow.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API | SaaS | Yes | Primary AI engine for AI-native product features |
| OpenAI API | SaaS | Yes | Commodity AI features (embeddings, vision, fine-tuning) |
| Langfuse | OSS/SaaS | Yes | AI product observability; measure quality per feature in production |
| PostHog | OSS/SaaS | Yes | Product analytics with AI event tracking; self-hostable |
| Linear | SaaS | Yes (API) | AI-native roadmap tracking and issue management |
| Notion | SaaS | Partial | Documentation layer for build-vs-buy decisions and compliance checklists |

## Templates & scripts
See `templates.md` for the AI integration layer map and build-vs-buy decision matrix templates.

Build-vs-buy scoring (reusable across planning cycles):
```python
from dataclasses import dataclass
from datetime import date, timedelta

@dataclass
class AIFeature:
    name: str
    is_differentiator: bool
    has_data_advantage: bool
    speed_priority: bool
    review_date: date = None

    def __post_init__(self):
        if self.review_date is None:
            # Set review date 12 months out by default
            self.review_date = date.today() + timedelta(days=365)

    def decision(self) -> str:
        if self.is_differentiator and self.has_data_advantage:
            return "BUILD"
        if self.speed_priority and not self.is_differentiator:
            return "BUY"
        if self.is_differentiator and not self.has_data_advantage:
            return "BUY (now) → BUILD (when data matures)"
        return "BUY"
```

## Best practices
- Treat inference cost as a first-class product metric alongside DAU, retention, and NPS — include it in every sprint review and roadmap update
- Lock AI model versions in the product spec; "latest" is not a version — specify the exact model ID and document the upgrade test plan
- Design the "human refines" step in the AI-native MVP loop as a product feature, not an internal workaround — user refinements are the highest-quality training signal for future model improvements
- Revisit build-vs-buy decisions annually or whenever a significant model or vendor change occurs; the landscape shifts fast enough to invalidate a 12-month-old decision
- Include AI behavior regression tests in the release process: when a model updates, validate that all AI-native features still produce outputs within the defined quality envelope

## AI-agent gotchas
- AI-native roadmaps often underestimate the "model maintenance" workload: prompt tuning, output quality monitoring, and model upgrade testing are ongoing costs that must appear in the roadmap as recurring tasks
- Human-in-the-loop checkpoint: build-vs-buy decisions made by an agent should always be reviewed by a product manager and a technical lead before being committed to the roadmap — the agent's analysis is a structured first draft, not the final answer
- EU AI Act obligation checklists generated by an agent are good starting points but are not legal advice; any product operating in a regulated domain must have legal counsel review the classification and obligations before public launch
- AI-native features that depend on third-party APIs introduce vendor risk: API deprecation, price changes, and capability regressions can all break the product without a code change — document the vendor risk and the fallback plan for each bought AI capability

## References
- https://docs.anthropic.com/en/docs (Anthropic Claude API)
- https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai (EU AI Act)
- https://langfuse.com/docs (AI product observability)
- https://mlflow.org/docs (AI model versioning)
- https://linear.app/docs/graphql (roadmap management API)
