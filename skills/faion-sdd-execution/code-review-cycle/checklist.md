# Code Review Cycle Checklist

## Pre-Review (Author)

### Code Quality
- [ ] Code follows project style guide
- [ ] No commented-out code or debug statements
- [ ] Error handling appropriate
- [ ] No hardcoded values (use constants/config)

### Functionality
- [ ] All acceptance criteria met
- [ ] Edge cases handled
- [ ] Changes work locally
- [ ] No regression in existing functionality

### Testing
- [ ] Unit tests cover new code
- [ ] Tests are meaningful, not just coverage
- [ ] All tests pass locally
- [ ] Integration tests updated if needed

### Documentation
- [ ] Code is self-documenting with clear names
- [ ] Complex logic has comments
- [ ] API docs updated if needed
- [ ] README updated if setup changed

### SDD Compliance
- [ ] Implementation matches design document
- [ ] Deviations documented and justified
- [ ] Traceability links correct

## During Review (Reviewer)

### Correctness
- [ ] Solves the stated problem
- [ ] Handles edge cases
- [ ] No obvious bugs
- [ ] Error handling appropriate

### Design
- [ ] Follows project patterns
- [ ] Appropriate abstraction level
- [ ] No unnecessary complexity
- [ ] Consistent with architecture

### Code Quality
- [ ] Clear naming
- [ ] Well-organized
- [ ] No code smells
- [ ] DRY (Don't Repeat Yourself)

### Testing
- [ ] Adequate test coverage
- [ ] Tests are meaningful
- [ ] Edge cases tested

### Security
- [ ] Input validation
- [ ] No hardcoded secrets
- [ ] Auth/authz correct

### Documentation
- [ ] Code is self-documenting
- [ ] Complex logic commented
- [ ] API docs updated

### SDD Compliance
- [ ] Matches design document
- [ ] Deviations justified
- [ ] Acceptance criteria met

## Post-Review

### Immediate
- [ ] Verify CI/CD success
- [ ] Check deployment health
- [ ] Update task status to "done"

### Documentation
- [ ] Update changelog (if user-facing)
- [ ] Update API docs (if API changed)
- [ ] Note lessons learned (if applicable)

### Reflexion
- [ ] Identify patterns - What worked well?
- [ ] Identify improvements - What could be better?
- [ ] Update memory (patterns_learned.jsonl)

## Verdict
- [ ] Approved
- [ ] Approved with suggestions
- [ ] Request changes
