# AI Code Review Checklist

## Summary

**One-sentence:** Twelve-check rubric for reviewing AI-generated diffs (Copilot, Claude, Cursor) before merge — hallucinated APIs, silent-skip tests, convention drift, supply-chain risk.

**One-paragraph:** Solves the dominant 2025-2026 PR-review failure mode: reviewer trusts the diff because it compiles and looks plausible, but it imports a non-existent package, deletes a failing test instead of fixing it, or adopts a pattern foreign to the codebase. Mechanism: a fixed 12-point checklist applied to any diff where ≥30% of new lines were AI-generated, with each check carrying a "block merge / request changes / approve with note" verdict. Primary output: a review-decision artefact + checklist trace recorded in the PR.

**Ефективно для:**

- Solo / outsource lead reviewing Copilot / Claude / Cursor-authored diffs.
- Team adopting AI-pair coding wanting deterministic merge gates rather than "reviewer judgement".
- Supply-chain audit: catches "slopsquatted" packages an AI imported by name.
- Repo's pre-commit AI-policy enforcement bot.

## Applies If (ALL must hold)

- pr_contains_ai_generated_diff == true (Copilot/Claude/Cursor commit signature OR author-disclosed)
- diff_size > 20 lines (smaller diffs use the generic code-review-process)
- target_branch is protected (main/master/production)
- reviewer is the author or a teammate doing human review (not just CI)

## Skip If (ANY kills it)

- diff is purely cosmetic (formatting, comments) — generic style review is enough
- diff is fully covered by deterministic codemod output — codemod review is different
- repo is a throwaway experiment without protected branches — overhead not justified
- AI generated only test data fixtures (no production code) — fixture review is different

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| AGENTS.md / CLAUDE.md / CONVENTIONS.md | Markdown | repo root |
| Pre-commit hooks installed | YAML | repo |
| Lockfile (package-lock / poetry.lock / Cargo.lock / go.sum) | text | repo |
| Diff with AI markers | git | repo |
| Codebase convention inventory | Markdown | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/bug-report-quality-rubric` | Bug-rubric for the surfacing-bug variant; sibling at intake. |
| `solo/dev/code-quality/tech-debt-management` | Provides "is this debt deferral disguised as a fix?" framing for check 11. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 checks + run + skip = 14 rules with detector + verdict policy | 1500 |
| `content/02-output-contract.xml` | essential | JSON Schema for the review-decision artefact + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 6 reviewer failure modes specific to AI-generated diffs | 900 |
| `content/04-procedure.xml` | medium | 5-step procedure: detect-AI → run 12 checks → aggregate → block/request/approve → record | 700 |
| `content/06-decision-tree.xml` | essential | Tree: any block-tier check fired? → block; else any request-changes? → request; else approve | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `static_checks_aggregation` | haiku | Pull together lint/type/test/lockfile signals. |
| `per-check_verdict` | sonnet | Bounded judgment per check; reads diff context. |
| `cross-check_synthesis` | opus | Final merge/block decision integrating 12 verdicts + repo conventions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-code-review-checklist.json` | JSON Schema for the review-decision artefact. |
| `templates/checklist-trace.md` | Markdown skeleton the reviewer fills (12 rows + verdict). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-code-review-checklist.py` | Validate the review-decision JSON against schema + verdict consistency. | Pre-merge bot; after reviewer completes the checklist. |

## Related

- [[code-quality/tech-debt-management]] — framing for "AI deferred this" detection.
- [[bug-pattern-to-lint-rule-conversion]] — convert recurring AI bugs into deterministic detectors.
- external: [GitHub Copilot review-resistance study (2024)](https://arxiv.org/abs/2404.10543) · [Stanford "Do Users Write More Insecure Code with AI Assistants?" (Perry et al., 2023)](https://arxiv.org/abs/2211.03622) · [Snyk supply-chain "slopsquatting" advisories (2025)]

## Decision tree

See `content/06-decision-tree.xml`. The tree iterates through the 12 checks; any block-tier failure forces verdict=block; any request-changes failure with no block forces verdict=request-changes; all approved-with-note OR pass = approve. Leaves emit `approve`, `request-changes`, or `block` and reference the specific check id from `01-core-rules.xml`.
