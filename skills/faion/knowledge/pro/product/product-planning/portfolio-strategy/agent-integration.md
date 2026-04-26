# Agent Integration — Portfolio Strategy (70/20/10)

## When to use
- Annual / quarterly product roadmap planning where multiple bets compete for the same engineering capacity and a single PM/CPO must defend allocation to finance or board.
- A multi-product company (or solopreneur with 3+ shipped products like the faion-net portfolio: nero, neromedia, pashtelka, ender, longlife, mediamanager) needs a defensible split between "keep the lights on" work and exploration.
- Macro shock — recession signal, funding cut, sudden churn spike — forces re-allocation from H3/H2 back into H1; the framework gives a numeric handle to argue with.
- Investor / leadership update where you must show the portfolio is not all moonshots and not all maintenance.
- Backlog sizing: tag every initiative H1/H2/H3 and check the sum against target ratios before committing the quarter.

## When NOT to use
- Single-product seed-stage startup with one bet — there is no portfolio yet; allocate 100% to PMF instead.
- Pure services / agency revenue where there is no product backlog to allocate against.
- Engineering-only resource planning (sprints, on-call, infra) — use capacity planning, not horizon allocation.
- Sub-feature prioritization inside one product — RICE / WSJF / Kano are sharper at that grain.
- Crisis quarters where survival demands 100% on one fire (fraud incident, P0 outage cascade, regulator deadline). Restore portfolio after.

## Where it fails / limitations
- Horizon labels become political: every team lobbies to be H3 (more freedom, fewer KPIs). Without a neutral arbiter the ratios drift.
- "10% transformational" gets starved first when H1 slips, because H3 has no near-term revenue defense. Teams then claim they "do innovation" while the budget shows zero.
- The 70/20/10 numbers are a Google PR artifact (2005 Schmidt era) — they are not empirically optimal. Treat as a starting heuristic, not law.
- Three Horizons (McKinsey, 1999) assumes time-sequenced horizons (H3 becomes H2 becomes H1). Many SaaS bets never graduate; they die or stay niche. Pure time framing misleads.
- LLMs reliably over-classify projects as H2/H3 because the descriptions sound novel; they under-count maintenance and tech-debt as H1. Counter with explicit rubric and revenue evidence.
- Cross-portfolio dependencies (shared platform, shared auth, shared data pipeline) are invisible in horizon math — moving one product can stall three others.

## Agentic workflow
Drive this with two passes. First, an analysis pass: a sonnet-class agent ingests the current backlog (CSV / markdown / Linear export), classifies each initiative H1/H2/H3 against an explicit rubric, and emits an allocation table. Second, a strategy pass: an opus-class agent compares actual vs. target allocation given the macro condition (Growth 60/25/15, Stable 70/20/10, Recession 80/15/5), proposes re-allocations, and flags items where horizon classification is ambiguous for human review. Both passes must produce structured JSON so a downstream review agent (or human) can audit, not prose. Use `faion-brainstorm` for the rebalance step when stakeholders disagree on which bets to cut.

### Recommended subagents
- `faion-sdd-executor-agent` — once allocation is approved, drive the per-horizon implementation plan (H1 features get full SDD; H3 bets get lightweight spike specs).
- `faion-brainstorm` — diverge / converge on candidate H3 bets when you only have allocation budget but no concrete ideas.
- `faion-improver` — quarterly review loop: read last quarter's allocation, compare to delivered outcomes, log mistakes (e.g. "we said 10% H3, shipped 0%"), feed back into next quarter's split.
- A custom `portfolio-classifier` subagent (worth creating): input = backlog item, output = `{horizon, confidence, rationale, revenue_evidence}`. Keep it small, cheap, and stateless.

### Prompt pattern
```
You are a portfolio classifier. For each backlog item below, output JSON:
{id, horizon: "H1"|"H2"|"H3", confidence: 0-1, rationale, revenue_evidence}
Rubric:
  H1 = serves an existing paying segment, ship within 12 months, known market.
  H2 = adjacent segment OR new pricing tier, 12-24 months, partial validation.
  H3 = new business model OR new tech foundation, 24-36 months, option value.
If revenue_evidence is empty, default to H3 and set confidence <= 0.4.
Backlog: <paste>
```

