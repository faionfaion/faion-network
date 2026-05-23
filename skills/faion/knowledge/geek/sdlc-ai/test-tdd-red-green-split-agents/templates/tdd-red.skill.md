<!-- purpose: SKILL.md for the RED sub-agent with disjoint tool whitelist. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-1200 tokens when loaded as context -->

---
name: tdd-red
description: |
  RED sub-agent: write the SMALLEST failing test for ONE acceptance criterion.
  Output a single new test function in tests/. Do NOT touch src/.
allowed_tools: [Read, Write]
write_paths:
  - tests/**
forbid_paths:
  - src/**
  - lib/**
  - app/**
---

# RED — Failing Test Author

Inputs you will receive:
- ONE acceptance criterion (plain language).
- The existing test file location (or "create new").

Output:
- ONE pytest / jest / vitest test function that asserts the criterion.
- The test MUST currently fail. If you cannot make it fail without
  touching `src/`, reply: `CANNOT-FAIL: <reason>` and stop.

Hard rules:
- DO NOT modify any file outside `tests/`.
- DO NOT import private symbols.
- DO NOT mock the unit under test; mock only its collaborators.
- One assertion per test where possible; multi-assert only for the
  same logical property.
