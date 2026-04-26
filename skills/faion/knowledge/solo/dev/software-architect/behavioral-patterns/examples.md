# Behavioral Patterns Examples

Real-world implementations in Python, TypeScript, and Go.

## Strategy Pattern

### Python: Payment Processing

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol
from decimal import Decimal


# Modern approach: Protocol (duck typing)
class PaymentStrategy(Protocol):
    def pay(self, amount: Decimal) -> dict: ...
    def refund(self, transaction_id: str) -> dict: ...


@dataclass(frozen=True)
class PaymentResult:
    success: bool
    transaction_id: str
    message: str


class CreditCardPayment:
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number[-4:]  # Store only last 4
        self.cvv = cvv

    def pay(self, amount: Decimal) -> dict:
        # Actual payment gateway integration
        return {
            "success": True,
            "transaction_id": f"CC_{self.card_number}_{amount}",
            "message": f"Charged ${amount} to card ending {self.card_number}"
        }

    def refund(self, transaction_id: str) -> dict:
        return {"success": True, "message": f"Refunded {transaction_id}"}


class PayPalPayment:
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: Decimal) -> dict:
        return {
            "success": True,
            "transaction_id": f"PP_{self.email}_{amount}",
            "message": f"PayPal payment ${amount} to {self.email}"
        }

    def refund(self, transaction_id: str) -> dict:
        return {"success": True, "message": f"PayPal refund {transaction_id}"}


class CryptoPayment:
    def __init__(self, wallet_address: str, currency: str = "ETH"):
        self.wallet = wallet_address
        self.currency = currency

    def pay(self, amount: Decimal) -> dict:
        return {
            "success": True,
            "transaction_id": f"CRYPTO_{self.currency}_{amount}",
            "message": f"Sent {amount} {self.currency}"
        }

    def refund(self, transaction_id: str) -> dict:
        return {"success": True, "message": f"Crypto refund initiated"}


class Checkout:
    def __init__(self, payment_strategy: PaymentStrategy):
        self._strategy = payment_strategy

    def set_payment_method(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def process_payment(self, amount: Decimal) -> dict:
        return self._strategy.pay(amount)


# Usage
checkout = Checkout(CreditCardPayment("4111111111111234", "123"))
result = checkout.process_payment(Decimal("99.99"))

# Switch strategy at runtime
checkout.set_payment_method(PayPalPayment("user@example.com"))
result = checkout.process_payment(Decimal("49.99"))
```

### TypeScript: Sorting Strategies

```typescript
// Strategy interface
interface SortStrategy<T> {
  sort(items: T[]): T[];
  readonly name: string;
}

// Concrete strategies
class QuickSort<T> implements SortStrategy<T> {
  readonly name = "QuickSort";

  sort(items: T[]): T[] {
    if (items.length <= 1) return items;

    const pivot = items[Math.floor(items.length / 2)];
    const left = items.filter(x => x < pivot);
    const middle = items.filter(x => x === pivot);
    const right = items.filter(x => x > pivot);

    return [...this.sort(left), ...middle, ...this.sort(right)];
  }
}

class MergeSort<T> implements SortStrategy<T> {
  readonly name = "MergeSort";

  sort(items: T[]): T[] {
    if (items.length <= 1) return items;

    const mid = Math.floor(items.length / 2);
    const left = this.sort(items.slice(0, mid));
    const right = this.sort(items.slice(mid));

    return this.merge(left, right);
  }

  private merge(left: T[], right: T[]): T[] {
    const result: T[] = [];
    let i = 0, j = 0;

    while (i < left.length && j < right.length) {
      if (left[i] < right[j]) {
        result.push(left[i++]);
      } else {
        result.push(right[j++]);
      }
    }

    return [...result, ...left.slice(i), ...right.slice(j)];
  }
}

// Context with strategy selection
class Sorter<T> {
  constructor(private strategy: SortStrategy<T>) {}

  setStrategy(strategy: SortStrategy<T>): void {
    this.strategy = strategy;
  }

  sort(items: T[]): T[] {
    console.log(`Sorting with ${this.strategy.name}`);
    return this.strategy.sort([...items]); // Don't mutate original
  }
}

// Usage
const sorter = new Sorter<number>(new QuickSort());
const sorted = sorter.sort([3, 1, 4, 1, 5, 9, 2, 6]);

sorter.setStrategy(new MergeSort());
const sorted2 = sorter.sort([3, 1, 4, 1, 5, 9, 2, 6]);
```

### Go: Compression Strategies

```go
package main

import (
    "bytes"
    "compress/gzip"
    "compress/zlib"
    "io"
)

// Strategy interface
type CompressionStrategy interface {
    Compress(data []byte) ([]byte, error)
    Decompress(data []byte) ([]byte, error)
    Name() string
}

// Gzip strategy
type GzipCompression struct{}

func (g *GzipCompression) Name() string { return "gzip" }

func (g *GzipCompression) Compress(data []byte) ([]byte, error) {
    var buf bytes.Buffer
    writer := gzip.NewWriter(&buf)
    if _, err := writer.Write(data); err != nil {
        return nil, err
    }
    if err := writer.Close(); err != nil {
        return nil, err
    }
    return buf.Bytes(), nil
}

func (g *GzipCompression) Decompress(data []byte) ([]byte, error) {
    reader, err := gzip.NewReader(bytes.NewReader(data))
    if err != nil {
        return nil, err
    }
    defer reader.Close()
    return io.ReadAll(reader)
}

// Zlib strategy
type ZlibCompression struct{}

func (z *ZlibCompression) Name() string { return "zlib" }

func (z *ZlibCompression) Compress(data []byte) ([]byte, error) {
    var buf bytes.Buffer
    writer := zlib.NewWriter(&buf)
    if _, err := writer.Write(data); err != nil {
        return nil, err
    }
    if err := writer.Close(); err != nil {
        return nil, err
    }
    return buf.Bytes(), nil
}

func (z *ZlibCompression) Decompress(data []byte) ([]byte, error) {
    reader, err := zlib.NewReader(bytes.NewReader(data))
    if err != nil {
        return nil, err
    }
    defer reader.Close()
    return io.ReadAll(reader)
}

// Context
type FileCompressor struct {
    strategy CompressionStrategy
}

func NewFileCompressor(strategy CompressionStrategy) *FileCompressor {
    return &FileCompressor{strategy: strategy}
}

func (fc *FileCompressor) SetStrategy(strategy CompressionStrategy) {
    fc.strategy = strategy
}

func (fc *FileCompressor) CompressFile(data []byte) ([]byte, error) {
    return fc.strategy.Compress(data)
}

// Usage
func main() {
    compressor := NewFileCompressor(&GzipCompression{})
    data := []byte("Hello, World!")

    compressed, _ := compressor.CompressFile(data)

    // Switch strategy
    compressor.SetStrategy(&ZlibCompression{})
    compressed2, _ := compressor.CompressFile(data)
}
```

## Observer Pattern

### Python: Event System with Weak References

```python
from typing import Protocol, Callable, Any
from dataclasses import dataclass, field
from weakref import WeakSet
from datetime import datetime


class Observer(Protocol):
    def update(self, event: "Event") -> None: ...


@dataclass
class Event:
    name: str
    data: dict
    timestamp: datetime = field(default_factory=datetime.now)


class EventEmitter:
    def __init__(self):
        self._observers: dict[str, WeakSet[Observer]] = {}

    def subscribe(self, event_name: str, observer: Observer) -> Callable[[], None]:
        if event_name not in self._observers:
            self._observers[event_name] = WeakSet()
        self._observers[event_name].add(observer)

        # Return unsubscribe function
        def unsubscribe():
            self._observers[event_name].discard(observer)
        return unsubscribe

    def emit(self, event_name: str, data: dict = None):
        event = Event(name=event_name, data=data or {})
        if event_name in self._observers:
            for observer in list(self._observers[event_name]):
                observer.update(event)


class EmailNotifier:
    def __init__(self, email: str):
        self.email = email

    def update(self, event: Event):
        print(f"Email to {self.email}: {event.name} - {event.data}")


class SlackNotifier:
    def __init__(self, channel: str):
        self.channel = channel

    def update(self, event: Event):
        print(f"Slack #{self.channel}: {event.name} - {event.data}")


class MetricsCollector:
    def __init__(self):
        self.events: list[Event] = []

    def update(self, event: Event):
        self.events.append(event)
        print(f"Metrics: recorded {event.name}")


# Usage
emitter = EventEmitter()

email = EmailNotifier("admin@example.com")
slack = SlackNotifier("orders")
metrics = MetricsCollector()

unsubscribe_email = emitter.subscribe("order.created", email)
emitter.subscribe("order.created", slack)
emitter.subscribe("order.created", metrics)

emitter.emit("order.created", {"order_id": "12345", "total": 99.99})

# Unsubscribe
unsubscribe_email()
emitter.emit("order.created", {"order_id": "12346", "total": 149.99})
```

### TypeScript: Reactive Store (Redux-like)

```typescript
type Listener<T> = (state: T) => void;
type Reducer<T, A> = (state: T, action: A) => T;

interface Store<T, A> {
  getState(): T;
  dispatch(action: A): void;
  subscribe(listener: Listener<T>): () => void;
}

function createStore<T, A>(
  reducer: Reducer<T, A>,
  initialState: T
): Store<T, A> {
  let state = initialState;
  const listeners = new Set<Listener<T>>();

  return {
    getState: () => state,

    dispatch(action: A): void {
      const prevState = state;
      state = reducer(state, action);

      // Only notify if state changed
      if (state !== prevState) {
        listeners.forEach(listener => listener(state));
      }
    },

    subscribe(listener: Listener<T>): () => void {
      listeners.add(listener);
      return () => listeners.delete(listener);
    }
  };
}

// Example: Counter store
interface CounterState {
  count: number;
}

type CounterAction =
  | { type: 'INCREMENT' }
  | { type: 'DECREMENT' }
  | { type: 'SET'; payload: number };

const counterReducer: Reducer<CounterState, CounterAction> = (state, action) => {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + 1 };
    case 'DECREMENT':
      return { count: state.count - 1 };
    case 'SET':
      return { count: action.payload };
    default:
      return state;
  }
};

