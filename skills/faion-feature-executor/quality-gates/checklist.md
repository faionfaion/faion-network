# Quality Gates Checklist

## Post-Task Validation

After EACH task:

- [ ] Tests executed
- [ ] All tests pass
- [ ] No new test failures introduced
- [ ] Coverage calculated
- [ ] Coverage >= threshold (default 80%)
- [ ] Coverage not decreased from previous baseline
- [ ] Build command executed
- [ ] Build succeeds
- [ ] Project runs without errors
- [ ] Hallucination check executed
- [ ] Task completion verified with evidence

## Test Validation

- [ ] Test framework detected (pytest/jest/vitest/go test)
- [ ] Test command from constitution loaded
- [ ] Tests run with coverage enabled
- [ ] Test output captured
- [ ] Failures analyzed (if any)
- [ ] Test retry attempted (max 3 times)
- [ ] Final test status: PASS

## Coverage Validation

- [ ] Coverage report generated
- [ ] Coverage percentage extracted
- [ ] Coverage compared to threshold
- [ ] Warning logged if below threshold
- [ ] Coverage report saved for reference
- [ ] Uncovered lines identified

## Build Validation

- [ ] Build command from constitution loaded
- [ ] Build executed successfully
- [ ] Build errors captured (if any)
- [ ] Build retry attempted (max 3 times)
- [ ] Run command executed (if specified)
- [ ] Project starts without errors

## Code Review Acceptance

- [ ] No critical issues
- [ ] No security issues
- [ ] No high-severity issues
- [ ] All tests pass
- [ ] Coverage meets threshold
- [ ] Build succeeds
- [ ] No style violations
- [ ] No unused imports
- [ ] All functions documented
- [ ] Type hints present (if applicable)

## Review Iteration Checklist

For EACH iteration:

- [ ] Code review executed via faion-code-agent
- [ ] Review output parsed
- [ ] Issues categorized by type
- [ ] Issues categorized by severity
- [ ] Critical issues count: 0
- [ ] Security issues count: 0
- [ ] Auto-fixable issues identified
- [ ] Auto-fixes applied
- [ ] Manual fixes applied
- [ ] Tests re-run after fixes
- [ ] All tests pass after fixes
- [ ] Max iterations not exceeded (5)

## Configuration Validation

From constitution.md:

- [ ] Test framework identified
- [ ] Test command loaded
- [ ] Coverage threshold loaded
- [ ] Build command loaded
- [ ] Run command loaded (optional)
- [ ] Format command loaded (optional)
- [ ] Max review iterations configured
- [ ] Max task retries configured

## Default Settings Applied

If not in constitution:

- [ ] Test command defaulted (pytest/npm test)
- [ ] Coverage threshold defaulted (80%)
- [ ] Build command defaulted (npm run build/make build)
- [ ] Max review iterations defaulted (5)
- [ ] Max task retries defaulted (3)

## Constraints Enforcement

MUST checks:

- [ ] Full context loaded before execution
- [ ] Tests run after EVERY task
- [ ] ALL review issues fixed before completing
- [ ] All changes documented
- [ ] Project verified to run

MUST NOT checks:

- [ ] No failing tests skipped
- [ ] No code review issues ignored
- [ ] No remote pushes without review
- [ ] No spec.md modifications
- [ ] No design.md modifications
- [ ] No tasks deleted
- [ ] No tasks skipped

## Output Validation

SUCCESS criteria:

- [ ] All tasks completed
- [ ] All tests pass
- [ ] Coverage >= threshold
- [ ] Code review: CLEAN
- [ ] Feature moved to done/
- [ ] Summary report generated

PARTIAL criteria:

- [ ] Some tasks completed
- [ ] Some tasks failed
- [ ] Blockers identified
- [ ] Required actions listed

FAILED criteria:

- [ ] Critical error occurred
- [ ] Last successful task identified
- [ ] Failed task identified
- [ ] Error details captured
- [ ] Recovery steps provided

## Hallucination Check Validation

- [ ] Task completion claims verified
- [ ] File existence verified
- [ ] Test results verified
- [ ] Coverage numbers verified
- [ ] Build status verified
- [ ] Acceptance criteria verified
- [ ] Evidence provided for all claims
- [ ] Status: VERIFIED/PARTIAL/FALSE
