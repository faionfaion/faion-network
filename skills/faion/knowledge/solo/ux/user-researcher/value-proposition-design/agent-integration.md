# Agent Integration — Value Proposition Design

## When to use
- Pre-launch positioning: before writing landing page copy or running ads
- After user research: translating raw interview findings into a structured Jobs/Pains/Gains canvas
- Competitive repositioning: when a new competitor enters and the current pitch no longer differentiates
- Investor pitch prep: the value proposition canvas maps directly to the "Why us?" slide
- Feature prioritization: pain relievers and gain creators ranked by severity guide the roadmap

## When NOT to use
- Before any user research — without customer evidence, the canvas is self-flattering fiction
- When the product is pivoting mid-development and the customer segment has not been re-validated
- As a one-time exercise — value propositions require iteration as the market responds; a canvas frozen at launch is a liability
- When the team cannot agree on the primary customer segment — resolve segmentation first

## Where it fails / limitations
- The canvas is a snapshot; it does not model how gains and pains shift as customers mature
- Agents filling the canvas without real user research data will hallucinate plausible-sounding pains that do not reflect the actual market
- "Fit" assessment is qualitative — the canvas does not calculate fit, it prompts structured thinking
- The formula-based value proposition statement (For/Who/Is/That/Unlike/We) produces mechanical copy; requires copywriter refinement for actual marketing use
- Pain severity ratings are subjective without explicit scoring methodology; teams disagree on what "extreme" means

## Agentic workflow
Claude subagents can generate a first-draft Value Proposition Canvas from a product description and available user research, produce the value proposition statement, and compare it against 2-3 listed competitors. The most reliable agent task is synthesizing interview findings into the Jobs/Pains/Gains structure — agent input should be raw quotes, not a summary. The Fit Assessment must be validated by a human with market context; agents will rate fit optimistically.

### Recommended subagents
- `faion-idea-generator-agent` — generates VP canvas, VP statement, and competitor positioning table
- `faion-research-agent` (mode: pains) — sources pain data from public channels to populate the Customer Profile

### Prompt pattern
```
Fill the Value Proposition Canvas for this product using the customer interview quotes below.
For each element, cite the specific quote that supports it.
Do NOT invent pains or gains not evidenced in the quotes.

Product: {description}
Target customer: {segment}
Interview quotes:
{quotes}

Output format:
- Customer Jobs: [list with evidence]
- Customer Pains: [list with severity: Extreme/Moderate/Minor, and evidence]
- Customer Gains: [list with type: Required/Expected/Desired, and evidence]
- Pain Relievers: [how product addresses each pain]
- Gain Creators: [how product creates each gain]
- Fit score: [1-5 per dimension, with reason]
```

```
Write 3 value proposition statement variants using the For/Who/Is/That/Unlike/We formula.
Each variant should emphasize a different differentiator.
Avoid marketing superlatives ("best", "easiest", "most powerful").

Customer: {segment}
Top pain: {pain}
Top gain: {gain}
Key differentiators vs. {competitor}: {differentiators}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `strategyzer` web app | Official VP Canvas tool; export to PDF/PNG | strategyzer.com |
| `miro` API | Create VP canvas boards programmatically | developers.miro.com |
| `notion` API | Store canvas as structured database | developers.notion.com |
| `figma` API | Export VP canvas diagrams from template | developers.figma.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Strategyzer | SaaS | No | Gold standard for the canvas; no API |
| Miro | SaaS | Partial | REST API for board creation; shapes and stickies supported |
| Notion | SaaS | Yes | Best for structured data storage of canvas elements |
| Typeform | SaaS | Yes | Customer survey to surface pains and gains at scale |
| Hotjar | SaaS | Partial | Open-text survey responses for pain mining |

## Templates & scripts
See `templates.md` for Value Proposition Canvas, Value Proposition One-Pager, and Fit Assessment.

Inline helper — score fit between customer profile and value map:
```python
def score_fit(pains: list[dict], pain_relievers: list[dict],
              gains: list[dict], gain_creators: list[dict]) -> dict:
    """
    Each pain/gain: {"label": str, "severity": "Extreme"|"Moderate"|"Minor"}
    Each reliever/creator: {"addresses": str, "relief_level": "Complete"|"Partial"}
    """
    addressed_pains = {r["addresses"] for r in pain_relievers}
    addressed_gains = {c["addresses"] for c in gain_creators}

    extreme_pains = [p for p in pains if p["severity"] == "Extreme"]
    covered_extreme = [p for p in extreme_pains if p["label"] in addressed_pains]

    required_gains = [g for g in gains if g["severity"] == "Required"]
    covered_required = [g for g in required_gains if g["label"] in addressed_gains]

    return {
        "pain_coverage": len(addressed_pains) / max(len(pains), 1),
        "extreme_pain_coverage": len(covered_extreme) / max(len(extreme_pains), 1),
        "required_gain_coverage": len(covered_required) / max(len(required_gains), 1),
        "overall_fit": "Strong" if len(covered_extreme) == len(extreme_pains) else "Partial",
    }
```

## Best practices
- Populate the Customer Profile before the Value Map — working in the opposite direction produces self-serving analysis
- Rank pains by severity before mapping pain relievers; a product that addresses 5 minor pains but ignores the one extreme pain has poor fit
- Use verbatim customer language in the canvas — "takes forever to sync" is more actionable than "slow synchronization"
- Test the value proposition statement with 5 target customers before using it in ads; if they cannot identify themselves in "For [target customer]", the segment is too narrow or the language is off
- Revisit the canvas after 90 days of shipping — pains that seemed extreme at discovery may have been solved by workarounds, revealing new priorities
- Map every gain creator and pain reliever to a specific product feature — if you cannot name the feature, the claim is aspirational, not a real proposition

## AI-agent gotchas
- Agents filling pains without interview data will anchor on the most common SaaS pains (pricing, onboarding, support) regardless of the actual product — always provide raw quotes as input
- VP statement generation tends to be generic when the differentiator is not explicitly named; force the agent to name the specific feature that makes the claim true
- Fit assessment by agents is optimistic by default; require the agent to identify the one extreme pain that the product does NOT address well
- "Gain" and "feature" are conflated by agents — a gain is a customer outcome ("feel in control"), not a product feature ("dashboard"); prompt must distinguish them
- Human checkpoint required before VP statement is used in marketing — agents cannot evaluate whether the claim is legally defensible or culturally appropriate

## References
- Alexander Osterwalder: *Value Proposition Design* (Wiley) — https://strategyzer.com/books/value-proposition-design
- April Dunford: *Obviously Awesome* — positioning methodology complementary to VP design
- Nielsen Norman Group: Communicating Value — https://www.nngroup.com/articles/value-proposition/
- Strategyzer Canvas tools: https://strategyzer.com/canvas/value-proposition-canvas
- April Dunford Positioning Canvas: https://aprildunford.com
