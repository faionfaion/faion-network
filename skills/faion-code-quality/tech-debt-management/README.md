---
id: tech-debt-management
name: "Technical Debt Management"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Technical Debt Management

## Overview

Strategic approaches for prioritizing, paying off, and preventing technical debt accumulation. This methodology focuses on execution strategies rather than debt identification.

## When to Use

- Prioritizing debt payoff in sprint planning
- Choosing debt reduction strategies
- Setting up debt prevention automation
- Planning refactoring initiatives

## Key Principles

- **Strategic prioritization**: Fix high-impact debt first
- **Continuous payoff**: Small regular payments better than big bang
- **Prevention first**: Automated quality gates prevent accumulation
- **Boy Scout Rule**: Leave code better than you found it

## Best Practices

### Prioritizing Debt Payoff

```markdown
## Debt Prioritization Matrix

### Factors to Consider
1. **Impact on Velocity**: How much does it slow development?
2. **Risk**: What's the probability and impact of failure?
3. **Interest Rate**: How much ongoing cost does it incur?
4. **Fix Cost**: How long to pay off?
5. **Dependencies**: Does other work depend on this fix?

### Priority Calculation
Priority Score = (Impact × Risk × Interest) / Fix Cost

### Example Scoring

| Item | Impact | Risk | Interest | Cost | Score | Priority |
|------|--------|------|----------|------|-------|----------|
| TD-001 | 5 | 4 | 4 | 60h | 1.33 | Medium |
| TD-002 | 5 | 5 | 5 | 40h | 3.13 | High |
| TD-003 | 3 | 3 | 3 | 24h | 1.13 | Medium |
| TD-004 | 2 | 1 | 2 | 80h | 0.05 | Low |

### When to Pay Off Debt

**Pay Now (High Priority)**
- Security vulnerabilities
- Data integrity risks
- Blocking other development
- High ongoing maintenance cost

**Pay Soon (Medium Priority)**
- Slowing feature development
- Causing frequent bugs
- Complexity spreading

**Pay Later (Low Priority)**
- Cosmetic issues
- Low-traffic areas
- Stable legacy code
```

### Strategies for Paying Down Debt

```python
# Strategy 1: Boy Scout Rule - Leave code better than you found it

# Before (encountered during feature work)
def process_data(d):
    r = []
    for x in d:
        if x > 0:
            r.append(x * 2)
    return r

# After (small improvement while working on related code)
def process_data(data: list[int]) -> list[int]:
    """Double positive numbers in the input list."""
    return [x * 2 for x in data if x > 0]


# Strategy 2: Dedicated Debt Sprints

"""
## Sprint Allocation Strategies

### Continuous (Recommended)
- 20% of each sprint for debt
- Every sprint has some debt work
- Debt never builds up too much

### Periodic
- Every 4th sprint is "tech debt sprint"
- Good for larger refactoring
- Risk: debt builds between sprints

### Triggered
- Debt sprint when threshold exceeded
- Reactive rather than proactive
- Can lead to crisis mode

### Hybrid
- 15% continuous + quarterly debt sprint
- Best of both approaches
- Handles both small and large debt
"""


# Strategy 3: Feature-Attached Debt Payoff

"""
## Attach Debt to Features

When planning a feature that touches debt-ridden code:

1. Identify debt in affected area
2. Include debt payoff in feature estimate
3. Pay debt as part of feature work
4. Prevents adding debt on top of debt

Example:
- Feature: Add subscription tiers
- Affected code: User billing module (has TD-003)
- Approach: Fix TD-003 first, then build feature
- Benefit: Clean foundation for new feature
"""


# Strategy 4: Strangler Fig Pattern for Large Debt

class LegacyOrderProcessor:
    """Old, debt-ridden implementation."""
    def process(self, order):
        # Complex, hard to maintain code
        pass

class ModernOrderProcessor:
    """New, clean implementation."""
    def process(self, order: Order) -> ProcessingResult:
        # Clean, well-tested code
        pass

class OrderProcessorFacade:
    """Gradually migrate from legacy to modern."""

    def __init__(self):
        self.legacy = LegacyOrderProcessor()
        self.modern = ModernOrderProcessor()

    def process(self, order):
        # Route to appropriate implementation based on feature flags
        if self._should_use_modern(order):
            return self.modern.process(order)
        return self.legacy.process(order)

    def _should_use_modern(self, order) -> bool:
        # Gradually increase modern usage
        return (
            feature_flags.is_enabled("modern_orders") and
            order.type in ["standard", "premium"]  # Start with subset
        )
```

