# Execution Workflow Checklist

## Pre-Execution

- [ ] Feature located in .aidocs/{status}/{feature}
- [ ] constitution.md exists and readable
- [ ] spec.md exists in feature folder
- [ ] design.md exists in feature folder
- [ ] implementation-plan.md exists in feature folder
- [ ] All task files are valid markdown
- [ ] No circular dependencies detected
- [ ] Test framework identified from constitution
- [ ] Build commands identified from constitution

## Context Loading

- [ ] Tech stack extracted from constitution
- [ ] Code standards loaded (linters, formatters)
- [ ] Testing requirements loaded (framework, coverage threshold)
- [ ] Build commands loaded
- [ ] Git conventions loaded
- [ ] All FR requirements extracted from spec.md
- [ ] All AD architecture decisions extracted from design.md
- [ ] CREATE/MODIFY file lists extracted
- [ ] Task dependencies mapped
- [ ] Context package built for task executor

## Task Discovery

- [ ] In-progress tasks found and queued first
- [ ] Todo tasks found and sorted by number
- [ ] Execution queue built
- [ ] Task count verified (not empty)

## Task Execution Loop

For EACH task:

- [ ] Task moved from todo to in-progress (if applicable)
- [ ] Task executed via faion-task-executor-agent
- [ ] Tests run successfully
- [ ] Coverage checked (meets threshold)
- [ ] Build verified (compiles/runs)
- [ ] Project runs without errors
- [ ] Task moved to done folder

## Post-Task Validation

For EACH task:

- [ ] All tests pass
- [ ] No new test failures
- [ ] Coverage >= threshold (default 80%)
- [ ] Build succeeds
- [ ] Project runs
- [ ] Hallucination check passed
- [ ] Task marked SUCCESS

## Code Review Cycle

- [ ] Code review initiated via faion-code-agent
- [ ] Review issues parsed and categorized
- [ ] Style/format issues auto-fixed
- [ ] Unused imports removed
- [ ] Missing docstrings added
- [ ] Type hints added where missing
- [ ] Security issues manually fixed
- [ ] Logic errors manually fixed
- [ ] Missing tests generated
- [ ] Tests re-run after fixes
- [ ] Review iteration completed
- [ ] Max 5 iterations not exceeded
- [ ] Final review status: CLEAN

## Finalization

- [ ] All tasks moved to {FEATURE_DIR}/done/
- [ ] No tasks remain in in-progress or todo
- [ ] Feature folder moved to .aidocs/done/{feature}
- [ ] Git commit created with feature summary
- [ ] Commit message includes FR and AD summaries
- [ ] Summary report generated
- [ ] Test coverage reported
- [ ] Code review status: PASSED

## Error Recovery

If failures occur:

- [ ] Error type identified (test/build/lint)
- [ ] Auto-fix attempted (formatters, etc.)
- [ ] Retry attempted (max 3 times)
- [ ] If max retries exceeded, task marked FAILED
- [ ] Blocked tasks identified and reported
- [ ] Recovery steps documented

## Quality Gates

- [ ] No critical issues
- [ ] No security issues
- [ ] All tests pass
- [ ] Coverage meets threshold
- [ ] Build succeeds
- [ ] No style violations
- [ ] All changes documented
- [ ] Feature ready for deployment
