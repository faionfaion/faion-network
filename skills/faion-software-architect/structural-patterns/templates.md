# Structural Patterns Templates

Copy-paste templates for quick pattern implementation.

---

## 1. Adapter Pattern

### Python Template

```python
from abc import ABC, abstractmethod
from typing import Protocol


# Target Interface (what client expects)
class TargetInterface(Protocol):
    def target_method(self, param: str) -> str:
        ...


# Adaptee (existing class with incompatible interface)
class Adaptee:
    def specific_method(self, data: dict) -> dict:
        """Existing method with different signature."""
        return {"result": data.get("input", "")}


# Adapter (converts Adaptee to Target)
class Adapter:
    def __init__(self, adaptee: Adaptee):
        self._adaptee = adaptee

    def target_method(self, param: str) -> str:
        # Convert target interface to adaptee interface
        adaptee_input = {"input": param}
        result = self._adaptee.specific_method(adaptee_input)
        return result["result"]


# Usage
def client_code(target: TargetInterface) -> None:
    result = target.target_method("test")
    print(f"Result: {result}")


adaptee = Adaptee()
adapter = Adapter(adaptee)
client_code(adapter)
```

### TypeScript Template

```typescript
// Target Interface
interface TargetInterface {
  targetMethod(param: string): string;
}

// Adaptee
class Adaptee {
  specificMethod(data: Record<string, unknown>): Record<string, unknown> {
    return { result: data.input ?? "" };
  }
}

// Adapter
class Adapter implements TargetInterface {
  constructor(private adaptee: Adaptee) {}

  targetMethod(param: string): string {
    const adapteeInput = { input: param };
    const result = this.adaptee.specificMethod(adapteeInput);
    return result.result as string;
  }
}

// Usage
function clientCode(target: TargetInterface): void {
  console.log(target.targetMethod("test"));
}

clientCode(new Adapter(new Adaptee()));
```

### Go Template

```go
package main

// Target Interface
type TargetInterface interface {
    TargetMethod(param string) string
}

// Adaptee
type Adaptee struct{}

func (a *Adaptee) SpecificMethod(data map[string]interface{}) map[string]interface{} {
    input, _ := data["input"].(string)
    return map[string]interface{}{"result": input}
}

// Adapter
type Adapter struct {
    adaptee *Adaptee
}

func NewAdapter(adaptee *Adaptee) *Adapter {
    return &Adapter{adaptee: adaptee}
}

func (a *Adapter) TargetMethod(param string) string {
    input := map[string]interface{}{"input": param}
    result := a.adaptee.SpecificMethod(input)
    return result["result"].(string)
}

// Usage
func ClientCode(target TargetInterface) {
    println(target.TargetMethod("test"))
}

func main() {
    adapter := NewAdapter(&Adaptee{})
    ClientCode(adapter)
}
```

---

## 2. Bridge Pattern

### Python Template

```python
from abc import ABC, abstractmethod


# Implementor Interface
class Implementor(ABC):
    @abstractmethod
    def operation_impl(self, data: str) -> str:
        pass


# Concrete Implementors
class ConcreteImplementorA(Implementor):
    def operation_impl(self, data: str) -> str:
        return f"ImplementorA: {data}"


class ConcreteImplementorB(Implementor):
    def operation_impl(self, data: str) -> str:
        return f"ImplementorB: {data.upper()}"


# Abstraction
class Abstraction(ABC):
    def __init__(self, implementor: Implementor):
        self._implementor = implementor

    @abstractmethod
    def operation(self, data: str) -> str:
        pass


# Refined Abstractions
class RefinedAbstractionX(Abstraction):
    def operation(self, data: str) -> str:
        processed = f"[X] {data}"
        return self._implementor.operation_impl(processed)


class RefinedAbstractionY(Abstraction):
    def operation(self, data: str) -> str:
        processed = f"[Y] {data}"
        return self._implementor.operation_impl(processed)


# Usage: Any abstraction with any implementor
impl_a = ConcreteImplementorA()
impl_b = ConcreteImplementorB()

abstraction_x_a = RefinedAbstractionX(impl_a)
abstraction_x_b = RefinedAbstractionX(impl_b)
abstraction_y_a = RefinedAbstractionY(impl_a)

print(abstraction_x_a.operation("test"))  # ImplementorA: [X] test
print(abstraction_x_b.operation("test"))  # ImplementorB: [X] TEST
```