```
You are a portfolio rebalancer. Given current allocation {h1, h2, h3}, target
{th1, th2, th3} (set by macro condition), and a list of classified items,
output the minimal set of cuts/promotions to reach target +/- 3pp. Output JSON
with rationale per change. Do not invent items.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `productboard` CLI / API | Pull roadmap items + tags, push horizon classification back as a custom field | https://developer.productboard.com |
| `linear` API (`@linear/sdk`) | Read issue list with labels (`H1`/`H2`/`H3`), bulk-update labels via mutation | https://developers.linear.app |
| `jira` REST + `jira-cli` | Same pattern for Jira-shop teams; JQL `labels in (H1,H2,H3)` | https://github.com/ankitpokhrel/jira-cli |
| `gh` (GitHub CLI) | If your roadmap lives in GitHub Projects v2: `gh project item-list` + GraphQL field updates | https://cli.github.com |
| `pandas` + `matplotlib` | Local ETL on a CSV export → allocation pie + drift chart per quarter | `pip install pandas matplotlib` |
| `csvkit` (`csvsql`, `csvstat`) | Quick allocation math from CSV without writing code | `pip install csvkit` |
| `claude` CLI (Claude Code) | Drive the classifier subagent on a backlog file, emit JSON to stdout | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Productboard | SaaS | Yes (REST API + webhooks) | Native "objectives" + "drivers" map cleanly to horizons; custom field for H1/H2/H3 |
| Aha! Roadmaps | SaaS | Partial (REST API, rate-limited) | Strong portfolio module; agents can read but bulk writes are slow |
| Linear | SaaS | Yes (GraphQL, fast) | Best-in-class API; label-based horizons work well |
| Jira Advanced Roadmaps (Plans) | SaaS | Yes (REST) | Heaviest tool; needed if PMO already standardized on it |
| GitHub Projects v2 | SaaS | Yes (GraphQL) | Cheapest path for solo / small teams; field-based horizons |
| OpenStrategy / Cascade Strategy | SaaS | Limited (UI-first) | Strategic-portfolio focus, exec audience; thin API |
| ProdPad | SaaS | Yes (REST) | Idea-stage portfolio; pairs with Three Horizons natively |
| airfocus | SaaS | Yes (REST) | Built-in portfolio scoring; agents can post scores |
| `react-flow` + custom OSS dashboard | OSS | Self-built | When SaaS is overkill: render allocation drift from a JSON file |

## Templates & scripts

Inline classifier-and-allocator script. Reads a CSV (`id,title,description,annual_revenue_usd`) and a target allocation, emits current allocation, drift, and prompts for an LLM classifier call per row missing a horizon label.

```bash
#!/usr/bin/env bash
# portfolio-allocate.sh — compute current vs target horizon allocation
# Usage: ./portfolio-allocate.sh backlog.csv stable
set -euo pipefail
CSV="${1:?backlog.csv required}"
COND="${2:-stable}"  # growth | stable | recession
case "$COND" in
  growth)    TH1=60; TH2=25; TH3=15;;
  stable)    TH1=70; TH2=20; TH3=10;;
  recession) TH1=80; TH2=15; TH3=5;;
  *) echo "unknown condition: $COND"; exit 2;;
esac
python3 - "$CSV" "$TH1" "$TH2" "$TH3" <<'PY'
import csv, sys
csv_path, th1, th2, th3 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
totals = {"H1": 0.0, "H2": 0.0, "H3": 0.0, "?": 0.0}
items = []
with open(csv_path) as f:
    for row in csv.DictReader(f):
        h = (row.get("horizon") or "?").strip().upper()
        cost = float(row.get("eng_cost_usd") or 0)
        totals[h if h in totals else "?"] += cost
        items.append((row.get("id"), h, cost, row.get("title", "")))
known = sum(v for k, v in totals.items() if k != "?")
if known == 0:
    print("no classified items — run classifier first"); sys.exit(1)
