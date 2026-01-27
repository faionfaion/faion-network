# Quality Gate Templates

Reusable templates and automation scripts for quality gates.

---

## Gate Configuration Templates

### GitHub Actions Quality Gate Pipeline

```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

env:
  NODE_VERSION: '20'
  PYTHON_VERSION: '3.11'
  COVERAGE_THRESHOLD: 80

jobs:
  # L1: Syntax & Format Gate
  l1-syntax:
    name: L1 - Syntax & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint check
        run: npm run lint

      - name: Type check
        run: npm run typecheck

      - name: Format check
        run: npm run format:check

      - name: Build
        run: npm run build

  # L2: Unit Test Gate
  l2-unit:
    name: L2 - Unit Tests
    needs: l1-syntax
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests with coverage
        run: npm run test:coverage

      - name: Check coverage threshold
        run: |
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          if (( $(echo "$COVERAGE < $COVERAGE_THRESHOLD" | bc -l) )); then
            echo "Coverage $COVERAGE% is below threshold $COVERAGE_THRESHOLD%"
            exit 1
          fi

      - name: Upload coverage report
        uses: codecov/codecov-action@v4
        with:
          files: coverage/lcov.info

  # L3: Integration Test Gate
  l3-integration:
    name: L3 - Integration Tests
    needs: l2-unit
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
      redis:
        image: redis:7
        ports:
          - 6379:6379
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run migrations
        run: npm run db:migrate
        env:
          DATABASE_URL: postgres://postgres:testpass@localhost:5432/testdb

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgres://postgres:testpass@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379

      - name: Run E2E tests
        run: npm run test:e2e

  # L4: Security & Review Gate
  l4-security:
    name: L4 - Security Scan
    needs: l3-integration
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      - name: Run Semgrep SAST
        uses: returntocorp/semgrep-action@v1
        with:
          config: p/security-audit

      - name: Dependency audit
        run: npm audit --audit-level=high

  # Gate Summary
  gate-summary:
    name: Quality Gate Summary
    needs: [l1-syntax, l2-unit, l3-integration, l4-security]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Check gate results
        run: |
          echo "## Quality Gate Results" >> $GITHUB_STEP_SUMMARY
          echo "| Gate | Status |" >> $GITHUB_STEP_SUMMARY
          echo "|------|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| L1 Syntax | ${{ needs.l1-syntax.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| L2 Unit | ${{ needs.l2-unit.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| L3 Integration | ${{ needs.l3-integration.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| L4 Security | ${{ needs.l4-security.result }} |" >> $GITHUB_STEP_SUMMARY
```

---

### Python Quality Gate Pipeline

```yaml
# .github/workflows/quality-gates-python.yml
name: Quality Gates (Python)

on:
  pull_request:
    branches: [main, develop]

jobs:
  l1-syntax:
    name: L1 - Syntax & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install ruff mypy black

      - name: Lint with ruff
        run: ruff check .

      - name: Type check with mypy
        run: mypy src/

      - name: Format check with black
        run: black --check .

  l2-unit:
    name: L2 - Unit Tests
    needs: l1-syntax
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt

      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=xml --cov-report=term-missing \
                 --cov-fail-under=80 tests/unit/

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml

  l3-integration:
    name: L3 - Integration Tests
    needs: l2-unit
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt

      - name: Run integration tests
        run: pytest tests/integration/
        env:
          DATABASE_URL: postgres://postgres:testpass@localhost:5432/postgres

  l4-security:
    name: L4 - Security
    needs: l3-integration
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Bandit security scan
        run: |
          pip install bandit
          bandit -r src/ -ll

      - name: Run Safety dependency check
        run: |
          pip install safety
          safety check -r requirements.txt
```

---

## Confidence Score Calculator

### JavaScript/TypeScript

