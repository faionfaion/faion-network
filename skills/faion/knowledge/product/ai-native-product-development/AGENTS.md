# AI-Native Product Development

## Summary

**One-sentence:** A product-strategy methodology for products where AI is not a feature but the delivery mechanism across all layers (research, design, development, testing, analytics, support), with pinned model versions, scored build-vs-buy, EU AI Act risk tier, and inference cost as first-class metrics.

**One-paragraph:** Products built without considering AI at the architecture level accumulate integration debt: AI is bolted on as a feature rather than woven into the delivery mechanism. The AI-native pattern shifts the dev loop from "build → test → iterate" to "define intent → AI generates → human refines → test", and treats the human refines step as a product feature with its own UX + telemetry. Inference cost, pinned model versions, build-vs-buy with a 12-18 month revisit date, and EU AI Act risk classification are first-class product concerns. Output: a per-component roadmap line carrying layer + model_id + risk_tier + build_or_buy + inference cost + refines UX.

**Ефективно для:** PM продукту, де AI — не фіча, а сам рушій доставки; не хоче, щоб roadmap перетворився на "напхати GPT в кожну кнопку".

## Applies If (ALL must hold)

- AI is the delivery mechanism, not a bolt-on feature.
- The team controls model selection (not a single managed vendor with no choice).
- Inference cost is material (≥10% of unit economics OR ≥$1k/month).
- The product spans ≥2 layers (research, design, dev, test, analytics, support) where AI could integrate.
- A named PM owner is accountable for the roadmap.

## Skip If (ANY kills it)

- The product has no AI components and none are planned — standard PM methodologies apply.
- Team is exploring whether to use AI at all — this methodology assumes the decision is made.
- Product operates in a domain where current AI cannot achieve acceptable quality (e.g. medical diagnosis without specialised fine-tuning).
- Sprint planning without strategic context — this methodology is strategy-layer, not task-execution.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Product description + target users | doc | product brief |
| Inference cost dashboard | URL | AI ops |
| EU AI Act risk-tier reference | doc | legal |
| Build-vs-buy scoring framework | YAML | this methodology's templates |
| Named PM owner | role + person | team roster |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/product/product-manager/agentic-ai-product-development` | Sibling for autonomous-agent products. |
| `geek/product/product-manager/ai-feature-de-risking` | Peer that consumes pinned model versions as gates. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: human-refines as feature, inference cost first-class, pinned models, scored build-vs-buy, EU AI Act hook | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~950 |
| `content/06-decision-tree.xml` | essential | AI-as-mechanism gate + build-vs-buy + risk-tier branches | ~360 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `layer_map_draft` | sonnet | Per-layer judgment from product description. |
| `build_vs_buy_score` | sonnet | Scoring against differentiator + data-advantage tests. |
| `eu_ai_act_classify` | opus | Cross-component risk reasoning with regulator alignment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-feature.py` | Build-vs-buy decision dataclass + recommendation logic. |
| `templates/prompt-layer-map.txt` | Prompt for the layer-map draft. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-native-product-development.py` | Validate roadmap-line JSON against the contract (pinned model_id, risk_tier present, build justified, inference cost set, refines UX wired). | Before roadmap commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[agentic-ai-product-development]] — sibling for autonomous-agent products.
- [[ai-feature-de-risking]] — peer methodology for shipping AI features safely.
- [[agent-pricing-and-unit-economics]] — peer that consumes the inference-cost figure.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first asks whether AI is the delivery mechanism. If just a bolt-on feature → route to traditional PM. Otherwise check pinned model + risk tier classified + build-vs-buy scored. If any are missing → block. Otherwise → emit the roadmap line.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ai-feature.py`

```python
"""AIFeature build-vs-buy decision model.

Input: feature attributes (differentiator, data advantage, speed priority).
Output: build/buy recommendation with 12-month review date.
"""
from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class AIFeature:
    name: str
    is_differentiator: bool
    has_data_advantage: bool
    speed_priority: bool
    review_date: date = field(default=None)

    def __post_init__(self):
        if self.review_date is None:
            self.review_date = date.today() + timedelta(days=365)

    def decision(self) -> str:
        if self.is_differentiator and self.has_data_advantage:
            return "BUILD"
        if self.is_differentiator and not self.has_data_advantage:
            return "BUY (now) -> BUILD (when data matures)"
        if self.speed_priority and not self.is_differentiator:
            return "BUY"
        return "BUY"
```

### `templates/prompt-layer-map.txt`

```text
You are a product manager creating an AI-native product strategy.

Product description: {product_description}
Target users: {target_users}
Current AI integration level: {current_level}  # none / partial / core

For each layer below, identify the top AI integration opportunity, rate it
(Impact 1-5, Effort 1-5), and recommend Build or Buy:

Layers: Research, Design, Development, Testing, Analytics, Support

Then apply the EU AI Act framework: classify each AI component by risk tier
(unacceptable / high / limited / minimal) and list the key obligations.

Output format:
Layer | Opportunity | Impact | Effort | Build/Buy
EU Component | Risk Tier | Key Obligations
```
