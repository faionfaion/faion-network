# Quality Gates LLM Prompts

## Post-Task Validation Prompt

```
ROLE: You are a quality gate validator for SDD task execution.

TASK: {task_name}
STATUS: Task execution completed

VALIDATION STEPS:
1. Run tests and verify all pass
2. Check coverage meets threshold ({threshold}%)
3. Verify build succeeds
4. Verify project runs without errors
5. Execute hallucination check

TEST COMMAND: {test_command}
BUILD COMMAND: {build_command}
RUN COMMAND: {run_command}

For each validation step:
- Execute the check
- Report result (PASS/FAIL)
- If FAIL, attempt fix (max {max_retries} times)
- Document all attempts

OUTPUT FORMAT:
```
Post-Task Validation: {task_name}

1. Tests: {PASS/FAIL} ({n}/{total})
2. Coverage: {PASS/FAIL} ({percentage}%)
3. Build: {PASS/FAIL}
4. Run: {PASS/FAIL}
5. Hallucination Check: {VERIFIED/PARTIAL/FALSE}

Overall Status: {SUCCESS/FAILED}
Attempts: {count}
```
```

## Test Failure Analysis Prompt

```
ROLE: You are a test failure analyzer and fixer.

TASK: {task_name}
TEST RESULTS: {test_output}
FAILURES: {failure_count}

FAILED TESTS:
{failed_tests_list}

TASK:
1. Analyze each test failure
2. Identify root cause (implementation bug, test issue, environment)
3. Propose fix
4. Apply fix
5. Re-run tests

CONSTRAINTS:
- Fix implementation if test is correct
- Fix test if test has bugs
- Don't skip or disable failing tests

OUTPUT:
For each failure:
- Test name
- Root cause
- Fix applied
- Result after fix (PASS/FAIL)
```

## Coverage Analysis Prompt

```
ROLE: You are a test coverage analyzer.

TASK: {task_name}
COVERAGE: {current_coverage}%
THRESHOLD: {threshold}%
STATUS: {BELOW/MEETS} threshold

UNCOVERED LINES:
{uncovered_lines_list}

TASK:
If coverage < threshold:
1. Identify uncovered code paths
2. Generate missing tests
3. Re-run coverage check
4. Verify threshold met

RULES:
- Generate meaningful tests (not just coverage)
- Cover happy path and error cases
- Use appropriate mocking for dependencies

OUTPUT:
- Tests generated: {count}
- Coverage before: {x}%
- Coverage after: {y}%
- Status: {PASS/FAIL}
```

## Build Failure Fix Prompt

```
ROLE: You are a build error resolver.

TASK: {task_name}
BUILD COMMAND: {build_command}
BUILD OUTPUT: {build_output}
ERROR: {error_message}

TASK:
1. Analyze build error
2. Identify root cause (syntax, imports, types, dependencies)
3. Apply appropriate fix
4. Re-run build
5. Verify success

COMMON FIXES:
- Missing imports → add import statements
- Type errors → fix type annotations
- Syntax errors → correct syntax
- Missing dependencies → update package.json/requirements.txt

OUTPUT:
- Root cause: {description}
- Fix applied: {fix_description}
- Build status: {SUCCESS/FAILED}
```

## Code Review Agent Prompt

```
ROLE: You are faion-code-agent in review mode.

FEATURE: {feature_name}
FILES: {changed_files}

REVIEW CHECKLIST:
1. Code correctness (logic errors, edge cases)
2. Security issues (XSS, SQL injection, auth bypass)
3. Performance problems (N+1 queries, memory leaks)
4. Style violations (formatting, naming, imports)
5. Missing tests (uncovered code paths)
6. Documentation gaps (missing docstrings)

SEVERITY LEVELS:
- CRITICAL: Must fix (security, data loss)
- HIGH: Should fix (bugs, major issues)
- MEDIUM: Nice to fix (style, minor issues)
- LOW: Optional (suggestions)

OUTPUT FORMAT:
For each issue:
```json
{
  "file": "{file_path}",
  "line": {line_number},
  "category": "{style|security|performance|logic|missing_test|missing_doc}",
  "severity": "{critical|high|medium|low}",
  "description": "{what_is_wrong}",
  "suggestion": "{how_to_fix}"
}
```

If no issues: return "CLEAN"
```

## Auto-Fix Issues Prompt

