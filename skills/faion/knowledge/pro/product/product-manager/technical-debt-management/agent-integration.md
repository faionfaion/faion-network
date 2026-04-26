# Agent Integration — Technical Debt Management

## When to use
- A PM is forced to defend roadmap velocity to the business (CEO / board / customer success) when shipping is visibly slowing despite the same headcount, and needs a quantified, item-by-item debt register instead of "engineering says it's slow".
- Quarterly planning where 15-20% of capacity is reserved for paydown; the PM must hand engineering a *prioritized* list (interest × contagion / effort) so reservation does not become a free-for-all.
- Right after a P0 outage, a noisy regression cluster, or a failed launch — when the post-mortem reveals debt as the root cause and the org is briefly willing to fund repayment.
- Before a major architectural change (auth rewrite, billing migration, multi-tenant cutover) — surface debt that touches the change surface so the rewrite eliminates it instead of carrying it forward.
- When acquiring a codebase / vendor / open-source fork: produce a baseline debt register before signing off on integration.
- For solopreneur / faion-net-style portfolios (nero, neromedia, pashtelka, etc.): a single PM-engineer needs a shared register across 5+ small repos so debt does not silently compound in the lower-traffic ones.

## When NOT to use
- Pre-PMF prototypes where the entire codebase is "deliberate prudent debt" by design — registering it just creates anxiety. Track only debt that blocks the *next* validation experiment.
- Single-file scripts and one-shot data migrations — the cost of registering exceeds the cost of rewriting.
- As a substitute for a real architecture review when the system needs redesign, not paydown. A 200-item debt list with no architectural narrative is itself a smell.
- When engineering has lost trust in PM prioritization — first repair the trust (run a few engineer-driven debt sprints) before imposing a scoring matrix.
- For bit-rot dependency upgrades that are fully automatable (Renovate / Dependabot) — automate, don't bureaucratize.
- Crisis quarters (runway < 6 months, regulator deadline) — freeze the register, ship survival features, resume after.

## Where it fails / limitations
- The "interest" metric (slowdown × frequency) is rarely measured — teams guess and the score becomes politics. Without instrumented build-time / PR-cycle-time / incident-frequency data, the matrix is theatre.
- Registers rot fast: items get fixed silently, descriptions go stale, owners leave. A 6-month-old register typically has 30-50% incorrect entries.
- "20% of every sprint" almost always degrades to 0% under feature pressure. Without a hard, visible budget line (separate JIRA epic, separate burn-down) the allocation evaporates.
- Boy-Scout-rule paydown is invisible to the register and the matrix — debt gets fixed but the metrics still say it's there. Counts of *closed* debt items mislead.
- Cross-cutting debt (e.g., "global auth context", "no event schema") cannot be scoped as one ticket. The matrix wants atomic items; reality has graphs. Debt items either explode into 40 tickets or get one ticket that never closes.
- Debt that lives in a *vendored or external* dependency (NPM, PyPI, third-party SaaS) often cannot be paid down at all — only worked around. Registers that don't separate "ours" from "theirs" misallocate effort.
- LLMs are trained on tutorial code. They will flag legitimate idiomatic patterns as "debt" (e.g., service objects, factories, dependency injection in Python) and miss structural debt (missing abstractions, wrong module boundaries) because it has no local syntactic signal.

## Agentic workflow
Drive paydown as a three-pass loop. Pass 1 (sonnet-class, cheap, batched): a code-scanner agent walks the repo, parses TODO/FIXME/XXX, lints (`ruff`, `eslint`, `vulture`, `deadcode`), checks dependency freshness (`npm outdated`, `pip-audit`, `cargo outdate`), test coverage deltas, and emits a candidate JSON debt list — one item per finding with a `confidence` score. Pass 2 (opus-class, fewer items): a triage agent merges candidates into the human-curated register, attaches `interest`, `contagion`, `effort`, `alignment` from a rubric, and flags items needing human input (root-cause unclear, owner missing, business impact ambiguous). Pass 3 (sonnet-class): a planner agent reads next-quarter's roadmap and re-scores `alignment` per item ("is this debt on the surface area we will touch?"), then produces a paydown plan: which items get fixed during feature work (lowest marginal cost), which get a dedicated ticket, which stay deferred with a revisit date. Always emit structured JSON; never trust prose. Use `faion-brainstorm` only when the team disagrees on what *counts* as debt.

