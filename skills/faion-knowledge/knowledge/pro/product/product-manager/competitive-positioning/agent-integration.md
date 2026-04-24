# Agent Integration — Competitive Positioning (PM angle)

> Sibling enrichment: `pro/product/product-planning/competitive-positioning/agent-integration.md` covers the Dunford methodology mechanics (canvas, six-step process, lint script, devil's-advocate pass). This file focuses on the **PM's role** — what positioning means inside a product org: how PM owns/influences it, how positioning becomes roadmap and prioritisation decisions, and how agents support the PM's specific responsibilities (not the marketer's).

## When to use
- PM owns a product whose positioning statement was last touched >2 quarters ago and the roadmap is starting to drift toward feature parity.
- New PM onboarding to an existing product: needs to internalise the positioning before approving any backlog item — agent helps reverse-engineer positioning from shipped features + landing copy + sales decks.
- Roadmap planning quarter: positioning must be the gate every initiative passes through ("does this initiative reinforce the unique attributes, or dilute them?").
- Pricing change or new tier launch: positioning constrains which features go in which tier; agent maps backlog items to positioning pillars.
- Feature kill decisions: a feature has shipped but doesn't reinforce any positioning pillar; PM uses positioning canvas as evidence to deprecate/sunset.
- Cross-functional alignment audit: marketing's landing page, sales' deck, support's macros, and product's roadmap all imply different positioning. PM owns reconciliation.
- Acquisition / inbound interest: investors or acquirers ask "what's your wedge?" — PM needs a positioning statement bound to product evidence (telemetry, win rates), not marketing claims.

## When NOT to use
- Marketing copy iteration — that's the CMO/marketing manager's domain. PM contributes inputs (unique attributes, target segment) but does not own headlines. Use `pro/marketing/growth-marketer/landing-page-design` instead.
- Brand/visual identity refresh — out of scope; positioning is strategic, brand is expressive.
- Pre-PMF products with <50 customers — there is no positioning to manage yet; run customer discovery first (`solo/product/product-planning/jobs-to-be-done`).
- Single-PM startups where PM = founder = marketer = sales — collapse roles and use the product-planning variant directly; the PM-specific role-split here adds overhead.
- Highly regulated B2B products where positioning is dictated by procurement RFPs and analyst categories (Gartner/Forrester) — PM's leverage is limited; the agent cannot influence analyst relations.

## Where it fails / limitations
- **Ownership ambiguity**: in many orgs positioning is "owned" by marketing but *constrained* by what the product actually is. Agents will cheerfully draft positioning that the product cannot deliver. PM must validate every claim against shipped behaviour, not roadmap promises.
- **Roadmap-positioning gap**: the canvas says "we are the simple alternative" but the backlog adds 14 enterprise features this quarter. Agents do not detect this drift unless explicitly asked to diff the backlog against the unique-attributes list.
- **Stakeholder-laundered positioning**: sales pushes for "we do X too" because they lost a deal; the agent will dutifully add X to the canvas. PM's job is to refuse, not to comply. Agents lack the political instinct.
- **Telemetry blindness**: positioning claims ("real-time collaboration is our differentiator") that aren't validated by usage data (only 3% of users use real-time collab). Agent doesn't pull telemetry unless given access — and even then, conflates "feature usage" with "feature value".
- **Incremental drift**: each quarter the agent's regenerated canvas is reasonable in isolation but the trajectory across 4 quarters has lost the original wedge. PM must track diffs across canvases, not just the latest one.
- **Roadmap prioritisation conflict**: RICE/ICE scoring inflates "Reach" and ignores "does this reinforce our positioning?". The agent will rank a positioning-diluting feature above a positioning-reinforcing one. Add a positioning-fit gate before the score.

## Agentic workflow
The PM uses positioning as a **decision filter**, not a deliverable. Agentic flow has three loops the PM owns: (1) **inbound loop** — the `faion-research-agent` consumes competitor analysis, user personas, and the existing canvas to keep positioning fresh; (2) **gate loop** — every backlog item, before it enters the next sprint, runs through a `positioning-fit-agent` that scores it against the unique-attributes list and flags drift; (3) **outbound loop** — when positioning shifts, the `faion-sdd-executor-agent` propagates the change into roadmap docs, PRDs, pricing pages, and OKRs. PM signs off at each loop boundary; agents do not own positioning decisions, they only surface evidence and produce drafts.