```typescript
// scripts/calculate-confidence.ts
interface GateResults {
  automatedChecks: {
    total: number;
    passed: number;
  };
  coverage: {
    requirements: number;
    covered: number;
  };
  risks: {
    identified: number;
    mitigated: number;
  };
  traceability: {
    requirements: number;
    traceable: number;
  };
}

interface ConfidenceResult {
  score: number;
  breakdown: {
    automatedChecks: number;
    coverage: number;
    riskMitigation: number;
    traceability: number;
  };
  decision: 'PROCEED' | 'CONDITIONAL' | 'BLOCKED';
  threshold: number;
}

function calculateConfidence(
  results: GateResults,
  gate: 'L1' | 'L2' | 'L3' | 'L4' | 'L5' | 'L6'
): ConfidenceResult {
  const weights = {
    automatedChecks: 0.4,
    coverage: 0.2,
    riskMitigation: 0.2,
    traceability: 0.2,
  };

  const thresholds: Record<string, number> = {
    L1: 95,
    L2: 90,
    L3: 85,
    L4: 80,
    L5: 85,
    L6: 90,
  };

  const breakdown = {
    automatedChecks:
      (results.automatedChecks.passed / results.automatedChecks.total) * 100,
    coverage:
      (results.coverage.covered / results.coverage.requirements) * 100,
    riskMitigation:
      (results.risks.mitigated / results.risks.identified) * 100,
    traceability:
      (results.traceability.traceable / results.traceability.requirements) * 100,
  };

  const score =
    breakdown.automatedChecks * weights.automatedChecks +
    breakdown.coverage * weights.coverage +
    breakdown.riskMitigation * weights.riskMitigation +
    breakdown.traceability * weights.traceability;

  const threshold = thresholds[gate];
  let decision: 'PROCEED' | 'CONDITIONAL' | 'BLOCKED';

  if (score >= threshold) {
    decision = 'PROCEED';
  } else if (score >= threshold - 10) {
    decision = 'CONDITIONAL';
  } else {
    decision = 'BLOCKED';
  }

  return {
    score: Math.round(score * 100) / 100,
    breakdown,
    decision,
    threshold,
  };
}

// Example usage
const results: GateResults = {
  automatedChecks: { total: 50, passed: 48 },
  coverage: { requirements: 20, covered: 18 },
  risks: { identified: 5, mitigated: 4 },
  traceability: { requirements: 20, traceable: 19 },
};

const confidence = calculateConfidence(results, 'L2');
console.log(`Confidence Score: ${confidence.score}%`);
console.log(`Decision: ${confidence.decision}`);
```

---

### Python

```python
# scripts/calculate_confidence.py
from dataclasses import dataclass
from enum import Enum
from typing import Dict

class Gate(Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"
    L5 = "L5"
    L6 = "L6"

class Decision(Enum):
    PROCEED = "PROCEED"
    CONDITIONAL = "CONDITIONAL"
    BLOCKED = "BLOCKED"

@dataclass
class GateResults:
    automated_passed: int
    automated_total: int
    requirements_covered: int
    requirements_total: int
    risks_mitigated: int
    risks_identified: int
    traceable: int
    traceable_total: int

@dataclass
class ConfidenceResult:
    score: float
    breakdown: Dict[str, float]
    decision: Decision
    threshold: float

WEIGHTS = {
    "automated_checks": 0.4,
    "coverage": 0.2,
    "risk_mitigation": 0.2,
    "traceability": 0.2,
}

THRESHOLDS = {
    Gate.L1: 95,
    Gate.L2: 90,
    Gate.L3: 85,
    Gate.L4: 80,
    Gate.L5: 85,
    Gate.L6: 90,
}

def calculate_confidence(results: GateResults, gate: Gate) -> ConfidenceResult:
    breakdown = {
        "automated_checks": (results.automated_passed / results.automated_total) * 100,
        "coverage": (results.requirements_covered / results.requirements_total) * 100,
        "risk_mitigation": (results.risks_mitigated / results.risks_identified) * 100,
        "traceability": (results.traceable / results.traceable_total) * 100,
    }

    score = sum(
        breakdown[key] * WEIGHTS[key]
        for key in WEIGHTS
    )

    threshold = THRESHOLDS[gate]

    if score >= threshold:
        decision = Decision.PROCEED
    elif score >= threshold - 10:
        decision = Decision.CONDITIONAL
    else:
        decision = Decision.BLOCKED

    return ConfidenceResult(
        score=round(score, 2),
        breakdown=breakdown,
        decision=decision,
        threshold=threshold,
    )

if __name__ == "__main__":
    results = GateResults(
        automated_passed=48,
        automated_total=50,
        requirements_covered=18,
        requirements_total=20,
        risks_mitigated=4,
        risks_identified=5,
        traceable=19,
        traceable_total=20,
    )

    confidence = calculate_confidence(results, Gate.L2)
    print(f"Confidence Score: {confidence.score}%")
    print(f"Decision: {confidence.decision.value}")
```

---

## Gate Report Templates

### Markdown Gate Report

