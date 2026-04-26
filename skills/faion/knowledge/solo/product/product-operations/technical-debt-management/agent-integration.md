# Agent Integration — Technical Debt Management

## When to use
- Codebase has aging dependencies, fragmented patterns, and "fear zones" engineers avoid.
- Onboarding session: agent surveys repo for hot-spots, surfaces undocumented assumptions.
- Quarterly debt-paydown planning: scoring + sequencing register against upcoming roadmap.
- Pre-acquisition / pre-investment due diligence: producing defensible debt inventory.
- Migration planning (lib upgrade, framework jump, monolith decomposition).

## When NOT to use
- One-person codebase < 6 months old: debt is rounding error; ship features.
- Debt that's actually a missing-feature: agent will misclassify "we never built X" as "we built X badly".
- Production incident response — debt management is a planning activity, not firefighting.
- Code-quality theater: don't run an agent to generate a debt list nobody will fund.

## Where it fails / limitations
- Agents over-flag style/lint as "debt"; conflate cosmetics with structural debt. Require severity rubric in prompt.
- "Reckless / Prudent / Inadvertent" quadrant placement requires history and intent — agent can guess from commit message but is often wrong.
- Time-tax estimates are LLM-confabulation; calibrate from actual `git blame` churn or "fear-tax" interviews with engineers.
- Coupling/contagion analysis needs static analysis (call graphs, import graphs) — LLM-only inspection is unreliable.
- Architectural-debt detection needs cross-file holistic view; LLM context windows + naive search miss this.

## Agentic workflow
Pipeline: (1) `repo-surveyor` agent runs static-analysis tools (radon, scc, semgrep, depgraph) and assembles raw signals — NOT debt yet. (2) `debt-classifier` agent reviews signals + recent PR comments + `// TODO/FIXME` + dependency staleness, classifies into 6 types, scores Interest/Contagion/Effort/Alignment. (3) Quarterly: `debt-prioritizer` agent intersects scored register with roadmap, proposes paydown sequence aligned with planned features (lowest marginal cost). (4) Boy-scout daily: agent reviews PRs, suggests "while-you're-here" cleanups inline. Apply via PR; never auto-merge debt-paydown changes.

### Recommended subagents
- `repo-surveyor` — sonnet, drives static analysis tools, returns raw metrics.
- `debt-classifier` — sonnet, reads signals + commit context to populate register.
- `debt-prioritizer` — opus, multi-criterion scoring against roadmap (strategy, not pattern).
- `boy-scout-reviewer` — haiku, PR-time inline suggestions.
- Reuse: `faion-code-agent` (existing) for refactoring execution.

### Prompt pattern
```
Repo: {git remote}
Static signals (provided):
- file_churn (90 days): {top 30 files by commits}
- complexity (radon): {top 30 by cyclomatic}
- todos: {grep TODO/FIXME with context}
- deps_outdated: {npm/pip outdated output}
- test_coverage_gaps: {coverage.xml low-coverage files}
- security: {semgrep findings}
Classify each signal as one of: deliberate, accidental, bit-rot,
design, docs, test debt. Output Debt Register entry with
Interest (1-5), Contagion (1-5), Effort (1-5), Alignment (1-5),
plus rationale citing the signal row.
Reject items where signal is purely stylistic.
```

```
Register: {register.json}
Roadmap (next quarter): {planned features with files-touched estimate}
Propose paydown sequence:
- batch debt items that touch same files as planned features (low marginal cost)
- batch debt items that block features (enables future work)
- defer purely cosmetic; flag reckless debt for explicit decision
Output sprint-level allocation at 15-20% capacity.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `scc` / `tokei` | LOC + complexity counts | `brew install scc tokei` |
| `radon` (Python) | Cyclomatic, maintainability | `pip install radon` |
| `lizard` | Multi-language complexity | `pip install lizard` |
| `semgrep` | Pattern + security findings | `brew install semgrep` |
| `dependency-cruiser` (JS) | Import graph, cycle detection | `npm i -g dependency-cruiser` |
| `pydeps` (Python) | Module graph | `pip install pydeps` |
| `pip-audit` / `npm audit` / `osv-scanner` | Dep vuln + outdated | per ecosystem |
| `git-of-theseus` | Code aging analysis | `pip install git-of-theseus` |
| `code-maat` | Hot-spot mining via git history | https://github.com/adamtornhill/code-maat |
| `claude` Skill tool | Drive sub-agents | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarQube / SonarCloud | OSS + SaaS | Yes (REST + sarif) | Severity-graded findings; integrates with PRs. |
| CodeScene | SaaS | Excellent | Hot-spot + behavioral code analysis; designed for debt mgmt. |
| Codacy / Code Climate | SaaS | Yes | Multi-language quality grades. |
| Snyk / Dependabot / Renovate | SaaS | Yes | Bot-driven dep upgrades; pairs with agent for review. |
| Trunk.io | SaaS + CLI | Yes | Aggregates linters; agent-friendly artifacts. |
| GitHub Code Scanning | SaaS | Yes (SARIF) | Free for OSS; agent reads JSON output. |
| Stepsize | SaaS | Yes | Debt tracking integrated with Jira/Linear/GitHub. |
| Backstage TechRadar / Tech Health | OSS | Yes | Org-level debt visibility. |
| Nx / Turborepo Cache | OSS | Indirect | Build-graph signals = architectural debt indicator. |

## Templates & scripts
See `templates.md` for Debt Register, Prioritization Matrix, Sprint Budget. Repo survey driver:

```bash
#!/usr/bin/env bash
# debt-survey.sh — run quarterly, populates ~/debt/<date>/
set -euo pipefail
REPO=${1:?repo path}
DATE=$(date +%F)
OUT=~/debt/$DATE
mkdir -p "$OUT"
cd "$REPO"