### Recommended subagents
- `faion-research-agent (mode: niche)` — owns the canvas itself; reused from the product-planning variant. Reads `competitive-analysis.md` + `user-personas.md`, regenerates canvas. Model: opus.
- `positioning-fit-agent` (custom; spawn via generic Task with the prompt below) — gate-loop evaluator. Takes a backlog item description + current canvas, returns `{score: 0-3, reinforces: [attr], dilutes: [attr], recommendation}`. Model: sonnet.
- `faion-research-agent (mode: competitors)` — upstream; quarterly competitor refresh. Outputs feed the canvas regeneration.
- `faion-sdd-executor-agent` — outbound-loop propagator; when canvas changes, it updates `roadmap.md`, OKR docs, pricing-page copy, sales enablement doc skeletons. PM reviews diffs.
- `faion-research-agent (mode: personas)` — when a positioning shift implies an ICP change, this regenerates the persona docs. PM must approve before the persona change ripples into PRDs.
- Devil's-advocate (second `faion-research-agent` invocation, role-prompt as competitor CMO) — same as the product-planning variant; PM runs this *before* socialising any new positioning internally so weak claims don't escape into Slack.
- `faion-domain-checker-agent` — if the canvas proposes a category-creation play, PM uses this to check if the candidate category name has a domain available (signal of seriousness).

### Prompt pattern

Gate-loop evaluator (run on every PRD/spec before it enters the sprint):

```
Task(
  subagent_type="general-purpose",
  prompt="You are a positioning-fit gate. Inputs:
  - canvas: {paste positioning-canvas.md}
  - backlog_item: {title + 1-paragraph description}
  Score the item 0-3 on 'reinforces our unique attributes':
    0 = orthogonal or dilutes (e.g. enterprise feature when we position as 'simple')
    1 = neutral (table-stakes; doesn't help or hurt)
    2 = reinforces one unique attribute
    3 = reinforces two or more unique attributes
  Return JSON: {score, reinforces:[attr], dilutes:[attr], rationale, recommendation:
  'ship|defer|reject|reframe'}. No prose outside JSON. If the item dilutes any
  unique attribute, recommendation must be 'reject' or 'reframe' regardless of score."
)
```

Quarterly canvas refresh trigger (PM runs at start of planning):

```
Task(
  subagent_type="faion-research-agent (mode: niche)",
  prompt="Refresh positioning canvas for {product}. Inputs:
  - .aidocs/product_docs/positioning-canvas.md (last quarter's)
  - .aidocs/product_docs/competitive-analysis.md (just refreshed)
  - .aidocs/product_docs/win-loss-q{N}.md (CRM dump)
  - .aidocs/product_docs/usage-telemetry-q{N}.md (which features actually get used)
  Produce: (1) new canvas, (2) diff vs last quarter (added/removed/reframed
  unique attributes), (3) drift report flagging unique attributes that are NOT
  supported by telemetry (claim without usage), (4) backlog-impact list:
  which in-flight roadmap items are now mis-aligned. Do NOT change the
  canvas if the diff would invalidate >50% of the in-flight roadmap without
  PM sign-off — instead, output a 'breaking-change' report."
)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh project` (GitHub Projects v2) | Tag every issue with a `positioning-pillar` field; PM filters roadmap by pillar coverage | `gh extension install github/gh-projects` |
| `linear-cli` | Same as above for Linear-using teams; tag issues with positioning attribute | `npm i -g @linear/cli` |
| `productboard` API via `curl` | Push refreshed positioning into Productboard so feature evidence stays bound to the canvas | docs.productboard.com/reference |
| `jira` CLI / `acli` | Add a `Positioning Fit` custom field to every story; gate-loop agent fills it | `brew install ankitpokhrel/jira-cli/jira-cli` |
| `pandoc` + `marp` | Render canvas + diff into a one-pager for the quarterly review | `apt install pandoc; npm i -g @marp-team/marp-cli` |
| `git diff --word-diff` on `positioning-canvas.md` | Quarter-over-quarter drift in the PM's own words | bundled |
| `vale` (proselint) | Lint roadmap docs / PRDs for off-positioning language ("enterprise-grade" in a "simple-tool" product) | `brew install vale` |
| `dbt` / `metabase` CLI | Pull usage telemetry to validate that claimed unique attributes are actually used | dbt-labs.com / metabase.com |
| `jq` + `yq` | Extract `unique_attributes[]` from canvas YAML, join against backlog export | `apt install jq; pip install yq` |
| `gong-api` (paid) / Reddit PRAW | Sales-call mining + community sentiment to ground "competitive alternatives" cell in real customer language | docs.gong.io / praw.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Productboard | SaaS | REST API | Bind every feature to a positioning pillar; PM's primary positioning-aware backlog tool |
| Linear / Jira | SaaS | API | Custom field `positioning-fit` (0-3) populated by gate-loop agent |
| Notion / Coda | SaaS | API | Living-canvas home; PMs publish + comment; agent reads/writes |
| Looker / Metabase / Hex | SaaS | API | Telemetry source for "is this unique attribute actually used?" |
| Gong / Chorus | SaaS | API (paid) | Sales-call language → competitive-alternatives input |
| Salesforce / HubSpot | SaaS | API | Win/loss reasons → positioning evidence; agents pull `Closed Lost Reason` |
| Productlift / Canny | SaaS | API | Customer requests; PM's signal that current positioning is or isn't being received |
| Dovetail / Aurelius | SaaS | API | Research-repo for personas; binds positioning to evidence quotes |
| Mixpanel / Amplitude / Posthog | SaaS / OSS | API | Feature-usage data validating each unique attribute |
| Pendo | SaaS | API | In-app messaging tied to positioning pillars; PM measures pillar comprehension |
| Klue / Crayon | SaaS | API (paid) | Always-on competitor watch; quarterly trigger for canvas refresh |
| Maze / Useberry | SaaS | API | Test positioning statements with users; PM owns the test |
| LangSmith / Helicone | SaaS | API | Trace positioning-fit agent calls; spot prompt drift, model regressions |