// Usage
const store = createStore(counterReducer, { count: 0 });

const unsubscribe = store.subscribe(state => {
  console.log('State changed:', state.count);
});

store.dispatch({ type: 'INCREMENT' });  // logs: State changed: 1
store.dispatch({ type: 'INCREMENT' });  // logs: State changed: 2
store.dispatch({ type: 'SET', payload: 10 });  // logs: State changed: 10

unsubscribe();
store.dispatch({ type: 'INCREMENT' });  // no log (unsubscribed)
```

### Go: Event Bus with Channels

```go
package main

import (
    "context"
    "sync"
)

type Event struct {
    Type string
    Data interface{}
}

type EventHandler func(Event)

type EventBus struct {
    mu          sync.RWMutex
    subscribers map[string][]chan Event
}

func NewEventBus() *EventBus {
    return &EventBus{
        subscribers: make(map[string][]chan Event),
    }
}

func (eb *EventBus) Subscribe(ctx context.Context, eventType string, handler EventHandler) {
    ch := make(chan Event, 10) // Buffered channel

    eb.mu.Lock()
    eb.subscribers[eventType] = append(eb.subscribers[eventType], ch)
    eb.mu.Unlock()

    // Handle events in goroutine
    go func() {
        for {
            select {
            case event := <-ch:
                handler(event)
            case <-ctx.Done():
                eb.unsubscribe(eventType, ch)
                return
            }
        }
    }()
}

func (eb *EventBus) unsubscribe(eventType string, ch chan Event) {
    eb.mu.Lock()
    defer eb.mu.Unlock()

    subs := eb.subscribers[eventType]
    for i, sub := range subs {
        if sub == ch {
            eb.subscribers[eventType] = append(subs[:i], subs[i+1:]...)
            close(ch)
            break
        }
    }
}

func (eb *EventBus) Publish(event Event) {
    eb.mu.RLock()
    defer eb.mu.RUnlock()

    if subs, ok := eb.subscribers[event.Type]; ok {
        for _, ch := range subs {
            select {
            case ch <- event:
            default:
                // Channel full, skip (or log warning)
            }
        }
    }
}

// Usage
func main() {
    bus := NewEventBus()
    ctx, cancel := context.WithCancel(context.Background())

    bus.Subscribe(ctx, "user.created", func(e Event) {
        println("User created:", e.Data.(string))
    })

    bus.Subscribe(ctx, "user.created", func(e Event) {
        println("Send welcome email to:", e.Data.(string))
    })

    bus.Publish(Event{Type: "user.created", Data: "john@example.com"})

    // Cleanup
    cancel()
}
```

## Command Pattern

### Python: Text Editor with Undo/Redo

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol


class Command(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...
    @property
    def description(self) -> str: ...


@dataclass
class TextEditor:
    content: str = ""
    cursor: int = 0


@dataclass
class InsertTextCommand:
    editor: TextEditor
    text: str
    position: int = field(default=None)

    def __post_init__(self):
        if self.position is None:
            self.position = self.editor.cursor

    def execute(self) -> None:
        self.editor.content = (
            self.editor.content[:self.position] +
            self.text +
            self.editor.content[self.position:]
        )
        self.editor.cursor = self.position + len(self.text)

    def undo(self) -> None:
        self.editor.content = (
            self.editor.content[:self.position] +
            self.editor.content[self.position + len(self.text):]
        )
        self.editor.cursor = self.position

    @property
    def description(self) -> str:
        return f"Insert '{self.text}' at {self.position}"


@dataclass
class DeleteTextCommand:
    editor: TextEditor
    start: int
    end: int
    deleted_text: str = field(default="", init=False)

    def execute(self) -> None:
        self.deleted_text = self.editor.content[self.start:self.end]
        self.editor.content = (
            self.editor.content[:self.start] +
            self.editor.content[self.end:]
        )
        self.editor.cursor = self.start

    def undo(self) -> None:
        self.editor.content = (
            self.editor.content[:self.start] +
            self.deleted_text +
            self.editor.content[self.start:]
        )
        self.editor.cursor = self.start + len(self.deleted_text)

    @property
    def description(self) -> str:
        return f"Delete '{self.deleted_text}' from {self.start} to {self.end}"


class CommandHistory:
    def __init__(self, max_size: int = 100):
        self.history: list[Command] = []
        self.redo_stack: list[Command] = []
        self.max_size = max_size

    def execute(self, command: Command) -> None:
        command.execute()
        self.history.append(command)
        self.redo_stack.clear()  # Clear redo on new command

        # Limit history size
        if len(self.history) > self.max_size:
            self.history.pop(0)

    def undo(self) -> bool:
        if not self.history:
            return False
        command = self.history.pop()
        command.undo()
        self.redo_stack.append(command)
        return True

    def redo(self) -> bool:
        if not self.redo_stack:
            return False
        command = self.redo_stack.pop()
        command.execute()
        self.history.append(command)
        return True


# Usage
editor = TextEditor()
history = CommandHistory()

history.execute(InsertTextCommand(editor, "Hello"))
history.execute(InsertTextCommand(editor, " World"))
print(editor.content)  # "Hello World"

history.undo()
print(editor.content)  # "Hello"

history.redo()
print(editor.content)  # "Hello World"

history.execute(DeleteTextCommand(editor, 5, 11))
print(editor.content)  # "Hello"
```