### TypeScript Template

```typescript
// Implementor Interface
interface Implementor {
  operationImpl(data: string): string;
}

// Concrete Implementors
class ConcreteImplementorA implements Implementor {
  operationImpl(data: string): string {
    return `ImplementorA: ${data}`;
  }
}

class ConcreteImplementorB implements Implementor {
  operationImpl(data: string): string {
    return `ImplementorB: ${data.toUpperCase()}`;
  }
}

// Abstraction
abstract class Abstraction {
  constructor(protected implementor: Implementor) {}
  abstract operation(data: string): string;
}

// Refined Abstraction
class RefinedAbstractionX extends Abstraction {
  operation(data: string): string {
    return this.implementor.operationImpl(`[X] ${data}`);
  }
}

// Usage
const implA = new ConcreteImplementorA();
const implB = new ConcreteImplementorB();

console.log(new RefinedAbstractionX(implA).operation("test"));
console.log(new RefinedAbstractionX(implB).operation("test"));
```

### Go Template

```go
package main

// Implementor Interface
type Implementor interface {
    OperationImpl(data string) string
}

// Concrete Implementors
type ConcreteImplementorA struct{}

func (i *ConcreteImplementorA) OperationImpl(data string) string {
    return "ImplementorA: " + data
}

type ConcreteImplementorB struct{}

func (i *ConcreteImplementorB) OperationImpl(data string) string {
    return "ImplementorB: " + strings.ToUpper(data)
}

// Abstraction
type Abstraction struct {
    implementor Implementor
}

// Refined Abstraction
type RefinedAbstractionX struct {
    Abstraction
}

func NewRefinedAbstractionX(impl Implementor) *RefinedAbstractionX {
    return &RefinedAbstractionX{Abstraction{implementor: impl}}
}

func (a *RefinedAbstractionX) Operation(data string) string {
    return a.implementor.OperationImpl("[X] " + data)
}

func main() {
    abstraction := NewRefinedAbstractionX(&ConcreteImplementorA{})
    println(abstraction.Operation("test"))
}
```

---

## 3. Composite Pattern

### Python Template

```python
from abc import ABC, abstractmethod
from typing import Iterator


# Component Interface
class Component(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def operation(self) -> str:
        pass


# Leaf
class Leaf(Component):
    def __init__(self, name: str, value: str):
        self._name = name
        self._value = value

    @property
    def name(self) -> str:
        return self._name

    def operation(self) -> str:
        return f"Leaf({self._name}): {self._value}"


# Composite
class Composite(Component):
    def __init__(self, name: str):
        self._name = name
        self._children: list[Component] = []

    @property
    def name(self) -> str:
        return self._name

    def add(self, component: Component) -> "Composite":
        self._children.append(component)
        return self

    def remove(self, component: Component) -> "Composite":
        self._children.remove(component)
        return self

    def operation(self) -> str:
        results = [f"Composite({self._name}):"]
        for child in self._children:
            results.append(f"  {child.operation()}")
        return "\n".join(results)

    def __iter__(self) -> Iterator[Component]:
        return iter(self._children)


# Usage
root = Composite("root")
root.add(Leaf("a", "value_a"))
root.add(Leaf("b", "value_b"))

branch = Composite("branch")
branch.add(Leaf("c", "value_c"))
root.add(branch)

print(root.operation())
```

### TypeScript Template

```typescript
// Component Interface
interface Component {
  name: string;
  operation(): string;
}

// Leaf
class Leaf implements Component {
  constructor(public name: string, private value: string) {}

  operation(): string {
    return `Leaf(${this.name}): ${this.value}`;
  }
}

// Composite
class Composite implements Component {
  private children: Component[] = [];

  constructor(public name: string) {}

  add(component: Component): this {
    this.children.push(component);
    return this;
  }

  remove(component: Component): this {
    const index = this.children.indexOf(component);
    if (index > -1) this.children.splice(index, 1);
    return this;
  }

  operation(): string {
    const results = [`Composite(${this.name}):`];
    for (const child of this.children) {
      results.push(`  ${child.operation()}`);
    }
    return results.join("\n");
  }
}

// Usage
const root = new Composite("root");
root.add(new Leaf("a", "value_a"));
root.add(new Leaf("b", "value_b"));

const branch = new Composite("branch");
branch.add(new Leaf("c", "value_c"));
root.add(branch);

console.log(root.operation());
```

