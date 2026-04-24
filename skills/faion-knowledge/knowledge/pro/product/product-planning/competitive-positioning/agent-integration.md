# Agent Integration — Competitive Positioning

## When to use
- Pre-launch positioning sprint: you have a product, 3-7 named alternatives, and need a defensible "for X who Y" statement before writing the landing page.
- Repositioning after a pivot or pricing change: existing copy no longer matches what you sell; agent regenerates the statement against current alternatives.
- New segment entry: you're keeping the product but targeting a new ICP and need a parallel positioning canvas for that segment.
- Pitch deck "why us, why now" slide: turn an analysed competitor matrix into a one-line differentiator with proof points.
- Category-creation decision: deciding between joining an existing category vs. naming a new one (highest-leverage strategic call; agent helps stress-test).
- Quarterly positioning audit: re-running the canvas to check whether the chosen unique attributes are still defensible.

## When NOT to use
- Before competitor analysis exists — positioning consumes a `competitor-analysis.md`; running it on imagined alternatives produces fiction. Run `pro/research/researcher/competitor-analysis` first.
- Before customer discovery: without 5-10 user interviews you cannot honestly fill "best-fit customer" or "what value do they care about". Run `user-research-at-scale` or `pain-points` first.
- Pure copywriting / headline polish — that is `landing-page-design`, not positioning. Positioning produces the strategic statement; copy is downstream.
- Internal tools, side projects, or anything where you are the only user — there is no market to position against.
- B2B-enterprise positioning that requires named-account research (Gartner Magic Quadrant placement, analyst relations) — agents lack the relationships and the data.

## Where it fails / limitations
- Garbage-in: if `competitive-alternatives` are wrong or imagined, every downstream section of the canvas is wrong; the agent will not flag this.
- "Better" trap: LLMs default to comparative-superlative language ("faster", "easier", "more powerful") even when prompted for differentiation. Requires explicit "no comparatives" instruction and a review pass.
- Category-creation overconfidence: agents will happily declare a new category for any product. Real category creation needs market education budget and 18-24 months; agent cannot estimate that cost.
- Best-fit-customer drift: without a hard segment definition, agents widen the ICP to "anyone who needs X". Pin the segment and reject any positioning that doesn't fail the "would this exclude Persona Y?" test.
- Defensibility blindness: agents call almost any attribute "unique" without checking whether competitors could ship it in a quarter. Force a "how long until competitors copy this?" column.
- Context rot: positioning is sensitive to wording; a regenerated statement 30 days later will drift even with the same inputs unless you version the canvas.

