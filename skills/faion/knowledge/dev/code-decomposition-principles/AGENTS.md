# Code Decomposition Principles

## Summary

**One-sentence:** Audits a file against the three decomposition principles (size, single-responsibility, LLM-context fit) and emits a decision record: split / leave / merge.

**One-paragraph:** A file is decomposable when three signals align: LOC > 300 / tokens > 10k, multiple responsibilities, and frequent churn against unrelated callers. This methodology audits each candidate file, emits a decision record with the triggering signals + the proposed action, and feeds candidates into `code-decomposition-patterns` for the actual move list. Output is a decision record (markdown frontmatter or JSON) — versioned, owner-named, reviewable. Anti-pattern: splitting because it 'feels big'.

**Ефективно для:**

- Аудит monorepo на decomposition candidates: ranking за churn + size — топ-10 кандидатів за один прохід.
- Code-review: рев'юер має детермінований чек 'чи варто розбивати'.
- Onboarding: новий розробник бачить, які файли planned-to-split (decision = split + status=queued).
- LLM-context tuning: файли &gt;10k токенів дражать context-window; рішення = split &lt;5k шматків.

## Applies If (ALL must hold)

- Repo has files ≥300 LOC OR ≥10k tokens (candidate pool exists).
- Working git history (≥3 months) so churn can be measured.
- A reviewer / owner can act on the decision record.

## Skip If (ANY kills it)

- Repo is &lt;500 files total — overhead beats payoff.
- Greenfield prototype where files will be rewritten before they stabilise.
- Files are auto-generated.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| File path list | newline-separated | find . -name '*.py' -size +5k |
| Git churn data | json | git log --pretty=format per file |
| Token counts | integer | tiktoken / tokenizer on file content |
| Responsibility map | tags per file | static analysis or AGENTS.md docs |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: size-trigger, srp-detector, churn-signal, llm-fit, owner-named | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for decision record | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: split-by-feeling, ignore-churn, decompose-and-rewrite, no-owner | 700 |
| `content/04-procedure.xml` | essential | 5-step audit procedure | 700 |
| `content/06-decision-tree.xml` | essential | split / leave / merge tree | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scan_candidates` | haiku | Static metrics: LOC, tokens, churn — deterministic. |
| `classify_responsibilities` | sonnet | Per-file judgment of which responsibilities exist; needs context. |
| `draft_decision_record` | sonnet | Synthesises signals into a one-page record. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decomp-candidates.sh` | Shell scan that lists files crossing decomposition thresholds |
| `templates/planner-prompt.txt` | LLM prompt that turns scan output into a decision record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-decomposition-principles.py` | Validate a decision record against the schema | After draft_decision_record, before posting to PR / owner |

## Related

- - [[code-decomposition-patterns]] — once a file is decided 'split', pick the pattern.
- - [[refactoring-patterns]] — low-level transforms inside each split.

## Decision tree

See `content/06-decision-tree.xml`. Tree branches: size threshold met? → responsibilities ≥2? → churn high vs. unrelated? Leaves: split (highest-confidence candidate), leave (one signal only), merge (file is unusually small but always edited with a sibling).