### TypeScript: Task Queue with Retry

```typescript
interface Command {
  execute(): Promise<void>;
  undo(): Promise<void>;
  readonly id: string;
  readonly retryable: boolean;
}

interface CommandResult {
  commandId: string;
  success: boolean;
  error?: Error;
  retriesUsed: number;
}

class CommandQueue {
  private queue: Command[] = [];
  private executed: Command[] = [];
  private isProcessing = false;
  private maxRetries = 3;

  async enqueue(command: Command): Promise<CommandResult> {
    this.queue.push(command);
    return this.processQueue();
  }

  private async processQueue(): Promise<CommandResult> {
    if (this.isProcessing || this.queue.length === 0) {
      return { commandId: '', success: true, retriesUsed: 0 };
    }

    this.isProcessing = true;
    const command = this.queue.shift()!;
    let retries = 0;
    let lastError: Error | undefined;

    while (retries <= (command.retryable ? this.maxRetries : 0)) {
      try {
        await command.execute();
        this.executed.push(command);
        this.isProcessing = false;

        // Process next command
        if (this.queue.length > 0) {
          this.processQueue();
        }

        return {
          commandId: command.id,
          success: true,
          retriesUsed: retries
        };
      } catch (error) {
        lastError = error as Error;
        retries++;
        await this.delay(Math.pow(2, retries) * 100); // Exponential backoff
      }
    }

    this.isProcessing = false;
    return {
      commandId: command.id,
      success: false,
      error: lastError,
      retriesUsed: retries
    };
  }

  async undoLast(): Promise<boolean> {
    const command = this.executed.pop();
    if (!command) return false;

    await command.undo();
    return true;
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Example: API commands
class CreateUserCommand implements Command {
  id: string;
  retryable = true;
  private userId?: string;

  constructor(private userData: { email: string; name: string }) {
    this.id = `create-user-${Date.now()}`;
  }

  async execute(): Promise<void> {
    // Simulate API call
    console.log(`Creating user: ${this.userData.email}`);
    this.userId = `user_${Date.now()}`;
  }

  async undo(): Promise<void> {
    if (this.userId) {
      console.log(`Deleting user: ${this.userId}`);
    }
  }
}

// Usage
const queue = new CommandQueue();

queue.enqueue(new CreateUserCommand({ email: 'a@test.com', name: 'Alice' }));
queue.enqueue(new CreateUserCommand({ email: 'b@test.com', name: 'Bob' }));
```

### Go: Database Transaction Commands

```go
package main

import (
    "context"
    "database/sql"
    "fmt"
)

type Command interface {
    Execute(ctx context.Context) error
    Undo(ctx context.Context) error
    Description() string
}

type InsertUserCommand struct {
    db       *sql.DB
    email    string
    name     string
    insertedID int64
}

func (c *InsertUserCommand) Execute(ctx context.Context) error {
    result, err := c.db.ExecContext(ctx,
        "INSERT INTO users (email, name) VALUES (?, ?)",
        c.email, c.name)
    if err != nil {
        return err
    }
    c.insertedID, _ = result.LastInsertId()
    return nil
}

func (c *InsertUserCommand) Undo(ctx context.Context) error {
    _, err := c.db.ExecContext(ctx,
        "DELETE FROM users WHERE id = ?", c.insertedID)
    return err
}

func (c *InsertUserCommand) Description() string {
    return fmt.Sprintf("Insert user %s", c.email)
}

type TransactionExecutor struct {
    commands []Command
    executed []Command
}

func (te *TransactionExecutor) Add(cmd Command) {
    te.commands = append(te.commands, cmd)
}

func (te *TransactionExecutor) Execute(ctx context.Context) error {
    for _, cmd := range te.commands {
        if err := cmd.Execute(ctx); err != nil {
            // Rollback executed commands
            te.Rollback(ctx)
            return fmt.Errorf("%s failed: %w", cmd.Description(), err)
        }
        te.executed = append(te.executed, cmd)
    }
    return nil
}

func (te *TransactionExecutor) Rollback(ctx context.Context) {
    // Undo in reverse order
    for i := len(te.executed) - 1; i >= 0; i-- {
        te.executed[i].Undo(ctx)
    }
    te.executed = nil
}

// Usage
func main() {
    // db := sql.Open(...)

    executor := &TransactionExecutor{}
    // executor.Add(&InsertUserCommand{db: db, email: "a@test.com", name: "Alice"})
    // executor.Add(&InsertUserCommand{db: db, email: "b@test.com", name: "Bob"})

    // ctx := context.Background()
    // if err := executor.Execute(ctx); err != nil {
    //     log.Printf("Transaction failed: %v", err)
    // }
}
```

## State Pattern

### Python: Order State Machine

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional


class OrderStatus(Enum):
    PENDING = auto()
    PAID = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


class OrderState(ABC):
    @abstractmethod
    def pay(self, order: "Order") -> None: ...

    @abstractmethod
    def ship(self, order: "Order") -> None: ...

    @abstractmethod
    def deliver(self, order: "Order") -> None: ...

    @abstractmethod
    def cancel(self, order: "Order") -> None: ...

    @property
    @abstractmethod
    def status(self) -> OrderStatus: ...


class PendingState(OrderState):
    status = OrderStatus.PENDING

    def pay(self, order: "Order") -> None:
        order.paid_at = datetime.now()
        order._state = PaidState()
        print(f"Order {order.id} paid successfully")

    def ship(self, order: "Order") -> None:
        raise ValueError("Cannot ship unpaid order")

    def deliver(self, order: "Order") -> None:
        raise ValueError("Cannot deliver unpaid order")

    def cancel(self, order: "Order") -> None:
        order.cancelled_at = datetime.now()
        order._state = CancelledState()
        print(f"Order {order.id} cancelled")


class PaidState(OrderState):
    status = OrderStatus.PAID

    def pay(self, order: "Order") -> None:
        raise ValueError("Order already paid")

    def ship(self, order: "Order") -> None:
        order.shipped_at = datetime.now()
        order._state = ShippedState()
        print(f"Order {order.id} shipped")

    def deliver(self, order: "Order") -> None:
        raise ValueError("Cannot deliver unshipped order")

    def cancel(self, order: "Order") -> None:
        # Refund logic here
        order.cancelled_at = datetime.now()
        order._state = CancelledState()
        print(f"Order {order.id} cancelled with refund")


class ShippedState(OrderState):
    status = OrderStatus.SHIPPED

    def pay(self, order: "Order") -> None:
        raise ValueError("Order already paid")

    def ship(self, order: "Order") -> None:
        raise ValueError("Order already shipped")

    def deliver(self, order: "Order") -> None:
        order.delivered_at = datetime.now()
        order._state = DeliveredState()
        print(f"Order {order.id} delivered")

    def cancel(self, order: "Order") -> None:
        raise ValueError("Cannot cancel shipped order")


