# AI-Native Product Development

## Summary

A product strategy methodology for products where AI is not a feature but the delivery mechanism across all layers (research, design, development, testing, analytics, support). The development loop shifts from "build → test → iterate" to "define intent → AI generates → human refines → test." Inference cost, model versioning, and explainability are first-class product concerns. Covers build-vs-buy decisions and EU AI Act compliance framing.

## Why

Products built without considering AI at the architecture level accumulate integration debt: AI is bolted on as a feature rather than woven into the delivery mechanism. The AI-native pattern treats the "human refines" step as a product feature — user refinements are the highest-quality training signal for future model improvements. Build-vs-buy decisions have a 12–18 month shelf life and must be revisited systematically.

## When To Use

- Writing roadmap strategy for a product where AI is the delivery mechanism across multiple layers
- Structuring a build-vs-buy decision for AI features for a stakeholder presentation
- Identifying which product layers are highest-priority candidates for AI integration
- Framing EU AI Act obligations for a product's AI components
- Transitioning a traditional product roadmap to AI-native where inference cost and model versioning are roadmap concerns

## When NOT To Use

- Product has no AI components and none are planned — standard product management applies
- Team is still exploring whether to use AI; this methodology assumes the decision is made
- Product operates in a domain where current models cannot achieve acceptable quality without specialized fine-tuning
- Sprint/quarter planning without a strategic product context — this operates at strategy layer, not task execution

## Content

| File | What's inside |
|------|---------------|
| `content/01-ai-layers.xml` | AI integration layer map; scoring opportunities by product layer |
| `content/02-build-vs-buy.xml` | Build-vs-buy decision rules; 12-month review cadence; compliance obligations |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-feature.py` | AIFeature dataclass with build/buy decision logic and review date |
| `templates/prompt-layer-map.txt` | Prompt for scoring AI integration opportunities per product layer |
