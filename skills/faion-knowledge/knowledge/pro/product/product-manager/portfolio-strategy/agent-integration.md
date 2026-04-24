# Agent Integration — Portfolio Strategy (Product Manager angle)

> Companion to `pro/product/product-planning/portfolio-strategy/agent-integration.md`,
> which covers the strategy-side mechanics (rubric, classifier, rebalancer, CLI).
> This file focuses on the **PM-as-role** angle: single-product PM vs portfolio
> PM, cross-product trade-offs, and PM-level vs portfolio-level prioritization.

## When to use
- A single PM has been asked to own ≥ 2 shipped products (common in solopreneur / small-team contexts: faion-net runs nero, neromedia, pashtelka, longlife, ender, mediamanager under one human owner) and needs an explicit framework before backlogs collide.
- Promoting an IC PM to Group PM / Portfolio PM: their decision frame must shift from "what is the best feature for product X" to "which product gets the next engineer-week".
- Two product squads each have a defensible quarterly plan, but the org cannot fund both at full speed — a portfolio-level PM call is needed to choose.
- Defining the **handoff line** between portfolio strategy (CPO / Head of Product) and product PM execution: who owns 70/20/10 ratios, who owns the in-product roadmap, who owns sequencing, who owns ship dates.
- Quarterly review: the product PM has hit their product-level OKRs but the portfolio is unbalanced (e.g. all PMs ship H1 incrementally, nobody owns H3). Need a re-allocation conversation.

## When NOT to use
- A single-product PM with one product line — there is no portfolio at the PM level; use feature-prioritization frameworks (RICE / WSJF / Kano) instead.
- Pure team-topology / hiring decisions (who reports to whom). Use Team Topologies, not portfolio strategy.
- Roadmap-internal trade-offs **inside** one product (feature A vs feature B in the same SKU). That is product-level prioritization, not portfolio.
- Resource arguments that are really about engineering capacity (sprint planning, on-call). Capacity planning ≠ portfolio strategy.
- Crisis quarter where one product is on fire — defer portfolio review until the fire is out.

## Where it fails / limitations
- **Role ambiguity**: in small orgs the same person plays product-PM and portfolio-PM; the framework cannot resolve a conflict-of-interest if the same human owns both hats. Force a written allocation memo to make the trade-off visible to others.
- **Local optimization**: a product PM optimizing their P&L will always argue for more H1 inside their product. Aggregate across PMs and the portfolio drifts to 95% H1 with no transformational bets. Counter-measure: the portfolio-PM owns the H3 budget separately.
- **Cross-product synergy invisibility**: portfolio math (70/20/10) does not score "shared platform leverage" — work that benefits 3 products simultaneously gets under-counted. Product PMs of dependent products will resist sharing their roadmap slot to fund shared infra.
- **Different lifecycle stages**: portfolio strategy assumes products are commensurable. A 6-month-old MVP and a 4-year-old cash cow have different KPIs (activation vs retention vs LTV); applying one set of horizon rubrics flattens that nuance.
- **PM career incentives skew bets**: PMs are promoted on launches → they prefer H1/H2 (ships predictably) over H3 (likely to die). Portfolio-PM must explicitly insulate H3 PMs from launch-count metrics.
- **Solo founder failure mode**: one human cannot really run a 70/20/10 split across 6 products — exploration time collapses to zero under operational load. Document the collapse honestly instead of pretending the ratio is real.

## Agentic workflow
Drive this with three role-aware passes. (1) **Product-PM pass** — for each product, a sonnet agent reads the product's backlog + OKRs + recent retros and emits a per-product allocation in horizon terms (`{product, h1_pct, h2_pct, h3_pct, key_evidence}`). (2) **Portfolio-PM pass** — an opus agent aggregates across products, weighs cost-of-engineering per product, and detects role-level anti-patterns ("PM A is 100% H1; PM B is 100% H3; portfolio is bimodal not balanced"). (3) **Reconciliation pass** — output a structured memo that names which product gets cut, which gets accelerated, and which PM owns the H3 budget for the next quarter. All three passes must produce JSON; the reconciliation memo is the only prose artifact, and it goes to a human PM-of-PMs for sign-off, never auto-applied.