class DeliveredState(OrderState):
    status = OrderStatus.DELIVERED

    def pay(self, order: "Order") -> None:
        raise ValueError("Order already paid")

    def ship(self, order: "Order") -> None:
        raise ValueError("Order already delivered")

    def deliver(self, order: "Order") -> None:
        raise ValueError("Order already delivered")

    def cancel(self, order: "Order") -> None:
        raise ValueError("Cannot cancel delivered order")


class CancelledState(OrderState):
    status = OrderStatus.CANCELLED

    def pay(self, order: "Order") -> None:
        raise ValueError("Order is cancelled")

    def ship(self, order: "Order") -> None:
        raise ValueError("Order is cancelled")

    def deliver(self, order: "Order") -> None:
        raise ValueError("Order is cancelled")

    def cancel(self, order: "Order") -> None:
        raise ValueError("Order already cancelled")


@dataclass
class Order:
    id: str
    total: float
    _state: OrderState = field(default_factory=PendingState)
    created_at: datetime = field(default_factory=datetime.now)
    paid_at: datetime | None = None
    shipped_at: datetime | None = None
    delivered_at: datetime | None = None
    cancelled_at: datetime | None = None

    @property
    def status(self) -> OrderStatus:
        return self._state.status

    def pay(self) -> None:
        self._state.pay(self)

    def ship(self) -> None:
        self._state.ship(self)

    def deliver(self) -> None:
        self._state.deliver(self)

    def cancel(self) -> None:
        self._state.cancel(self)


# Usage
order = Order(id="ORD-001", total=99.99)
print(f"Status: {order.status}")  # PENDING

order.pay()
print(f"Status: {order.status}")  # PAID

order.ship()
print(f"Status: {order.status}")  # SHIPPED

order.deliver()
print(f"Status: {order.status}")  # DELIVERED
```

### TypeScript: Document Workflow with XState-like

```typescript
// Type-safe state machine
type DocumentState = 'draft' | 'review' | 'approved' | 'published' | 'archived';

type DocumentEvent =
  | { type: 'SUBMIT' }
  | { type: 'APPROVE' }
  | { type: 'REJECT' }
  | { type: 'PUBLISH' }
  | { type: 'ARCHIVE' };

interface StateConfig<S extends string, E extends { type: string }> {
  initial: S;
  states: {
    [K in S]: {
      on?: Partial<{ [T in E['type']]: S }>;
      entry?: () => void;
      exit?: () => void;
    };
  };
}

class StateMachine<S extends string, E extends { type: string }> {
  private currentState: S;

  constructor(private config: StateConfig<S, E>) {
    this.currentState = config.initial;
    this.runEntry(this.currentState);
  }

  get state(): S {
    return this.currentState;
  }

  send(event: E): S {
    const stateConfig = this.config.states[this.currentState];
    const nextState = stateConfig.on?.[event.type as E['type']];

    if (nextState && nextState !== this.currentState) {
      this.runExit(this.currentState);
      this.currentState = nextState;
      this.runEntry(this.currentState);
    }

    return this.currentState;
  }

  private runEntry(state: S): void {
    this.config.states[state].entry?.();
  }

  private runExit(state: S): void {
    this.config.states[state].exit?.();
  }

  can(eventType: E['type']): boolean {
    return !!this.config.states[this.currentState].on?.[eventType];
  }
}

// Document state machine
const documentMachine = new StateMachine<DocumentState, DocumentEvent>({
  initial: 'draft',
  states: {
    draft: {
      on: { SUBMIT: 'review' },
      entry: () => console.log('Entered draft state'),
    },
    review: {
      on: { APPROVE: 'approved', REJECT: 'draft' },
      entry: () => console.log('Document submitted for review'),
    },
    approved: {
      on: { PUBLISH: 'published', REJECT: 'draft' },
      entry: () => console.log('Document approved'),
    },
    published: {
      on: { ARCHIVE: 'archived' },
      entry: () => console.log('Document published!'),
    },
    archived: {
      entry: () => console.log('Document archived'),
    },
  },
});

// Usage
console.log(documentMachine.state);  // 'draft'
console.log(documentMachine.can('SUBMIT'));  // true
console.log(documentMachine.can('PUBLISH'));  // false

documentMachine.send({ type: 'SUBMIT' });  // -> 'review'
documentMachine.send({ type: 'APPROVE' });  // -> 'approved'
documentMachine.send({ type: 'PUBLISH' });  // -> 'published'
```

### Go: Connection State Machine

```go
package main

import (
    "errors"
    "fmt"
    "sync"
)

type ConnectionState int

const (
    Disconnected ConnectionState = iota
    Connecting
    Connected
    Disconnecting
)

func (s ConnectionState) String() string {
    return [...]string{"Disconnected", "Connecting", "Connected", "Disconnecting"}[s]
}

type Connection struct {
    mu    sync.RWMutex
    state ConnectionState
    addr  string
}

func NewConnection(addr string) *Connection {
    return &Connection{
        state: Disconnected,
        addr:  addr,
    }
}

func (c *Connection) State() ConnectionState {
    c.mu.RLock()
    defer c.mu.RUnlock()
    return c.state
}

func (c *Connection) Connect() error {
    c.mu.Lock()
    defer c.mu.Unlock()

    switch c.state {
    case Disconnected:
        c.state = Connecting
        // Simulate connection
        c.state = Connected
        fmt.Printf("Connected to %s\n", c.addr)
        return nil
    case Connected:
        return errors.New("already connected")
    case Connecting:
        return errors.New("connection in progress")
    case Disconnecting:
        return errors.New("disconnection in progress")
    }
    return nil
}

func (c *Connection) Disconnect() error {
    c.mu.Lock()
    defer c.mu.Unlock()

    switch c.state {
    case Connected:
        c.state = Disconnecting
        // Simulate disconnection
        c.state = Disconnected
        fmt.Printf("Disconnected from %s\n", c.addr)
        return nil
    case Disconnected:
        return errors.New("not connected")
    case Connecting:
        return errors.New("cannot disconnect while connecting")
    case Disconnecting:
        return errors.New("disconnection in progress")
    }
    return nil
}

func (c *Connection) Send(data []byte) error {
    c.mu.RLock()
    defer c.mu.RUnlock()

    if c.state != Connected {
        return fmt.Errorf("cannot send: state is %s", c.state)
    }

    fmt.Printf("Sent %d bytes to %s\n", len(data), c.addr)
    return nil
}

