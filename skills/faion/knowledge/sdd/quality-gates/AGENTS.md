# Quality Gates

## Summary

**One-sentence:** Declares the quality gates each stack type requires (API tests for backend; Playwright pos+neg for user-facing; etc.); consumed by `readiness-checklist` when computing which items apply.

**One-paragraph:** Quality gates are NOT prescriptive about test frameworks (pytest / jest / go-test / Playwright). They ARE prescriptive about which kind of test must exist for which kind of change. The matrix maps stack-touched → gate-required. Each gate is enforced twice: once in `readiness.md` (human judgement re: applicability) and once in CI (machine actual run). Both required.

**Ефективно для:**

- Reviewer computing readiness item 5 / 6 applicability from the git diff.
- Subagent close-out logic deciding whether to run API tests, Playwright, both, or neither.
- New-project setup — pin which gates apply before code is written.

## Applies If (ALL must hold)

- Project uses readiness-checklist methodology.
- CI exists (lint + typecheck + unit minimum).
- A user-facing or API surface exists in at least part of the codebase.

## Skip If (ANY kills it)

- Throwaway prototype.
- Pure-documentation project.

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 11 testable rules: the six matrix rows (backend / full-stack / user-facing flow / frontend / pure data / infra), applicability from the git diff, readiness tick-or-n/a, CI runs every gate, framework neutrality, API tests live with the code | ~1600 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the per-change gate-applicability record (layers, required gates, readiness disposition, CI run); valid / invalid examples; 6 forbidden patterns | ~1600 |
| `content/03-failure-modes.xml` | essential | Why both layers, then 4 antipatterns: "no UI change" claimed, CI-alone rubber stamp, readiness without CI, Postman as the API gate | ~950 |
| `content/04-procedure.xml` | essential | 5 steps: classify layers from the diff, look up the matrix, pick tools, dispose each gate in readiness.md, CI runs green before done/ | ~950 |
| `content/05-examples.xml` | recommended | The stack-to-gate matrix as a lookup table and the recommended (not prescriptive) tools per layer | ~1100 |
| `content/06-decision-tree.xml` | essential | Preconditions gate, diff-not-self-assessment check, then layers touched → matrix row; readiness-vs-CI mismatch branches | ~950 |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-quality-gates.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[readiness-checklist]] — primary consumer; items 4, 5, 6 derive applicability from this matrix.
- [[user-flows-template]] — provides the Playwright pos+neg artefact this matrix gates.
- [[ui-ux-design-template]] — provides the UI heuristics artefact this matrix gates.

## Decision tree

For any change: identify which stack layers it touches → look up required gates in the matrix → tick or justify-n/a each in readiness.md.