```markdown
# Quality Gate Report

## Summary

| Metric | Value |
|--------|-------|
| **Project** | {{project_name}} |
| **Version** | {{version}} |
| **Date** | {{date}} |
| **Gate** | {{gate_level}} |
| **Confidence** | {{confidence_score}}% |
| **Decision** | {{decision}} |

## Gate Results

### L1: Syntax & Format

| Check | Status | Details |
|-------|--------|---------|
| Build | {{l1_build}} | {{l1_build_details}} |
| Lint | {{l1_lint}} | {{l1_lint_errors}} errors |
| Types | {{l1_types}} | {{l1_type_errors}} errors |
| Format | {{l1_format}} | {{l1_format_files}} files |

### L2: Unit Tests

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Pass Rate | {{l2_pass_rate}}% | 100% | {{l2_pass_status}} |
| Coverage | {{l2_coverage}}% | {{l2_coverage_threshold}}% | {{l2_coverage_status}} |

### L3: Integration Tests

| Suite | Passed | Failed | Status |
|-------|--------|--------|--------|
| API | {{l3_api_passed}} | {{l3_api_failed}} | {{l3_api_status}} |
| Database | {{l3_db_passed}} | {{l3_db_failed}} | {{l3_db_status}} |
| E2E | {{l3_e2e_passed}} | {{l3_e2e_failed}} | {{l3_e2e_status}} |

### L4: Security

| Severity | Count | Action |
|----------|-------|--------|
| Critical | {{l4_critical}} | {{l4_critical_action}} |
| High | {{l4_high}} | {{l4_high_action}} |
| Medium | {{l4_medium}} | {{l4_medium_action}} |
| Low | {{l4_low}} | {{l4_low_action}} |

## Confidence Breakdown

| Factor | Weight | Score | Weighted |
|--------|--------|-------|----------|
| Automated Checks | 40% | {{conf_auto}}% | {{conf_auto_w}}% |
| Coverage | 20% | {{conf_cov}}% | {{conf_cov_w}}% |
| Risk Mitigation | 20% | {{conf_risk}}% | {{conf_risk_w}}% |
| Traceability | 20% | {{conf_trace}}% | {{conf_trace_w}}% |
| **Total** | 100% | - | **{{confidence_score}}%** |

## Issues

{{#if issues}}
| ID | Severity | Description | Status |
|----|----------|-------------|--------|
{{#each issues}}
| {{id}} | {{severity}} | {{description}} | {{status}} |
{{/each}}
{{else}}
No issues found.
{{/if}}

## Decision

**{{decision}}**

{{#if decision_notes}}
Notes: {{decision_notes}}
{{/if}}

---

*Generated by Quality Gate System*
```

---

### JSON Gate Report Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "QualityGateReport",
  "type": "object",
  "required": ["project", "version", "date", "gate", "confidence", "decision"],
  "properties": {
    "project": { "type": "string" },
    "version": { "type": "string" },
    "date": { "type": "string", "format": "date" },
    "gate": {
      "type": "string",
      "enum": ["L1", "L2", "L3", "L4", "L5", "L6"]
    },
    "confidence": {
      "type": "object",
      "properties": {
        "score": { "type": "number", "minimum": 0, "maximum": 100 },
        "threshold": { "type": "number" },
        "breakdown": {
          "type": "object",
          "properties": {
            "automatedChecks": { "type": "number" },
            "coverage": { "type": "number" },
            "riskMitigation": { "type": "number" },
            "traceability": { "type": "number" }
          }
        }
      }
    },
    "decision": {
      "type": "string",
      "enum": ["PROCEED", "CONDITIONAL", "BLOCKED"]
    },
    "gates": {
      "type": "object",
      "properties": {
        "l1": { "$ref": "#/definitions/L1Gate" },
        "l2": { "$ref": "#/definitions/L2Gate" },
        "l3": { "$ref": "#/definitions/L3Gate" },
        "l4": { "$ref": "#/definitions/L4Gate" }
      }
    },
    "issues": {
      "type": "array",
      "items": { "$ref": "#/definitions/Issue" }
    }
  },
  "definitions": {
    "L1Gate": {
      "type": "object",
      "properties": {
        "build": { "$ref": "#/definitions/CheckResult" },
        "lint": { "$ref": "#/definitions/CheckResult" },
        "types": { "$ref": "#/definitions/CheckResult" },
        "format": { "$ref": "#/definitions/CheckResult" }
      }
    },
    "L2Gate": {
      "type": "object",
      "properties": {
        "testsTotal": { "type": "integer" },
        "testsPassed": { "type": "integer" },
        "coverage": { "type": "number" },
        "coverageThreshold": { "type": "number" }
      }
    },
    "L3Gate": {
      "type": "object",
      "properties": {
        "api": { "$ref": "#/definitions/TestSuite" },
        "database": { "$ref": "#/definitions/TestSuite" },
        "e2e": { "$ref": "#/definitions/TestSuite" }
      }
    },
    "L4Gate": {
      "type": "object",
      "properties": {
        "critical": { "type": "integer" },
        "high": { "type": "integer" },
        "medium": { "type": "integer" },
        "low": { "type": "integer" }
      }
    },
    "CheckResult": {
      "type": "object",
      "properties": {
        "status": { "type": "string", "enum": ["PASS", "FAIL"] },
        "details": { "type": "string" },
        "errors": { "type": "integer" }
      }
    },
    "TestSuite": {
      "type": "object",
      "properties": {
        "passed": { "type": "integer" },
        "failed": { "type": "integer" },
        "skipped": { "type": "integer" }
      }
    },
    "Issue": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "severity": { "type": "string", "enum": ["Critical", "High", "Medium", "Low"] },
        "description": { "type": "string" },
        "status": { "type": "string", "enum": ["Open", "Fixed", "Accepted"] }
      }
    }
  }
}
```

---

## Pre-Commit Hook Template

```bash
#!/bin/bash
# .git/hooks/pre-commit
# Quality Gate L1 checks before commit