// Usage
func main() {
    conn := NewConnection("localhost:8080")

    fmt.Println("State:", conn.State())  // Disconnected

    conn.Connect()
    fmt.Println("State:", conn.State())  // Connected

    conn.Send([]byte("Hello"))

    conn.Disconnect()
    fmt.Println("State:", conn.State())  // Disconnected
}
```

## Chain of Responsibility

### Python: HTTP Middleware Pipeline

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Any
import time
import logging


@dataclass
class Request:
    path: str
    method: str
    headers: dict = field(default_factory=dict)
    body: Any = None
    user: dict | None = None
    start_time: float = field(default_factory=time.time)


@dataclass
class Response:
    status: int
    body: Any = None
    headers: dict = field(default_factory=dict)


Handler = Callable[[Request], Response]


class Middleware(ABC):
    def __init__(self):
        self._next: Handler | None = None

    def set_next(self, handler: Handler) -> None:
        self._next = handler

    @abstractmethod
    def handle(self, request: Request) -> Response:
        pass

    def call_next(self, request: Request) -> Response:
        if self._next:
            return self._next(request)
        return Response(status=404, body="Not Found")


class LoggingMiddleware(Middleware):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def handle(self, request: Request) -> Response:
        self.logger.info(f"{request.method} {request.path}")
        response = self.call_next(request)
        duration = time.time() - request.start_time
        self.logger.info(f"{request.method} {request.path} -> {response.status} ({duration:.3f}s)")
        return response


class AuthMiddleware(Middleware):
    def __init__(self, secret: str):
        super().__init__()
        self.secret = secret

    def handle(self, request: Request) -> Response:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")

        if not token:
            return Response(status=401, body="Unauthorized")

        # Validate token (simplified)
        if token == self.secret:
            request.user = {"id": "user_123", "role": "admin"}
            return self.call_next(request)

        return Response(status=403, body="Forbidden")


class RateLimitMiddleware(Middleware):
    def __init__(self, max_requests: int = 100):
        super().__init__()
        self.max_requests = max_requests
        self.request_counts: dict[str, int] = {}

    def handle(self, request: Request) -> Response:
        client_ip = request.headers.get("X-Forwarded-For", "unknown")
        count = self.request_counts.get(client_ip, 0)

        if count >= self.max_requests:
            return Response(
                status=429,
                body="Too Many Requests",
                headers={"Retry-After": "60"}
            )

        self.request_counts[client_ip] = count + 1
        return self.call_next(request)


class MiddlewarePipeline:
    def __init__(self):
        self.middlewares: list[Middleware] = []
        self._handler: Handler | None = None

    def use(self, middleware: Middleware) -> "MiddlewarePipeline":
        self.middlewares.append(middleware)
        return self

    def handle(self, final_handler: Handler) -> Handler:
        self._handler = final_handler

        # Build chain in reverse
        handler = final_handler
        for middleware in reversed(self.middlewares):
            middleware.set_next(handler)
            handler = middleware.handle

        return handler


# Usage
def app_handler(request: Request) -> Response:
    return Response(
        status=200,
        body={"message": f"Hello, {request.user['id']}!"}
    )


pipeline = MiddlewarePipeline()
pipeline.use(LoggingMiddleware())
pipeline.use(RateLimitMiddleware(max_requests=100))
pipeline.use(AuthMiddleware(secret="secret-token"))

handler = pipeline.handle(app_handler)

# Test request
request = Request(
    path="/api/users",
    method="GET",
    headers={"Authorization": "Bearer secret-token", "X-Forwarded-For": "192.168.1.1"}
)

response = handler(request)
print(f"Status: {response.status}, Body: {response.body}")
```

### TypeScript: Validation Chain

```typescript
interface ValidationResult {
  valid: boolean;
  errors: string[];
}

interface Validator<T> {
  validate(data: T): ValidationResult;
  setNext(validator: Validator<T>): Validator<T>;
}

abstract class BaseValidator<T> implements Validator<T> {
  private next?: Validator<T>;

  setNext(validator: Validator<T>): Validator<T> {
    this.next = validator;
    return validator;
  }

  validate(data: T): ValidationResult {
    const result = this.doValidate(data);

    if (!result.valid) {
      return result;
    }

    if (this.next) {
      const nextResult = this.next.validate(data);
      return {
        valid: nextResult.valid,
        errors: [...result.errors, ...nextResult.errors]
      };
    }

    return result;
  }

  protected abstract doValidate(data: T): ValidationResult;
}

// User validation example
interface UserInput {
  email: string;
  password: string;
  age: number;
}

class EmailValidator extends BaseValidator<UserInput> {
  protected doValidate(data: UserInput): ValidationResult {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(data.email)) {
      return { valid: false, errors: ['Invalid email format'] };
    }

    return { valid: true, errors: [] };
  }
}

class PasswordValidator extends BaseValidator<UserInput> {
  protected doValidate(data: UserInput): ValidationResult {
    const errors: string[] = [];

    if (data.password.length < 8) {
      errors.push('Password must be at least 8 characters');
    }

    if (!/[A-Z]/.test(data.password)) {
      errors.push('Password must contain uppercase letter');
    }

    if (!/[0-9]/.test(data.password)) {
      errors.push('Password must contain a number');
    }

    return { valid: errors.length === 0, errors };
  }
}

class AgeValidator extends BaseValidator<UserInput> {
  constructor(private minAge: number = 18) {
    super();
  }

  protected doValidate(data: UserInput): ValidationResult {
    if (data.age < this.minAge) {
      return {
        valid: false,
        errors: [`Must be at least ${this.minAge} years old`]
      };
    }
    return { valid: true, errors: [] };
  }
}

// Build validation chain
function createUserValidator(): Validator<UserInput> {
  const email = new EmailValidator();
  const password = new PasswordValidator();
  const age = new AgeValidator(18);

  email.setNext(password).setNext(age);

  return email;
}

// Usage
const validator = createUserValidator();

const validUser = {
  email: 'user@example.com',
  password: 'SecurePass123',
  age: 25
};
console.log(validator.validate(validUser));
// { valid: true, errors: [] }

const invalidUser = {
  email: 'invalid',
  password: 'weak',
  age: 16
};
console.log(validator.validate(invalidUser));
// { valid: false, errors: ['Invalid email format'] }
```

### Go: Request Handler Chain

```go
package main

import (
    "context"
    "fmt"
    "net/http"
)

type Handler interface {
    Handle(ctx context.Context, r *http.Request) (*http.Response, error)
    SetNext(handler Handler)
}

type BaseHandler struct {
    next Handler
}

func (h *BaseHandler) SetNext(handler Handler) {
    h.next = handler
}

func (h *BaseHandler) HandleNext(ctx context.Context, r *http.Request) (*http.Response, error) {
    if h.next != nil {
        return h.next.Handle(ctx, r)
    }
    return nil, fmt.Errorf("no handler available")
}

// Authentication handler
type AuthHandler struct {
    BaseHandler
    apiKey string
}

func NewAuthHandler(apiKey string) *AuthHandler {
    return &AuthHandler{apiKey: apiKey}
}

func (h *AuthHandler) Handle(ctx context.Context, r *http.Request) (*http.Response, error) {
    key := r.Header.Get("X-API-Key")
    if key != h.apiKey {
        return &http.Response{StatusCode: 401}, nil
    }

    // Add user to context
    ctx = context.WithValue(ctx, "user", "authenticated")
    return h.HandleNext(ctx, r)
}

// Logging handler
type LogHandler struct {
    BaseHandler
}

func (h *LogHandler) Handle(ctx context.Context, r *http.Request) (*http.Response, error) {
    fmt.Printf("[LOG] %s %s\n", r.Method, r.URL.Path)
    return h.HandleNext(ctx, r)
}

// Cache handler
type CacheHandler struct {
    BaseHandler
    cache map[string]*http.Response
}

func NewCacheHandler() *CacheHandler {
    return &CacheHandler{cache: make(map[string]*http.Response)}
}

func (h *CacheHandler) Handle(ctx context.Context, r *http.Request) (*http.Response, error) {
    if r.Method == "GET" {
        if cached, ok := h.cache[r.URL.Path]; ok {
            fmt.Println("[CACHE] Hit:", r.URL.Path)
            return cached, nil
        }
    }

    resp, err := h.HandleNext(ctx, r)
    if err == nil && r.Method == "GET" && resp.StatusCode == 200 {
        h.cache[r.URL.Path] = resp
    }
    return resp, err
}

// Final handler
type APIHandler struct {
    BaseHandler
}

func (h *APIHandler) Handle(ctx context.Context, r *http.Request) (*http.Response, error) {
    return &http.Response{StatusCode: 200}, nil
}

// Build chain
func BuildChain(apiKey string) Handler {
    auth := NewAuthHandler(apiKey)
    log := &LogHandler{}
    cache := NewCacheHandler()
    api := &APIHandler{}

    auth.SetNext(log)
    log.SetNext(cache)
    cache.SetNext(api)

    return auth
}

func main() {
    chain := BuildChain("secret-key")

    req, _ := http.NewRequest("GET", "/api/users", nil)
    req.Header.Set("X-API-Key", "secret-key")

    ctx := context.Background()
    resp, err := chain.Handle(ctx, req)

    if err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("Response status:", resp.StatusCode)
    }
}
```

