# Behavioral Design Patterns

## Summary

**One-sentence:** Nine GoF behavioral patterns (Strategy, Observer, Command, State, Chain of Responsibility, Template Method, Mediator, Iterator, Visitor) for controlling object communication at runtime.

**One-paragraph:** Behavioral patterns address how objects communicate and distribute responsibility. Output is a per-codebase pattern selection record naming which patterns are intentionally used, the rule for picking among confusable patterns (Strategy vs State vs Chain of Responsibility), and the lint / review check that prevents accidental misuse.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Codebase has runtime variance in behaviour (e.g., 'choose one of N algorithms', 'react to events').
- You see if/else or switch on type that grows weekly.
- ≥2 engineers will touch the variance-bearing code.

## Skip If (ANY kills it)

- Codebase is small (<5K LOC) and behaviour is stable.
- Solo founder with throwaway prototype.
- Pattern would add ≥2 layers of indirection over a 1-line if/else.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Variance hotspot list | list of files/methods | tech lead |
| Refactoring budget | story points / hours | PM |
| Language idiom catalogue | doc | tech lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/creational-patterns` | Object creation patterns complement behavioural ones. |
| `solo/dev/software-architect/arch-pattern-clean` | Behavioural patterns live in the inner rings. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the pattern selection record + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: locate variance → diagnose → pick pattern → refactor → review | ~700 |
| `content/05-examples.xml` | medium | Worked example: refactoring an if/elif/else into Strategy | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-variance` | sonnet | Decide which pattern (Strategy/State/Chain) fits the variance. |
| `draft-refactor` | sonnet | Per-pattern refactor scaffold. |
| `cross-codebase-audit` | opus | Spot misuse patterns across modules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pattern-selection.md.j2` | Behavioural pattern selection record. |
| `templates/pattern-selection.md` | Behavioural pattern selection record. Generated from `templates/pattern-selection.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/chain-py.py` | Chain of Responsibility Python skeleton with fluent `set_next` chaining. |
| `templates/command-py.py` | Command pattern Python skeleton with invoker + undo/redo stack. |
| `templates/observer-py.py` | Observer pattern Python skeleton: subject + subscribe/unsubscribe + notify. |
| `templates/state-py.py` | State pattern Python skeleton: context delegates behaviour to current state. |
| `templates/strategy-py.py` | Strategy pattern Python skeleton: interchangeable algorithm objects. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-behavioral-patterns.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[creational-patterns]]
- [[arch-pattern-clean]]
- [[arch-pattern-hexagonal]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/chain-py.py`