## Agentic workflow
Drive this with the `faion-research-agent` (or a dedicated `faion-positioning-agent` if available; otherwise reuse `faion-research-agent` in `mode: niche`) as the orchestrator on top of an existing `competitive-analysis.md`. The orchestrator runs Dunford's six steps serially because each step constrains the next: alternatives → unique attributes → value translation → best-fit customer → market category → statement. Fan out only the value-translation step (one parallel "so-what laddering" Task per attribute) since attributes are independent. Final synthesis writes `.aidocs/product_docs/positioning-canvas.md` and a one-page `positioning-statement.md`. Always run a `devil's-advocate` pass with a different model (sonnet → opus) that critiques the statement from each named competitor's CMO perspective.

### Recommended subagents
- `faion-research-agent (mode: niche)` — orchestrator; reads `competitive-analysis.md`, drives the six-step canvas, writes outputs. Model: opus (strategic synthesis, novel framing).
- `faion-research-agent (mode: competitors)` — upstream dependency; produces the alternatives table the canvas consumes.
- `faion-research-agent (mode: personas)` — upstream; produces best-fit-customer profiles. Without these, step 4 of the canvas is hand-waving.
- Per-attribute fan-out: spawn N parallel `Task` calls (haiku) for the "so-what laddering" — each takes one unique attribute and produces 3 levels of customer value.
- `faion-domain-checker-agent` — invoked if category creation produces a candidate name that needs a domain (`<category>.com` availability).
- `faion-sdd-executor-agent` — downstream consumer; reads `positioning-statement.md` when scoping landing-page copy, pricing-page hierarchy, or feature-prioritisation specs.
- Devil's-advocate: a second `faion-research-agent` invocation with role-prompt "you are the CMO of {competitor}; tear apart this positioning statement". Catches "better" framing and unsubstantiated claims.

### Prompt pattern

Orchestrator entry:

```
Task(
  subagent_type="faion-research-agent (mode: niche)",
  prompt="Build positioning canvas for {product}. Inputs:
  - .aidocs/product_docs/competitive-analysis.md (alternatives + matrix)
  - .aidocs/product_docs/user-personas.md (best-fit-customer source)
  Use Dunford's 6-step framework in
  pro/product/product-planning/competitive-positioning/README.md.
  Hard rules: no comparatives ('better/faster/easier'); every unique
  attribute must have a 'time-to-copy' estimate (quarters); reject any
  best-fit segment that includes >30% of the alternatives' user bases.
  Output: positioning-canvas.md + positioning-statement.md (one page).
  Then spawn devil's-advocate Task to critique from each top-3
  competitor's CMO POV; iterate once."
)
```

Per-attribute value-laddering fan-out:

```
Task(
  subagent_type="general-purpose",
  prompt="So-what ladder for attribute: '{attribute}'.
  Three levels: feature benefit → business benefit → emotional/strategic
  outcome. Bind the outcome to a measurable: hours saved, revenue,
  retention, peace-of-mind. No vague verbs ('improve', 'enhance')."
)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandoc` | Render canvas markdown → PDF/HTML for stakeholder review | `apt install pandoc` |
| `mermaid-cli` (`mmdc`) | Generate 2x2 positioning maps from the canvas as SVG | `npm i -g @mermaid-js/mermaid-cli` |
| `gh issue create` | File the canvas as a tracked decision in your repo for revisits | `gh` CLI |
| `git diff --word-diff` | Diff successive positioning statements quarter-over-quarter | bundled |
| `marp-cli` | Turn the canvas into a slide deck for the pitch | `npm i -g @marp-team/marp-cli` |
| `vale` (with proselint) | Linter that flags banned comparatives ("best", "better", "faster") | `brew install vale` |
| `searxng` (self-hosted) | Cross-check that competitor positioning statements match what you wrote | already running on faion infra (port 8888) |
| `wayback-cli` | Pull historical positioning lines from competitor homepages | `pip install waybackpack` |
| `jq` | Extract `unique_attributes[]` from a YAML canvas for downstream tooling | `apt install jq` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| April Dunford's *Obviously Awesome* workbook | Book | n/a | Source-of-truth methodology; agent should follow chapters 5-9 verbatim |
| Productboard | SaaS | API (paid) | Stores positioning per release; agent can push canvas via REST |
| Notion / Coda | SaaS | API | Living-document home for the canvas; agents can read/write via official APIs |
| Figma / FigJam | SaaS | Plugin API | Visual 2x2 positioning maps; export PNG to feed into the canvas doc |
| Mural / Miro | SaaS | API | Collaborative canvas-building if humans need to weigh in |
| Salesforce CRM (Won/Lost) | SaaS | API | Reality-check best-fit customer against actual won deals |
| Gong / Chorus | SaaS | API (paid) | Mine sales calls for the words customers use to describe alternatives — feeds the "competitive alternatives" cell with real language |
| Reddit (PRAW) | OSS lib | Python API | "We chose X over Y because…" threads; ground-truth for competitor weaknesses |
| Hacker News Algolia | Free | REST API | Sentiment around category-creation language (does "AI-powered X" land or feel hollow?) |
| Crayon / Klue | SaaS | API (paid) | Continuous competitive intel — feeds quarterly repositioning cycles |
| LangSmith / Helicone | SaaS | API | Track positioning-agent outputs over time; spot drift |
| Perplexity / Exa | SaaS | API | Cited search for "<competitor> positioning statement" — verify what they actually claim |

## Templates & scripts

The README ships the Positioning Canvas and Positioning Map templates. For agent-driven runs, this validator catches the most common LLM failure mode (comparative language masquerading as differentiation):

```bash
#!/usr/bin/env bash
# positioning-lint.sh — flag banned comparative language in a canvas
# Usage: ./positioning-lint.sh <positioning-statement.md>
set -euo pipefail
FILE="${1:?usage: $0 <file.md>}"

# Banned: pure comparatives without a stated dimension and number.
BANNED='\b(better|easier|simpler|faster|cheaper|more powerful|most|best)\b'
# Allowed: "5x faster than X", "30% cheaper at 10K subs" — flagged but kept.
ALLOWED_NUM='[0-9]+(x|%|\s*(min|hours|seats|subscribers))'

violations=$(grep -nEi "$BANNED" "$FILE" | grep -vE "$ALLOWED_NUM" || true)
if [ -n "$violations" ]; then
  echo "FAIL: comparative language without dimension+number:"
  echo "$violations"
  echo "→ rewrite as 'unlike X, we Y' with a concrete attribute."
  exit 1
fi

# Require structural skeleton: For/Who/Is/That/Unlike/We
for kw in "^For " "^Who " " is " "^That " "^Unlike " "^We "; do
  grep -qE "$kw" "$FILE" || { echo "FAIL: missing '$kw' line"; exit 1; }