### Recommended subagents
- `faion-brainstorm` — when product PMs deadlock over which product is H3-eligible, run a diverge / converge / review cycle with each PM as a synthetic role.
- `faion-improver` — quarterly meta-loop: read last quarter's portfolio memo, the actual delivered allocation, and the PM-level OKR scores; log "what the portfolio said vs what the PMs actually shipped" as a recurring mistake-pattern.
- `faion-sdd-executor-agent` — once the portfolio memo is signed off, spin per-product SDD plans whose scope is bounded by the agreed allocation.
- A custom `pm-role-classifier` subagent (worth creating): input = a PM's quarterly plan; output = `{role_mode: "product"|"portfolio"|"mixed", scope_overlap_with_other_pms, recommended_handoff_line}`. Use it before promotions or re-orgs.
- `faion-feature-executor` — for the H1 portion of each product, where execution discipline matters more than strategic exploration.

### Prompt pattern
```
You are a portfolio PM. Inputs: list of products with {product_id, owner_pm,
quarterly_plan, eng_cost_usd, current_revenue_usd, lifecycle_stage}. Output JSON:
{
  per_product: [{product_id, recommended_horizon_mix:{h1,h2,h3}, rationale}],
  portfolio_total: {h1,h2,h3},
  pm_role_findings: [{owner_pm, role_mode, risk}],
  reallocation_memo: "<<= 6 bullets, plain English, names cuts and bets>>"
}
Constraints:
- Do NOT invent products not in the input.
- If two PMs own overlapping scope (>30%), flag as `role_conflict` in pm_role_findings.
- Never recommend >10% H3 for a product whose lifecycle_stage = "pre-PMF".
```

```
You are a single-product PM defending allocation. Given your product's backlog
and the portfolio's target {th1, th2, th3}, output JSON:
{
  agreed_cuts: [{item_id, reason}],
  contested_cuts: [{item_id, counter_argument, evidence_url}],
  cross_product_dependencies: [{item_id, depends_on_product, blocking_severity}]
}
Stay inside your product. Do not propose cuts to other products.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `linear` API (`@linear/sdk`) | Read per-project (= per-product) issue counts, owners, labels; aggregate per-PM | https://developers.linear.app |
| `productboard` API | Pull "products" + "objectives"; map each PM's owned objectives to a horizon | https://developer.productboard.com |
| `airtable` CLI / API | Cheap per-product roster ↔ PM matrix; agents can read both sides | https://airtable.com/developers |
| `notion` API | If portfolio memo lives in Notion, agent posts the reconciliation memo as a draft for human sign-off | https://developers.notion.com |
| `gh` (GitHub CLI) | Map PM → owned repos / projects v2 boards; useful when "product" = "repo" (faion-net case) | https://cli.github.com |
| `pandas` + `seaborn` | Local pivot: PM × horizon × eng_cost heatmap, flag bimodal portfolios | `pip install pandas seaborn` |
| `claude` CLI | Drive the portfolio-PM pass on aggregated JSON; emit the reconciliation memo as Markdown | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Productboard | SaaS | Yes (REST + webhooks) | "Products" + "owners" map cleanly to PM-portfolio view |
| Aha! Roadmaps | SaaS | Partial (REST) | Strong portfolio module, weak per-PM cuts |
| Lattice / 15Five | SaaS | Yes (REST) | PM OKRs by person — pair with portfolio data to detect role-skew |
| Linear (multi-team) | SaaS | Yes (GraphQL) | Each team ≈ one product; PM-level rollups via labels |
| Jira Plans (Advanced Roadmaps) | SaaS | Yes (REST) | Heaviest; needed when PMO already enforces it |
| Notion + database views | SaaS | Yes (REST) | Cheapest portfolio register for solo / small teams |
| Reforge / Ravio benchmarking | SaaS | Read-only | Useful for sanity-checking PM-to-product ratios against industry |
| GitHub Projects v2 | SaaS | Yes (GraphQL) | Works for repo-as-product orgs (faion-net) |

## Templates & scripts
Companion script — flags PM-role anti-patterns from a single CSV. Reads
`pm,product,horizon,eng_cost_usd` rows and prints PMs whose mix is degenerate
(all H1, all H3, or bimodal with no H2 bridge). Use before quarterly review to
prep the reconciliation memo.

```bash
#!/usr/bin/env bash
# pm-role-skew.sh — detect single-product vs portfolio PM patterns
# Usage: ./pm-role-skew.sh pm_allocations.csv
set -euo pipefail
CSV="${1:?pm_allocations.csv required}"
python3 - "$CSV" <<'PY'
import csv, sys, collections
path = sys.argv[1]
by_pm = collections.defaultdict(lambda: collections.Counter())
products = collections.defaultdict(set)
with open(path) as f:
    for r in csv.DictReader(f):
        pm, prod, h = r["pm"], r["product"], r["horizon"].upper()
        cost = float(r.get("eng_cost_usd") or 0)
        by_pm[pm][h] += cost
        products[pm].add(prod)