```python
"""
Chain of Responsibility in Python with fluent set_next chaining.

Models a request validation + processing pipeline (auth → rate-limit → handler).
set_next() returns the next handler, enabling builder-style chains:
    auth_handler.set_next(rate_limit_handler).set_next(business_handler)

Use when: multiple handlers may process a request; handler set is configurable.
Skip when: a simple list of functions achieves the same result with less ceremony.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Request:
    user_id: str
    api_key: str
    path: str
    payload: dict = field(default_factory=dict)


@dataclass
class Response:
    status: int
    body: str


# ---------------------------------------------------------------------------
# Abstract handler
# ---------------------------------------------------------------------------
class Handler(ABC):
    def __init__(self) -> None:
        self._next: Handler | None = None

    def set_next(self, handler: Handler) -> Handler:
        """Chain the next handler. Returns next for fluent builder syntax."""
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request: Request) -> Response | None:
        """Return a Response to short-circuit, or pass_to_next() to continue."""

    def pass_to_next(self, request: Request) -> Response | None:
        if self._next is not None:
            return self._next.handle(request)
        return None


# ---------------------------------------------------------------------------
# Concrete handlers
# ---------------------------------------------------------------------------
VALID_API_KEYS = {"key-abc", "key-xyz"}


class AuthHandler(Handler):
    def handle(self, request: Request) -> Response | None:
        if request.api_key not in VALID_API_KEYS:
            return Response(status=401, body="Unauthorized: invalid API key")
        return self.pass_to_next(request)


class RateLimitHandler(Handler):
    """Trivial in-memory rate limiter (replace with Redis in production)."""

    def __init__(self, max_requests: int = 100) -> None:
        super().__init__()
        self._counts: dict[str, int] = {}
        self._max = max_requests

    def handle(self, request: Request) -> Response | None:
        count = self._counts.get(request.user_id, 0)
        if count >= self._max:
            return Response(status=429, body="Too Many Requests")
        self._counts[request.user_id] = count + 1
        return self.pass_to_next(request)


class RouteHandler(Handler):
    """Final handler: routes to the appropriate business logic by path."""

    def handle(self, request: Request) -> Response | None:
        if request.path == "/ping":
            return Response(status=200, body="pong")
        if request.path.startswith("/api/"):
            return Response(status=200, body=f"Handled {request.path}")
        return Response(status=404, body=f"Not found: {request.path}")


class DefaultHandler(Handler):
    """Fallback if no previous handler returned a Response."""

    def handle(self, request: Request) -> Response | None:
        return Response(status=500, body="No handler produced a response")


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Build chain
    auth = AuthHandler()
    rate_limit = RateLimitHandler(max_requests=3)
    router = RouteHandler()
    fallback = DefaultHandler()

    auth.set_next(rate_limit).set_next(router).set_next(fallback)

    # Valid request
    req = Request(user_id="u1", api_key="key-abc", path="/api/items")
    resp = auth.handle(req)
    print(resp)  # Response(status=200, body='Handled /api/items')

    # Invalid key
    req2 = Request(user_id="u2", api_key="bad-key", path="/api/items")
    resp2 = auth.handle(req2)
    print(resp2)  # Response(status=401, body='Unauthorized: invalid API key')

    # Rate limited (max 3 requests)
    for i in range(4):
        req3 = Request(user_id="u3", api_key="key-xyz", path="/ping")
        resp3 = auth.handle(req3)
        print(f"Request {i + 1}: {resp3}")
    # Requests 1–3: status=200; Request 4: status=429
```

### `templates/command-py.py`

```python
"""
Command pattern in Python with undo/redo Invoker.

Use when: undo/redo, operation queuing, audit logging, saga steps.
Skip when: simple operations with no undo requirement — just call the function.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Command interface
# ---------------------------------------------------------------------------
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        """Perform the operation."""

    @abstractmethod
    def undo(self) -> None:
        """Reverse the operation."""


# ---------------------------------------------------------------------------
# Receiver: the object that performs the actual work
# ---------------------------------------------------------------------------
@dataclass
class TextEditor:
    content: str = ""

    def insert(self, text: str) -> None:
        self.content += text

    def delete(self, n: int) -> None:
        self.content = self.content[:-n] if n > 0 else self.content


# ---------------------------------------------------------------------------
# Concrete commands
# ---------------------------------------------------------------------------
@dataclass
class InsertTextCommand(Command):
    editor: TextEditor
    text: str

    def execute(self) -> None:
        self.editor.insert(self.text)

    def undo(self) -> None:
        self.editor.delete(len(self.text))


@dataclass
class DeleteTextCommand(Command):
    editor: TextEditor
    n: int
    _deleted: str = field(default="", init=False)

    def execute(self) -> None:
        self._deleted = self.editor.content[-self.n:] if self.n > 0 else ""
        self.editor.delete(self.n)

    def undo(self) -> None:
        self.editor.insert(self._deleted)


# ---------------------------------------------------------------------------
# Invoker: manages history and redo stacks
# ---------------------------------------------------------------------------
class Invoker:
    def __init__(self) -> None:
        self._history: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()  # new command invalidates redo history

    def undo(self) -> bool:
        if not self._history:
            return False
        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)
        return True

    @property
    def can_undo(self) -> bool:
        return bool(self._history)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo_stack)


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    editor = TextEditor()
    invoker = Invoker()

    invoker.execute(InsertTextCommand(editor, "Hello"))
    invoker.execute(InsertTextCommand(editor, ", World"))
    print(editor.content)  # "Hello, World"

    invoker.undo()
    print(editor.content)  # "Hello"

    invoker.redo()
    print(editor.content)  # "Hello, World"

    invoker.execute(DeleteTextCommand(editor, 6))
    print(editor.content)  # "Hello"

    invoker.undo()
    print(editor.content)  # "Hello, World"
```