### Recommended subagents
- `faion-sdd-executor-agent` — once the paydown plan is approved, drive each debt-paydown ticket as a normal SDD task with constitution / spec / test-plan; debt fixes that skip SDD reintroduce debt.
- `faion-improver` — quarterly review loop: read last quarter's register, compare planned vs. actual paydown, log the gap as a *meta-debt* item ("we said 20%, shipped 6%"), feed forward.
- `faion-feature-executor` — when a feature ticket is tagged "touches debt area X", auto-include the debt fix in the same task plan (Boy Scout, but explicit).
- A custom `debt-scanner` subagent (worth creating): input = repo path + last register; output = `{candidate_items[], confidence, evidence_paths[], suggested_type}`. Stateless, run on every PR or nightly.
- A custom `debt-triage` subagent: input = candidate list + register + roadmap; output = scored register + paydown plan JSON. Cheap to re-run weekly.

### Prompt pattern
```
You are a technical-debt scanner. Walk the repo at <path>. Emit JSON only:
[{id, type: deliberate|accidental|bit_rot|design|docs|test,
  location: "file:line", description, evidence: ["lint_rule", "TODO_text", ...],
  confidence: 0-1, suggested_type, related_files: [...]}]
Rules:
  - Do not flag idiomatic framework patterns (service objects, DI, factories).
  - Require ≥2 evidence types for confidence > 0.6.
  - Skip vendored / generated / .venv / node_modules paths.
  - Group findings by module; one item per logical defect, not per line.
```

```
You are a debt triage PM. Given <register.json>, <new_candidates.json>,
<roadmap.json>, output JSON: updated register with interest (0-5), contagion (0-5),
effort (0-5), alignment (0-5), priority_score = (interest + contagion) * alignment / max(effort, 1).
Mark items needing human review (no business impact stated, owner unknown,
description ambiguous). Do not invent items. Do not auto-close existing items —
flag them as "fixed?" instead and require a human confirmation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `code-climate` CLI / Codacy CLI | Static debt scoring (cyclomatic, duplication, churn-vs-complexity hotspots) | https://codeclimate.com/quality |
| `sonar-scanner` (SonarQube / SonarCloud) | Industry-default debt rating (A-E) + remediation-time estimates per file | https://docs.sonarsource.com |
| `cloc` + `tokei` | Quantify per-module size; pair with churn for a hotspot map | `apt install cloc; cargo install tokei` |
| `git log --pretty=format:"%h %s" --shortstat` + `git-of-theseus` | Code-age + churn analysis; debt clusters live where churn is high but tests are absent | `pip install git-of-theseus` |
| `vulture` (Python) / `ts-unused-exports` / `knip` (JS-TS) | Dead-code detection; dead code is debt with negative interest | `pip install vulture`; `npm i -g knip` |
| `pip-audit`, `npm audit`, `cargo audit`, `osv-scanner` | Bit-rot debt: insecure / outdated deps | https://github.com/pypa/pip-audit |
| `Renovate` / `Dependabot` CLI configs | Continuous, automated bit-rot paydown | https://docs.renovatebot.com |
| `lizard` | Cyclomatic complexity per function across 20+ languages | `pip install lizard` |
| `radon` | Python-specific maintainability index, halstead metrics | `pip install radon` |
| `git hotspots` (custom one-liner, see Templates) | Fastest free signal of where debt actually hurts | n/a |
| `gh` / `glab` / `jira-cli` | Bulk-tag issues with `tech-debt`, query `is:open label:tech-debt` for the register | https://cli.github.com |
| `claude` CLI (Claude Code) | Drive scanner / triage / planner subagents on the register and emit JSON | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarQube / SonarCloud | OSS + SaaS | Yes (REST API, webhooks) | "Technical debt ratio" + "remediation effort" per file; PM-readable; expensive at scale |
| Code Climate Quality | SaaS | Partial (REST, rate-limited) | Maintainability grade per file; good PR-bot; weak on architectural debt |
| Codacy | SaaS | Yes (REST) | Multi-language, OSS-friendly free tier, GitHub-native |
| Snyk Code | SaaS | Yes (REST + CLI) | Combines security debt + bit-rot debt; agent-driven auto-PRs |
| Stepsize (acquired by GitClear) | SaaS | Yes (REST) | Built specifically for debt registers tied to JIRA/Linear; PM-oriented |
| GitClear | SaaS | Yes (REST) | Diff-quality + churn-based debt analytics for PMs |
| Cortex / OpsLevel / Backstage | SaaS / OSS | Yes (REST + plugins) | Service catalogs with "scorecards" — good place to track org-wide debt KPIs |
| Linear / Jira / GitHub Projects | SaaS | Yes | Where the register actually lives; pair with API for bulk updates |
| Productboard / Aha! | SaaS | Partial | Surface a debt "lane" alongside features so it competes for capacity in the same UI |
| Grafana + Prometheus + custom exporters | OSS | Yes | DIY dashboard: build-time, PR-cycle-time, flaky-test rate, MTTR — the *consequences* of debt |

## Templates & scripts

The README ships a debt-register template and a prioritization matrix. Add this hotspot script — it produces the *candidate* list the scanner should triage. Hotspot = high churn + high complexity + low test coverage. ≤50 lines.

```bash
#!/usr/bin/env bash
# debt-hotspots.sh — find files most likely to be debt
# Usage: ./debt-hotspots.sh [since=6.months.ago] [top=20]
set -euo pipefail
SINCE="${1:-6.months.ago}"
TOP="${2:-20}"
TMP="$(mktemp -d)"
# 1. churn: commits per file
git log --since="$SINCE" --name-only --pretty=format: \
  | grep -E '\.(py|ts|tsx|js|jsx|go|rs|java|rb)$' \
  | sort | uniq -c | sort -rn > "$TMP/churn.txt"
