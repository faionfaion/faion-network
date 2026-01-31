# Execution Workflow Templates

## Context Package Template

```markdown
## Project Context

### Constitution Summary
- Tech: {tech_stack}
- Standards: {linters}, {formatters}
- Testing: {framework}, coverage {threshold}%
- Build: {build_command}
- Run: {run_command}
- Format: {format_command}

### Feature: {feature_name}

#### Requirements (from spec.md)
- FR-1: {requirement_text}
- FR-2: {requirement_text}
- FR-N: {requirement_text}

#### Architecture (from design.md)
- AD-1: {decision_text}
- AD-2: {decision_text}
- AD-N: {decision_text}

#### Files
**CREATE:**
- {file_path_1}
- {file_path_2}

**MODIFY:**
- {file_path_3}
- {file_path_4}

#### Task Dependencies
- TASK-001 → TASK-002
- TASK-002 → TASK-003, TASK-004
```

## Task Executor Prompt Template

```
PROJECT: {project_name}
FEATURE: {feature_name}
FEATURE_DIR: {feature_directory_path}
TASKS_DIR: {tasks_directory_path}

## Context Package
{context_package_content}

## Task to Execute
{task_file_name}

Execute this task following SDD workflow.
```

## Code Review Prompt Template

```
task_type: review
project_path: {project_path}
context: Review all code changes for feature {feature_name}

Focus on:
1. Code correctness
2. Security issues
3. Performance problems
4. Style violations
5. Missing tests
6. Documentation gaps

Feature files:
{list_of_changed_files}
```

## Success Report Template

```markdown
# Feature Execution: {project}/{feature}

## Status: SUCCESS

### Summary
| Metric | Value |
|--------|-------|
| Tasks Completed | {completed}/{total} |
| Tests | {passed} passed |
| Coverage | {coverage}% |
| Review Iterations | {iterations} |

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

## Partial Success Report Template

```markdown
# Feature Execution: {project}/{feature}

## Status: PARTIAL

### Summary
| Metric | Value |
|--------|-------|
| Tasks Completed | {completed}/{total} |
| Tasks Failed | {failed} |
| Blockers | {blocked} |

### Failed Tasks

| Task | Status | Reason | Attempts |
|------|--------|--------|----------|
| TASK-N | FAILED | {reason} | {count} |
| TASK-M | BLOCKED | Depends on TASK-N | - |

### Required Actions
1. {action_1}
2. {action_2}
```

## Failed Report Template

```markdown
# Feature Execution: {project}/{feature}

## Status: FAILED

### Reason
{error_description}

### Context
- Last successful task: {task_name}
- Failed at: {task_name}
- Error: {error_details}

### Recovery Steps
1. {step_1}
2. {step_2}
3. {step_3}
```

## Git Commit Template

```
feat({feature_name}): complete feature implementation

Implements:
- FR-1: {summary}
- FR-2: {summary}
- FR-N: {summary}

Following architecture decisions:
- AD-1: {summary}
- AD-2: {summary}

Tasks completed: {count}
Test coverage: {percentage}%
Code review: PASSED
```

## Task Queue Template

```python
tasks = []

# In-progress first (resume)
for task in glob("{FEATURE_DIR}/in-progress/TASK-*.md"):
    tasks.append({
        'path': task,
        'status': 'resuming',
        'priority': 1
    })

# Then todo (sorted)
for task in sorted(glob("{FEATURE_DIR}/todo/TASK-*.md")):
    tasks.append({
        'path': task,
        'status': 'new',
        'priority': 2
    })
```

## Issue Fix Template

```python
def fix_issue(issue):
    """Fix review issue based on category."""

    fixes = {
        "style": lambda: run_formatters(),
        "unused_import": lambda: remove_line(issue.file, issue.line),
        "missing_docstring": lambda: add_docstring(issue.target),
        "missing_type_hint": lambda: add_type_hint(issue.target),
        "missing_test": lambda: generate_test(issue.target),
        "security": lambda: manual_fix(issue),
        "logic": lambda: manual_fix(issue)
    }

    fix_fn = fixes.get(issue.category)
    if fix_fn:
        fix_fn()
```