### `templates/observer-py.py`

```python
"""
Observer / EventEmitter in Python.
- WeakSet prevents memory leaks when observer objects go out of scope.
- subscribe() returns an unsubscribe callable (no separate unsubscribe method needed).
- Errors in one observer are logged and do not block subsequent observers.

Use when: one-to-many notification; subject doesn't need to know subscribers.
Skip when: one-to-one relationship; use direct injection or a callback instead.
"""
from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any
from weakref import WeakSet

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Observer protocol
# ---------------------------------------------------------------------------
class EventEmitter:
    """Simple synchronous event emitter with WeakSet subscribers."""

    def __init__(self) -> None:
        # event_name → set of observers (weak references)
        # WeakSet: if the observer is garbage-collected, it is automatically removed.
        self._listeners: dict[str, WeakSet[Any]] = {}

    def subscribe(
        self,
        event: str,
        handler: Callable[[dict], None],
    ) -> Callable[[], None]:
        """
        Subscribe handler to event.
        Returns an unsubscribe callable:
            unsub = emitter.subscribe("user.created", my_handler)
            unsub()  # stop receiving events
        """
        if event not in self._listeners:
            self._listeners[event] = WeakSet()
        self._listeners[event].add(handler)

        def unsubscribe() -> None:
            if event in self._listeners:
                self._listeners[event].discard(handler)

        return unsubscribe

    def emit(self, event: str, data: dict | None = None) -> None:
        """Notify all subscribers for event. Errors are logged, not raised."""
        if event not in self._listeners:
            return
        payload = data or {}
        for handler in list(self._listeners[event]):  # copy to allow mutation
            try:
                handler(payload)
            except Exception:
                logger.exception("Error in observer for event %r", event)


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    emitter = EventEmitter()

    def on_user_created(data: dict) -> None:
        print(f"[email] Welcome {data['email']}")

    def on_user_created_audit(data: dict) -> None:
        print(f"[audit] User created: {data['user_id']}")

    unsub_email = emitter.subscribe("user.created", on_user_created)
    unsub_audit = emitter.subscribe("user.created", on_user_created_audit)

    emitter.emit("user.created", {"user_id": "u-123", "email": "alice@example.com"})
    # Output:
    #   [email] Welcome alice@example.com
    #   [audit] User created: u-123

    unsub_email()  # stop email notifications

    emitter.emit("user.created", {"user_id": "u-456", "email": "bob@example.com"})
    # Output:
    #   [audit] User created: u-456
```

### `templates/state-py.py`

