# Agent Integration — Technical Debt Basics

## When to use
- Quarterly/sprint planning where an agent has to surface debt before humans pick payoff items.
- Post-incident reviews — debt that caused the incident must be registered with severity, location, "interest" cost.
- New-codebase onboarding: have an agent inventory existing debt before estimating work.
- Trade-off discussions during a feature: decide deliberately to take prudent debt and log it in the same commit.

## When NOT to use
- Greenfield prototypes that may be thrown away — registering debt is overhead with no reader.
- Sub-100-line scripts; "debt" framework is heavier than the code.
- Code under active rewrite — log the rewrite, not item-level debt that will be deleted next week.
- When the team has no payoff process — registering debt no one will pay is theatre.

## Where it fails / limitations
- LLMs over-report "debt": every TODO, every long function gets flagged. Without a severity/impact filter the register becomes noise.
- The "interest rate" estimate (hours/week lost) is hard to verify; agents tend to invent confident numbers. Require evidence (incident IDs, slow query logs, churn data).
- Agents conflate code smells with debt; not every smell has a business cost worth tracking.
- Single-shot scans miss "process debt" (manual deploys, missing CI) that lives outside source files.

## Agentic workflow
Run debt collection as a periodic batch job. A scanner subagent walks the repo + git history + linter output and emits debt-item candidates with evidence. A triager subagent (Opus) deduplicates against the existing register and assigns severity/impact. A human approves before items are appended to `TECH_DEBT_REGISTER.md`. Payoff is then pulled into the normal SDD task flow via `faion-feature-executor`.

### Recommended subagents
- `faion-sdd-executor-agent` — turns approved debt items into SDD tasks with quality gates.
- Scanner subagent (Sonnet) — runs `radon`, `lizard`, `jscpd`, `git log` and emits candidates as JSON.
- Triager subagent (Opus) — applies Fowler quadrant (deliberate/inadvertent × reckless/prudent), severity, business-impact estimate.
- `faion-improver` skill — fits the "investigate → brainstorm → apply" loop for paying down a single debt item.

### Prompt pattern
```
Scan <repo> for technical debt candidates. For each, output JSON:
{ "id", "type": "code|design|test|doc|infra|process",
  "severity": "low|med|high", "location": "<file:line>",
  "evidence": "<commit / linter rule / metric>",
  "estimated_payoff_tokens": <int> }
Skip anything without concrete evidence. Max 30 items.
```
```
Triage candidates against existing register at TECH_DEBT_REGISTER.md.
For each: dedupe (same root cause), classify in Fowler quadrant,
estimate business impact (cite incidents/PR latency/etc.).
Output diff of new register entries only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `radon` | Python complexity / maintainability index | https://radon.readthedocs.io |
| `lizard` | Multi-lang complexity, oversize functions | https://github.com/terryyin/lizard |
| `jscpd` | Copy-paste detector across languages | https://github.com/kucherenko/jscpd |
| `pip-audit` | Python CVEs in deps (security debt) | https://github.com/pypa/pip-audit |
| `npm audit` / `pnpm audit` | JS dep CVEs | npm / pnpm docs |
| `dependabot` / `renovate` | Outdated dep detection (infra debt) | dependabot.com / renovatebot.com |
| `git-of-theseus` | Code churn / age cohort plots | https://github.com/erikbern/git-of-theseus |
| `tokei` | Quick LOC inventory | https://github.com/XAMPPRocky/tokei |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarQube / SonarCloud | OSS + SaaS | Yes (REST API) | "Technical Debt" metric in days, per-file hotspots |
| CodeScene | SaaS | Yes (CLI + REST API) | Behavioural code analysis, hotspot prioritisation by churn |
| CodeClimate Quality | SaaS | Yes (CLI + API) | Maintainability scores, debt remediation cost |
| Stepsize | SaaS | Yes (API + IDE plug-ins) | Built specifically as a debt tracker tied to Jira/Linear |
| DebtMap (OSS) | OSS | Yes (CLI) | Lightweight markdown debt register tooling |
| Linear / Jira | SaaS | Yes (API) | Use a `tech-debt` label + saved view; agent files items via API |

## Templates & scripts
The methodology already ships a `TECH_DEBT_REGISTER.md` template and a Python `analyze_complexity` helper in `templates.md`. Useful agent companion: a one-shot scan that posts new candidates to a register file.

```bash
#!/usr/bin/env bash
# scan-debt.sh — emit candidate debt items as JSONL.
# Designed to be piped into a triage agent.
set -euo pipefail
ROOT="${1:-.}"

# Code-debt: high-complexity functions
if command -v lizard >/dev/null; then
  lizard -C 15 "$ROOT" --csv 2>/dev/null \
    | awk -F, 'NR>1 && $3+0>15 {printf "{\"type\":\"code\",\"location\":\"%s:%d\",\"evidence\":\"CCN=%s\"}\n",$NF,$5,$3}'
fi

# Test-debt: files lacking a sibling test_ file (Python heuristic)
find "$ROOT" -name '*.py' -not -path '*/tests/*' | while read -r f; do
  base=$(basename "$f" .py); dir=$(dirname "$f")
  if ! find "$ROOT" -name "test_${base}.py" -print -quit | grep -q .; then
    echo "{\"type\":\"test\",\"location\":\"$f\",\"evidence\":\"no test_${base}.py found\"}"
  fi
done

# Infra-debt: outdated deps
if [ -f "$ROOT/package.json" ] && command -v npm >/dev/null; then
  (cd "$ROOT" && npm outdated --json 2>/dev/null \
    | jq -r 'to_entries[] | "{\"type\":\"infra\",\"location\":\"package.json:\(.key)\",\"evidence\":\"outdated \(.value.current)→\(.value.latest)\"}"')
fi
```

## Best practices
- Always attach **evidence** (commit hash, linter rule ID, incident ID, slow-query trace) to every debt entry — agent-generated items without evidence get rejected.
- Cap the register: top 20-30 items only. Anything below that is below the noise floor.
- Track payoff velocity (debt closed per sprint), not absolute count — count keeps growing and demoralises teams.
- Tie each new feature to "debt taken / debt paid" notes in the PR description; agents can fill these in from the diff.
- Differentiate Fowler-quadrant: prudent-deliberate is fine, reckless-anything is a red flag for code review.
- Never let the agent close a debt item; closure requires verification (tests + metric improvement).

## AI-agent gotchas
- **Severity inflation.** LLMs default to "high"; require concrete impact metrics or downgrade automatically.
- **Phantom debt.** Agent invents items in code it never read. Force it to cite line numbers and recheck file existence.
- **Stale references.** Items in the register point at moved/renamed files; require a weekly link-check pass.
- **Mixing TODO and debt.** TODO ≠ debt. Filter on "has business impact" and "would not exist if redone today".
- **Recursive debt.** "Refactor the debt tracker itself" loops. Cap recursion depth in the loop.
- **Human checkpoint.** Never let an autonomous agent merge a debt-payoff PR — the rewrite risk is high; require human review on the pre-merge gate.

## References
- https://martinfowler.com/bliki/TechnicalDebt.html — Fowler quadrant
- https://martinfowler.com/articles/is-quality-worth-cost.html
- https://insights.sei.cmu.edu/library/managing-technical-debt-collection/
- https://www.amazon.com/Managing-Technical-Debt-Reducing-Development/dp/0135645824 — Kruchten/Nord/Ozkaya
- https://codescene.com/, https://docs.sonarsource.com/sonarqube/latest/user-guide/metric-definitions/
- https://github.com/erikbern/git-of-theseus — code-age analysis
