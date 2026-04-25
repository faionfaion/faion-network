# Agent Integration — Brand Positioning

## When to use
- New product / new market segment: derive a positioning statement from research before writing copy.
- Refresh of stale messaging: existing positioning blends with competitors, prospects can't repeat what you do.
- Pre-launch evaluation: stress-test a positioning statement against competitive alternatives and customer interviews.
- Sales / marketing alignment: produce the messaging hierarchy (one-liner → elevator pitch → 3 key messages → proof points).
- Category strategy decision: existing-category vs sub-category vs new-category framing with explicit tradeoffs.

## When NOT to use
- Tactical copy production (headlines, ads, email subject lines) — use copywriting methodologies; positioning is upstream.
- Brand-identity (logo, palette, typography) — different domain (`faion-ui-designer`).
- Personas-from-scratch — use persona-building methodology; positioning consumes personas, doesn't produce them.
- Competitive intelligence on individual rivals — use `growth-competitor-analysis`; positioning consumes that output.
- Repositioning a public-traded brand under shareholder scrutiny — communications/PR coordination beyond methodology scope.

## Where it fails / limitations
- Methodology assumes the team has done customer interviews; without that input, agents will hallucinate target-customer pain.
- "Find your only" exercise often produces fake uniqueness if research is thin — small teams claim differentiators competitors trivially also have.
- Category creation guidance is brief; the failure mode (creating a category nobody searches for) is real and harder than the doc implies.
- Positioning maps (2x2 grids) bias toward two axes; multi-dimensional differentiation is hard to render and hard to communicate.
- Doesn't cover repositioning during pivots — different psychological/customer-trust dynamics.
- B2B-leaning frame; B2C consumer-brand positioning often hinges on emotional/identity vectors barely addressed.

## Agentic workflow
Sequence: (1) research agent gathers customer interview transcripts + competitor pages + review-site data, (2) synthesizer agent produces draft positioning canvas, (3) validator agent runs Dunford-style check (is it specific? is it grounded in real alternatives? does it own one differentiator?), (4) human refines, (5) agent rolls forward to messaging hierarchy and Wynter-style preference tests. Pair with `growth-gtm-strategy`, `research/market-researcher`, `comms/communicator`.

### Recommended subagents
- `faion-content-agent` (source README) — owns canvas synthesis and messaging hierarchy.
- `faion-researcher` — pulls customer interviews, competitor pages, review sites, sub-reddit threads.
- `faion-brainstorm` — diverge phase: candidate angles, alternative target-customer slices, different category framings.
- `faion-improver` — quarterly: review whether positioning is still distinctive vs newly-launched competitors.
- General-purpose Claude subagent — Dunford "Obviously Awesome" validator pass against the canvas.

### Prompt pattern
```
You are running the April Dunford positioning validator on this draft:
<canvas>
Check: (1) is target customer specific enough to disqualify wrong-fit prospects?
(2) is the unique value something competitors literally cannot claim?
(3) is the category choice intentional and defended? (4) would a customer repeat
this positioning back accurately? Output: per-question pass/fail + improvement suggestion.
```

