# Design Pattern Templates

Copy-paste templates for implementing design patterns across languages.

## Creational Patterns

### Factory Method

#### Python

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class Product(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass

class ConcreteProductA(Product):
    def operation(self) -> str:
        return "ProductA operation"

class ConcreteProductB(Product):
    def operation(self) -> str:
        return "ProductB operation"

class Creator(ABC):
    @abstractmethod
    def factory_method(self) -> Product:
        pass

    def some_operation(self) -> str:
        product = self.factory_method()
        return f"Creator: {product.operation()}"

class ConcreteCreatorA(Creator):
    def factory_method(self) -> Product:
        return ConcreteProductA()

class ConcreteCreatorB(Creator):
    def factory_method(self) -> Product:
        return ConcreteProductB()
```

#### TypeScript

```typescript
interface Product {
    operation(): string;
}

class ConcreteProductA implements Product {
    operation(): string {
        return "ProductA operation";
    }
}

class ConcreteProductB implements Product {
    operation(): string {
        return "ProductB operation";
    }
}

abstract class Creator {
    abstract factoryMethod(): Product;

    someOperation(): string {
        const product = this.factoryMethod();
        return `Creator: ${product.operation()}`;
    }
}

class ConcreteCreatorA extends Creator {
    factoryMethod(): Product {
        return new ConcreteProductA();
    }
}

class ConcreteCreatorB extends Creator {
    factoryMethod(): Product {
        return new ConcreteProductB();
    }
}
```

#### Go

```go
package factory

type Product interface {
    Operation() string
}

type ConcreteProductA struct{}

func (p *ConcreteProductA) Operation() string {
    return "ProductA operation"
}

type ConcreteProductB struct{}

func (p *ConcreteProductB) Operation() string {
    return "ProductB operation"
}

type Creator interface {
    FactoryMethod() Product
}

func NewProduct(productType string) Product {
    switch productType {
    case "A":
        return &ConcreteProductA{}
    case "B":
        return &ConcreteProductB{}
    default:
        return nil
    }
}
```

### Builder

#### Python

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Product:
    parts: List[str] = field(default_factory=list)

class Builder(ABC):
    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def build_part_a(self) -> Builder:
        pass

    @abstractmethod
    def build_part_b(self) -> Builder:
        pass

    @abstractmethod
    def build_part_c(self) -> Builder:
        pass

    @abstractmethod
    def get_result(self) -> Product:
        pass

class ConcreteBuilder(Builder):
    def __init__(self) -> None:
        self._product: Product = Product()

    def reset(self) -> None:
        self._product = Product()

    def build_part_a(self) -> Builder:
        self._product.parts.append("PartA")
        return self

    def build_part_b(self) -> Builder:
        self._product.parts.append("PartB")
        return self

    def build_part_c(self) -> Builder:
        self._product.parts.append("PartC")
        return self

    def get_result(self) -> Product:
        result = self._product
        self.reset()
        return result

# Usage with fluent interface
builder = ConcreteBuilder()
product = (builder
    .build_part_a()
    .build_part_b()
    .build_part_c()
    .get_result())
```

#### TypeScript

```typescript
interface Builder<T> {
    reset(): void;
    getResult(): T;
}

class Product {
    parts: string[] = [];
}

class ProductBuilder implements Builder<Product> {
    private product: Product = new Product();

    reset(): void {
        this.product = new Product();
    }

    buildPartA(): ProductBuilder {
        this.product.parts.push("PartA");
        return this;
    }

    buildPartB(): ProductBuilder {
        this.product.parts.push("PartB");
        return this;
    }

    buildPartC(): ProductBuilder {
        this.product.parts.push("PartC");
        return this;
    }

    getResult(): Product {
        const result = this.product;
        this.reset();
        return result;
    }
}

// Usage
const product = new ProductBuilder()
    .buildPartA()
    .buildPartB()
    .buildPartC()
    .getResult();
```

### Singleton

#### Python (Thread-Safe)

```python
import threading
from typing import Optional

class Singleton:
    _instance: Optional['Singleton'] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> 'Singleton':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Initialize only once
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # Your initialization code here
```

#### TypeScript

```typescript
class Singleton {
    private static instance: Singleton;

    private constructor() {
        // Private constructor prevents direct instantiation
    }

    static getInstance(): Singleton {
        if (!Singleton.instance) {
            Singleton.instance = new Singleton();
        }
        return Singleton.instance;
    }
}

// Modern alternative: Module pattern
// config.ts
const config = {
    apiUrl: process.env.API_URL,
    debug: process.env.DEBUG === 'true',
};
export default config;
```

## Structural Patterns

### Adapter

#### Python

```python
from typing import Protocol

# Target interface (what client expects)
class Target(Protocol):
    def request(self) -> str:
        ...

# Adaptee (incompatible interface)
class Adaptee:
    def specific_request(self) -> str:
        return "Adaptee's specific behavior"

# Adapter (makes Adaptee work with Target)
class Adapter:
    def __init__(self, adaptee: Adaptee) -> None:
        self._adaptee = adaptee

    def request(self) -> str:
        return f"Adapter: {self._adaptee.specific_request()}"

# Usage
adaptee = Adaptee()
adapter = Adapter(adaptee)
result = adapter.request()
```

#### TypeScript

```typescript
// Target interface
interface Target {
    request(): string;
}

// Adaptee
class Adaptee {
    specificRequest(): string {
        return "Adaptee's specific behavior";
    }
}

// Adapter
class Adapter implements Target {
    constructor(private adaptee: Adaptee) {}

    request(): string {
        return `Adapter: ${this.adaptee.specificRequest()}`;
    }
}
```

### Decorator

#### Python

```python
from abc import ABC, abstractmethod
from typing import Protocol

class Component(Protocol):
    def operation(self) -> str:
        ...

class ConcreteComponent:
    def operation(self) -> str:
        return "ConcreteComponent"

class Decorator(ABC):
    def __init__(self, component: Component) -> None:
        self._component = component

    @abstractmethod
    def operation(self) -> str:
        pass

class ConcreteDecoratorA(Decorator):
    def operation(self) -> str:
        return f"DecoratorA({self._component.operation()})"

class ConcreteDecoratorB(Decorator):
    def operation(self) -> str:
        return f"DecoratorB({self._component.operation()})"

# Usage: Stack decorators
component = ConcreteComponent()
decorated = ConcreteDecoratorA(ConcreteDecoratorB(component))
print(decorated.operation())  # DecoratorA(DecoratorB(ConcreteComponent))
```

#### TypeScript (Function-based)

```typescript
// Modern functional approach
type Handler<T, R> = (input: T) => R;

function withLogging<T, R>(handler: Handler<T, R>): Handler<T, R> {
    return (input: T): R => {
        console.log(`Input: ${JSON.stringify(input)}`);
        const result = handler(input);
        console.log(`Output: ${JSON.stringify(result)}`);
        return result;
    };
}

function withTiming<T, R>(handler: Handler<T, R>): Handler<T, R> {
    return (input: T): R => {
        const start = performance.now();
        const result = handler(input);
        console.log(`Duration: ${performance.now() - start}ms`);
        return result;
    };
}

// Usage: Compose decorators
const processData = (data: number[]): number => data.reduce((a, b) => a + b, 0);
const decoratedProcess = withLogging(withTiming(processData));
```

### Facade

#### Python

```python
class SubsystemA:
    def operation_a1(self) -> str:
        return "SubsystemA: operation_a1"

    def operation_a2(self) -> str:
        return "SubsystemA: operation_a2"

class SubsystemB:
    def operation_b1(self) -> str:
        return "SubsystemB: operation_b1"

class SubsystemC:
    def operation_c1(self) -> str:
        return "SubsystemC: operation_c1"

class Facade:
    def __init__(self) -> None:
        self._subsystem_a = SubsystemA()
        self._subsystem_b = SubsystemB()
        self._subsystem_c = SubsystemC()

    def operation(self) -> str:
        """Simplified interface to complex subsystems"""
        results = []
        results.append(self._subsystem_a.operation_a1())
        results.append(self._subsystem_b.operation_b1())
        results.append(self._subsystem_c.operation_c1())
        return "\n".join(results)

# Usage
facade = Facade()
print(facade.operation())
```

## Behavioral Patterns

### Strategy

#### Python

```python
from typing import Protocol, List

class SortStrategy(Protocol):
    def sort(self, data: List[int]) -> List[int]:
        ...

class QuickSort:
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class MergeSort:
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self._merge(left, right)

    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

class Sorter:
    def __init__(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def sort(self, data: List[int]) -> List[int]:
        return self._strategy.sort(data)

# Usage
sorter = Sorter(QuickSort())
result = sorter.sort([3, 1, 4, 1, 5, 9, 2, 6])
sorter.set_strategy(MergeSort())
result = sorter.sort([3, 1, 4, 1, 5, 9, 2, 6])
```

#### TypeScript (Functional)

```typescript
// Modern functional approach
type SortStrategy<T> = (data: T[]) => T[];

const quickSort: SortStrategy<number> = (data) => {
    if (data.length <= 1) return data;
    const pivot = data[Math.floor(data.length / 2)];
    const left = data.filter(x => x < pivot);
    const middle = data.filter(x => x === pivot);
    const right = data.filter(x => x > pivot);
    return [...quickSort(left), ...middle, ...quickSort(right)];
};

const bubbleSort: SortStrategy<number> = (data) => {
    const arr = [...data];
    for (let i = 0; i < arr.length; i++) {
        for (let j = 0; j < arr.length - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
            }
        }
    }
    return arr;
};

// Usage: Strategy as function parameter
function processData(data: number[], sortStrategy: SortStrategy<number>): number[] {
    return sortStrategy(data);
}

const result = processData([3, 1, 4, 1, 5], quickSort);
```

### Observer

#### Python

```python
from abc import ABC, abstractmethod
from typing import List, Any

class Observer(ABC):
    @abstractmethod
    def update(self, subject: 'Subject', *args: Any, **kwargs: Any) -> None:
        pass

class Subject:
    def __init__(self) -> None:
        self._observers: List[Observer] = []
        self._state: Any = None

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, *args: Any, **kwargs: Any) -> None:
        for observer in self._observers:
            observer.update(self, *args, **kwargs)

    @property
    def state(self) -> Any:
        return self._state

    @state.setter
    def state(self, value: Any) -> None:
        self._state = value
        self.notify()

class ConcreteObserverA(Observer):
    def update(self, subject: Subject, *args: Any, **kwargs: Any) -> None:
        print(f"ObserverA reacted to state: {subject.state}")

class ConcreteObserverB(Observer):
    def update(self, subject: Subject, *args: Any, **kwargs: Any) -> None:
        print(f"ObserverB reacted to state: {subject.state}")

# Usage
subject = Subject()
subject.attach(ConcreteObserverA())
subject.attach(ConcreteObserverB())
subject.state = "new state"  # Both observers notified
```

#### TypeScript (Event Emitter)

```typescript
type EventHandler<T> = (data: T) => void;

class EventEmitter<Events extends Record<string, any>> {
    private handlers = new Map<keyof Events, Set<EventHandler<any>>>();

    on<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>): () => void {
        if (!this.handlers.has(event)) {
            this.handlers.set(event, new Set());
        }
        this.handlers.get(event)!.add(handler);
        return () => this.handlers.get(event)?.delete(handler);
    }

    emit<K extends keyof Events>(event: K, data: Events[K]): void {
        this.handlers.get(event)?.forEach(handler => handler(data));
    }

    once<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>): void {
        const unsubscribe = this.on(event, (data) => {
            handler(data);
            unsubscribe();
        });
    }
}

// Usage
interface AppEvents {
    'user:login': { userId: string };
    'user:logout': { userId: string };
    'data:update': { key: string; value: any };
}

const events = new EventEmitter<AppEvents>();
events.on('user:login', (data) => console.log(`User ${data.userId} logged in`));
events.emit('user:login', { userId: '123' });
```

### Command

#### Python

```python
from abc import ABC, abstractmethod
from typing import List

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

class TextEditor:
    def __init__(self) -> None:
        self.text: str = ""

    def insert(self, text: str, position: int) -> None:
        self.text = self.text[:position] + text + self.text[position:]

    def delete(self, start: int, end: int) -> str:
        deleted = self.text[start:end]
        self.text = self.text[:start] + self.text[end:]
        return deleted

class InsertCommand(Command):
    def __init__(self, editor: TextEditor, text: str, position: int) -> None:
        self.editor = editor
        self.text = text
        self.position = position

    def execute(self) -> None:
        self.editor.insert(self.text, self.position)

    def undo(self) -> None:
        self.editor.delete(self.position, self.position + len(self.text))

class DeleteCommand(Command):
    def __init__(self, editor: TextEditor, start: int, end: int) -> None:
        self.editor = editor
        self.start = start
        self.end = end
        self.deleted_text: str = ""

    def execute(self) -> None:
        self.deleted_text = self.editor.delete(self.start, self.end)

    def undo(self) -> None:
        self.editor.insert(self.deleted_text, self.start)

class CommandManager:
    def __init__(self) -> None:
        self.history: List[Command] = []
        self.redo_stack: List[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self.history.append(command)
        self.redo_stack.clear()

    def undo(self) -> None:
        if self.history:
            command = self.history.pop()
            command.undo()
            self.redo_stack.append(command)

    def redo(self) -> None:
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.history.append(command)

# Usage
editor = TextEditor()
manager = CommandManager()

manager.execute(InsertCommand(editor, "Hello", 0))
manager.execute(InsertCommand(editor, " World", 5))
print(editor.text)  # "Hello World"

manager.undo()
print(editor.text)  # "Hello"

manager.redo()
print(editor.text)  # "Hello World"
```

## Distributed Patterns

### Circuit Breaker Template

```python
import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, TypeVar, Optional, Generic

T = TypeVar('T')

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreaker(Generic[T]):
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    half_open_max_calls: int = 3

    _state: CircuitState = field(default=CircuitState.CLOSED, init=False)
    _failure_count: int = field(default=0, init=False)
    _success_count: int = field(default=0, init=False)
    _last_failure_time: float = field(default=0.0, init=False)

    def call(
        self,
        func: Callable[[], T],
        fallback: Optional[Callable[[], T]] = None
    ) -> T:
        if self._should_allow_request():
            try:
                result = func()
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                if fallback:
                    return fallback()
                raise
        else:
            if fallback:
                return fallback()
            raise CircuitOpenError("Circuit breaker is open")

    def _should_allow_request(self) -> bool:
        if self._state == CircuitState.CLOSED:
            return True
        if self._state == CircuitState.OPEN:
            if time.time() - self._last_failure_time >= self.recovery_timeout:
                self._state = CircuitState.HALF_OPEN
                self._success_count = 0
                return True
            return False
        return True  # HALF_OPEN

    def _on_success(self) -> None:
        self._failure_count = 0
        if self._state == CircuitState.HALF_OPEN:
            self._success_count += 1
            if self._success_count >= self.half_open_max_calls:
                self._state = CircuitState.CLOSED

    def _on_failure(self) -> None:
        self._failure_count += 1
        self._last_failure_time = time.time()
        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.OPEN
        elif self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN

class CircuitOpenError(Exception):
    pass
```

### Repository Template

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List
from dataclasses import dataclass

T = TypeVar('T')
ID = TypeVar('ID')

class Repository(ABC, Generic[T, ID]):
    @abstractmethod
    def find_by_id(self, id: ID) -> Optional[T]:
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        pass

    @abstractmethod
    def save(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, id: ID) -> None:
        pass

    @abstractmethod
    def exists(self, id: ID) -> bool:
        pass

# Concrete implementation
@dataclass
class User:
    id: str
    name: str
    email: str

class InMemoryUserRepository(Repository[User, str]):
    def __init__(self) -> None:
        self._storage: dict[str, User] = {}

    def find_by_id(self, id: str) -> Optional[User]:
        return self._storage.get(id)

    def find_all(self) -> List[User]:
        return list(self._storage.values())

    def save(self, entity: User) -> User:
        self._storage[entity.id] = entity
        return entity

    def delete(self, id: str) -> None:
        self._storage.pop(id, None)

    def exists(self, id: str) -> bool:
        return id in self._storage

class PostgresUserRepository(Repository[User, str]):
    def __init__(self, connection_string: str) -> None:
        self._conn_string = connection_string
        # Initialize connection pool

    def find_by_id(self, id: str) -> Optional[User]:
        # SQL query implementation
        pass

    # ... other methods
```

### Unit of Work Template

```python
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Generator

class UnitOfWork(ABC):
    @abstractmethod
    def __enter__(self) -> 'UnitOfWork':
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self._session_factory = session_factory
        self._session = None

    def __enter__(self) -> 'SqlAlchemyUnitOfWork':
        self._session = self._session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            self.rollback()
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()

    @property
    def users(self) -> UserRepository:
        return SqlAlchemyUserRepository(self._session)

    @property
    def orders(self) -> OrderRepository:
        return SqlAlchemyOrderRepository(self._session)

# Usage
with SqlAlchemyUnitOfWork(session_factory) as uow:
    user = uow.users.find_by_id("123")
    user.name = "New Name"
    uow.users.save(user)
    uow.commit()  # Explicit commit
```

---

*Design Pattern Templates v1.0*
