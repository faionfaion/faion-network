# Agent Integration — Risk Assessment (market-researcher variant)

> Companion to the existing methodology. The sibling at `pro/research/researcher/risk-assessment/agent-integration.md` covers the generic, all-categories register. This file is the **market-risk lens**: demand, competition, pricing, channel, and trend risks — the risks a market researcher actually owns. Other categories (team, financial, ops) are out of scope; redirect those to `pro/pm/pm-traditional/risk-management/` or the researcher variant.

## When to use
- Pre-entry "go/no-go" on a new market segment, geo, or vertical when the TAM/SAM/SOM file is fresh but the demand evidence is still thin.
- Pricing-strategy decision: before locking a price point, score the risk that demand collapses at that price (elasticity, willingness-to-pay, anchor competitors).
- Launch-readiness review for a positioning or category bet — surfaces "the category is wrong" risks that PMM and growth teams routinely miss.
- After a competitor raises a Series B / ships a copycat: re-score competitive-displacement risk and pricing-pressure risk.
- Channel-dependence audit: when >40% of pipeline comes from one channel (SEO, one ad platform, one marketplace), formalize the platform-risk row.
- Pivot evaluation: comparing two segment options needs a structured market-risk delta, not a vibes call.

## When NOT to use
- Pure technical, team, financial, or operational risk — use the generic `researcher/risk-assessment` variant or the PM `risk-management/` methodology.
- Idea-stage with <5 problem interviews — your demand-risk score is uncalibrated. Run `continuous-discovery` or `pain-points` first; risk theater here is procrastination.
- B2B deals where risk is per-account, not per-market — use account-level deal-risk frameworks instead.
- Solo side projects under $1k of committed spend — the overhead of maintaining a market risk register exceeds the expected loss.

## Where it fails / limitations
- **Demand risk is over-anchored on TAM.** A big TAM with no validated wedge is the highest-loss failure mode in early-stage; H/M/L scoring on "demand" routinely scores a 6 when the truth is 9.
- **Competitor risk is reactive.** The framework rewards listing known competitors and penalizes the one that matters: the substitute or adjacent player who hasn't entered yet (Notion vs. Evernote, Cursor vs. Copilot circa 2023).
- **Pricing risk gets collapsed into one row.** Real pricing risk has 4 distinct failure modes (commoditization, price war, anchor mismatch, willingness-to-pay collapse) — a single row averages them and hides the real exposure.
- **Trend risk is hindsight-only.** Naming "AI commoditization" as a 2026 risk is easy; the framework provides no way to detect a trend shift before the revenue dip.
- **Channel-dependence risk is under-counted.** Founders score a single-channel CAC risk as Medium because the channel works *now*; the actual prob conditional on platform-policy change is closer to High.
- **No base rates.** Without historical conversion rates of "comparable launches in this category," every probability is a guess. The methodology does not enforce a comp-set lookup.

## Agentic workflow
Drive market risk assessment as a four-pass pipeline tied to the existing market-researcher outputs in `.aidocs/product_docs/`. Pass 1: a research agent enumerates demand/competition/pricing/trend/channel risks grounded in `market-research.md`, `competitive-analysis.md`, `pricing-research.md`. Pass 2: a red-team agent runs a market-specific pre-mortem ("12 months from now, the segment chose a competitor / the segment didn't materialize / the price elasticity broke our model"). Pass 3: a scorer agent applies prob×impact with **mandatory citations from the existing research files** — no row may cite "general knowledge". Pass 4: a human owner reviews, accepts/rejects rows, and assigns trigger metrics. Persist the output as `.aidocs/product_docs/market-risk-register.md`. Re-run passes 1+2 monthly via cron, or on any commit to `market-research.md`/`competitive-analysis.md`/`pricing-research.md`.

