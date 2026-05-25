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

| File | What's inside |
|------|---------------|
| `content/01-stack-matrix.xml` | Table mapping stack-touched (backend / frontend / user-facing / pure data) to required gates (unit / API / Playwright pos+neg). |
| `content/02-enforcement.xml` | Two-layer enforcement: readiness.md (human applicability) + CI (machine run). Both required. |
| `content/03-test-tools.xml` | Recommended (not prescriptive) tools per layer: pytest / jest / go-test for unit; supertest / requests for API; Playwright for E2E. |

## Related

- [[readiness-checklist]] — primary consumer; items 4, 5, 6 derive applicability from this matrix.
- [[user-flows-template]] — provides the Playwright pos+neg artefact this matrix gates.
- [[ui-ux-design-template]] — provides the UI heuristics artefact this matrix gates.

## Decision tree

For any change: identify which stack layers it touches → look up required gates in the matrix → tick or justify-n/a each in readiness.md.
