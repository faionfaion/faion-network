# Agent Integration — Creational Patterns

## When to use
- Agent is asked to write object-creation code where the type is decided at runtime, the constructor has many optional params, or the lifecycle differs from "new + use".
- Refactoring existing code that has duplicated `if/elif/elif` instantiation chains, sprawling constructors, or hidden global state.
- Reviewing legacy code for Singleton overuse, asking the agent to propose Dependency Injection migrations.
- Generating language-idiomatic implementations (Python, TS, Go) of Factory / Builder / DI / Object Pool from a spec.
- Writing test fixtures and mocks — DI and Factory Method dramatically reduce test scaffolding.

## When NOT to use
- Trivial constructors with no optional params and a single concrete class — `dataclass` / record / struct is enough.
- Cross-cutting infra concerns where DI containers already exist (FastAPI, NestJS, Spring) — let the framework own creation.
- One-off scripts / glue code — pattern overhead exceeds the value.
- High-performance hot paths where DI lookup or pool acquisition cost matters; benchmark first.

## Where it fails / limitations
- LLMs over-apply Singleton ("config" "logger" "cache") even when modules already provide singleton-by-import semantics in Python/JS.
- Agents generate Builder classes with 20+ setters when a `dataclass` + keyword args would do.
- Object Pool implementations from agents rarely reset object state on return — silent state-leak bugs.
- Prototype: agents default to `copy.deepcopy` without considering closures, file handles, locks, or DB sessions inside the prototype.
- DI: agents pick framework-specific containers (Spring annotations) when the project uses something else; check imports before applying.
- Singleton thread-safety: double-checked-locking idiom written by LLMs is often subtly wrong in Python (GIL hides bugs) and Java (volatile missing).

## Agentic workflow
This is a haiku-default methodology — most application is mechanical pattern matching. Sonnet only when refactoring legacy code requires reading 3+ files to choose between Factory and Abstract Factory, or when DI graph design matters. Run as a single-pass: agent reads the call site, suggests pattern + writes implementation + writes test. Always ask for the "before/after" diff and the alternative considered (e.g., "DI vs Singleton"). Pair with `code-review` skill for one-pass review.

### Recommended subagents
- `faion-sdd-executor-agent` — owns the refactor task end-to-end (apply pattern + tests + ADR if non-trivial).
- `simplify` skill (built-in) — after applying the pattern, simplify removes leftover indirection.
- `faion-improver` — captures pattern-application mistakes in `.aidocs/memory/patterns.md` for future prevention.

### Prompt pattern
```
Refactor this code to use <Factory Method | Builder | DI | Object Pool> in <Python/TS/Go>.
Context: <framework, e.g. FastAPI, NestJS, Gin>.
Constraints: must be testable with mocks, must keep public API stable, no global state.
Show: 1) before/after diff, 2) one alternative pattern with trade-offs, 3) the test that proves
mock injection works.
```

```
Find Singleton anti-patterns in <module/path>. For each, propose a DI-based replacement
and explain the testability gain in one sentence.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` | Lint Python for `B008` (mutable default args), unused imports | `pip install ruff` |
| `mypy` / `pyright` | Static check that DI signatures match | `pip install mypy` / `npm i -g pyright` |
| `eslint` + `typescript-eslint` | Catch Singleton misuse, factory typos | `npm i -D eslint @typescript-eslint/parser` |
| `golangci-lint` | Detects unused params, ineffectual assignments in factories | https://golangci-lint.run/ |
| `wire` | Google's compile-time DI for Go | `go install github.com/google/wire/cmd/wire@latest` |
| `inversifyjs` | Decorator-based DI for TS | `npm i inversify reflect-metadata` |
| `dependency-injector` | Python container (declarative wiring) | `pip install dependency-injector` |
| `pytest --fixtures` | Discover injectable fixtures (DI for tests) | `pip install pytest` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Spring Framework | OSS | Yes | Java DI; agents understand `@Component`/`@Autowired` well. |
| FastAPI Depends | OSS | Yes | Function-arg DI; pairs naturally with pytest fixtures. |
| NestJS DI | OSS | Yes | Decorator + module system; agent prompt should specify provider scope. |
| Wire (Google) | OSS | Yes | Compile-time DI; agent emits provider sets, not magic. |
| dependency-injector (Py) | OSS | Yes | Declarative containers; YAML/Pydantic config supported. |
| Dagger (Java/Kotlin) | OSS | Partial | Compile-time, requires annotation processor setup — agent can scaffold. |

## Templates & scripts
See `templates.md` and `examples.md` for Python/TS/Go pattern code. Inline minimal pytest DI fixture template that replaces a Singleton:

```python
# conftest.py — DI replacement for a Singleton "Settings" object
import pytest
from myapp.settings import Settings, get_settings

@pytest.fixture
def settings(monkeypatch) -> Settings:
    s = Settings(env="test", db_url="sqlite:///:memory:")
    monkeypatch.setattr("myapp.settings.get_settings", lambda: s)
    return s
```

## Best practices
- Default to DI; reach for Singleton only for truly process-global ambient resources (logger, metrics emitter), never for app config or state.
- Keep Builder / Factory inside the package that owns the type; never place factories in shared "utils" — that recreates global state.
- For Object Pool: enforce `reset()` contract via abstract method; agent code must call it on return, not on borrow.
- Prefer constructor injection over setter injection — required deps stay required, refactoring is type-checker-driven.
- For Prototype, prefer immutable types + structural sharing (Python `frozen` dataclass, TS `Readonly<T>`) over deep-copy.
- Document the chosen pattern in a one-line comment at the top of the class so future agents don't rewrite it.

## AI-agent gotchas
- Singletons hidden as module-level objects in Python: agents propose "Singleton class" without realizing `module = singleton`. Push for module-level functions instead.
- TS Singleton + ESM: re-importing across `dist/` paths can break "single instance" guarantee; agent code looks correct but runtime has two instances.
- Go: agents reach for sync.Once globals when context-scoped factories are cleaner; reject globals on review.
- Object Pool with goroutines: agent forgets that `sync.Pool` items can be GC'd between Put/Get; not a true pool. For real pooling use a buffered channel.
- DI containers: agent declares circular dependencies that compile-time checkers (Wire, Dagger) catch but runtime ones (Inversify, dependency-injector) only fail at first request — run the smoke test.
- Prototype copying with closures or open file handles: agent never warns; always require a "what happens to non-cloneable members?" answer.
- Builder fluent chaining: agent emits `return self` everywhere but forgets terminal `build()` validation; demand validation before object hand-off.

## References
- Refactoring.Guru — Creational Patterns. https://refactoring.guru/design-patterns/creational-patterns
- "Design Patterns: Elements of Reusable Object-Oriented Software" (GoF, 1994).
- Python Patterns Guide — https://python-patterns.guide/
- Mark Seemann, "Dependency Injection Principles, Practices, and Patterns" (2019).
- Google Wire docs — https://github.com/google/wire/blob/main/docs/best-practices.md
- "The Singleton Pattern Is a Refactoring Nightmare" — https://thenewstack.io/unmasking-the-singleton-anti-pattern/
- FastAPI dependency injection — https://fastapi.tiangolo.com/tutorial/dependencies/