# 1. Hot-spots: file churn × complexity
git log --since='90 days ago' --name-only --pretty=format: \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -50 > "$OUT/churn.txt"
scc --by-file --format json . > "$OUT/scc.json"
radon cc -j -s . > "$OUT/cc.json" 2>/dev/null || true

# 2. TODO/FIXME with line numbers
grep -rn -E 'TODO|FIXME|HACK|XXX' --include='*.py' --include='*.ts' \
  --include='*.js' --include='*.go' . > "$OUT/todos.txt" || true

# 3. Outdated deps
[ -f package.json ] && npm outdated --json > "$OUT/npm-outdated.json" || true
[ -f requirements.txt ] && pip list --outdated --format=json \
  > "$OUT/pip-outdated.json" || true

# 4. Coverage gaps
[ -f coverage.xml ] && cp coverage.xml "$OUT/" || true

# 5. Send to classifier
claude -p "$(cat ~/prompts/debt-classify.txt)" \
  --input-files "$OUT"/*.json "$OUT"/*.txt \
  > "$OUT/register.md"
```

## Best practices
- **Make debt visible with money, not adjectives**: "this slows us 6 dev-days/quarter" beats "this is bad code".
- **Pay down where you're already touching**: lowest marginal cost. Pair debt items with feature work.
- **Boy-scout rule with limits**: 30-min cap per PR; agent flags scope creep.
- **15-20% sustained allocation > debt sprints**: sprint approach lets debt re-accumulate.
- **Track trend, not absolute**: total debt count is meaningless; high-interest count + interest trend matter.
- **Reckless debt requires architectural decision record (ADR)**: agent should refuse to file new debt without an ADR link.
- **Test debt isn't optional**: untested code can't be refactored safely; prioritize test debt before structural.
- **Bit-rot has a clock**: dependency upgrades compound — Renovate/Dependabot weekly.
- **Don't refactor working code without a reason**: agent must tie every refactor to a feature/bug/risk.

## AI-agent gotchas
- LLMs love rewrites; bias toward big-bang refactors which are exactly the wrong move. Prompt: "minimal local change; avoid >20-line diffs without reason".
- Style nits flagged as "design debt" inflate the register. Filter at signal stage, not rationalization stage.
- Generated "fix approaches" routinely hallucinate APIs/libraries. Verify with build before committing.
- Cyclomatic complexity ≠ debt — sometimes inherent. Force comparison vs. team baseline.
- Estimates are confabulation: agent says "2 days"; actual is 2 weeks. Calibrate via past resolved-debt items.
- **Human-in-loop checkpoint**: paydown allocation decision is engineering-leadership territory. Agent proposes, human approves capacity %.
- Dependency upgrade auto-merges break consumers; pin "breaking change" detection (semver-major) and route to humans.
- Long-context whole-repo scans cost compute; tier the analysis (cheap signals → mid → deep dive only on top-20 hot files).
- Agents conflate "old code" with "bad code"; old + working + low-churn = leave alone.

## References
- Ward Cunningham (1992) — original "debt metaphor" essay
- Martin Fowler — "Technical Debt Quadrant" blog post
- Adam Tornhill — "Your Code as a Crime Scene", "Software Design X-Rays" (hot-spot analysis)
- Michael Feathers — "Working Effectively with Legacy Code"
- "Beyond Legacy Code" — David Bernstein
- CodeScene blog — behavioral code analysis case studies
- ThoughtWorks Tech Radar — organization-level debt visibility