print(f"{'PM':<18}{'#prod':>6}{'H1%':>7}{'H2%':>7}{'H3%':>7}  flag")
for pm, mix in by_pm.items():
    total = sum(mix.values()) or 1
    h1, h2, h3 = (round(100*mix[k]/total, 1) for k in ("H1","H2","H3"))
    flag = []
    if len(products[pm]) == 1: flag.append("single-product")
    if len(products[pm]) >= 3: flag.append("portfolio-PM")
    if h1 >= 95: flag.append("h1-only-risk")
    if h3 >= 50: flag.append("h3-zombie-risk")
    if h2 < 5 and h1 > 0 and h3 > 0: flag.append("bimodal-no-bridge")
    print(f"{pm:<18}{len(products[pm]):>6}{h1:>7}{h2:>7}{h3:>7}  {','.join(flag) or 'ok'}")
PY
```

For the strategy-side allocator script (`portfolio-allocate.sh`), see
`pro/product/product-planning/portfolio-strategy/agent-integration.md`. Do not
duplicate it here — chain the two scripts in CI.

## Best practices
- **Name the role explicitly each quarter**. Each PM gets a written tag: `product-PM` or `portfolio-PM` or `mixed (X% portfolio time)`. Ambiguity here is the root cause of most allocation fights.
- **Separate budgets, not just labels**. The H3 portion must be funded out of a portfolio budget that no single product PM can raid; otherwise it becomes overflow for late H1 features.
- **Score PMs on portfolio outcomes, not just product outcomes**, when they own ≥ 2 products. Otherwise they will silently let H3 die because no one rewards them for it.
- **Cross-product trade-offs go in one memo, signed by the portfolio-PM, not negotiated 1:1 between product PMs**. Bilateral deals leak budget and never balance.
- **Every product gets a `lifecycle_stage` field** (pre-PMF / scaling / mature / declining). Apply different horizon rubrics per stage — pre-PMF products allocate 100% to PMF and only enter the portfolio model after.
- **Run the role-skew script before reviews, not after**. Surfacing "PM B is 100% H1 across 3 products" lets the conversation start at the diagnosis instead of at the symptom.
- **Document the kill criteria for cross-product bets** at funding time. Shared-platform investments that don't ship in 2 quarters are silently subsidized forever.

## AI-agent gotchas
- LLMs conflate "PM owns more products" with "PM is more strategic". They will tag the multi-product PM as portfolio-PM regardless of how that PM actually spends their time. Force the classifier to use a `time_allocation` field, not a product count.
- Agents over-recommend "promote IC PM to Group PM" because the prompt sounds like a career arc. Suppress this — the framework is about scope partitioning, not titles.
- When two PMs disagree, agents default to splitting the difference. That hides the actual trade-off. Constrain the rebalancer to pick a side and explain why, not to compromise.
- Reconciliation memos generated by an LLM read fluent but bury the cut. Require a `cuts:` section at the very top of the JSON, and inspect that field before reading the prose.
- Agents will quietly drop the `pre-PMF` exception. Pass it as a hard constraint, not a sentence in the prompt body.
- LLMs will not detect cross-product dependencies unless they are present as edges in the input. Always pre-compute the dep graph (a separate `cross_product_deps.csv`) and pass it; otherwise the agent invents synergies that don't exist.
- Solo-founder portfolios mislead the model — it will recommend a clean 70/20/10 split for one human running 6 products. Pass `owner_count` and let the agent flag "headcount insufficient for stated allocation" rather than pretend the ratio is achievable.
- The agent's confidence on PM-role classification is unreliable below ~5 quarters of history. Treat single-quarter outputs as advisory, not decisional.

## References
- Marty Cagan — *Empowered* (2020), chapters on product leadership vs portfolio leadership.
- Roman Pichler — *Strategize* (2nd ed., 2022) — portfolio canvas, role separation between PM and product strategist.
- Melissa Perri — *Escaping the Build Trap* (2018) — the "feature factory" failure mode that single-product PMs replicate at portfolio scale.
- Lenny's Newsletter / Reforge essays on Group PM vs Director PM scope (2022–2024).
- Team Topologies (Skelton & Pais, 2019) — for the team-shape angle, complementary to PM-role allocation.
- Companion file: `pro/product/product-planning/portfolio-strategy/agent-integration.md` — strategy-side rubric, classifier, rebalancer, allocator script.
- Linear API: https://developers.linear.app · Productboard API: https://developer.productboard.com