### Go Template

```go
package main

import (
    "fmt"
    "strings"
)

// Component Interface
type Component interface {
    Name() string
    Operation() string
}

// Leaf
type Leaf struct {
    name  string
    value string
}

func NewLeaf(name, value string) *Leaf {
    return &Leaf{name: name, value: value}
}

func (l *Leaf) Name() string      { return l.name }
func (l *Leaf) Operation() string { return fmt.Sprintf("Leaf(%s): %s", l.name, l.value) }

// Composite
type Composite struct {
    name     string
    children []Component
}

func NewComposite(name string) *Composite {
    return &Composite{name: name, children: []Component{}}
}

func (c *Composite) Name() string { return c.name }

func (c *Composite) Add(component Component) *Composite {
    c.children = append(c.children, component)
    return c
}

func (c *Composite) Operation() string {
    var results []string
    results = append(results, fmt.Sprintf("Composite(%s):", c.name))
    for _, child := range c.children {
        results = append(results, "  "+child.Operation())
    }
    return strings.Join(results, "\n")
}

func main() {
    root := NewComposite("root")
    root.Add(NewLeaf("a", "value_a"))
    root.Add(NewLeaf("b", "value_b"))

    branch := NewComposite("branch")
    branch.Add(NewLeaf("c", "value_c"))
    root.Add(branch)

    fmt.Println(root.Operation())
}
```

---

## 4. Decorator Pattern

### Python Template (Class-Based)

```python
from abc import ABC, abstractmethod


# Component Interface
class Component(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass


# Concrete Component
class ConcreteComponent(Component):
    def operation(self) -> str:
        return "ConcreteComponent"


# Base Decorator
class Decorator(Component):
    def __init__(self, component: Component):
        self._component = component

    def operation(self) -> str:
        return self._component.operation()


# Concrete Decorators
class DecoratorA(Decorator):
    def operation(self) -> str:
        return f"DecoratorA({super().operation()})"


class DecoratorB(Decorator):
    def operation(self) -> str:
        return f"DecoratorB({super().operation()})"


# Usage: Stack decorators
component = ConcreteComponent()
decorated = DecoratorA(DecoratorB(component))
print(decorated.operation())  # DecoratorA(DecoratorB(ConcreteComponent))
```

### Python Template (Function Decorator)

```python
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def decorator_template(func: Callable[P, R]) -> Callable[P, R]:
    """Template for function decorator."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # Before
        print(f"Before {func.__name__}")

        result = func(*args, **kwargs)

        # After
        print(f"After {func.__name__}")
        return result
    return wrapper


def decorator_with_params(param: str):
    """Template for parameterized decorator."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"Param: {param}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Usage
@decorator_template
@decorator_with_params("custom_value")
def my_function(x: int) -> int:
    return x * 2


result = my_function(5)
```

### TypeScript Template

```typescript
// Component Interface
interface Component {
  operation(): string;
}

// Concrete Component
class ConcreteComponent implements Component {
  operation(): string {
    return "ConcreteComponent";
  }
}

// Base Decorator
abstract class Decorator implements Component {
  constructor(protected component: Component) {}

  operation(): string {
    return this.component.operation();
  }
}

// Concrete Decorators
class DecoratorA extends Decorator {
  operation(): string {
    return `DecoratorA(${super.operation()})`;
  }
}

class DecoratorB extends Decorator {
  operation(): string {
    return `DecoratorB(${super.operation()})`;
  }
}

// Usage
const component = new ConcreteComponent();
const decorated = new DecoratorA(new DecoratorB(component));
console.log(decorated.operation());
```

### Go Template

```go
package main

// Component Interface
type Component interface {
    Operation() string
}

// Concrete Component
type ConcreteComponent struct{}

func (c *ConcreteComponent) Operation() string {
    return "ConcreteComponent"
}

// Decorator
type Decorator struct {
    component Component
}

func (d *Decorator) Operation() string {
    return d.component.Operation()
}

// Concrete Decorator
type DecoratorA struct {
    Decorator
}

func NewDecoratorA(c Component) *DecoratorA {
    return &DecoratorA{Decorator{component: c}}
}

func (d *DecoratorA) Operation() string {
    return "DecoratorA(" + d.Decorator.Operation() + ")"
}

func main() {
    component := &ConcreteComponent{}
    decorated := NewDecoratorA(component)
    println(decorated.Operation())
}
```