```
Given customer interview snippets <attached>, extract:
- exact phrases customers use for the problem,
- alternatives they considered or use today,
- top 2 emotional drivers,
- top 2 functional drivers,
- objections to current solutions.
Do not paraphrase — keep customer language verbatim.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Track positioning artifacts in repo; PRs for amendments | cli.github.com |
| `pandoc` | Convert canvas markdown to PDF for stakeholder review | pandoc.org |
| `whisper` (OpenAI Whisper or whisper.cpp) | Transcribe customer interview recordings locally | github.com/openai/whisper |
| `claude-cli` (this harness) | Drive multi-step diverge/converge synthesis | docs.anthropic.com/en/docs/claude-code |
| `playwright` | Pull competitor homepage copy for comparison | playwright.dev |
| `archiver-cli` (Wayback) | Track competitor messaging changes over time | archive.org/wayback/availability |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Wynter | SaaS | Partial | B2B message-testing with real ICP panels; manual but high-signal. |
| UserTesting | SaaS | Partial | Recorded reactions to messaging; agent processes transcripts. |
| Maze | SaaS | Yes | Unmoderated tests + APIs; quick A/B on message variants. |
| Crayon / Klue | SaaS | Yes | Competitor-intel automation; surfaces messaging diffs. |
| Kompyte | SaaS | Yes | Competitive monitoring with API. |
| Gong / Chorus | SaaS | Yes | Sales-call transcripts → ICP language extraction. |
| Grain | SaaS | Yes | Lighter Gong alternative; transcript API. |
| Notion / Frontify / Lingo | SaaS | Yes | Brand guidelines + messaging hierarchy hosting. |
| FletchPMM templates | Service | n/a | Anthony Pierri's homepage templates; useful reference. |

## Templates & scripts
See `templates.md` for positioning canvas, messaging hierarchy, and brand voice doc. Inline canvas validator:

```python
# Lightweight Dunford-style canvas check
def validate_canvas(canvas):
    issues = []
    target = canvas.get("target_customer", "")
    if len(target.split()) < 6 or "businesses" in target.lower() or "developers" in target.lower():
        issues.append("Target customer too broad — name role + company-type + situation.")
    alts = canvas.get("alternatives", [])
    if not alts or len(alts) < 2:
        issues.append("List at least 2 competitive alternatives + the status-quo option.")
    unique = canvas.get("unique_capabilities", [])
    if len(unique) > 3:
        issues.append("Pick 1-2 differentiators to own; >3 dilutes the claim.")
    if not canvas.get("category"):
        issues.append("Choose category strategy: existing | sub-category | new | versus.")
    proof = canvas.get("proof_points", [])
    if len(proof) < 2:
        issues.append("Need >=2 proof points (metrics, named customers, awards).")
    return {"ok": not issues, "issues": issues}
```

## Best practices
- Interview customers in their words first; positioning written without verbatim language reads as marketing-team folklore.
- Disqualify prospects on purpose. Strong positioning shrinks the addressable market by design and lifts conversion among fit.
- Pick one differentiator and over-invest in it for 12+ months. Multi-pillar positioning is forgettable.
- Frame against alternatives explicitly ("unlike X, we Y"); customers always frame against alternatives, so own the framing.
- Test the positioning by asking customers to describe you to a peer. If they invent their own version, your positioning isn't sticking.
- Track competitor homepage diffs monthly; if a competitor moves toward your space, escalate to a positioning review.
- Keep an internal positioning doc separate from customer-facing one-liner; the internal doc is denser and covers tradeoffs.
- Only create a new category if you can fund market education for 2+ years. Otherwise use sub-category framing.

## AI-agent gotchas
- LLMs default to category-defining puffery ("the leading platform"); strip these before any review. Force concrete claims tied to proof points.
- Agents will conflate features with differentiators. Run a follow-up pass: "Can a competitor ship this in 6 months? If yes, it's a feature, not positioning."
- Positioning generated without customer-language input reads as bland and inside-out. Block synthesis until verbatim quotes are in context.
- Competitive analysis from web scraping captures stated positioning, not actual market perception. Layer in review-site sentiment.
- Auto-generated category names are often unsearchable nonsense ("Revenue Intelligence Cloud Platform"). Validate against Google search volume and analyst categories.
- Messaging hierarchies will drift if regenerated each cycle; maintain the hierarchy in version control and amend, don't recreate.
- Agents over-cite Dunford / Crossing the Chasm / Ries-Trout without distinguishing when each applies; Crossing the Chasm is for early-market enterprise tech, not consumer SaaS.
- Translation/localization: positioning that works in English often fails when literally translated. Re-do the canvas per language market.

## References
- April Dunford — "Obviously Awesome" — https://www.aprildunford.com/obviously-awesome
- April Dunford — "Sales Pitch" — https://www.aprildunford.com/sales-pitch
- Anthony Pierri / FletchPMM — homepage messaging — https://www.fletchpmm.com/
- Geoffrey Moore — "Crossing the Chasm" — https://www.amazon.com/dp/0062292986
- Ries & Trout — "Positioning: The Battle for Your Mind" — https://www.amazon.com/dp/0071373586
- Wynter B2B message testing — https://wynter.com/
- Sibling methodology: `growth-gtm-strategy/README.md`
- Sibling methodology in copywriting skill: `copywriting-fundamentals`
