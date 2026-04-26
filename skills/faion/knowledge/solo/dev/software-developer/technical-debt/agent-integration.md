# Agent Integration — Technical Debt

## When to use
- Auditing a legacy codebase before a refactor cycle to surface and rank debt items.
- Sprint capacity planning when a team needs to allocate a fixed % to debt paydown vs feature work.
- After a quarter of fast shipping, to reconcile what was promised "we'll fix later" vs what shipped.
- During architecture reviews where debt-quadrant categorization (Fowler) clarifies whether debt was strategic or accidental.
- When stakeholder communication requires concrete cost/interest framing of code-level issues.

## When NOT to use
- Greenfield projects in week one — debt tracking is overhead before any code exists.
- As a substitute for actual refactoring work — a beautiful debt register that never gets paid down is shelfware.
- For code-style nits that linters/formatters fix automatically — those aren't debt, they're hygiene.
- For "I don't like this design" disagreements without measurable impact — keep the register evidence-based.

## Where it fails / limitations
- Subjective severity: agents and reviewers disagree on Severity=High vs Medium without rubric; needs a fixed scoring scheme.
- Stale registers: items rot, descriptions become inaccurate, ownership changes. The register itself accrues debt.
- Gaming: items get closed by being renamed or split, not fixed.
- Metrics gaming: cyclomatic complexity ≤ 10 is achievable by extracting nonsense helpers without reducing real complexity.
- Conflating bugs with debt — "missing input validation" is a bug, not technical debt.
- Missing the strategic dimension: a register without "why we took this debt" loses context for future devs.

## Agentic workflow
Run a recurring (weekly/biweekly) audit subagent that (1) walks the codebase via radon/lizard/SonarQube, (2) cross-references with `// TODO`, `// HACK`, `// FIXME`, and a pre-defined `TECH_DEBT(TD-NNN)` marker, (3) updates `TECH_DEBT_REGISTER.md` with new items, closes resolved ones, and re-scores severity from updated metrics, (4) opens a tracking issue per High/Critical item. Pair with a "debt-paydown" agent during dev cycles that proposes one item to tackle alongside each feature.

### Recommended subagents
- `debt-auditor` (Sonnet) — runs static-analysis tools, scans for TODO/HACK/FIXME, updates the register.
- `debt-prioritizer` (Sonnet) — applies a scoring rubric (impact × interest × fix cost) to rank items.
- `debt-paydown-implementer` (Sonnet) — picks an item from the top of the queue, implements, updates register on close.
- `debt-reporter` (Haiku) — generates monthly trend report (items opened/closed, severity distribution).

### Prompt pattern
```
Audit run:
1. Scan repo for: TODO|HACK|FIXME|XXX|TECH_DEBT comments. Capture file:line + author from blame.
2. Run radon cc + radon mi on src/ (Python) or eslint --rule complexity (TS).
3. Cross-ref with existing TECH_DEBT_REGISTER.md. Output:
   - new items (not in register)
   - closed items (no longer present)
   - severity-changed items
4. Open one PR updating the register; do NOT touch source code.
```