---

## 5. Facade Pattern

### Python Template

```python
# Complex Subsystem Classes
class SubsystemA:
    def operation_a1(self) -> str:
        return "SubsystemA: operation_a1"

    def operation_a2(self) -> str:
        return "SubsystemA: operation_a2"


class SubsystemB:
    def operation_b1(self) -> str:
        return "SubsystemB: operation_b1"


class SubsystemC:
    def operation_c1(self, data: str) -> str:
        return f"SubsystemC: {data}"


# Facade
class Facade:
    """Simplified interface to complex subsystem."""

    def __init__(self):
        self._subsystem_a = SubsystemA()
        self._subsystem_b = SubsystemB()
        self._subsystem_c = SubsystemC()

    def simple_operation(self) -> str:
        """High-level operation hiding complexity."""
        results = []
        results.append(self._subsystem_a.operation_a1())
        results.append(self._subsystem_b.operation_b1())
        results.append(self._subsystem_c.operation_c1("processed"))
        return " -> ".join(results)

    def another_operation(self) -> str:
        """Another simplified operation."""
        return self._subsystem_a.operation_a2()


# Usage
facade = Facade()
print(facade.simple_operation())
print(facade.another_operation())
```

### TypeScript Template

```typescript
// Subsystem Classes
class SubsystemA {
  operationA1(): string {
    return "SubsystemA: operation_a1";
  }
  operationA2(): string {
    return "SubsystemA: operation_a2";
  }
}

class SubsystemB {
  operationB1(): string {
    return "SubsystemB: operation_b1";
  }
}

class SubsystemC {
  operationC1(data: string): string {
    return `SubsystemC: ${data}`;
  }
}

// Facade
class Facade {
  private subsystemA = new SubsystemA();
  private subsystemB = new SubsystemB();
  private subsystemC = new SubsystemC();

  simpleOperation(): string {
    const results = [
      this.subsystemA.operationA1(),
      this.subsystemB.operationB1(),
      this.subsystemC.operationC1("processed"),
    ];
    return results.join(" -> ");
  }

  anotherOperation(): string {
    return this.subsystemA.operationA2();
  }
}

// Usage
const facade = new Facade();
console.log(facade.simpleOperation());
```

### Go Template

```go
package main

// Subsystem classes
type SubsystemA struct{}

func (s *SubsystemA) OperationA1() string { return "SubsystemA: operation_a1" }
func (s *SubsystemA) OperationA2() string { return "SubsystemA: operation_a2" }

type SubsystemB struct{}

func (s *SubsystemB) OperationB1() string { return "SubsystemB: operation_b1" }

type SubsystemC struct{}

func (s *SubsystemC) OperationC1(data string) string { return "SubsystemC: " + data }

// Facade
type Facade struct {
    subsystemA *SubsystemA
    subsystemB *SubsystemB
    subsystemC *SubsystemC
}

func NewFacade() *Facade {
    return &Facade{
        subsystemA: &SubsystemA{},
        subsystemB: &SubsystemB{},
        subsystemC: &SubsystemC{},
    }
}

func (f *Facade) SimpleOperation() string {
    return f.subsystemA.OperationA1() + " -> " +
           f.subsystemB.OperationB1() + " -> " +
           f.subsystemC.OperationC1("processed")
}

func main() {
    facade := NewFacade()
    println(facade.SimpleOperation())
}
```

---

## 6. Proxy Pattern

### Python Template

