# Agent Integration — Technical Debt Management

## When to use
- Sprint planning where engineering velocity has visibly decayed and the team disagrees on which debt to address.
- Onboarding a new codebase where debt is undocumented and you need a quick triage of high-impact items.
- Setting up CI quality gates and pre-commit hooks to prevent debt accumulation on a fresh project.
- Planning a Strangler Fig migration of a legacy module that cannot be replaced atomically.
- Deciding between Boy Scout Rule, dedicated debt sprints, feature-attached payoff, or strangler-fig per debt item.

## When NOT to use
- Greenfield codebase <6 months old — there is no real debt yet, just inexperience; focus on prevention (linters, tests, ADRs).
- Codebase you intend to throw away in <3 months — paying down debt on a doomed system is sunk cost.
- During an outage / launch crunch — debt management requires calm and capacity.
- As a substitute for refactoring patterns — debt management is *prioritization*; the actual code work is in `refactoring-patterns`.
- Solo project with no other contributors — most debt frameworks optimize for team coordination overhead you do not have.

## Where it fails / limitations
- Priority Score = (Impact × Risk × Interest) / Cost is multiplicative; one inflated factor dominates the ranking.
- "Interest rate" is the hardest factor to quantify and the most often guessed; bad inputs poison the ranking.
- 20% sprint allocation is a heuristic — works at scale, breaks for 1-2 person teams who need lumpy debt sprints.
- Strangler Fig fails when the legacy interface is not stable enough to wrap — sometimes you must rewrite atomically.
- Pre-commit / CI gates that are too strict become bypassed (`--no-verify` epidemic) and lose all force.
- Tracking debt in a separate "debt backlog" decouples it from feature work and guarantees it is never paid.

## Agentic workflow
A debt-discovery agent runs static analysis (radon, pylint, sonar, semgrep) plus codebase grep for `TODO|FIXME|HACK|XXX|TECH_DEBT` and produces an inventory with file paths, line counts, and complexity metrics. A scoring agent assigns Impact / Risk / Interest / Cost per item with rationale tied to the metric. A strategy-picker agent chooses payoff strategy per item: Boy Scout for low-cost-incidental, feature-attached for items in code about to change, debt sprint for high-impact-isolated, Strangler Fig for high-cost-systemic. A prevention-agent generates the CI / pre-commit config matched to the language. Human reviews scoring and approves the strategy mix.

### Recommended subagents
- `faion-sdd-executor-agent` — once a debt item is committed, runs as a regular SDD task with quality gates.
- A static-analysis runner agent (Sonnet) — invokes radon / pylint / semgrep / `cloc` and shapes results into a debt inventory.
- A "boy-scout" agent — small-scope: while editing file X for feature Y, propose 1-3 nearby cleanups, no scope expansion.
- A debt-scoring agent (Sonnet) — applies Impact/Risk/Interest/Cost rationale.
- A strangler-fig planner agent (Opus) — designs the legacy/modern facade and rollout plan; this is architecture work.

### Prompt pattern
```
Run static analysis on <repo path>. For each file with cyclomatic complexity > 10
or duplication > 50 lines, output:
- file: path
- top_issue: <complexity|duplication|dead_code|outdated_dep|missing_tests>
- evidence: tool output line
- estimated_payoff_hours: integer
- depends_on_feature_in_flight: <feature_id or none>
Sort by (complexity * line_count) desc.
```

```
You are the boy-scout. While editing <file> for feature <id>:
Propose 1-3 small cleanups in this file ONLY (no other files).
Each cleanup: ≤20 LOC change, no behavior change, named with the safety pattern (rename, extract method, remove dead branch).
Reject suggestions that touch public API or require new tests.
```