## Template Method

### Python: Data Export Framework

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
import json
import csv
import io


@dataclass
class ExportConfig:
    include_headers: bool = True
    pretty_print: bool = False
    encoding: str = "utf-8"


class DataExporter(ABC):
    """Template Method pattern for data export."""

    def export(self, data: list[dict], config: ExportConfig | None = None) -> str:
        """Template method - defines the algorithm skeleton."""
        config = config or ExportConfig()

        # Step 1: Validate data (hook - can be overridden)
        self.validate(data)

        # Step 2: Transform data (hook - can be overridden)
        transformed = self.transform(data)

        # Step 3: Format data (abstract - must be implemented)
        formatted = self.format(transformed, config)

        # Step 4: Post-process (hook - can be overridden)
        result = self.post_process(formatted, config)

        return result

    def validate(self, data: list[dict]) -> None:
        """Hook: validate data before export. Override if needed."""
        if not data:
            raise ValueError("No data to export")

    def transform(self, data: list[dict]) -> list[dict]:
        """Hook: transform data before formatting. Override if needed."""
        return data

    @abstractmethod
    def format(self, data: list[dict], config: ExportConfig) -> str:
        """Abstract: format data to target format. Must implement."""
        pass

    def post_process(self, output: str, config: ExportConfig) -> str:
        """Hook: post-process output. Override if needed."""
        return output


class JSONExporter(DataExporter):
    def format(self, data: list[dict], config: ExportConfig) -> str:
        indent = 2 if config.pretty_print else None
        return json.dumps(data, indent=indent, ensure_ascii=False)


class CSVExporter(DataExporter):
    def format(self, data: list[dict], config: ExportConfig) -> str:
        if not data:
            return ""

        output = io.StringIO()
        fieldnames = list(data[0].keys())

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        if config.include_headers:
            writer.writeheader()
        writer.writerows(data)

        return output.getvalue()


class XMLExporter(DataExporter):
    def format(self, data: list[dict], config: ExportConfig) -> str:
        indent = "  " if config.pretty_print else ""
        newline = "\n" if config.pretty_print else ""

        lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        lines.append(f"<items>{newline}")

        for item in data:
            lines.append(f"{indent}<item>{newline}")
            for key, value in item.items():
                lines.append(f"{indent}{indent}<{key}>{value}</{key}>{newline}")
            lines.append(f"{indent}</item>{newline}")

        lines.append("</items>")
        return "".join(lines)


class SanitizedJSONExporter(JSONExporter):
    """Extended exporter with custom transform step."""

    SENSITIVE_FIELDS = {"password", "ssn", "credit_card"}

    def transform(self, data: list[dict]) -> list[dict]:
        """Override transform to sanitize sensitive data."""
        return [
            {k: "***" if k in self.SENSITIVE_FIELDS else v
             for k, v in item.items()}
            for item in data
        ]


# Usage
data = [
    {"id": 1, "name": "Alice", "email": "alice@test.com", "password": "secret123"},
    {"id": 2, "name": "Bob", "email": "bob@test.com", "password": "password456"},
]

config = ExportConfig(pretty_print=True)

json_exporter = JSONExporter()
print(json_exporter.export(data, config))

csv_exporter = CSVExporter()
print(csv_exporter.export(data))

sanitized = SanitizedJSONExporter()
print(sanitized.export(data, config))  # Passwords are masked
```

### TypeScript: Report Generator

```typescript
interface ReportData {
  title: string;
  data: Record<string, unknown>[];
  generatedAt: Date;
}

abstract class ReportGenerator {
  // Template method
  generate(data: Record<string, unknown>[]): string {
    const reportData = this.prepareData(data);
    const header = this.generateHeader(reportData);
    const body = this.generateBody(reportData);
    const footer = this.generateFooter(reportData);

    return this.assemble(header, body, footer);
  }

  // Hook: can be overridden
  protected prepareData(data: Record<string, unknown>[]): ReportData {
    return {
      title: 'Report',
      data,
      generatedAt: new Date()
    };
  }

  // Abstract: must be implemented
  protected abstract generateHeader(data: ReportData): string;
  protected abstract generateBody(data: ReportData): string;

  // Hook: default implementation
  protected generateFooter(data: ReportData): string {
    return `Generated at: ${data.generatedAt.toISOString()}`;
  }

  // Hook: can be overridden
  protected assemble(header: string, body: string, footer: string): string {
    return `${header}\n\n${body}\n\n${footer}`;
  }
}

class HTMLReportGenerator extends ReportGenerator {
  protected generateHeader(data: ReportData): string {
    return `
<!DOCTYPE html>
<html>
<head><title>${data.title}</title></head>
<body>
<h1>${data.title}</h1>`;
  }

  protected generateBody(data: ReportData): string {
    if (data.data.length === 0) return '<p>No data</p>';

    const headers = Object.keys(data.data[0]);
    const headerRow = headers.map(h => `<th>${h}</th>`).join('');

    const rows = data.data.map(row => {
      const cells = headers.map(h => `<td>${row[h]}</td>`).join('');
      return `<tr>${cells}</tr>`;
    }).join('\n');

    return `
<table>
  <thead><tr>${headerRow}</tr></thead>
  <tbody>${rows}</tbody>
</table>`;
  }

  protected generateFooter(data: ReportData): string {
    return `
<footer>
  <p>Generated: ${data.generatedAt.toLocaleDateString()}</p>
</footer>
</body>
</html>`;
  }

  protected assemble(header: string, body: string, footer: string): string {
    return header + body + footer;
  }
}

class MarkdownReportGenerator extends ReportGenerator {
  protected generateHeader(data: ReportData): string {
    return `# ${data.title}\n`;
  }

  protected generateBody(data: ReportData): string {
    if (data.data.length === 0) return '_No data_\n';

    const headers = Object.keys(data.data[0]);
    const headerRow = `| ${headers.join(' | ')} |`;
    const separator = `| ${headers.map(() => '---').join(' | ')} |`;

    const rows = data.data.map(row =>
      `| ${headers.map(h => row[h]).join(' | ')} |`
    ).join('\n');

    return `${headerRow}\n${separator}\n${rows}`;
  }
}

// Usage
const salesData = [
  { product: 'Widget A', quantity: 100, revenue: 5000 },
  { product: 'Widget B', quantity: 75, revenue: 3750 },
];

const htmlReport = new HTMLReportGenerator();
console.log(htmlReport.generate(salesData));