```python
"""
State pattern in Python with Context and abstract State base.

Use when: object behavior changes significantly per state, FSMs, lifecycle workflows.
Skip when: 2–3 simple states with minimal branching — use an enum + match instead.

This template models an order lifecycle: PENDING → CONFIRMED → SHIPPED → DELIVERED.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# ---------------------------------------------------------------------------
# Abstract state
# ---------------------------------------------------------------------------
class OrderState(ABC):
    @property
    @abstractmethod
    def status(self) -> OrderStatus:
        ...

    @abstractmethod
    def confirm(self, order: Order) -> None:
        ...

    @abstractmethod
    def ship(self, order: Order) -> None:
        ...

    @abstractmethod
    def deliver(self, order: Order) -> None:
        ...

    @abstractmethod
    def cancel(self, order: Order) -> None:
        ...


# ---------------------------------------------------------------------------
# Concrete states
# ---------------------------------------------------------------------------
class PendingState(OrderState):
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.PENDING

    def confirm(self, order: Order) -> None:
        print("Order confirmed.")
        order._state = ConfirmedState()

    def ship(self, order: Order) -> None:
        print("Cannot ship: order not confirmed.")

    def deliver(self, order: Order) -> None:
        print("Cannot deliver: order not confirmed.")

    def cancel(self, order: Order) -> None:
        print("Order cancelled.")
        order._state = CancelledState()


class ConfirmedState(OrderState):
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.CONFIRMED

    def confirm(self, order: Order) -> None:
        print("Order is already confirmed.")

    def ship(self, order: Order) -> None:
        print("Order shipped.")
        order._state = ShippedState()

    def deliver(self, order: Order) -> None:
        print("Cannot deliver: order not shipped yet.")

    def cancel(self, order: Order) -> None:
        print("Order cancelled.")
        order._state = CancelledState()


class ShippedState(OrderState):
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.SHIPPED

    def confirm(self, order: Order) -> None:
        print("Cannot confirm: order already shipped.")

    def ship(self, order: Order) -> None:
        print("Order is already shipped.")

    def deliver(self, order: Order) -> None:
        print("Order delivered.")
        order._state = DeliveredState()

    def cancel(self, order: Order) -> None:
        print("Cannot cancel: order already shipped.")


class DeliveredState(OrderState):
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.DELIVERED

    def confirm(self, order: Order) -> None:
        print("Order already delivered.")

    def ship(self, order: Order) -> None:
        print("Order already delivered.")

    def deliver(self, order: Order) -> None:
        print("Order already delivered.")

    def cancel(self, order: Order) -> None:
        print("Cannot cancel: order already delivered.")


class CancelledState(OrderState):
    @property
    def status(self) -> OrderStatus:
        return OrderStatus.CANCELLED

    def confirm(self, order: Order) -> None:
        print("Cannot confirm: order is cancelled.")

    def ship(self, order: Order) -> None:
        print("Cannot ship: order is cancelled.")

    def deliver(self, order: Order) -> None:
        print("Cannot deliver: order is cancelled.")

    def cancel(self, order: Order) -> None:
        print("Order is already cancelled.")


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------
@dataclass
class Order:
    order_id: str
    _state: OrderState = field(default_factory=PendingState, init=False)

    @property
    def status(self) -> OrderStatus:
        return self._state.status

    def confirm(self) -> None:
        self._state.confirm(self)

    def ship(self) -> None:
        self._state.ship(self)

    def deliver(self) -> None:
        self._state.deliver(self)

    def cancel(self) -> None:
        self._state.cancel(self)


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    order = Order(order_id="ORD-001")
    print(order.status)  # PENDING

    order.ship()         # Cannot ship: order not confirmed.
    order.confirm()      # Order confirmed.
    print(order.status)  # CONFIRMED

    order.ship()         # Order shipped.
    print(order.status)  # SHIPPED

    order.cancel()       # Cannot cancel: order already shipped.
    order.deliver()      # Order delivered.
    print(order.status)  # DELIVERED
```

### `templates/strategy-py.py`

```python
"""
Strategy pattern in Python using Protocol for duck typing.

Use when: multiple algorithms for the same task, swappable at runtime.
Apply when: 3+ algorithm variants growing into if/else chains.
Skip when: 2 variants unlikely to change — use a simple conditional.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


# ---------------------------------------------------------------------------
# Strategy interface (Protocol = duck typing, no inheritance required)
# ---------------------------------------------------------------------------
class SortStrategy(Protocol):
    def sort(self, data: list[int]) -> list[int]:
        ...


# ---------------------------------------------------------------------------
# Concrete strategies
# ---------------------------------------------------------------------------
class BubbleSortStrategy:
    def sort(self, data: list[int]) -> list[int]:
        result = data.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result


class QuickSortStrategy:
    def sort(self, data: list[int]) -> list[int]:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        mid  = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + mid + self.sort(right)


class BuiltinSortStrategy:
    def sort(self, data: list[int]) -> list[int]:
        return sorted(data)


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------
@dataclass
class Sorter:
    strategy: SortStrategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self.strategy = strategy

    def sort(self, data: list[int]) -> list[int]:
        return self.strategy.sort(data)


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sorter = Sorter(strategy=BuiltinSortStrategy())
    result = sorter.sort([5, 3, 1, 4, 2])
    print(f"Builtin:  {result}")

    sorter.set_strategy(QuickSortStrategy())
    result = sorter.sort([5, 3, 1, 4, 2])
    print(f"Quicksort: {result}")

    # Functional variant — a plain function also satisfies the Protocol
    sorter.set_strategy(type("Reverse", (), {"sort": lambda self, d: sorted(d, reverse=True)})())
    result = sorter.sort([5, 3, 1, 4, 2])
    print(f"Reverse:  {result}")
```
