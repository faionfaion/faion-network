# Tech Debt Basics

## Summary

**One-sentence:** Builds a capped tech-debt register (≤30 rows) classified by Fowler's quadrant with severity, evidence, and weekly interest cost per row.

**One-paragraph:** Untracked tech debt accrues silently; tracking everything turns the register into a graveyard. This methodology produces a TECH_DEBT_REGISTER.md capped at 20-30 active rows, each carrying: type (Fowler quadrant), severity, file location, evidence link (PR / postmortem), and a weekly interest cost estimate. Agents scan to surface candidates; humans approve before adding. Register is reviewed monthly: items past 90 days without action are escalated or closed.

**Ефективно для:**

- Команди, що 'знають що в нас борг', але не можуть назвати топ-3.
- Quarterly planning: register дає reasoning 'що рефакторити' замість gut feel.
- Onboarding senior: register показує 'тут небезпеки' за 5 хв замість трьох тижнів.
- AI-driven scan: агент пропонує кандидатів, людина approves.

## Applies If (ALL must hold)

- Codebase is &gt;6 months old.
- Team has authority to schedule refactor time.
- An owner is willing to maintain the register monthly.

## Skip If (ANY kills it)

- Pre-product-market-fit prototype — debt is mostly intentional and uniform.
- Codebase is end-of-life — register has no payoff.
- Team already has a working bug-tracker that handles debt — don't duplicate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo + git history | path | git rev-parse |
| Postmortem archive | path or URL | team docs |
| Owner | string | team handbook |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: register-cap, fowler-quadrant, evidence-link, monthly-review, agent-scan-human-approve | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for debt register entries | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: graveyard, unclassified, no-owner | 600 |
| `content/05-examples.xml` | reference | Sample 3-row register | 500 |
| `content/06-decision-tree.xml` | essential | Quadrant picker tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scan_candidates` | haiku | Static scan + churn metrics. |
| `classify_quadrant` | sonnet | Per-item Fowler classification. |
| `estimate_interest` | sonnet | Per-item cost estimate. |

## Templates

| File | Purpose |
|------|---------|
| `templates/TECH_DEBT_REGISTER.md.j2` | Skeleton register the team commits to repo |
| `templates/TECH_DEBT_REGISTER.md` | Skeleton register the team commits to repo Generated from `templates/TECH_DEBT_REGISTER.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/scan-debt.sh` | Shell scan that surfaces candidates |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tech-debt-basics.py` | Validate register against schema | Before commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- - [[refactoring-patterns]] — register items in 'reckless' quadrant route here for fix.
- - [[code-decomposition-principles]] — register often surfaces decomposition candidates.

## Decision tree

See `content/06-decision-tree.xml`. Tree asks: was the debt incurred deliberately? was the team aware of the consequence? Combines the two into the four Fowler quadrants; each quadrant routes to a recommended action (refactor / accept / educate / monitor).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/scan-debt.sh`

```bash
#!/usr/bin/env bash
# scan-debt.sh — emit candidate technical debt items as JSONL.
# Pipe output into a triage agent for deduplication and severity classification.
# Usage: scan-debt.sh [src-dir]
set -euo pipefail

ROOT="${1:-.}"

# Code debt: high-complexity functions (CCN > 15)
if command -v lizard >/dev/null 2>&1; then
  lizard -C 15 "$ROOT" --csv 2>/dev/null \
    | awk -F, 'NR>1 && $3+0>15 {
        printf "{\"type\":\"code\",\"location\":\"%s:%s\",\"evidence\":\"CCN=%s\"}\n",
        $NF, $5, $3
      }'
fi

# Test debt: Python files lacking a sibling test_ file
find "$ROOT" -name '*.py' -not -path '*/tests/*' -not -path '*/__pycache__/*' \
  | while read -r f; do
    base=$(basename "$f" .py)
    if ! find "$ROOT" -name "test_${base}.py" -print -quit 2>/dev/null | grep -q .; then
      echo "{\"type\":\"test\",\"location\":\"$f\",\"evidence\":\"no test_${base}.py found\"}"
    fi
  done

# Infra debt: outdated npm dependencies
if [ -f "$ROOT/package.json" ] && command -v npm >/dev/null 2>&1; then
  (cd "$ROOT" && npm outdated --json 2>/dev/null \
    | jq -r 'to_entries[] |
        "{\"type\":\"infra\",\"location\":\"package.json:\(.key)\",\"evidence\":\"outdated \(.value.current)→\(.value.latest)\"}"' \
    2>/dev/null || true)
fi

# Infra debt: outdated Python deps
if [ -f "$ROOT/pyproject.toml" ] && command -v pip >/dev/null 2>&1; then
  pip list --outdated --format=json 2>/dev/null \
    | jq -r '.[] | "{\"type\":\"infra\",\"location\":\"pyproject.toml:\(.name)\",\"evidence\":\"outdated \(.version)→\(.latest_version)\"}"' \
    2>/dev/null || true
fi
```