done
echo "OK: positioning statement structurally sound."
```

Wire this into pre-commit on `.aidocs/product_docs/positioning-statement.md` so the agent cannot land a statement full of "we're better".

## Best practices
- Run positioning AFTER competitor-analysis AND user-personas — never in parallel. Both are inputs; canvas without them is fiction.
- Force the agent to fill the "Competitive Alternatives" cell with the literal verbatim from won/lost CRM notes ("we considered X but went with Y because…"), not from Google searches.
- Cap "unique attributes" at 3. More than 3 = no positioning, just a feature list. Agents over-list; trim hard.
- Add a "time-to-copy" column to the unique-attributes table. Anything copyable in <2 quarters is not a positioning anchor; it's a feature.
- The "so-what" ladder must terminate in a measurable outcome (hours, dollars, percent, retention) — not a vague verb. Reject "save time" without a number.
- Best-fit customer narrows over iterations, never widens. If round 2 of the canvas has a broader ICP than round 1, the agent regressed.
- Run a separate devil's-advocate pass with a different model (sonnet/opus combo) that role-plays each top-3 competitor's CMO and tries to dismiss your positioning. Iterate once.
- Version the canvas in git with a date stamp; quarter-over-quarter diff reveals positioning drift before customers notice.
- Test the statement against three "would this exclude…?" questions: (a) a persona you don't want, (b) a use case you don't serve, (c) a price point above/below yours. If none get excluded, the positioning is too broad.
- For category-creation decisions, require the agent to budget the education cost (analyst briefings, content marketing months, sales enablement). If the budget exceeds GTM runway, fall back to subcategory positioning.

## AI-agent gotchas
- Comparative language by default: LLMs love "better/faster/easier"; positioning demands "different". Mitigation: explicit prompt rule + `positioning-lint.sh` pre-commit hook (see above).
- Hallucinated competitor positioning: agent invents a tagline for Asana from training data instead of WebFetching their current homepage. Mitigation: pass live homepage HTML/text into the prompt, never let the agent rely on memory.
- Ladder collapse: the "so-what" laddering produces three levels that are paraphrases of the same thing. Mitigation: force each level to use a different noun (feature → business → emotion/strategy) and a measurable.
- Category-creation inflation: every product becomes "the first AI-native X". Mitigation: require a citation that the proposed category does NOT yet exist (G2 search returning zero results, no Wikipedia entry).
- Best-fit-customer fluff: agent writes "ambitious teams who want to ship faster" — meaningless. Mitigation: enforce a persona schema (role, company size, trigger event, current alternative, willingness-to-pay).
- Statement template skipping: agent drops the "Unlike" line because it feels confrontational. Mitigation: fail the build if the statement doesn't contain all six clauses.
- Drift on regeneration: re-running the canvas with the same inputs produces different language each time. Mitigation: temperature 0 for the synthesis step + commit the prompt seed alongside the output.
- "Future competitors are easy to dismiss" trap: agent dismisses big-tech threats; or alternatively over-inflates them. Mitigation: separate Task with a 5-year-horizon prompt and an evidence requirement (job posting, acquisition, beta product).
- Self-flattery in proof points: agent fills "Proof Points" with marketing copy ("trusted by leaders"). Mitigation: every proof point must be a citable URL, customer quote, or measurable outcome.
- **Human-in-the-loop checkpoints:** (1) approve the unique-attributes shortlist (no more than 3) before laddering, (2) sign off on best-fit-customer narrowing before the statement is drafted, (3) approve the final positioning statement before it lands in marketing/landing-page/pricing copy — this is a strategic decision agents must not own.

## References
- April Dunford, *Obviously Awesome* (2019) — canonical 10-step positioning framework; chapters 5-9 are the source for the canvas.
- April Dunford, *Sales Pitch* (2023) — extends positioning into the deck; useful for the proof-points section.
- Geoffrey Moore, *Crossing the Chasm* (1991/2014) — segment-and-niche-dominance reasoning; foundation for steps 4-5.
- Al Ries & Jack Trout, *Positioning: The Battle for Your Mind* (1981) — the original "you are positioned in the customer's mind, not in your spec sheet".
- Michael Porter, *Competitive Strategy* (1980) — Five Forces underlying competitive-alternatives analysis.
- A. Osterwalder, *Value Proposition Design* (2014) — pain-gain-job mapping for the value-translation step.
- `pro/research/researcher/competitor-analysis/agent-integration.md` — upstream dependency; how to produce the alternatives input this canvas consumes.
- `pro/research/researcher/agent-invocation/README.md` — `faion-research-agent` invocation reference.
- `solo/product/product-planning/` — sibling solo-tier positioning material when full PM stack isn't needed.
- Anthropic, *Building effective agents* (2024) — orchestrator-workers pattern (used here for value-laddering fan-out).
- Pmarca / a16z, *The only thing that matters* — product-market-fit lens for pressure-testing best-fit customer.
