# Quality Gates Templates

## Post-Task Validation Function

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

## Constitution Configuration Template

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

quality:
  max_review_iterations: 5   # max code review cycles
  max_task_retries: 3        # max retries per task
```

## Success Output Template

```markdown
# Feature Execution: {project}/{feature}

## Status: SUCCESS

### Summary
| Metric | Value |
|--------|-------|
| Tasks Completed | {n}/{n} |
| Tests | {x} passed |
| Coverage | {y}% |
| Review Iterations | {z} |

### Task Results

| Task | Status | Tests | Coverage | Commit |
|------|--------|-------|----------|--------|
| TASK-001 | ✅ | {n}/{n} | {x}% | {hash} |
| TASK-002 | ✅ | {n}/{n} | {x}% | {hash} |
| TASK-N | ✅ | {n}/{n} | {x}% | {hash} |

### Code Review
- Iterations: {count}
- Issues Fixed: {count}
- Final Status: CLEAN

### Files Changed
- `{file_path}` (CREATE, {lines} lines)
- `{file_path}` (MODIFY, {lines} lines)

### Next Steps
- Feature moved to `done/`
- Ready for deployment
```

## Partial Success Output Template

```markdown
# Feature Execution: {project}/{feature}

## Status: PARTIAL

### Summary
| Metric | Value |
|--------|-------|
| Tasks Completed | {m}/{n} |
| Tasks Failed | {k} |
| Blockers | {l} |

### Failed Tasks

| Task | Status | Reason | Attempts |
|------|--------|--------|----------|
| TASK-{x} | FAILED | {reason} | {count} |
| TASK-{y} | BLOCKED | Depends on TASK-{x} | - |

### Required Actions
1. {action_1}
2. {action_2}
```

## Failed Output Template

```markdown
# Feature Execution: {project}/{feature}

## Status: FAILED

### Reason
{error_description}

### Context
- Last successful task: TASK-{x}
- Failed at: TASK-{y}
- Error: {error_details}

### Recovery Steps
1. {step_1}
2. {step_2}
```

## Test Execution Template

```bash
# Python (pytest)
pytest -v --tb=short --cov={module} --cov-report=term-missing

# JavaScript (Jest)
npm test -- --coverage --verbose

# JavaScript (Vitest)
vitest run --coverage

# Go
go test -v -cover ./...

# Rust
cargo test --all-features
```

## Coverage Report Parse Template

```python
def parse_coverage(output):
    """Extract coverage percentage from test output."""

    patterns = {
        'pytest': r'TOTAL\s+\d+\s+\d+\s+(\d+)%',
        'jest': r'All files\s+\|\s+(\d+\.?\d*)',
        'go': r'coverage:\s+(\d+\.?\d*)%',
        'cargo': r'test result: ok\. \d+ passed.*coverage: (\d+\.?\d*)%'
    }

    for framework, pattern in patterns.items():
        match = re.search(pattern, output)
        if match:
            return float(match.group(1))

    return None
```

## Review Issue Template

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

## Hallucination Check Template

```
ROLE: You are faion-hallucination-checker-agent.

TASK: {task_name}
CLAIMED_STATUS: SUCCESS

VERIFICATION CHECKLIST:
1. Files claimed as created/modified exist
2. Tests claimed as passing actually pass
3. Coverage claimed as {X}% actually achieved
4. Build claimed as successful actually succeeds
5. Acceptance criteria actually met

VERIFY EACH CLAIM:
{claim_list}

OUTPUT:
- VERIFIED: All claims accurate
- PARTIAL: Some claims inaccurate (list discrepancies)
- FALSE: Major claims incorrect (list all)
```

## Default Settings Template

```python
DEFAULT_SETTINGS = {
    'python': {
        'test_command': 'pytest -v --cov',
        'build_command': 'python -m py_compile',
        'format_command': 'black . && isort .'
    },
    'javascript': {
        'test_command': 'npm test',
        'build_command': 'npm run build',
        'format_command': 'npm run format'
    },
    'typescript': {
        'test_command': 'npm test',
        'build_command': 'tsc && npm run build',
        'format_command': 'npm run format'
    },
    'go': {
        'test_command': 'go test -v ./...',
        'build_command': 'go build ./...',
        'format_command': 'go fmt ./...'
    },
    'rust': {
        'test_command': 'cargo test',
        'build_command': 'cargo build',
        'format_command': 'cargo fmt'
    }
}

DEFAULT_THRESHOLDS = {
    'coverage_threshold': 80,
    'max_review_iterations': 5,
    'max_task_retries': 3
}
```