```
For debt item <id> with profile <impact, risk, interest, cost>:
Pick payoff strategy from {boy_scout, feature_attached, dedicated_sprint, strangler_fig}.
Justify in 2 sentences. State a stop-condition: "we abandon this strategy if X."
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `radon` | Python cyclomatic complexity, maintainability index | https://radon.readthedocs.io |
| `lizard` | Multi-language complexity (C, JS, Python, Go, Rust) | https://github.com/terryyin/lizard |
| `cloc` | Lines-of-code per file/language; baseline for size | https://github.com/AlDanial/cloc |
| `semgrep` | Pattern-based static analysis; custom debt rules | https://semgrep.dev/docs |
| `sonar-scanner` | SonarQube CLI; debt as time-units estimate | https://docs.sonarsource.com/sonarqube |
| `safety` (Python) / `npm audit` / `cargo audit` | Vulnerable dependency debt | https://pyup.io/safety |
| `depcheck` | Unused JS/TS dependencies | https://github.com/depcheck/depcheck |
| `vulture` | Find dead Python code | https://github.com/jendrikseipp/vulture |
| `git-quick-stats` | Hot-spot analysis: files changed most often = debt risk | https://github.com/arzzen/git-quick-stats |
| `code-maat` | Hotspot + complexity from git history | https://github.com/adamtornhill/code-maat |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarQube / SonarCloud | OSS / SaaS | Yes (REST API) | Debt expressed in "remediation hours"; agents read via Web API. |
| Codacy | SaaS | Yes (REST API) | Lower-friction SonarQube alternative. |
| CodeClimate | SaaS | Yes (REST API) | Maintainability scores per file. |
| Snyk | SaaS | Yes (CLI + REST API) | Dependency-debt focused. |
| Stepsize / SteadyBit | SaaS | Yes (API) | Tech-debt-as-issues, links debt to feature tickets. |
| Trunk.io | SaaS | Yes (CLI) | Multi-linter wrapper, code health dashboard. |
| GitHub CodeQL | SaaS | Yes (Actions) | Pattern-based code scanning. |
| Refactor.io | SaaS | Limited | Hotspot visualizations. |
| Renovate / Dependabot | OSS / SaaS | Yes (PR bot) | Automates dependency-debt payoff. |

## Templates & scripts
See `README.md` for the priority matrix, payoff strategies, CI quality gates, and pre-commit debt-comment validator. Inline hotspot finder:

```bash
#!/usr/bin/env bash
# debt-hotspots.sh — files most frequently changed AND most complex.
# Output: rank, file, change_count, complexity
set -euo pipefail
cd "${1:-.}"

# Top-50 most-churned files in last 12 months
git log --since="12 months ago" --name-only --pretty=format: \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -50 \
  > /tmp/churn.txt

# Add complexity per file (Python/JS via lizard)
while read -r count file; do
  if [[ -f "$file" ]]; then
    cmplx=$(lizard "$file" 2>/dev/null | awk '/^[0-9]+/ {sum+=$2} END {print sum+0}')
    printf "%6d  %4d  %s\n" "$count" "$cmplx" "$file"
  fi
done < /tmp/churn.txt | sort -k1,1 -nr -k2,2 -nr | head -20
```

## Best practices
- Track debt as labels on existing tickets, not in a separate backlog. A separate backlog is where debt goes to die.
- Every `TODO`/`FIXME` must reference a ticket: `TODO(PROJ-123): description`. Enforce via pre-commit.
- Use git-history hotspots to prioritize: files churned often AND complex are the highest-leverage payoff targets.
- Hybrid sprint allocation (15% continuous + quarterly debt sprint) outperforms pure 20% continuous for most teams.
- Strangler Fig is correct when the legacy interface is stable; if the interface is also debt, rewrite atomically inside a feature flag.
- Boy Scout cleanups must be ≤20 LOC and same-file; larger touches expand PR scope and stall reviews.
- Pre-commit gates with override discipline beat CI-only gates that pass-by-default. CI catches ≠ team behavior.
- Measure debt before and after a quarter. If complexity / duplication does not drop, your strategy is wrong.

## AI-agent gotchas
- LLMs proposing refactors will silently change behavior. Require: tests must exist before refactor, and the agent must show test results pre and post.
- Coding agents over-expand "small" cleanups. Cap LOC per agent change explicitly (≤20-50) and reject scope expansion.
- Agents will dismiss any debt comment they did not write ("looks fine to me"). Force them to chase the linked ticket and get its resolution status.
- Static-analysis output is verbose; agents truncate and miss tail items. Pipe through `head -N` deliberately and tell the agent how many items it has.
- Boy-scout agents create review fatigue: 5 unrelated cleanups per PR. Cap at 1-3 per PR; all must be local to the file being modified.
- Strangler Fig is high-risk; do not let the agent ship the modern path to >1% of traffic without human sign-off and a rollback feature flag.
- Human-in-loop checkpoint: any payoff > 1 sprint requires explicit human approval — agents underestimate cost by 2-3×.
- Human-in-loop checkpoint: pre-commit hook config is permanent infrastructure; humans must review the rule list.
- Do not let the agent close debt tickets based on diff-size heuristics; require linked test runs that demonstrate the underlying issue is gone.

## References
- Ward Cunningham — original debt metaphor: https://wiki.c2.com/?WardExplainsDebtMetaphor
- Martin Fowler — Strangler Fig pattern: https://martinfowler.com/bliki/StranglerFigApplication.html
- Robert C. Martin — Boy Scout Rule, "97 Things Every Programmer Should Know": https://www.oreilly.com/library/view/97-things-every/9780596809515/ch08.html
- Adam Tornhill — "Your Code as a Crime Scene" + code-maat hotspot analysis: https://www.adamtornhill.com/articles/crimescene/codeascrimescene.htm
- Philippe Kruchten et al. — "Managing Technical Debt" book (SEI series).
- ThoughtWorks Tech Radar — debt-related techniques: https://www.thoughtworks.com/radar
- Sibling: `tech-debt-basics.md`, `refactoring-patterns/`, `code-review/`.