pct = {h: round(100 * totals[h] / known, 1) for h in ("H1", "H2", "H3")}
print(f"current   H1={pct['H1']}%  H2={pct['H2']}%  H3={pct['H3']}%  unclassified=${totals['?']:.0f}")
print(f"target    H1={th1}%  H2={th2}%  H3={th3}%   condition=set")
drift = {h: pct[h] - t for h, t in zip(("H1","H2","H3"), (th1,th2,th3))}
print(f"drift_pp  H1={drift['H1']:+.1f}  H2={drift['H2']:+.1f}  H3={drift['H3']:+.1f}")
if abs(drift["H3"]) > 3 or abs(drift["H2"]) > 3 or abs(drift["H1"]) > 3:
    print("REBALANCE_NEEDED")
PY
```

For the classifier prompt template and the rebalancer prompt, see the prompts in the **Prompt pattern** section above; copy them verbatim into the agent call.

## Best practices
- Anchor each H1/H2/H3 label to a **revenue evidence string** (URL to MRR chart, signed contract, validated landing-page conversion). Without evidence, default to H3 with low confidence — this stops the "everything is H1" drift.
- Re-classify quarterly, not annually. SaaS bets graduate or die fast; an H3 from Q1 is often H2 by Q3 or already cancelled.
- Track allocation by **engineering cost (loaded $ or person-weeks)**, not by ticket count. A 1-line H1 fix and a 3-engineer-month H3 spike both count as "1 ticket" and that destroys the math.
- Use the macro-condition lever (Growth / Stable / Recession) explicitly. Write the condition into the OKR doc, not just the allocation. When the condition changes, the ratio change is automatic and uncontroversial.
- Pre-commit a **kill threshold** for every H3 bet at funding time (e.g. "kill if no design partner by month 4"). Without it, H3 zombies eat next year's H2 budget.
- Pair allocation review with a **graduation review**: any H3 bet that hit its validation gate should explicitly be re-tagged H2 (and budgeted H2-level), or it stays under-resourced.
- Surface cross-portfolio dependencies in a separate matrix; allocation math alone hides them.

## AI-agent gotchas
- LLMs over-tag items as H2/H3 because the prose sounds novel — force the classifier to require a `revenue_evidence` field and to default to H3 with confidence ≤ 0.4 when missing.
- Without a numeric eng-cost field per item, agents will count tickets and produce confidently wrong percentages. Validate the input schema before classifying.
- Agents will silently drop the macro condition if it is buried in a long prompt. Pass `condition` as a structured field, not a sentence.
- The rebalancer will hallucinate new initiatives if the prompt is open-ended ("suggest H3 bets"). Constrain it to picking from the existing list; if you want new bets, run a separate `faion-brainstorm` cycle and feed the survivors back in.
- Quarterly drift detection is mechanical — automate it (cron + the script above) and only escalate to a human when drift > 3 pp on any horizon. Do not let the agent make the rebalance decision unsupervised; that is a CPO call.
- When sources disagree (Productboard says H1, Linear label says H3), trust the system that holds the **revenue evidence**, not the one with the prettier UI.
- Three Horizons literature is heavy on time-sequencing language; LLMs will parrot "H3 becomes H2" as if guaranteed. Instruct the agent that horizons are about **risk + evidence today**, not a fixed escalator.

## References
- McKinsey, Baghai, Coley, White — "The Alchemy of Growth" (1999) — original Three Horizons model.
- Eric Schmidt / Google — 70/20/10 allocation rule, popularized 2005.
- Reforge — "Product Portfolio Strategy" essays (2022–2024).
- Marty Cagan, "Inspired" / "Empowered" — chapters on product strategy and bets.
- Roman Pichler, "Strategize" (2nd ed., 2022) — portfolio canvas and horizon mapping.
- Morgan Stanley 2026 macro outlook (referenced in `README.md`) — context for the recession-bias 80/15/5 split.
- Productboard docs: https://developer.productboard.com
- Linear API: https://developers.linear.app
