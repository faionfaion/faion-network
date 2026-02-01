# Quality Gates

Validation checkpoints after each task and feature completion.

---

## Post-Task Validation

After EACH task completion:

```python
def post_task_validation(task):
    """Run quality gates after task execution."""

    # 1. Run tests
    test_result = run_tests()
    if not test_result.passed:
        fix_tests(test_result.failures)
        # Retry up to 3 times

    # 2. Check coverage
    coverage = check_coverage()
    if coverage < threshold:
        log_warning(f"Coverage {coverage}% below threshold {threshold}%")

    # 3. Verify project runs
    build_result = run_build()
    if not build_result.success:
        fix_build(build_result.errors)
        # Retry up to 3 times

    # 4. Verify with hallucination checker
    Task(
        subagent_type="faion-hallucination-checker-agent",
        prompt=f"Verify task {task.name} completion with evidence"
    )
```

---

## Review Acceptance Criteria

Review cycle ends when:
- [ ] No critical issues
- [ ] No security issues
- [ ] All tests pass
- [ ] Coverage meets threshold
- [ ] Build succeeds
- [ ] No style violations

---

## Configuration

### From Constitution

The skill reads these settings from `constitution.md`:

```yaml
testing:
  framework: pytest          # or jest, vitest, go test
  command: make test-dev     # test execution command
  coverage_threshold: 80     # minimum coverage %

build:
  command: make build        # build command
  run_command: make run-dev  # run/verify command

formatting:
  command: make fix          # auto-format command
```

### Defaults

If not specified in constitution:

| Setting | Default |
|---------|---------|
| Test command | `pytest` / `npm test` |
| Coverage threshold | 80% |
| Build command | `npm run build` / `make build` |
| Max review iterations | 5 |
| Max task retries | 3 |

---

## Constraints

**Must:**
- Load full context before execution
- Run tests after EVERY task
- Fix ALL review issues before completing
- Document all changes
- Verify project runs

**Must NOT:**
- Skip failing tests
- Ignore code review issues
- Push to remote without review
- Modify spec or design (only implementation)
- Delete or skip tasks

---

## Output Format

### Success

```markdown
# Feature Execution: {project}/{feature}

## Status: SUCCESS

### Summary
| Metric | Value |
|--------|-------|
| Tasks Completed | N/N |
| Tests | X passed |
| Coverage | Y% |
| Review Iterations | Z |
| Total Duration | HH:MM |

### Task Results

| Task | Status | Tests | Coverage | Commit |
|------|--------|-------|----------|--------|
| TASK_001 | ✅ | 12/12 | 85% | abc123 |
| TASK_002 | ✅ | 8/8 | 82% | def456 |
| TASK_003 | ✅ | 15/15 | 88% | ghi789 |

### Code Review
- Iterations: 2
- Issues Fixed: 7
- Final Status: CLEAN

### Files Changed
- `app/models/refund.py` (CREATE, 120 lines)
- `app/services/refund.py` (CREATE, 200 lines)
- `app/views/refund.py` (CREATE, 80 lines)
- `tests/test_refund.py` (CREATE, 150 lines)

### Next Steps
- Feature moved to `done/`
- Ready for deployment
```

### Partial Success

```markdown
# Feature Execution: {project}/{feature}

## Status: PARTIAL

### Summary
| Metric | Value |
|--------|-------|
| Tasks Completed | M/N |
| Tasks Failed | K |
| Blockers | L |

### Failed Tasks

| Task | Status | Reason | Attempts |
|------|--------|--------|----------|
| TASK_003 | FAILED | Tests failing | 3 |
| TASK_004 | BLOCKED | Depends on TASK_003 | - |

### Required Actions
1. Fix TASK_003 test failures manually
2. Re-run feature executor
```

### Failed

```markdown
# Feature Execution: {project}/{feature}

## Status: FAILED

### Reason
{Critical error description}

### Context
- Last successful task: TASK_002
- Failed at: TASK_003
- Error: {error details}

### Recovery Steps
1. {Step 1}
2. {Step 2}
```

---

*faion-feature-executor/quality-gates.md*

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Run test suite, update task status, commit code | haiku | Mechanical execution and status updates |
| Review acceptance criteria completeness | sonnet | Evaluation and analysis |
| Unblock task dependencies, triage failures | sonnet | Problem-solving and diagnosis |
| Plan complex feature spanning multiple services | opus | Architecture and coordination |
| Implement quality gates and CI/CD checks | sonnet | Engineering patterns and practices |
| Resolve production incidents blocking releases | opus | Complex troubleshooting, high-impact decisions |
| Refactor shared code across multiple tasks | sonnet | Code analysis and transformation |