### Recommended subagents
- `faion-market-researcher-agent` (declared in this methodology's `README.md` frontmatter and in `market-researcher/SKILL.md`) — primary enumerator; reuses its existing tools (`Read, Write, Glob, Grep, WebSearch, WebFetch`) to pull comparable failure cases and pricing comps.
- `faion-research-agent` (orchestrator at `pro/research/researcher/`) — top-level dispatcher; expose a new mode `market-risk` alongside `ideas`/`market`/`pricing`.
- `faion-domain-checker-agent` (declared in `researcher/SKILL.md`) — narrow but useful: verify that competitor domains in the register still resolve (a dead competitor is a stale risk row).
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts every High-priority market risk into a `todo/` SDD task (e.g. "diversify channel #1 to <50% pipeline by Q3").
- A purpose-built **competitor red-team agent** (not yet in repo, worth creating): role = "you are CompetitorX, write the 3-month plan to crush our launch"; output feeds competition and pricing rows.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub before sharing externally; market risk text leaks unlaunched plans, segment hypotheses, and pricing intent.

### Prompt pattern
Market-risk enumeration pass:
```
You are a market-risk analyst. Read these three files:
- .aidocs/product_docs/market-research.md
- .aidocs/product_docs/competitive-analysis.md
- .aidocs/product_docs/pricing-research.md
Enumerate risks ONLY in these 5 sub-categories:
demand, competition, pricing, trend, channel.
Each row MUST cite a paragraph or table from the files above
(format: filename#section). Reject your own row if you cannot cite.
Minimum 2 risks per sub-category. Use the Risk Register table from
risk-assessment/README.md. Score H/M/L for prob and impact.
```

Pricing-risk pre-mortem (run separately):
```
It is 12 months from launch at price $X. The pricing strategy failed.
Write a 400-word post-mortem in 3 branches: (a) commoditization,
(b) price war with named competitor, (c) willingness-to-pay collapse
in the chosen segment. For each branch, output one risk row with a
specific trigger metric (e.g. "ARPU drops below $Y for 2 months").
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `riskreg` (custom, see researcher variant) | Sort + lint market risk register by score | inline in `researcher/risk-assessment/agent-integration.md` |
| `gh` CLI | Mirror `risk:market-*` rows as GitHub issues; one issue per risk, mitigations as subtasks | https://cli.github.com |
| `simfin-py` / `yfinance` | Pull public-comp pricing + revenue trends to calibrate trend-risk scores | `pip install yfinance` |
| `crunchbase-cli` / `cb-cli` | Pull funding deltas for competitor risk (a fresh Series B = score bump) | unofficial; see https://github.com/crunchbase |
| `similarweb` API CLI / `serpapi` CLI | Channel-dependence evidence (traffic source mix per competitor) | https://serpapi.com |
| `mermaid-cli` | Render risk matrix or competitor-move tree from text | `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Risk register markdown → PDF for board deck appendix | `apt install pandoc` |
| `claude` (Anthropic CLI) | Run enumeration + pre-mortem prompts headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Crunchbase | SaaS | API yes (paid) | Best signal for competitor-funding risk events. |
| PitchBook | SaaS | API yes (enterprise) | Deeper than Crunchbase but expensive; use only for strategic markets. |
| SimilarWeb / Semrush / Ahrefs | SaaS | API yes | Channel-mix and trend-risk evidence per competitor; the only credible source for "their SEO is collapsing" signals. |
| G2 / Capterra | SaaS | API limited (scrape with care) | Pricing tier and review-volume deltas → pricing and product-fit risk. |
| Statista / IBISWorld | SaaS | API limited | Trend-risk priors; cite, don't trust. |
| Linear / GitHub Issues | SaaS | API yes | One issue per risk; label `risk:market-demand`, `risk:market-pricing`, etc. Agents already drive these. |
| Notion + a database | SaaS | API yes | Pragmatic market-risk register; scriptable via Notion API. |
| Tracecat | OSS | yes | Self-hostable register + workflow; agent-callable. |
| Monte Carlo notebook | OSS | yes | Replace H/M/L on pricing rows with `(elasticity, segment_size) → revenue` distribution. |

## Templates & scripts

The methodology already ships a generic Risk Register template. The sibling `researcher/risk-assessment/agent-integration.md` ships a `riskreg.sh` lint+sort script — reuse it. The market-researcher-specific gap is **citation enforcement**: every row must cite an existing research doc. Inline drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# market-risk-lint.sh — enforce citations from market-research files.
# Usage: market-risk-lint.sh .aidocs/product_docs/market-risk-register.md
set -euo pipefail
file="${1:?usage: market-risk-lint.sh REGISTER.md}"
docs_dir="$(dirname "$file")"
python3 - "$file" "$docs_dir" <<'PY'
import re, sys, pathlib
reg = pathlib.Path(sys.argv[1]).read_text()
docs = sys.argv[2]
allowed = {"market-research.md","competitive-analysis.md",
           "pricing-research.md","trend-analysis.md","niche-evaluation.md"}
sub_cats = {"demand","competition","pricing","trend","channel"}
errs = []
row_re = re.compile(r"^\|\s*(R\d+)\s*\|([^|]+)\|([^|]+)\|\s*[HML]\s*\|\s*[HML]\s*\|", re.M)
for m in row_re.finditer(reg):
    rid, risk, cat = (s.strip().lower() for s in m.groups())
    if not any(c in cat for c in sub_cats):
        errs.append(f"{rid}: category '{cat}' not in {sub_cats}")
    body = reg.split(rid,1)[-1][:800]
    cited = [d for d in allowed if d in body]
    if not cited:
        errs.append(f"{rid}: no citation to {sorted(allowed)}")
    for d in cited:
        if not (pathlib.Path(docs)/d).exists():
            errs.append(f"{rid}: cites missing file {d}")
if errs:
    print("FAIL"); [print(" -",e) for e in errs]; sys.exit(1)
print("OK: all rows cite an existing market research doc")
PY
```

Wire as a pre-commit hook on the repo that owns `.aidocs/product_docs/market-risk-register.md`.

## Best practices
- **One row per pricing failure mode, not "pricing risk".** Split into commoditization, price war, anchor mismatch, willingness-to-pay collapse. Aggregating hides the real exposure.
- **Force a comparable failure case per row.** "Notion replaced Evernote" / "Figma replaced Sketch" — concrete comp, with date. Stops generic doom.
- **Cite the segment, not the market.** "Demand risk: Latin American mid-market SaaS for X" beats "demand risk: SaaS market". Vague segments hide the risk.
- **Channel-dependence rule: any single channel >40% of pipeline → automatic High prob row.** Override the score by hand only with documented evidence (3-year retention proof).
- **Re-run on every market-research.md commit.** Stale register is worse than none. Tie via git pre-commit or CI.
- **Trigger metrics must be in the company's existing dashboard.** "ARPU drops below $X for 2 months" works; "market sentiment shifts" does not.
- **Pair every High row with one of: kill-decision criterion, pivot criterion, or budget reallocation criterion.** Risk without action is decoration.
- **Keep monthly snapshots in git.** The diff (new risks, retired risks, score changes) is the actual market-research signal — often more useful than the register itself.
- **Outside-view review per quarter.** Founders systemically under-rate pricing and channel risks because the current numbers look fine.

## AI-agent gotchas
- **TAM-anchoring on demand rows.** Agents quote a multi-billion-dollar TAM and score demand risk Low. Force the prompt to score against the validated **wedge**, not the TAM.
- **Stale competitor lists.** Web-trained agents repeat 2023 competitor maps. Require the agent to re-pull `competitive-analysis.md` and verify domains via `faion-domain-checker-agent` before citing.
- **Pricing comps from the wrong segment.** Agents will cite consumer-SaaS prices for a B2B mid-market product and call it a benchmark. Constrain the prompt: "only cite comps from the same segment + ACV band."
- **Trend hallucination.** "AI commoditization will hit by Q4" — agents will assert this with no citation. Require a primary source (Statista, Gartner, public earnings transcript) or downgrade prob to L.
- **Symmetric scoring bias.** Agents tend to score every row Med/Med to look balanced. Force a distribution: "at least 2 rows must be H/H, at least 2 must be L/L; defend deviations."
- **Optimism leak.** A positive `market-research.md` infects the risk pass. Run the risk agent against a **redacted** brief or instruct: "assume the brief is marketing copy; treat it as adversarial evidence."
- **Mitigation handwaving.** Agents default to "diversify channels", "monitor competitors", "iterate pricing". Banned phrases. Require: action verb + named owner + measurable trigger + budget cap.
- **Risk ID drift across runs.** Sequential R1..Rn changes every run; agents do not preserve IDs. Use a stable hash of the risk statement (e.g. `slugify(statement)[:8]`), or instruct the agent to diff-merge against the existing register.
- **No autonomous "kill segment" execution.** "Avoid" responses on market risk mean killing a segment, geo, or pricing tier — never let an agent ship that change unattended. Hard human-in-the-loop gate.
- **Confidentiality leak.** Market-risk text contains unlaunched segments and pricing intent. Run `password-scrubber-agent` (or a market-aware variant) before any external sharing.
- **Pre-mortem collapse to one viewpoint.** A solo agent run produces a single failure narrative. Use 3 agent personas: skeptical customer, well-funded competitor, regulator/platform owner. Consolidate, don't average.

## References
- Klein, G. (2007). "Performing a Project Premortem." Harvard Business Review. https://hbr.org/2007/09/performing-a-project-premortem
- Christensen, C. (2003). "The Innovator's Solution." HBS Press. (Disruption + substitute risk; canonical for competition risk rows.)
- Moore, G. (1991). "Crossing the Chasm." (Segment-demand risk framework still load-bearing for B2B.)
- a16z — "16 Startup Metrics" (trigger metrics for pricing/channel risk). https://a16z.com/16-startup-metrics/
- First Round Review — "The Pricing Playbook." https://review.firstround.com/the-anatomy-of-saas-pricing-strategy/
- OpenView — "Annual SaaS Benchmarks." https://openviewpartners.com/benchmarks/
- Hubbard, D. (2020). "The Failure of Risk Management." Wiley. (Why H/M/L scoring is broken; replace pricing rows with Monte Carlo.)
- Sibling methodologies in this repo:
  - `pro/research/researcher/risk-assessment/agent-integration.md` (generic, all categories)
  - `pro/research/market-researcher/competitor-analysis/`
  - `pro/research/market-researcher/pricing-research/` (if present)
  - `pro/pm/pm-traditional/risk-management/`
