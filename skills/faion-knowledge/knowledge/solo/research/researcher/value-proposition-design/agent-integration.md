# Agent Integration — Value Proposition Design

## When to use
- Pre-launch: drafting positioning before landing-page copy, ad copy, or sales decks.
- Repositioning: when conversion is low and copy reads generic ("AI-powered platform for businesses").
- New segment expansion: same product, new audience needs a new value prop.
- Competitive shift: a major competitor changes pricing/positioning and you must respond.

## When NOT to use
- Before talking to users — you'll guess pains and gains.
- For mature products with established positioning where the cost of churn from rebrand is high.
- For internal tools where the "value" question is irrelevant.
- As a substitute for messaging tests — the canvas is a draft, not a final.

## Where it fails / limitations
- Strategyzer Value Proposition Canvas tempts feature-listing in the "Products & Services" box; LLMs will fall into this trap.
- The "fit" assessment is subjective; agents inflate fit scores when no negative evidence is provided.
- Pain Relievers and Gain Creators get conflated; a feature can't relieve every pain and create every gain.
- "Unlike X / We Y" formula is a positioning template, not a value prop — easy to confuse.
- Pains, gains, and jobs are interview outputs, not LLM guesses; without research, the canvas is fiction.

## Agentic workflow
Three-stage pipeline: (1) ingest validated research (interviews, JTBD, persona) and extract Customer Profile (jobs/pains/gains), (2) draft Value Map (products/relievers/creators), (3) check fit and produce a positioning statement + 3 testable headline variants. Run a separate "feature-leak detector" pass to flag value-prop drafts that read as feature lists. Human picks final headline; agent ships variants.

### Recommended subagents
- `customer-profile-builder` (sonnet) — extracts jobs/pains/gains from interview JSON.
- `value-map-drafter` (sonnet) — proposes Pain Relievers and Gain Creators per row, citing product feature.
- `feature-leak-detector` (haiku) — flags drafts that lead with capability instead of outcome.
- `headline-generator` (opus) — produces 5-7 differentiated headline variants for testing.
- `faion-idea-generator-agent` (referenced in README) for brainstorming differentiation angles.

### Prompt pattern
```
Role: customer-profile-builder.
Input: interviews.json, persona.md.
Output JSON: {jobs:{functional:[], emotional:[], social:[]},
              pains:[{description, severity:"extreme|moderate|minor", frequency, citations:[interview_ids]}],
              gains:[{description, type:"required|expected|desired|unexpected", citations:[]}]}.
Rule: every entry must cite ≥1 interview ID; refuse to output without research input.
```

```
Role: feature-leak-detector.
Input: value_proposition_draft.md.
Task: scan headline + benefits; flag any that lead with feature ("uses AI", "API-based", "with real-time"). Suggest outcome-led rewrite per flag.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandoc` | Convert canvas markdown ↔ slides for stakeholder reviews | https://pandoc.org |
| `htmlq` | Scrape competitor positioning from landing pages | https://github.com/mgdm/htmlq |
| `wcag-color-contrast` | Validate that on-brand value-prop copy meets WCAG | varies |
| `lighthouse` | Test landing-page performance after value-prop deploys | https://github.com/GoogleChrome/lighthouse |
| `optimizely-cli` / `vwo-cli` | A/B test headline variants | vendor-specific |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Strategyzer | SaaS | Limited (some API) | Native VPC tool; canonical templates. |
| Miro / Mural | SaaS | Yes (API) | Collaborative VPC boards; agent can populate. |
| Figma / FigJam | SaaS | Yes (API) | VPC frames with persona linkage. |
| Notion | SaaS | Yes (API) | Database-style canvas with research relations. |
| Wynter | SaaS | Yes (API) | B2B ICP message testing — cleaner than self-survey. |
| UsabilityHub / Lyssna | SaaS | Yes (API) | 5-second + preference tests for headlines. |
| Optimizely | SaaS | Yes (API) | Multi-variant headline tests. |
| VWO | SaaS | Yes (API) | Affordable A/B for headline tests. |
| PostHog feature flags | OSS+Cloud | Yes (API) | Roll out copy variants by cohort. |

## Templates & scripts
See `templates.md` for the Value Proposition Canvas and One-Pager.

Inline outcome-language linter (Python, ≤30 lines):
```python
import re, sys
FEATURE_LEAKS = [
    r"\bAI[- ]?powered\b", r"\bblockchain\b", r"\bcloud[- ]?native\b",
    r"\bAPI[- ]?based\b", r"\breal[- ]?time\b", r"\bplatform\b",
    r"\benterprise[- ]?grade\b", r"\bnext[- ]?generation\b",
]
text = open(sys.argv[1]).read()
for pat in FEATURE_LEAKS:
    for m in re.finditer(pat, text, flags=re.IGNORECASE):
        line = text[:m.start()].count("\n") + 1
        print(f"line {line}: feature-leak '{m.group(0)}'")
```

## Best practices
- Build the Customer Profile first, in full, BEFORE thinking about your product. This prevents reverse-engineering pains to fit features.
- One value prop per segment. A single line that fits everyone fits no one.
- Lead with the strongest pain or the desired gain — never the product category.
- Test 3-5 headline variants on cold traffic; intuition is unreliable.
- Refresh quarterly; markets move and yesterday's differentiator becomes table stakes.
- Tie each Pain Reliever / Gain Creator to a specific product feature — if you can't, the canvas is aspirational.

## AI-agent gotchas
- LLMs default to feature-led copy; explicit "no feature words" constraint plus a linter pass is mandatory.
- "Unlike X" is filled with weak differentiators ("more user-friendly"); require a measurable claim or named alternative.
- Pain severity is over-reported by the agent — every pain becomes "extreme". Force a distribution constraint (e.g., max 30% extreme).
- Gain types collapse to "expected"; force at least one "desired" or "unexpected" to push differentiation thinking.
- Headline generation works best at opus; fit assessment and template filling at haiku/sonnet.
- Human-in-loop checkpoints: (1) Customer Profile sanity check against interviews, (2) headline variant selection, (3) competitive claim verification.

## References
- Alex Osterwalder et al., "Value Proposition Design" (Strategyzer, 2014) — canonical text.
- Geoffrey Moore, "Crossing the Chasm" — the "For ... Who ... Unlike" template origin.
- April Dunford, "Obviously Awesome" — positioning practitioner guide, pairs with VPC.
- Bob Moesta, "Demand-Side Sales 101" — JTBD-driven value prop.
- Joanna Wiebe, Copyhackers — outcome-led copy patterns and message-mining workshops.
- Wynter "Message Testing" research reports — empirical data on B2B value prop performance.