const mdReport = new MarkdownReportGenerator();
console.log(mdReport.generate(salesData));
```

## Visitor Pattern

### Python: AST Visitor for Code Analysis

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol


class ASTVisitor(Protocol):
    def visit_function(self, node: "FunctionNode") -> None: ...
    def visit_class(self, node: "ClassNode") -> None: ...
    def visit_variable(self, node: "VariableNode") -> None: ...
    def visit_call(self, node: "CallNode") -> None: ...


class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor: ASTVisitor) -> None:
        pass


@dataclass
class FunctionNode(ASTNode):
    name: str
    params: list[str]
    body: list[ASTNode] = field(default_factory=list)

    def accept(self, visitor: ASTVisitor) -> None:
        visitor.visit_function(self)
        for node in self.body:
            node.accept(visitor)


@dataclass
class ClassNode(ASTNode):
    name: str
    methods: list[FunctionNode] = field(default_factory=list)

    def accept(self, visitor: ASTVisitor) -> None:
        visitor.visit_class(self)
        for method in self.methods:
            method.accept(visitor)


@dataclass
class VariableNode(ASTNode):
    name: str
    value: str | None = None

    def accept(self, visitor: ASTVisitor) -> None:
        visitor.visit_variable(self)


@dataclass
class CallNode(ASTNode):
    function_name: str
    args: list[str] = field(default_factory=list)

    def accept(self, visitor: ASTVisitor) -> None:
        visitor.visit_call(self)


# Concrete visitors
class MetricsVisitor:
    """Collects code metrics."""

    def __init__(self):
        self.function_count = 0
        self.class_count = 0
        self.variable_count = 0
        self.call_count = 0

    def visit_function(self, node: FunctionNode) -> None:
        self.function_count += 1

    def visit_class(self, node: ClassNode) -> None:
        self.class_count += 1

    def visit_variable(self, node: VariableNode) -> None:
        self.variable_count += 1

    def visit_call(self, node: CallNode) -> None:
        self.call_count += 1

    def report(self) -> dict:
        return {
            "functions": self.function_count,
            "classes": self.class_count,
            "variables": self.variable_count,
            "calls": self.call_count,
        }


class DependencyVisitor:
    """Collects function call dependencies."""

    def __init__(self):
        self.current_function: str | None = None
        self.dependencies: dict[str, set[str]] = {}

    def visit_function(self, node: FunctionNode) -> None:
        self.current_function = node.name
        self.dependencies[node.name] = set()

    def visit_class(self, node: ClassNode) -> None:
        pass

    def visit_variable(self, node: VariableNode) -> None:
        pass

    def visit_call(self, node: CallNode) -> None:
        if self.current_function:
            self.dependencies[self.current_function].add(node.function_name)

    def get_dependencies(self) -> dict[str, list[str]]:
        return {k: list(v) for k, v in self.dependencies.items()}


class PrintVisitor:
    """Pretty prints the AST."""

    def __init__(self):
        self.indent = 0

    def _print(self, text: str):
        print("  " * self.indent + text)

    def visit_function(self, node: FunctionNode) -> None:
        self._print(f"Function: {node.name}({', '.join(node.params)})")
        self.indent += 1

    def visit_class(self, node: ClassNode) -> None:
        self._print(f"Class: {node.name}")
        self.indent += 1

    def visit_variable(self, node: VariableNode) -> None:
        self._print(f"Variable: {node.name} = {node.value}")

    def visit_call(self, node: CallNode) -> None:
        self._print(f"Call: {node.function_name}({', '.join(node.args)})")


# Usage
ast = ClassNode(
    name="Calculator",
    methods=[
        FunctionNode(
            name="add",
            params=["a", "b"],
            body=[
                VariableNode(name="result", value="a + b"),
                CallNode(function_name="log", args=["result"]),
            ]
        ),
        FunctionNode(
            name="multiply",
            params=["a", "b"],
            body=[
                CallNode(function_name="add", args=["a", "b"]),
                VariableNode(name="result", value="a * b"),
            ]
        ),
    ]
)

# Apply different visitors
metrics = MetricsVisitor()
ast.accept(metrics)
print("Metrics:", metrics.report())

deps = DependencyVisitor()
ast.accept(deps)
print("Dependencies:", deps.get_dependencies())

print("\nAST Structure:")
printer = PrintVisitor()
ast.accept(printer)
```

### TypeScript: Document Element Visitor

```typescript
// Element hierarchy
interface DocumentElement {
  accept(visitor: DocumentVisitor): void;
}

class Paragraph implements DocumentElement {
  constructor(public text: string) {}

  accept(visitor: DocumentVisitor): void {
    visitor.visitParagraph(this);
  }
}

class Heading implements DocumentElement {
  constructor(public level: number, public text: string) {}

  accept(visitor: DocumentVisitor): void {
    visitor.visitHeading(this);
  }
}

class Image implements DocumentElement {
  constructor(public src: string, public alt: string) {}

  accept(visitor: DocumentVisitor): void {
    visitor.visitImage(this);
  }
}

class Table implements DocumentElement {
  constructor(
    public headers: string[],
    public rows: string[][]
  ) {}

  accept(visitor: DocumentVisitor): void {
    visitor.visitTable(this);
  }
}

class Document implements DocumentElement {
  constructor(public elements: DocumentElement[]) {}

  accept(visitor: DocumentVisitor): void {
    visitor.visitDocument(this);
    for (const element of this.elements) {
      element.accept(visitor);
    }
  }
}

// Visitor interface
interface DocumentVisitor {
  visitDocument(doc: Document): void;
  visitParagraph(p: Paragraph): void;
  visitHeading(h: Heading): void;
  visitImage(img: Image): void;
  visitTable(t: Table): void;
}

// HTML renderer
class HTMLRenderer implements DocumentVisitor {
  private output: string[] = [];

  visitDocument(doc: Document): void {
    this.output.push('<!DOCTYPE html>\n<html><body>');
  }

  visitParagraph(p: Paragraph): void {
    this.output.push(`<p>${this.escape(p.text)}</p>`);
  }

  visitHeading(h: Heading): void {
    this.output.push(`<h${h.level}>${this.escape(h.text)}</h${h.level}>`);
  }

  visitImage(img: Image): void {
    this.output.push(`<img src="${img.src}" alt="${this.escape(img.alt)}">`);
  }

  visitTable(t: Table): void {
    const headers = t.headers.map(h => `<th>${this.escape(h)}</th>`).join('');
    const rows = t.rows.map(row =>
      `<tr>${row.map(c => `<td>${this.escape(c)}</td>`).join('')}</tr>`
    ).join('');

    this.output.push(`<table><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table>`);
  }

  private escape(text: string): string {
    return text.replace(/[<>&"]/g, c => ({
      '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;'
    })[c] || c);
  }

  getOutput(): string {
    return this.output.join('\n') + '\n</body></html>';
  }
}

// Markdown renderer
class MarkdownRenderer implements DocumentVisitor {
  private output: string[] = [];

  visitDocument(doc: Document): void {
    // No header needed for Markdown
  }

  visitParagraph(p: Paragraph): void {
    this.output.push(`${p.text}\n`);
  }

  visitHeading(h: Heading): void {
    this.output.push(`${'#'.repeat(h.level)} ${h.text}\n`);
  }

  visitImage(img: Image): void {
    this.output.push(`![${img.alt}](${img.src})\n`);
  }

  visitTable(t: Table): void {
    const headers = `| ${t.headers.join(' | ')} |`;
    const separator = `| ${t.headers.map(() => '---').join(' | ')} |`;
    const rows = t.rows.map(row => `| ${row.join(' | ')} |`).join('\n');

    this.output.push(`${headers}\n${separator}\n${rows}\n`);
  }

  getOutput(): string {
    return this.output.join('\n');
  }
}

// Word count visitor
class WordCountVisitor implements DocumentVisitor {
  private count = 0;

  visitDocument(doc: Document): void {}

  visitParagraph(p: Paragraph): void {
    this.count += this.countWords(p.text);
  }

  visitHeading(h: Heading): void {
    this.count += this.countWords(h.text);
  }

  visitImage(img: Image): void {
    this.count += this.countWords(img.alt);
  }

  visitTable(t: Table): void {
    this.count += t.headers.reduce((sum, h) => sum + this.countWords(h), 0);
    this.count += t.rows.flat().reduce((sum, c) => sum + this.countWords(c), 0);
  }

  private countWords(text: string): number {
    return text.trim().split(/\s+/).filter(w => w.length > 0).length;
  }

  getCount(): number {
    return this.count;
  }
}

// Usage
const doc = new Document([
  new Heading(1, 'Welcome'),
  new Paragraph('This is a sample document with multiple elements.'),
  new Image('/img/logo.png', 'Company Logo'),
  new Table(
    ['Name', 'Role'],
    [['Alice', 'Developer'], ['Bob', 'Designer']]
  ),
]);

const htmlRenderer = new HTMLRenderer();
doc.accept(htmlRenderer);
console.log(htmlRenderer.getOutput());

const mdRenderer = new MarkdownRenderer();
doc.accept(mdRenderer);
console.log(mdRenderer.getOutput());

const wordCounter = new WordCountVisitor();
doc.accept(wordCounter);
console.log('Word count:', wordCounter.getCount());
```

