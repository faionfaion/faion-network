# Behavioral Design Patterns

## Summary

Nine GoF behavioral patterns (Strategy, Observer, Command, State, Chain of Responsibility, Template Method, Mediator, Iterator, Visitor) for controlling how objects communicate and distribute responsibilities at runtime. Apply them when measured code smells — cyclomatic complexity &gt;15, repeated switch-on-type, growing if-state chains — justify the abstraction cost. Start with the simplest representation (function, lookup table); promote to a class-based pattern only when type signatures or shared state demand it.

## Why

Behavioral patterns solve a specific class of design problem: behavior that varies at runtime (Strategy, State), fan-out notification (Observer), operation history (Command), or extensible processing pipelines (Chain of Responsibility). Applying them off metrics (complexity, duplication, change frequency) prevents over-abstraction; applying them off aesthetics produces one-impl interfaces that add ceremony without extensibility.

## When To Use

- Code review: long switch/match on type, duplicated event-listener boilerplate, or growing if/else state machines.
- New feature: multiple algorithms selectable at runtime (Strategy), domain events fan-out to N consumers (Observer), explicit state machine with guards (State).
- Refactoring a monolithic class into smaller testable pieces by externalizing variable behavior.
- Building extensible middleware/handler chains (Chain of Responsibility): request validation, auth pipelines, log enrichers.

## When NOT To Use

- Two-line if/else with one likely future variant — pattern overhead outweighs benefit; revisit at third variant.
- Pure data-transformation pipelines mapping cleanly to functions or streams — patterns add ceremony.
- Languages with first-class FP idioms (Rust, Haskell, modern TS) — many GoF behavioral patterns reduce to higher-order functions.

## Content

| File | What's inside |
|------|---------------|
| `content/01-strategy-observer-command.xml` | Strategy, Observer, Command patterns: when-to/when-NOT, modern trends, selection rules. |
| `content/02-state-cor-template-mediator.xml` | State, Chain of Responsibility, Template Method, Mediator patterns: when-to/when-NOT, modern trends. |
| `content/03-iterator-visitor-selection.xml` | Iterator, Visitor patterns, pattern relationships, selection matrix, antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/strategy-py.py` | Strategy pattern in Python using Protocol for duck typing. |
| `templates/observer-py.py` | Observer/EventEmitter in Python with WeakSet and unsubscribe return. |
| `templates/command-py.py` | Command pattern in Python with undo/redo Invoker. |
| `templates/state-py.py` | State pattern in Python with Context and abstract State base. |
| `templates/chain-py.py` | Chain of Responsibility in Python with fluent set_next chaining. |
