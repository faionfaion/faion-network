<!-- purpose: Quick scan checklist mapping diff observations → named signal -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300 tokens when loaded as context -->

# 6-signal overreliance scan checklist

Walk the diff once. Tick every signal that fires.

- [ ] **mismatched-naming** — variable names or method names that don't match the codebase convention (camelCase vs snake_case, `userId` vs `user_id`).
- [ ] **library-of-the-day** — new dependency added with no compare-rationale to existing libs in pom.xml / package.json / Gemfile.
- [ ] **undefended-exception** — `catch (Exception e) {}` / `printStackTrace()` / `pass` swallowing errors without context.
- [ ] **copy-pasted-prompt-artifact** — comments like "// This function" / "Here is the implementation" / triple-backticks leaking into source.
- [ ] **no-comment-integration** — non-trivial code with no comment explaining *why*; AI default-omits intent.
- [ ] **style-mix** — two clashing styles in the same file (e.g. half functional, half imperative; half explicit-return, half implicit).

## Decision

| Signals | Action |
|---------|--------|
| 0 | Acknowledge + approve |
| 1 | Ask one probing question |
| 2+ | Block with delta-format comment |
| 2+ AND blocked 3+ this month | Escalate to manager |
