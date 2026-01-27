# Quality Gates & Confidence Checks

> **Entry point:** `/faion-net` - invoke for automatic routing.

Quality gates are systematic checkpoints ensuring LLM-generated code and documentation meet defined standards before proceeding to the next phase.

## Overview

| Aspect | Description |
|--------|-------------|
| **Purpose** | Prevent defects from propagating through development phases |
| **Principle** | "Shift left" - catch issues early, fix cheaply |
| **Automation** | Maximize automated checks, minimize manual review |
| **LLM Context** | Validate AI outputs before integration |

---

## Quality Gate Levels (L1-L6)

### L1: Syntax & Format

**What:** Basic structural validity
**When:** Immediately after generation
**Automated:** 100%

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Code parses | Compiler/Interpreter | No syntax errors |
| Linter passes | ESLint/Pylint/etc. | Zero errors (warnings OK) |
| Format valid | Prettier/Black | Auto-formatted |
| Types valid | TypeScript/mypy | No type errors |

**Confidence Required:** 95%+

---

### L2: Unit Tests

**What:** Individual component correctness
**When:** After L1 passes
**Automated:** 100%

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Tests execute | Jest/Pytest | All tests run |
| Tests pass | Test runner | 100% pass rate |
| Coverage met | Istanbul/Coverage.py | >= project minimum (typically 80%) |
| Edge cases | Custom tests | Boundary conditions covered |

**Confidence Required:** 90%+

---

### L3: Integration Tests

**What:** Component interaction correctness
**When:** After L2 passes
**Automated:** 95%

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| API contracts | Supertest/httpx | Endpoints match spec |
| DB operations | Test DB | CRUD operations work |
| External services | Mocks/Stubs | Integrations behave correctly |
| Data flow | E2E scenarios | Data propagates correctly |

**Confidence Required:** 85%+

---

### L4: Code Review

**What:** Human/AI review of code quality
**When:** After L3 passes
**Automated:** 50% (AI-assisted)

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Logic correctness | Review | Algorithm implements spec |
| Security | SAST tools + review | No vulnerabilities |
| Performance | Profiling | Meets NFRs |
| Maintainability | Review | Code is readable, documented |
| Patterns | Review | Follows project conventions |

**Confidence Required:** 80%+

---

### L5: Staging Validation

**What:** Production-like environment testing
**When:** After L4 passes
**Automated:** 70%

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Deployment | CI/CD pipeline | Deploys without errors |
| Smoke tests | Automated suite | Core flows work |
| Load testing | k6/Locust | Meets performance SLOs |
| Security scan | DAST tools | No critical vulnerabilities |
| Manual QA | Human testing | UX acceptable |

**Confidence Required:** 85%+

---

### L6: Production Gate

**What:** Final pre-production verification
**When:** Before production deployment
**Automated:** 60%

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Change approval | CAB/Review board | Approved |
| Rollback plan | Documentation | Plan exists and tested |
| Monitoring ready | Alerts configured | Dashboards/alerts active |
| Feature flags | Toggle system | Can disable if needed |
| Stakeholder sign-off | Approval | Business owner approved |

**Confidence Required:** 90%+

---

## Confidence Checks

### What is Confidence?

Confidence is a quantitative measure of readiness to proceed. It combines:

1. **Automated check results** (objective)
2. **Coverage completeness** (objective)
3. **Risk assessment** (subjective)
4. **Requirement traceability** (objective)

### Confidence Score Calculation

```
Confidence = (Automated_Pass * 0.4) + (Coverage * 0.2) +
             (Risk_Mitigation * 0.2) + (Traceability * 0.2)
```

| Factor | Weight | Measurement |
|--------|--------|-------------|
| Automated_Pass | 40% | % of automated checks passing |
| Coverage | 20% | % of requirements covered by tests |
| Risk_Mitigation | 20% | % of identified risks with mitigations |
| Traceability | 20% | % of requirements traceable to implementation |

### Confidence Thresholds

| Gate | Minimum | Recommended | Action if Below |
|------|---------|-------------|-----------------|
| L1 | 95% | 99% | Block - fix immediately |
| L2 | 90% | 95% | Block - add tests |
| L3 | 85% | 90% | Block - fix integrations |
| L4 | 80% | 85% | Review - conditional proceed |
| L5 | 85% | 90% | Block - fix staging issues |
| L6 | 90% | 95% | Block - no production without confidence |

### Pre-Phase Confidence Check

Before starting any phase:

```markdown
## Confidence Check: [Phase Name]

### Prerequisites Met
- [ ] Previous gate passed
- [ ] Required artifacts exist
- [ ] Dependencies available
- [ ] Context understood

### Current Confidence: X%

### Proceed?
- [ ] YES (>= threshold)
- [ ] NO (< threshold) - Reason: [...]
```

---

## Validating LLM Output

### The LLM Validation Pipeline

```
LLM Output → L1 Check → L2 Check → AI Review → Human Spot-Check → Merge
                ↓           ↓           ↓              ↓
              Fail?       Fail?     Issues?        Issues?
                ↓           ↓           ↓              ↓
            Re-prompt   Re-prompt   Fix/Re-prompt   Fix manually
```

### LLM-Specific Validation

| Concern | Check | Tool/Method |
|---------|-------|-------------|
| Hallucinated APIs | Static analysis | Verify imports exist |
| Outdated patterns | Pattern matching | Check against current docs |
| Security anti-patterns | SAST | Snyk/Semgrep/Bandit |
| Logic errors | Unit tests | TDD-generated tests |
| Inconsistent style | Linter | Project config |
| Missing error handling | Coverage | Exception path coverage |

### LLM-as-Judge Pattern

Use a secondary LLM to evaluate primary LLM output:

```
Primary LLM → Code → Evaluator LLM → Score + Issues → Threshold Check
```

**Evaluator Criteria:**
- Correctness (does it solve the problem?)
- Completeness (are all requirements addressed?)
- Quality (is the code clean and maintainable?)
- Security (are there obvious vulnerabilities?)

### Multi-Agent Validation

| Agent | Role | Focus |
|-------|------|-------|
| Analyst | Requirement verification | Does code match spec? |
| Coder | Implementation review | Is code correct? |
| Tester | Test coverage | Are tests sufficient? |
| Security | Security review | Any vulnerabilities? |

---

## CI/CD Integration

### Quality Gate Pipeline

```yaml
# .github/workflows/quality-gates.yml
stages:
  - L1_syntax:
      - lint
      - typecheck
      - format-check
  - L2_unit:
      - unit-tests
      - coverage-check
  - L3_integration:
      - integration-tests
      - api-contract-tests
  - L4_review:
      - ai-code-review
      - security-scan
  - L5_staging:
      - deploy-staging
      - smoke-tests
      - load-tests
```

### Gate Enforcement

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| Hard block | Pipeline fails, no proceed | L1, L2 gates |
| Soft block | Warning, require approval | L3, L4 gates |
| Advisory | Log issues, allow proceed | Non-critical checks |

---

## Best Practices

### For LLM-Assisted Development

1. **Incremental generation** - Generate small, testable chunks
2. **Test first** - Have tests before generating implementation
3. **Specification clarity** - Clear specs reduce hallucinations
4. **Pattern libraries** - Provide examples of correct patterns
5. **Immediate validation** - Check LLM output before integration

### For Quality Gates

1. **Automate everything possible** - Manual gates slow down delivery
2. **Fast feedback** - L1/L2 should complete in < 5 minutes
3. **Clear criteria** - No ambiguous pass/fail conditions
4. **Consistent enforcement** - No bypassing gates under pressure
5. **Continuous improvement** - Update gates based on escaped defects

### For Confidence Checks

1. **Objective over subjective** - Prefer measurable criteria
2. **Track trends** - Monitor confidence over time
3. **Calibrate thresholds** - Adjust based on project maturity
4. **Document assumptions** - Make confidence factors explicit

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [checklist.md](checklist.md) | Phase-specific quality gate checklists |
| [examples.md](examples.md) | Gate pass/fail examples with analysis |
| [templates.md](templates.md) | Gate templates and automation scripts |
| [llm-prompts.md](llm-prompts.md) | Prompts for quality validation |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-sdd-execution](../faion-sdd-execution/CLAUDE.md) | Uses quality gates during task execution |
| [faion-testing-developer](../../faion-testing-developer/CLAUDE.md) | Implements test gates |
| [faion-cicd-engineer](../../faion-cicd-engineer/CLAUDE.md) | Implements CI/CD gates |
| [faion-code-quality](../../faion-code-quality/CLAUDE.md) | Code review practices |

## External References

- [Addy Osmani - LLM Coding Workflow 2026](https://addyosmani.com/blog/ai-coding-workflow/)
- [SonarSource - LLM Code Generation Quality](https://www.sonarsource.com/resources/library/llm-code-generation/)
- [Confident AI - LLM Testing Methods](https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies)
- [Anthropic - Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

---

*Quality Gates & Confidence Checks | SDD Execution | Version 2.0*