```python
from abc import ABC, abstractmethod
from typing import Optional


# Subject Interface
class Subject(ABC):
    @abstractmethod
    def request(self) -> str:
        pass


# Real Subject
class RealSubject(Subject):
    def __init__(self):
        self._load()

    def _load(self) -> None:
        """Expensive initialization."""
        print("RealSubject: Loading...")

    def request(self) -> str:
        return "RealSubject: Handling request"


# Virtual Proxy (Lazy Loading)
class LazyProxy(Subject):
    def __init__(self):
        self._real_subject: Optional[RealSubject] = None

    def request(self) -> str:
        if self._real_subject is None:
            print("LazyProxy: Creating RealSubject on first access")
            self._real_subject = RealSubject()
        return self._real_subject.request()


# Protection Proxy (Access Control)
class ProtectionProxy(Subject):
    def __init__(self, real_subject: RealSubject, user_role: str):
        self._real_subject = real_subject
        self._user_role = user_role

    def _check_access(self) -> bool:
        return self._user_role in ["admin", "user"]

    def request(self) -> str:
        if self._check_access():
            return self._real_subject.request()
        return "ProtectionProxy: Access denied"


# Cache Proxy
class CacheProxy(Subject):
    def __init__(self, real_subject: RealSubject):
        self._real_subject = real_subject
        self._cached_result: Optional[str] = None

    def request(self) -> str:
        if self._cached_result is None:
            print("CacheProxy: Cache miss, calling RealSubject")
            self._cached_result = self._real_subject.request()
        else:
            print("CacheProxy: Cache hit")
        return self._cached_result


# Usage
print("=== Lazy Proxy ===")
lazy = LazyProxy()  # No loading yet
print(lazy.request())  # Now loads

print("\n=== Protection Proxy ===")
real = RealSubject()
protected = ProtectionProxy(real, "guest")
print(protected.request())  # Denied
```

### TypeScript Template

```typescript
// Subject Interface
interface Subject {
  request(): string;
}

// Real Subject
class RealSubject implements Subject {
  constructor() {
    this.load();
  }

  private load(): void {
    console.log("RealSubject: Loading...");
  }

  request(): string {
    return "RealSubject: Handling request";
  }
}

// Lazy Proxy
class LazyProxy implements Subject {
  private realSubject: RealSubject | null = null;

  request(): string {
    if (!this.realSubject) {
      console.log("LazyProxy: Creating on first access");
      this.realSubject = new RealSubject();
    }
    return this.realSubject.request();
  }
}

// Cache Proxy
class CacheProxy implements Subject {
  private cachedResult: string | null = null;

  constructor(private realSubject: RealSubject) {}

  request(): string {
    if (!this.cachedResult) {
      console.log("CacheProxy: Cache miss");
      this.cachedResult = this.realSubject.request();
    } else {
      console.log("CacheProxy: Cache hit");
    }
    return this.cachedResult;
  }
}

// Usage
const lazy = new LazyProxy();
console.log(lazy.request());
```

### Go Template

```go
package main

// Subject Interface
type Subject interface {
    Request() string
}

// Real Subject
type RealSubject struct{}

func NewRealSubject() *RealSubject {
    println("RealSubject: Loading...")
    return &RealSubject{}
}

func (r *RealSubject) Request() string {
    return "RealSubject: Handling request"
}

// Lazy Proxy
type LazyProxy struct {
    realSubject *RealSubject
}

func (p *LazyProxy) Request() string {
    if p.realSubject == nil {
        println("LazyProxy: Creating on first access")
        p.realSubject = NewRealSubject()
    }
    return p.realSubject.Request()
}

// Cache Proxy
type CacheProxy struct {
    realSubject  *RealSubject
    cachedResult *string
}

func NewCacheProxy(real *RealSubject) *CacheProxy {
    return &CacheProxy{realSubject: real}
}

func (p *CacheProxy) Request() string {
    if p.cachedResult == nil {
        println("CacheProxy: Cache miss")
        result := p.realSubject.Request()
        p.cachedResult = &result
    } else {
        println("CacheProxy: Cache hit")
    }
    return *p.cachedResult
}

func main() {
    lazy := &LazyProxy{}
    println(lazy.Request())
}
```

---

## 7. Flyweight Pattern

### Python Template

```python
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)  # Immutable
class Flyweight:
    """Flyweight: Stores intrinsic (shared) state."""
    shared_state_1: str
    shared_state_2: int


class FlyweightFactory:
    """Factory managing flyweight objects."""
    _flyweights: ClassVar[dict[tuple, Flyweight]] = {}

    @classmethod
    def get_flyweight(cls, state_1: str, state_2: int) -> Flyweight:
        key = (state_1, state_2)
        if key not in cls._flyweights:
            cls._flyweights[key] = Flyweight(state_1, state_2)
        return cls._flyweights[key]

    @classmethod
    def count(cls) -> int:
        return len(cls._flyweights)


@dataclass
class Context:
    """Context: Contains extrinsic state + flyweight reference."""
    unique_state: str  # Extrinsic
    flyweight: Flyweight  # Shared

    def operation(self) -> str:
        return f"Context({self.unique_state}) with {self.flyweight}"


# Usage
flyweight1 = FlyweightFactory.get_flyweight("shared", 100)
flyweight2 = FlyweightFactory.get_flyweight("shared", 100)  # Same instance

print(f"Same instance: {flyweight1 is flyweight2}")  # True

context1 = Context("unique_1", flyweight1)
context2 = Context("unique_2", flyweight1)  # Same flyweight

print(f"Unique flyweights: {FlyweightFactory.count()}")
```