## Iterator Pattern

### Go: Custom Collection Iterator

```go
package main

import (
    "fmt"
)

// Generic iterator interface
type Iterator[T any] interface {
    HasNext() bool
    Next() T
    Reset()
}

// Collection interface
type Iterable[T any] interface {
    Iterator() Iterator[T]
    ReverseIterator() Iterator[T]
}

// User type
type User struct {
    ID    int
    Name  string
    Email string
}

// User collection
type UserCollection struct {
    users []User
}

func NewUserCollection(users ...User) *UserCollection {
    return &UserCollection{users: users}
}

func (c *UserCollection) Add(user User) {
    c.users = append(c.users, user)
}

func (c *UserCollection) Iterator() Iterator[User] {
    return &UserIterator{
        collection: c,
        index:      0,
    }
}

func (c *UserCollection) ReverseIterator() Iterator[User] {
    return &ReverseUserIterator{
        collection: c,
        index:      len(c.users) - 1,
    }
}

// Forward iterator
type UserIterator struct {
    collection *UserCollection
    index      int
}

func (i *UserIterator) HasNext() bool {
    return i.index < len(i.collection.users)
}

func (i *UserIterator) Next() User {
    user := i.collection.users[i.index]
    i.index++
    return user
}

func (i *UserIterator) Reset() {
    i.index = 0
}

// Reverse iterator
type ReverseUserIterator struct {
    collection *UserCollection
    index      int
}

func (i *ReverseUserIterator) HasNext() bool {
    return i.index >= 0
}

func (i *ReverseUserIterator) Next() User {
    user := i.collection.users[i.index]
    i.index--
    return user
}

func (i *ReverseUserIterator) Reset() {
    i.index = len(i.collection.users) - 1
}

// Filtered iterator
type FilteredIterator[T any] struct {
    inner     Iterator[T]
    predicate func(T) bool
    current   T
    hasValue  bool
}

func NewFilteredIterator[T any](iter Iterator[T], pred func(T) bool) *FilteredIterator[T] {
    fi := &FilteredIterator[T]{
        inner:     iter,
        predicate: pred,
    }
    fi.advance()
    return fi
}

func (i *FilteredIterator[T]) advance() {
    for i.inner.HasNext() {
        item := i.inner.Next()
        if i.predicate(item) {
            i.current = item
            i.hasValue = true
            return
        }
    }
    i.hasValue = false
}

func (i *FilteredIterator[T]) HasNext() bool {
    return i.hasValue
}

func (i *FilteredIterator[T]) Next() T {
    result := i.current
    i.advance()
    return result
}

func (i *FilteredIterator[T]) Reset() {
    i.inner.Reset()
    i.advance()
}

func main() {
    users := NewUserCollection(
        User{1, "Alice", "alice@test.com"},
        User{2, "Bob", "bob@test.com"},
        User{3, "Charlie", "charlie@test.com"},
    )

    // Forward iteration
    fmt.Println("Forward:")
    iter := users.Iterator()
    for iter.HasNext() {
        user := iter.Next()
        fmt.Printf("  %d: %s\n", user.ID, user.Name)
    }

    // Reverse iteration
    fmt.Println("\nReverse:")
    revIter := users.ReverseIterator()
    for revIter.HasNext() {
        user := revIter.Next()
        fmt.Printf("  %d: %s\n", user.ID, user.Name)
    }

    // Filtered iteration
    fmt.Println("\nFiltered (ID > 1):")
    filteredIter := NewFilteredIterator(users.Iterator(), func(u User) bool {
        return u.ID > 1
    })
    for filteredIter.HasNext() {
        user := filteredIter.Next()
        fmt.Printf("  %d: %s\n", user.ID, user.Name)
    }
}
```

## Mediator Pattern

### Python: Chat Room

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol


class ChatMediator(Protocol):
    def send_message(self, message: str, sender: "User") -> None: ...
    def send_private(self, message: str, sender: "User", recipient: str) -> None: ...


@dataclass
class Message:
    content: str
    sender: str
    timestamp: datetime = field(default_factory=datetime.now)
    private: bool = False
    recipient: str | None = None


class User:
    def __init__(self, name: str, mediator: ChatMediator):
        self.name = name
        self.mediator = mediator
        self.messages: list[Message] = []

    def send(self, message: str) -> None:
        self.mediator.send_message(message, self)

    def send_private(self, message: str, recipient: str) -> None:
        self.mediator.send_private(message, self, recipient)

    def receive(self, message: Message) -> None:
        self.messages.append(message)
        prefix = f"[PRIVATE from {message.sender}]" if message.private else f"[{message.sender}]"
        print(f"{self.name} received: {prefix} {message.content}")


class ChatRoom:
    def __init__(self):
        self.users: dict[str, User] = {}
        self.message_history: list[Message] = []

    def join(self, user: User) -> None:
        self.users[user.name] = user
        self.broadcast(f"{user.name} joined the chat", system=True)

    def leave(self, user: User) -> None:
        if user.name in self.users:
            del self.users[user.name]
            self.broadcast(f"{user.name} left the chat", system=True)

    def send_message(self, message: str, sender: User) -> None:
        msg = Message(content=message, sender=sender.name)
        self.message_history.append(msg)

        for name, user in self.users.items():
            if name != sender.name:
                user.receive(msg)

    def send_private(self, message: str, sender: User, recipient: str) -> None:
        if recipient in self.users:
            msg = Message(
                content=message,
                sender=sender.name,
                private=True,
                recipient=recipient
            )
            self.message_history.append(msg)
            self.users[recipient].receive(msg)
        else:
            print(f"User {recipient} not found")

    def broadcast(self, message: str, system: bool = False) -> None:
        msg = Message(content=message, sender="SYSTEM" if system else "")
        for user in self.users.values():
            user.receive(msg)


# Usage
chat = ChatRoom()

alice = User("Alice", chat)
bob = User("Bob", chat)
charlie = User("Charlie", chat)

chat.join(alice)
chat.join(bob)
chat.join(charlie)

alice.send("Hello everyone!")
bob.send_private("Hey Alice, how are you?", "Alice")
charlie.send("Good morning!")

chat.leave(bob)
```

## Related

- [README.md](README.md) - Pattern overview and selection guide
- [templates.md](templates.md) - Copy-paste templates
- [llm-prompts.md](llm-prompts.md) - Prompts for LLM-assisted design