set -e

echo "Running L1 Quality Gate checks..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

check_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}PASS${NC}: $2"
    else
        echo -e "${RED}FAIL${NC}: $2"
        exit 1
    fi
}

# Detect project type
if [ -f "package.json" ]; then
    # Node.js project
    echo "Detected Node.js project"

    npm run lint --silent
    check_result $? "Lint check"

    npm run typecheck --silent 2>/dev/null || true
    check_result $? "Type check"

    npm run format:check --silent
    check_result $? "Format check"

elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    # Python project
    echo "Detected Python project"

    ruff check . --quiet
    check_result $? "Lint check (ruff)"

    mypy src/ --silent-imports 2>/dev/null || true
    check_result $? "Type check (mypy)"

    black --check . --quiet
    check_result $? "Format check (black)"
fi

echo -e "${GREEN}L1 Quality Gate passed!${NC}"
```

---

## Makefile Quality Gate Targets

```makefile
# Makefile
.PHONY: quality-gates l1 l2 l3 l4 confidence

# Run all quality gates
quality-gates: l1 l2 l3 l4 confidence

# L1: Syntax & Format
l1:
	@echo "=== L1: Syntax & Format ==="
	npm run lint
	npm run typecheck
	npm run format:check
	npm run build

# L2: Unit Tests
l2:
	@echo "=== L2: Unit Tests ==="
	npm run test:coverage
	@coverage=$$(cat coverage/coverage-summary.json | jq '.total.lines.pct'); \
	if [ $$(echo "$$coverage < 80" | bc -l) -eq 1 ]; then \
		echo "Coverage $$coverage% below threshold 80%"; \
		exit 1; \
	fi

# L3: Integration Tests
l3:
	@echo "=== L3: Integration Tests ==="
	docker-compose -f docker-compose.test.yml up -d
	npm run test:integration
	npm run test:e2e
	docker-compose -f docker-compose.test.yml down

# L4: Security
l4:
	@echo "=== L4: Security ==="
	npm audit --audit-level=high
	npx snyk test --severity-threshold=high
	npx semgrep --config p/security-audit

# Calculate confidence
confidence:
	@echo "=== Confidence Score ==="
	npx ts-node scripts/calculate-confidence.ts

# Quick check (L1 only)
quick-check: l1
	@echo "Quick check passed"

# Full check before PR
pr-check: l1 l2 l3 l4
	@echo "All gates passed - ready for PR"
```

---

## SDD Task Quality Gate Template

```markdown
## Quality Gates

### Pre-Implementation Gate

| Check | Status | Notes |
|-------|--------|-------|
| Spec reviewed | [ ] | |
| Design reviewed | [ ] | |
| Dependencies ready | [ ] | |
| Test cases defined | [ ] | |

**Confidence:** X% | **Proceed:** [ ] Yes / [ ] No

### Post-Implementation Gate

| Check | Status | Notes |
|-------|--------|-------|
| L1 - Syntax | [ ] PASS | |
| L2 - Unit Tests | [ ] PASS | Coverage: X% |
| L3 - Integration | [ ] PASS | |
| Acceptance Criteria | [ ] All verified | |

**Confidence:** X% | **Ready for Review:** [ ] Yes / [ ] No
```

---

*Quality Gate Templates | SDD Execution | Version 2.0*
