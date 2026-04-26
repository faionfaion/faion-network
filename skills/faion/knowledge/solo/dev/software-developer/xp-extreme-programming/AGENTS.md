# Extreme Programming (XP)

## Summary

An agile methodology built on 12 engineering practices taken to their logical extreme: TDD (test everything), continuous integration (integrate many times daily), pair programming (review all code), simple design (fewest elements that pass), and collective ownership (anyone changes anything). For solo + AI dev, Claude acts as the pair partner and TDD is non-negotiable.

## Why

Teams adopting Scrum without engineering practices get process overhead without quality payoff. XP's practices are mutually reinforcing: TDD makes refactoring safe; refactoring keeps simple design; simple design enables collective ownership; collective ownership requires coding standards; standards are enforced by pre-commit and CI. Kent Beck's four rules of simple design are the concrete, testable definition of "clean code".

## When To Use

- Small teams (2-12) with rapidly changing requirements and direct customer access.
- Greenfield projects where TDD, CI, and pair programming can be established from day one.
- Recovering a brownfield codebase where quality has rotted — XP's practices are a culture reset.
- Solo + AI dev: most XP practices map cleanly onto a human-in-loop with Claude as the pair.
- Teams adopting agile but failing on engineering excellence (Scrum-without-XP).

## When NOT To Use

- Compliance-heavy / regulated work where every change needs upfront sign-off — "embrace change" clashes.
- Distributed teams with poor async culture and no shared timezone — pair programming falls apart.
- Outsourced arrangements where the customer is unreachable.
- Hardware / firmware where test-refactor cycle is dominated by hardware-in-loop.
- Research / exploratory ML where most code is thrown away — TDD overhead exceeds value.

## Content

| File | What's inside |
|------|---------------|
| `content/01-practices.xml` | 12 XP practices with descriptions, solo-dev applicability, and Kent Beck's four simple-design rules. |
| `content/02-tdd-workflow.xml` | Red-green-refactor loop, commit discipline, test-suite speed rules, mutation testing. |
| `content/03-antipatterns.xml` | Production code before tests, speculative generality, hero culture, no customer access, sustainable pace violation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pre-commit-xp.yaml` | pre-commit config enforcing ruff + pytest fast suite + no test skips. |

## Scripts

(none)