## Templates & scripts

The product-planning sibling ships the canvas template and a comparative-language linter. The PM-specific addition is a **roadmap-vs-canvas drift report** that catches a backlog actively diluting positioning:

```bash
#!/usr/bin/env bash
# roadmap-positioning-drift.sh — flag backlog items that dilute positioning.
# Inputs:
#   $1 — positioning-canvas.md (with a YAML frontmatter `unique_attributes:`)
#   $2 — backlog.csv with columns: id,title,description,positioning_fit
# Output: drift table + non-zero exit if dilution detected.
set -euo pipefail
CANVAS="${1:?canvas.md}"; BACKLOG="${2:?backlog.csv}"

# Pull unique attributes from frontmatter.
ATTRS=$(awk '/^unique_attributes:/{flag=1;next}/^[a-z_]+:/{flag=0}flag' "$CANVAS" \
  | sed 's/^[[:space:]]*-[[:space:]]*//;/^$/d')

[ -z "$ATTRS" ] && { echo "FAIL: no unique_attributes in canvas frontmatter"; exit 1; }

# Score each backlog item against attribute reinforcement (regex grep, naive).
echo "id,title,positioning_fit,reinforces,dilutes"
DILUTED=0
while IFS=',' read -r id title desc fit; do
  [ "$id" = "id" ] && continue
  reinforces=""; dilutes=""
  while IFS= read -r attr; do
    grep -qiE "$attr" <<<"$title $desc" && reinforces="$reinforces;$attr"
  done <<<"$ATTRS"
  # Heuristic: if fit is 0 or contains "enterprise|sso|audit" while attrs say "simple|solo", flag dilution.
  if [ "$fit" = "0" ] || grep -qiE '\b(enterprise|sso|saml|audit-log|compliance)\b' <<<"$title $desc" \
     && grep -qiE '\b(simple|solo|individual|personal)\b' <<<"$ATTRS"; then
    dilutes="enterprise-vs-simple"; DILUTED=$((DILUTED+1))
  fi
  echo "$id,\"$title\",$fit,${reinforces#;},$dilutes"
done < "$BACKLOG"

[ $DILUTED -gt 0 ] && { echo "FAIL: $DILUTED items dilute positioning" >&2; exit 2; }
echo "OK: no dilution detected." >&2
```

Wire into CI for the `roadmap.md` repo or run as a pre-planning gate. Output goes into the quarterly review; PM defends or reframes each flagged item.

## Best practices
- **Positioning is a gate, not a deliverable**: every PRD's first page must answer "which positioning pillar does this reinforce?". Reject PRDs that cannot answer.
- **Bind positioning claims to telemetry**: a unique attribute that <10% of users actually exercise is not a positioning anchor — it's a marketing fiction. PM owns the validation.
- **Cap the canvas at 3 unique attributes**, then map every roadmap initiative to exactly one. If an initiative reinforces zero, kill or reframe.
- **Diff canvases quarter-over-quarter**, not just the latest. Drift over 4 quarters is invisible in any single diff.
- **Use win/loss reasons as ground truth** for the "competitive alternatives" cell — what did we actually compete against, in customers' words. Trumps any agent-generated competitor list.
- **PM signs off, agents draft**: never let the agent's regenerated canvas auto-publish. Human-in-the-loop at every canvas update.
- **Roadmap reviews include a "positioning fit" column** alongside RICE; veto positioning-zero items even if RICE-high.
- **Cross-functional alignment ritual**: once per quarter, PM walks marketing, sales, and support through the canvas. Capture mismatches; close them in 30 days.
- **Resist sales-driven positioning expansion**: every "we lost a deal because we don't do X" request must be answered with "is X aligned with our positioning?" — most aren't.
- **Track "off-positioning shipped"** as an anti-metric: count features shipped that scored 0 on positioning-fit. Trend-down target.
- **Tie pricing tiers to positioning pillars**: the most-differentiated pillar belongs in the highest tier; commodity features in the lowest. Agent surfaces conflicts; PM decides.