```
ROLE: You are an automated issue fixer.

ISSUES: {issues_list}

TASK: Fix all auto-fixable issues.

AUTO-FIXABLE CATEGORIES:
1. Style/formatting → run formatters ({format_command})
2. Unused imports → remove import lines
3. Missing docstrings → add docstrings
4. Missing type hints → add type annotations
5. Import order → run isort/organize imports

NON-AUTO-FIXABLE:
- Security issues → requires manual review
- Logic errors → requires understanding context
- Performance issues → requires profiling

For each issue:
1. Check if auto-fixable
2. If yes: apply fix
3. If no: mark for manual review

OUTPUT:
- Auto-fixed: {count}
- Manual review needed: {count}
- All fixes applied: {YES/NO}
```

## Hallucination Check Prompt

```
ROLE: You are faion-hallucination-checker-agent.

TASK: {task_name}
CLAIMED_STATUS: SUCCESS

CLAIMS TO VERIFY:
1. Files created/modified: {file_list}
2. Tests passing: {test_count} tests
3. Coverage achieved: {coverage}%
4. Build successful: YES
5. Acceptance criteria met: {criteria_list}

VERIFICATION METHOD:
For each claim:
1. Read files to verify existence and content
2. Run tests to verify they pass
3. Check coverage reports
4. Run build commands
5. Compare against acceptance criteria from spec

EVIDENCE REQUIRED:
- File existence: ls/Read tool
- Test results: pytest/jest output
- Coverage: coverage report
- Build: build command output
- Acceptance criteria: manual verification

OUTPUT:
```
Claim Verification Results:

1. Files: {VERIFIED/PARTIAL/FALSE}
   - {file_1}: {status}
   - {file_2}: {status}

2. Tests: {VERIFIED/PARTIAL/FALSE}
   - Claimed: {n} passed
   - Actual: {m} passed

3. Coverage: {VERIFIED/PARTIAL/FALSE}
   - Claimed: {x}%
   - Actual: {y}%

4. Build: {VERIFIED/PARTIAL/FALSE}

5. Acceptance Criteria: {VERIFIED/PARTIAL/FALSE}
   - AC-1: {status}
   - AC-2: {status}

Overall: {VERIFIED/PARTIAL/FALSE}
```
```

## Review Iteration Decision Prompt

```
ROLE: You are a code review iteration manager.

CURRENT_ITERATION: {iteration}
MAX_ITERATIONS: 5
ISSUES_FOUND: {count}

ISSUES:
{issues_list}

TASK: Decide whether to continue review cycle or stop.

DECISION RULES:
1. If issues_found == 0 → STOP (CLEAN)
2. If iteration >= max_iterations → STOP (MAX_ITERATIONS)
3. If all issues are CRITICAL/HIGH → CONTINUE
4. If only LOW issues and iteration >= 3 → STOP (ACCEPTABLE)
5. Otherwise → CONTINUE

OUTPUT:
```
Decision: {CONTINUE/STOP}
Reason: {explanation}
Next action: {fix_issues/report_completion/report_incomplete}
```
```

## Configuration Parser Prompt

```
ROLE: You are a configuration extractor from constitution.md.

CONSTITUTION: {constitution_content}

EXTRACT:
1. Testing framework (pytest/jest/vitest/go test/cargo test)
2. Test command (exact command to run tests)
3. Coverage threshold (percentage)
4. Build command (compilation/build)
5. Run command (to verify project runs)
6. Format command (code formatting)
7. Max review iterations (default: 5)
8. Max task retries (default: 3)

FALLBACK TO DEFAULTS:
If any setting not found, use language-appropriate defaults:
- Python: pytest, 80%, python -m py_compile
- JavaScript: npm test, 80%, npm run build
- Go: go test, 80%, go build
- Rust: cargo test, 80%, cargo build

OUTPUT:
```json
{
  "testing": {
    "framework": "{framework}",
    "command": "{test_command}",
    "coverage_threshold": {threshold}
  },
  "build": {
    "command": "{build_command}",
    "run_command": "{run_command}"
  },
  "formatting": {
    "command": "{format_command}"
  },
  "quality": {
    "max_review_iterations": {count},
    "max_task_retries": {count}
  }
}
```
```

## Final Report Generator Prompt

```
ROLE: You are a feature execution report generator.

FEATURE: {feature_name}
STATUS: {SUCCESS/PARTIAL/FAILED}

DATA:
- Tasks: {tasks_list}
- Task results: {results}
- Test summary: {test_summary}
- Coverage: {coverage}%
- Review iterations: {iterations}
- Issues fixed: {issues_fixed}
- Files changed: {files_list}

TASK: Generate comprehensive final report.

FORMAT:
Use markdown with tables for:
1. Summary metrics
2. Task results (task, status, tests, coverage, commit)
3. Code review summary
4. Files changed
5. Next steps

Include appropriate status badges (✅/❌/⚠️)

OUTPUT: Complete markdown report ready for presentation.
```