# 2. size: lines per file (proxy for complexity if no lizard)
if command -v lizard >/dev/null; then
  lizard -l python -l javascript -l typescript -X -w 2>/dev/null \
    | awk -F, 'NR>1 {print $5"\t"$1}' | sort > "$TMP/cx.txt"
else
  awk '{ print FILENAME"\t"NR }' $(awk '{print $2}' "$TMP/churn.txt") 2>/dev/null \
    | awk '{a[$1]=$2} END{for (f in a) print a[f]"\t"f}' | sort > "$TMP/cx.txt"
fi
# 3. join: hotspot_score = churn * complexity_norm
awk '{print $2"\t"$1}' "$TMP/churn.txt" | sort > "$TMP/churn_keyed.txt"
join -1 1 -2 2 "$TMP/churn_keyed.txt" "$TMP/cx.txt" 2>/dev/null \
  | awk '{print $1"\t"$2*$3"\t"$2"\t"$3}' \
  | sort -k2 -rn | head -n "$TOP" \
  | awk 'BEGIN{print "file\tscore\tchurn\tcomplexity"} {print}'
# 4. emit JSON for the scanner subagent
awk 'NR>1 {printf "{\"file\":\"%s\",\"score\":%s,\"churn\":%s,\"cx\":%s}\n",$1,$2,$3,$4}' \
  > "$TMP/hotspots.jsonl"