```
Score every item with: severity (1-5), impact ($/week or hours/week wasted),
fix-cost (S/M/L/XL), strategic value of NOT fixing (low/med/high).
Rank top 10 by impact × severity / fix-cost.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `radon` | Python complexity, MI, raw metrics | `pip install radon` |
| `lizard` | Multi-language complexity | `pip install lizard` |
| `eslint` (`complexity`, `max-lines`) | JS/TS complexity | https://eslint.org |
| `gocyclo` | Go cyclomatic complexity | `go install github.com/fzipp/gocyclo/cmd/gocyclo@latest` |
| `cargo geiger` | Rust unsafe-block audit | `cargo install cargo-geiger` |
| `jscpd` | Copy-paste / duplication detector | `npm i -g jscpd` |
| `git-of-theseus` | Code longevity / churn | `pip install git-of-theseus` |
| `code-maat` | Hotspot analysis from git history | https://github.com/adamtornhill/code-maat |
| `tokei` / `cloc` | LOC by language for trend tracking | `cargo install tokei` |
| `dependency-cruiser` | JS/TS module-dep visualizer | `npm i -D dependency-cruiser` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarCloud / SonarQube | SaaS / OSS | Yes via API | "Code Smells" + Maintainability Rating; webhook on every PR |
| CodeScene | SaaS | Yes via API | Hotspots from git history; predicts where debt hurts most |
| Code Climate | SaaS | Yes via API | Maintainability + duplication metrics |
| Codacy | SaaS | Yes | Aggregates linters into a debt grade |
| Stepsize | SaaS | Yes via VS Code | In-IDE debt issues, syncs with Jira/Linear |
| Linear / Jira / GitHub Projects | SaaS | Yes via API/MCP | Track items as a normal backlog with `tech-debt` label |
| Renovate / Dependabot | SaaS / OSS | Yes | Dep-debt automation (the easiest debt to pay) |
| Snyk | SaaS | Yes | CVE-driven debt (security debt subset) |

## Templates & scripts
See `templates.md` for the register layout. Useful audit one-liner agents can run weekly:

```bash
#!/usr/bin/env bash
# Usage: ./audit-debt.sh
# Surfaces unresolved TODO/HACK/FIXME with blame metadata.
set -euo pipefail
PATTERN='TODO|HACK|FIXME|XXX|TECH_DEBT'
git grep -nE "$PATTERN" -- '*.py' '*.ts' '*.tsx' '*.go' '*.rs' \
  | while IFS=: read -r file line rest; do
      author=$(git blame -L "$line,$line" --porcelain "$file" \
        | awk '/^author /{$1=""; print substr($0,2); exit}')
      ts=$(git blame -L "$line,$line" --porcelain "$file" \
        | awk '/^author-time /{print $2; exit}')
      age_days=$(( ( $(date +%s) - ts ) / 86400 ))
      printf '%s:%s\t%-20s\t%4dd\t%s\n' "$file" "$line" "$author" "$age_days" "$rest"
    done | sort -k3 -nr | head -50
```

## Best practices
- Define a fixed severity rubric (e.g., 1=cosmetic, 5=blocks release) and document it next to the register.
- Track *interest* (cost/week) explicitly, not just *principal* (cost to fix). Items with high interest jump priority.
- Allocate a budget (e.g., 20% of sprint capacity) to debt paydown — protect it like any other commitment.
- Pair every "we shipped fast" decision with a TD-NNN entry created at merge time, not retroactively.
- Never let agents close debt items without a linked PR/commit; treat the register as code, review changes.
- Use code hotspot analysis (`code-maat`) — pay down debt in files that change often, ignore stable old code.
- Distinguish debt categories in metadata: `code | design | test | infra | docs | process | dependency` — different teams own different categories.
- Write the "why we accepted this" line for any new entry — future you will thank present you.

## AI-agent gotchas
- Agents over-classify: every code smell becomes "tech debt", flooding the register. Require a minimum impact threshold (e.g., "costs ≥ 30 min/week") for entry.
- Severity inflation: agents bump everything to High. Cap with rubric and require evidence (incident link, blame data).
- Phantom resolution: agents mark items "closed" when the file moves; require a real diff in the PR description.
- Agents propose huge "big-bang" rewrites instead of incremental paydown — explicit prompt constraint: "smallest change that reduces this item's interest by ≥ 50%".
- Reading register during feature work and then expanding scope ("while I'm here…") — keep debt PRs separate from feature PRs.
- Hallucinated metrics: agents invent complexity numbers. Require tool output (radon JSON, eslint output) attached to severity claims.
- Human-in-loop checkpoint: closing any item with severity ≥ 4 needs human sign-off; agents close after their fix but humans verify.

## References
- https://martinfowler.com/bliki/TechnicalDebt.html
- https://martinfowler.com/bliki/TechnicalDebtQuadrant.html
- https://www.oreilly.com/library/view/managing-technical-debt/9780135645949/
- https://adamtornhill.com/articles/swdebt/swdebt.htm (Code as a Crime Scene)
- https://refactoring.com
- https://radon.readthedocs.io
- https://docs.sonarsource.com/sonarcloud/
- https://stepsize.com/blog/the-ultimate-guide-to-tracking-technical-debt