### TypeScript Template

```typescript
// Flyweight: Intrinsic state
interface Flyweight {
  sharedState1: string;
  sharedState2: number;
}

// Flyweight Factory
class FlyweightFactory {
  private static flyweights = new Map<string, Flyweight>();

  static getFlyweight(state1: string, state2: number): Flyweight {
    const key = `${state1}-${state2}`;

    if (!this.flyweights.has(key)) {
      this.flyweights.set(key, {
        sharedState1: state1,
        sharedState2: state2,
      });
    }

    return this.flyweights.get(key)!;
  }

  static count(): number {
    return this.flyweights.size;
  }
}

// Context with extrinsic state
interface Context {
  uniqueState: string;
  flyweight: Flyweight;
}

// Usage
const fw1 = FlyweightFactory.getFlyweight("shared", 100);
const fw2 = FlyweightFactory.getFlyweight("shared", 100);

console.log(`Same instance: ${fw1 === fw2}`); // true

const ctx1: Context = { uniqueState: "unique_1", flyweight: fw1 };
const ctx2: Context = { uniqueState: "unique_2", flyweight: fw1 };

console.log(`Unique flyweights: ${FlyweightFactory.count()}`);
```

### Go Template (Thread-Safe)

```go
package main

import (
    "fmt"
    "sync"
)

// Flyweight: Intrinsic state (immutable)
type Flyweight struct {
    SharedState1 string
    SharedState2 int
}

// Flyweight Factory (thread-safe)
type FlyweightFactory struct {
    mu         sync.RWMutex
    flyweights map[string]*Flyweight
}

func NewFlyweightFactory() *FlyweightFactory {
    return &FlyweightFactory{
        flyweights: make(map[string]*Flyweight),
    }
}

func (f *FlyweightFactory) GetFlyweight(state1 string, state2 int) *Flyweight {
    key := fmt.Sprintf("%s-%d", state1, state2)

    f.mu.RLock()
    if fw, exists := f.flyweights[key]; exists {
        f.mu.RUnlock()
        return fw
    }
    f.mu.RUnlock()

    f.mu.Lock()
    defer f.mu.Unlock()

    // Double-check
    if fw, exists := f.flyweights[key]; exists {
        return fw
    }

    fw := &Flyweight{SharedState1: state1, SharedState2: state2}
    f.flyweights[key] = fw
    return fw
}

func (f *FlyweightFactory) Count() int {
    f.mu.RLock()
    defer f.mu.RUnlock()
    return len(f.flyweights)
}

// Context
type Context struct {
    UniqueState string
    Flyweight   *Flyweight
}

func main() {
    factory := NewFlyweightFactory()

    fw1 := factory.GetFlyweight("shared", 100)
    fw2 := factory.GetFlyweight("shared", 100)

    fmt.Printf("Same instance: %v\n", fw1 == fw2)

    ctx1 := Context{UniqueState: "unique_1", Flyweight: fw1}
    ctx2 := Context{UniqueState: "unique_2", Flyweight: fw1}

    fmt.Printf("Unique flyweights: %d\n", factory.Count())
    fmt.Printf("Contexts: %+v, %+v\n", ctx1, ctx2)
}
```

---

## Quick Reference

| Pattern | Python Key | TypeScript Key | Go Key |
|---------|------------|----------------|--------|
| Adapter | Protocol + wrap | interface + implement | Interface + embed |
| Bridge | ABC + injection | abstract class + constructor | Interface + struct |
| Composite | ABC + list[Component] | interface + array | Interface + slice |
| Decorator | Wrap + super() | extends + super | Embed + method override |
| Facade | Init subsystems | private properties | Private fields |
| Proxy | Optional real subject | nullable property | Pointer field |
| Flyweight | @dataclass(frozen=True) | Object.freeze or readonly | Immutable struct + sync.RWMutex |
