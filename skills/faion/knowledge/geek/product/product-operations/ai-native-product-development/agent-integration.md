# Agent Integration — AI-Native Product Development

## When to use
- Defining the AI integration strategy for a new product from day one (not retrofitting AI onto an existing feature)
- Evaluating which layers of the product stack (research, design, development, testing, analytics, support) should use AI tooling vs. traditional approaches
- Making build-vs-buy decisions for AI features: is this a core differentiator or a commodity capability?
- Ensuring EU AI Act compliance is designed into the product before launch rather than bolted on after
- Choosing the right MVP pattern when the product's UX loop involves AI generation (define intent → AI generates → human refines)
- Briefing a product team or stakeholder on what "AI-native" means operationally and what it changes about delivery

## When NOT to use
- Product is purely data-driven without a generative or reasoning component — use standard product operations instead
- Team has no ML/AI production experience; AI-native development amplifies complexity for inexperienced teams before it accelerates delivery
- Infrastructure for AI (inference budget, observability, data pipelines) does not yet exist — set this up first
- Evaluating an existing feature for incremental AI enhancement; that is AI-augmentation, not AI-native design

## Where it fails / limitations
- "AI-native" often becomes "AI everywhere" — adding AI to every layer without a clear value hypothesis creates maintenance burden without user benefit
- EU AI Act compliance requirements are still being operationalized; specific obligations for AI systems in the EU change as implementing acts are finalized
- Bias testing in product development requires a representative dataset that most small teams do not have at MVP stage
- AI-generated content in product (copy, images, recommendations) can become stale or wrong as the underlying model is updated — versioning and regression testing AI outputs is non-trivial
- Build-vs-buy decisions have a time horizon: buying an API is faster today, but APIs can deprecate, raise prices, or change behavior without notice
- Cost model uncertainty: inference costs at scale are hard to predict accurately at MVP stage; many teams underestimate by 5–10x

## Agentic workflow
Use a product-design subagent to map the AI integration opportunities across all product layers (research, design, dev, test, analytics, support) and produce a scored recommendation table (impact vs. implementation effort). A second subagent generates the build-vs-buy decision matrix for each candidate AI feature by evaluating differentiation potential, data advantage, and time-to-market. A compliance subagent flags EU AI Act obligations for the product category and generates a compliance checklist tailored to the product type.

### Recommended subagents
- `faion-mlp-agent` (mode: analyze) — maps current product state and identifies gaps where AI integration would have the highest impact
- `ai-layer-mapper` — enumerates AI integration opportunities per product layer and scores them by impact and feasibility
- `build-vs-buy-evaluator` — applies the build/buy framework to each candidate AI feature; outputs a decision table
- `eu-ai-act-classifier` — classifies the product's AI components by risk tier and generates the required compliance checklist

### Prompt pattern
```
You are an AI product strategist. Given this product description, identify AI integration opportunities across these layers:
- Research: user research, sentiment analysis
- Design: AI design tools, prototyping
- Development: copilots, code generation
- Testing: AI test generation, bug detection
- Analytics: predictive analytics, anomaly detection
- Support: chatbots, ticket routing

For each opportunity, rate:
- Impact (1–5): how much does this improve the product?
- Effort (1–5): how hard is it to implement?
- Build or Buy: is this a differentiator (build) or commodity (buy)?

Product: {product_description}
Target users: {target_users}
```

```
Apply the EU AI Act framework to this product. Classify each AI component by risk tier
(unacceptable / high / limited / minimal) and list the obligations that apply.
Product AI components: {components}
Jurisdiction: EU
Deployment: {deployment_context}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` | Claude API for AI-native feature implementation | `pip install anthropic` / https://docs.anthropic.com |
| `openai` | OpenAI API for commodity AI features | `pip install openai` / https://platform.openai.com/docs |
| `langfuse` | AI product observability: track AI feature usage, quality, cost | `pip install langfuse` / https://langfuse.com |
| `great-expectations` | Data quality validation — critical for AI features that depend on training/inference data | `pip install great-expectations` / https://docs.greatexpectations.io |
| `mlflow` | Track AI model versions, experiments, and deployments | `pip install mlflow` / https://mlflow.org/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API | SaaS | Yes | Core reasoning, generation, and analysis features |
| OpenAI API | SaaS | Yes | Vision, embeddings, fine-tuning for commodity AI features |
| Langfuse | OSS/SaaS | Yes | AI product analytics: usage, cost, quality metrics per feature |
| PostHog | OSS/SaaS | Yes | Product analytics with AI event tracking; self-hostable |
| Weights & Biases | SaaS | Yes | Track AI model versions and evaluation results for built features |
| Intercom | SaaS | Partial | AI support chatbot; buy-not-build for commodity support layer |
| Linear | SaaS | Yes (API) | Issue tracking; integrates with AI-native dev workflow |

## Templates & scripts
See `templates.md` for the AI integration layer map template and build-vs-buy decision matrix.

Build vs. buy scoring function:
```python
from dataclasses import dataclass

@dataclass
class AIFeatureCandidate:
    name: str
    is_core_differentiator: bool   # True = unique to your product
    has_unique_data_advantage: bool # True = you have data competitors don't
    time_to_market_priority: bool   # True = speed matters more than control

def build_vs_buy(f: AIFeatureCandidate) -> str:
    """Simple heuristic: build if differentiator + data advantage; buy otherwise."""
    if f.is_core_differentiator and f.has_unique_data_advantage:
        return "BUILD"
    if f.time_to_market_priority and not f.is_core_differentiator:
        return "BUY"
    if f.is_core_differentiator and not f.has_unique_data_advantage:
        return "BUY (short-term) → BUILD (long-term)"
    return "BUY"
```

## Best practices
- Lock AI model versions in production; never pin to "latest" — model updates can silently break your product's behavior
- Design explainability into the UX from day one: users of AI-native products trust the product more when they understand why the AI made a decision
- Run bias audits on AI-generated content before launch, not after — catching bias in user research, generated copy, or recommendations requires a structured test plan
- Budget for inference costs at 3x your estimate; AI-native products consistently underestimate inference spend at scale
- Treat AI components as dependencies with SLAs: API uptime, latency percentiles, and version stability all affect your product reliability
- Version and regression-test AI outputs: if a model update changes the format or quality of generated content, you need to detect it before users do

## AI-agent gotchas
- Agents performing the "define intent → AI generates → human refines" loop must preserve the human refinement as training signal — do not discard user edits; they are the highest-quality signal for improvement
- EU AI Act compliance is not a one-time checklist — it requires ongoing monitoring and re-assessment when the model or training data changes; build compliance review into the release process
- Human-in-the-loop checkpoint: any AI-native product feature that personalizes content, makes recommendations, or takes action on behalf of the user requires a visible user control (turn off, override, explain) — this is both a regulatory requirement and a trust-building mechanism
- AI-generated UI copy or product content can drift from brand voice as underlying models update — establish a content QA step that compares new outputs against brand guidelines before deployment

## References
- https://docs.anthropic.com/en/docs (Anthropic Claude API)
- https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai (EU AI Act)
- https://langfuse.com/docs (AI product observability)
- https://mlflow.org/docs (model versioning and tracking)
- https://www.gartner.com/en/articles/what-is-agentic-ai (AI product trends 2026)
