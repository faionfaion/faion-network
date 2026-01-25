# Behavioral Design Patterns

Patterns for object interaction and communication.

## Overview

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| Strategy | Interchangeable algorithms | Multiple approaches to same task |
| Observer | Notify multiple objects of changes | Event systems, reactive |
| Command | Encapsulate request as object | Undo, queue operations |
| State | Change behavior based on state | Finite state machines |
| Chain of Responsibility | Pass request along chain | Middleware, handlers |
| Template Method | Define algorithm skeleton | Shared workflow steps |

## Strategy

Interchangeable algorithms at runtime.

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str: pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} via Credit Card"

class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} via PayPal"

class Checkout:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def process(self, amount: float) -> str:
        return self.strategy.pay(amount)

# Usage - swap strategies
checkout = Checkout(CreditCardPayment())
checkout.process(100)

checkout.strategy = PayPalPayment()
checkout.process(100)
```

## Observer

Notify subscribers of changes.

```python
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, data): pass

class Subject:
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, data):
        for observer in self._observers:
            observer.update(data)

# Concrete observer
class EmailNotifier(Observer):
    def update(self, data):
        print(f"Email sent: {data}")

class SlackNotifier(Observer):
    def update(self, data):
        print(f"Slack message: {data}")

# Usage
order_events = Subject()
order_events.attach(EmailNotifier())
order_events.attach(SlackNotifier())
order_events.notify("Order #123 placed")
```

## Command

Encapsulate action as object.

```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self): pass
    @abstractmethod
    def undo(self): pass

class AddTextCommand(Command):
    def __init__(self, editor, text: str):
        self.editor = editor
        self.text = text

    def execute(self):
        self.editor.content += self.text

    def undo(self):
        self.editor.content = self.editor.content[:-len(self.text)]

class Editor:
    def __init__(self):
        self.content = ""
        self.history: list[Command] = []

    def execute(self, command: Command):
        command.execute()
        self.history.append(command)

    def undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()

# Usage
editor = Editor()
editor.execute(AddTextCommand(editor, "Hello "))
editor.execute(AddTextCommand(editor, "World"))
print(editor.content)  # "Hello World"
editor.undo()
print(editor.content)  # "Hello "
```

## State

Change behavior based on internal state.

```python
from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def handle(self, context): pass

class Draft(State):
    def handle(self, context):
        print("Moving from Draft to Moderation")
        context.state = Moderation()

class Moderation(State):
    def handle(self, context):
        print("Moving from Moderation to Published")
        context.state = Published()

class Published(State):
    def handle(self, context):
        print("Already published, cannot transition")

class Document:
    def __init__(self):
        self.state = Draft()

    def publish(self):
        self.state.handle(self)

# Usage
doc = Document()
doc.publish()  # Draft -> Moderation
doc.publish()  # Moderation -> Published
doc.publish()  # Already published
```

## Chain of Responsibility

Pass request along handler chain.

```python
from abc import ABC, abstractmethod

class Handler(ABC):
    def __init__(self):
        self._next: Handler = None

    def set_next(self, handler: 'Handler') -> 'Handler':
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request): pass

    def pass_to_next(self, request):
        if self._next:
            return self._next.handle(request)
        return None

class AuthHandler(Handler):
    def handle(self, request):
        if not request.get('authenticated'):
            return "Auth failed"
        return self.pass_to_next(request)

class RateLimitHandler(Handler):
    def handle(self, request):
        if request.get('rate_exceeded'):
            return "Rate limit exceeded"
        return self.pass_to_next(request)

class BusinessHandler(Handler):
    def handle(self, request):
        return "Request processed"

# Usage
auth = AuthHandler()
rate = RateLimitHandler()
business = BusinessHandler()

auth.set_next(rate).set_next(business)

result = auth.handle({'authenticated': True, 'rate_exceeded': False})
```

## Template Method

Define algorithm skeleton in base class.

```python
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    def process(self):
        """Template method - defines algorithm"""
        data = self.read_data()
        processed = self.transform(data)
        self.save(processed)

    @abstractmethod
    def read_data(self): pass

    @abstractmethod
    def transform(self, data): pass

    def save(self, data):
        """Default implementation"""
        print(f"Saving: {data}")

class CSVProcessor(DataProcessor):
    def read_data(self):
        return "CSV data"

    def transform(self, data):
        return f"Transformed {data}"

class JSONProcessor(DataProcessor):
    def read_data(self):
        return "JSON data"

    def transform(self, data):
        return f"Parsed {data}"
```

## When to Use

| Situation | Pattern |
|-----------|---------|
| "Multiple algorithms, choose at runtime" | Strategy |
| "Notify many objects of changes" | Observer |
| "Undo, queue, log operations" | Command |
| "Object behaves differently per state" | State |
| "Middleware, request handlers" | Chain of Responsibility |
| "Same algorithm steps, different details" | Template Method |

## Related

- [creational-patterns.md](creational-patterns.md) - Object creation
- [structural-patterns.md](structural-patterns.md) - Object composition