echo "--- jsonl ---"
cat "$TMP/hotspots.jsonl"
```

Pipe `hotspots.jsonl` into the scanner prompt above as the *seed list* — this stops the LLM from flagging boring idiomatic code and concentrates it on files that actually hurt.

## Best practices
- **Anchor every register item to evidence.** Required fields: `interest_evidence` (URL to a slow-build chart, an incident post-mortem, a PR-review-time graph) and `business_evidence` (cost in $ or hours, named affected feature). Items without both default to `priority = 0` and never get scheduled.
- **Track paydown by interest reduction, not item count.** Closing 20 cheap items can be theatre; closing the one item that drops PR cycle time 40% is the win. Pair the register with build-time / cycle-time / MTTR dashboards and report deltas.
- **Couple debt budget to roadmap budget in the same UI.** If the register lives in a separate tool, debt loses every prioritization fight. Same backlog, same scoring, same review cadence.
- **Auto-bit-rot.** Anything machine-fixable (deps, formatters, unused-imports) should be a Renovate / Dependabot / pre-commit hook, not a register entry. Register only debt that requires judgment.
- **Boy-Scout-rule with a ledger.** When a feature ticket touches a debt area, the engineer must close the related register item *or* explicitly defer with a reason. Without the ledger, Boy Scout work is invisible to PM.
- **Re-baseline quarterly.** Delete items where the original author left and no one can describe the impact. Stale items are noise; noise kills the register.
- **Pre-commit a kill rule.** Any debt item that has been deferred 4+ quarters either gets done next quarter or gets *closed as accepted debt* — a positive choice not to fix it. Zombie items destroy register credibility.
- **Separate "ours" from "theirs".** Track vendored / SaaS / external-dep debt in a different list with different remediation strategies (workaround, fork, replace, accept).
- **Tie the 20% allocation to the engineering manager's quarterly review**, not just the PM's. If only the PM owns the budget, engineering will trade it away every sprint.

## AI-agent gotchas
- Scanner agents over-flag idiomatic patterns (DI, factories, service classes, async generators, match-case). Counter with a per-language allow-list of patterns and a `≥2 evidence types` rule before raising confidence above 0.6.
- LLMs are blind to *missing* abstractions. They cannot detect "this should have been a state machine" or "this module should not exist". Hotspot + churn analysis must come from deterministic tooling, not the LLM.
- Triage agents will silently re-rank items each run because LLM scoring is non-deterministic. Persist the *previous* score in the register and require the agent to justify any score change > 1 point.
- Auto-closing items is the most common destructive failure mode. Force the agent to mark items `fixed?` (with evidence) and require a human or CI signal (test passing, lint clean, dep upgraded) before close.
- Debt registers grow unboundedly when agents run unchecked — every PR adds 5 new items. Cap candidate output (top-N by hotspot score) and require human ack before items enter the canonical register.
- LLMs will hallucinate "estimated remediation time"; prefer T-shirt sizes (S/M/L/XL) over hours. Time estimates from agents have negative information value.
- Cross-cutting debt ("we have no event bus") looks identical to a thousand small items in the scanner output. Run a separate `architecture-review` pass (opus, low frequency) to detect graph-level debt; do not expect the file-level scanner to see it.
- For solopreneur multi-repo setups (faion-net portfolio): run scanners per-repo but maintain *one* cross-repo register, otherwise the same dependency upgrade gets logged 6 times and "fixed" 6 times.
- Never let an agent ship a paydown PR unsupervised on production code. Debt fixes change behaviour silently more often than feature PRs do; require human review and full test suite green.

## References
- Ward Cunningham, "The WyCash Portfolio Management System" (OOPSLA 1992) — original debt metaphor.
- Martin Fowler, "Technical Debt Quadrant" (2009) — deliberate / inadvertent × prudent / reckless framing used in this methodology's README.
- Philippe Kruchten, Robert Nord, Ipek Ozkaya, "Managing Technical Debt" (Addison-Wesley, 2019) — SEI-derived treatment, the standard reference.
- Adam Tornhill, "Software Design X-Rays" (Pragmatic, 2018) — hotspot analysis (churn × complexity); foundation for the script above.
- McConnell, Steve — "Managing Technical Debt" (Construx whitepaper, 2008) — taxonomy still used by Sonar.
- Carnegie Mellon SEI — "Measuring Technical Debt" research line: https://www.sei.cmu.edu/our-work/projects/display.cfm?customel_datapageid_4050=21339
- Stripe — "The Developer Coefficient" (2018) — quantified business cost of debt; PM-friendly numbers.
- SonarSource SQALE method documentation: https://docs.sonarsource.com/sonarqube/latest/user-guide/metric-definitions/
- Stepsize / GitClear blog archives (2020-2024) — practical PM-engineering debt operating models.
- Renovate docs: https://docs.renovatebot.com — automated bit-rot paydown blueprint.