### Preventing Debt Accumulation

```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check complexity
        run: |
          pip install radon
          radon cc src/ -a -nc  # Fail on complexity > 10

      - name: Check coverage
        run: |
          pytest --cov=src --cov-fail-under=80

      - name: Check duplication
        run: |
          pip install pylint
          pylint src/ --disable=all --enable=duplicate-code

      - name: Check dependencies
        run: |
          pip install safety
          safety check -r requirements.txt

      - name: Check TODO/FIXME count
        run: |
          count=$(grep -r "TODO\|FIXME\|HACK\|XXX" src/ | wc -l)
          if [ "$count" -gt 50 ]; then
            echo "Too many TODOs: $count"
            exit 1
          fi
```

```python
# Pre-commit hooks for debt prevention
# .pre-commit-config.yaml

repos:
  - repo: local
    hooks:
      - id: check-complexity
        name: Check cyclomatic complexity
        entry: python scripts/check_complexity.py
        language: python
        types: [python]

      - id: check-debt-comments
        name: Check debt comments have tickets
        entry: python scripts/check_debt_comments.py
        language: python
        types: [python]

# scripts/check_debt_comments.py
import re
import sys

DEBT_PATTERN = r'(TODO|FIXME|HACK|XXX|TECH_DEBT)'
TICKET_PATTERN = r'(TODO|FIXME|HACK|XXX|TECH_DEBT)\s*\([A-Z]+-\d+\)'

def check_file(filepath):
    with open(filepath) as f:
        content = f.read()

    debt_comments = re.findall(DEBT_PATTERN, content)
    ticketed_comments = re.findall(TICKET_PATTERN, content)

    if len(debt_comments) > len(ticketed_comments):
        print(f"{filepath}: Debt comments must include ticket reference")
        print("Example: TODO(PROJ-123): description")
        return False
    return True

if __name__ == "__main__":
    all_good = all(check_file(f) for f in sys.argv[1:])
    sys.exit(0 if all_good else 1)
```

## Sprint Allocation

### Recommended Approach: Continuous 20%

```markdown
## Weekly Sprint (40 hours)

### Feature Work (32 hours / 80%)
- New features
- User-facing improvements
- Business requirements

### Debt Work (8 hours / 20%)
- Refactoring
- Test improvements
- Documentation
- Dependency updates
- Small architectural improvements

### Benefits
- Prevents debt accumulation
- Sustainable pace
- Predictable capacity
- Continuous improvement
```

## Anti-patterns

- **Zero debt tolerance**: Over-engineering, slow delivery
- **Ignoring prevention**: Only paying off, never preventing
- **Analysis paralysis**: Spending too much time measuring
- **Hidden debt**: Not tracking or communicating debt
- **Blame-driven**: Punishing debt instead of managing it

## References

- [Ward Cunningham's Debt Metaphor](https://wiki.c2.com/?WardExplainsDebtMetaphor)
- [Managing Technical Debt Book](https://www.amazon.com/Managing-Technical-Debt-Reducing-Development/dp/0135645824)
- [Strangler Fig Pattern](https://martinfowler.com/bliki/StranglerFigApplication.html)
- [Boy Scout Rule](https://www.oreilly.com/library/view/97-things-every/9780596809515/ch08.html)

## Related

- [tech-debt-basics.md](tech-debt-basics.md) - Debt types, tracking, and metrics
- [refactoring-patterns.md](refactoring-patterns.md) - Refactoring techniques
- [code-review.md](code-review.md) - Review process for debt prevention