## AI-agent gotchas
- **Roadmap-blind canvas regeneration**: agent regenerates the canvas without checking whether the in-flight backlog can deliver the new positioning. Mitigation: every regen prompt must include the in-flight roadmap and emit a "breaking-change" report when >50% would be invalidated.
- **Telemetry-claim divergence**: agent claims "real-time collab is unique" because it appears in marketing copy, while only 2% of MAU touches it. Mitigation: pass usage data into the canvas prompt; require unique attributes to have ≥10% adoption or an explicit "future bet" tag.
- **Sales-laundered positioning**: agent dutifully widens the canvas to absorb every lost-deal feature request. Mitigation: pre-process win/loss notes to extract *category* of competitor, not feature checklists; reject feature-list dilution at prompt level.
- **PRD positioning-section autofill fluff**: agents generate "this reinforces our customer-centric approach" as a generic answer. Mitigation: require a specific named unique attribute from the canvas; reject "customer-centric" / "best-in-class" / "innovative" as positioning fillers.
- **OKR cascade misalignment**: the agent updates the canvas but doesn't propagate to OKRs; quarterly OKRs still reference last quarter's positioning. Mitigation: outbound-loop agent must touch `okrs.md`, `roadmap.md`, `pricing.md`, `sales-deck.md` atomically with a single PR.
- **Positioning-fit score gaming**: backlog authors learn the agent's heuristics and stuff PRDs with positioning keywords to score 3. Mitigation: rotate the scoring prompt; require a citation (canvas section + telemetry signal) for any score ≥2.
- **Pricing-tier conflation**: agent puts table-stakes features in the high tier because they're "differentiated"; PM ends up with a non-competitive low tier. Mitigation: separate "unique attribute" from "premium feature"; require the agent to mark each.
- **Devil's-advocate fatigue**: PM stops running the competitor-CMO critique because it always finds something. Mitigation: track which critiques the PM rejected and why; agents that lose 80%+ of critiques get prompt-tuned, not silenced.
- **Acronym drift**: positioning claims use jargon ("AI-native", "agentic", "vertical-AI") that means nothing to customers. Mitigation: lint the statement against a banned-buzzword list; reject if customer interview transcripts don't contain the term.
- **Human-in-the-loop checkpoints (PM-specific):** (1) PM approves the regenerated canvas before any downstream doc updates; (2) PM signs off on each "ship/defer/reject" recommendation from the gate-loop agent — agents must not auto-close issues; (3) PM personally walks marketing/sales/support through canvas changes — agents draft the talking points, not the meeting; (4) PM owns the call on category-creation vs subcategory positioning — agents flag the question, never decide it.

## References
- April Dunford, *Obviously Awesome* (2019) — base methodology; mechanics covered in the product-planning sibling file.
- Marty Cagan, *Inspired* (2017) — PM's role in product strategy; positioning as the strategic frame for prioritisation.
- Marty Cagan, *Empowered* (2020) — product-strategy chapters on focus and insight; the PM's job is to choose what NOT to do.
- Melissa Perri, *Escaping the Build Trap* (2018) — outcome-over-output framing; positioning is the outcome scaffold for the roadmap.
- John Cutler, *The Product Model & The Strategy Stack* (Substack, 2023+) — multi-layer alignment from positioning → bets → roadmap → backlog.
- Roman Pichler, *Strategize* (2020) — product strategy tied to positioning; PM-centric vocabulary.
- Teresa Torres, *Continuous Discovery Habits* (2021) — keeps positioning honest by binding it to ongoing customer evidence.
- April Dunford, *Sales Pitch* (2023) — bridges positioning to sales-deck structure; PM uses it to align sales narrative.
- `pro/product/product-planning/competitive-positioning/agent-integration.md` — sibling Dunford-mechanics enrichment; this PM file builds on it.
- `pro/product/product-manager/release-planning/` — downstream consumer; release plans must inherit positioning fit.
- `pro/product/product-manager/portfolio-strategy/` — multi-product positioning where canvases must be mutually consistent.
- `pro/product/product-manager/stakeholder-management/agent-integration.md` — cross-functional alignment patterns referenced above.
- Anthropic, *Building effective agents* (2024) — orchestrator-workers and evaluator-optimizer patterns used for the gate-loop.
