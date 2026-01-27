# Behavioral Patterns Templates

Copy-paste templates for each behavioral pattern in Python, TypeScript, and Go.

## Strategy Pattern

### Python Template

```python
from typing import Protocol
from dataclasses import dataclass


# Strategy interface using Protocol (duck typing)
class Strategy(Protocol):
    def execute(self, data: dict) -> dict:
        """Execute the strategy with given data."""
        ...


# Concrete strategies
class ConcreteStrategyA:
    def execute(self, data: dict) -> dict:
        # Implement algorithm A
        return {"result": "Strategy A", **data}


class ConcreteStrategyB:
    def execute(self, data: dict) -> dict:
        # Implement algorithm B
        return {"result": "Strategy B", **data}


# Context
@dataclass
class Context:
    strategy: Strategy

    def set_strategy(self, strategy: Strategy) -> None:
        self.strategy = strategy

    def execute_strategy(self, data: dict) -> dict:
        return self.strategy.execute(data)


# Usage
context = Context(strategy=ConcreteStrategyA())
result = context.execute_strategy({"input": "test"})

context.set_strategy(ConcreteStrategyB())
result = context.execute_strategy({"input": "test"})
```

### TypeScript Template

```typescript
// Strategy interface
interface Strategy<TInput, TOutput> {
  execute(data: TInput): TOutput;
}

// Concrete strategies
class ConcreteStrategyA implements Strategy<string, number> {
  execute(data: string): number {
    return data.length;
  }
}

class ConcreteStrategyB implements Strategy<string, number> {
  execute(data: string): number {
    return data.split(' ').length;
  }
}

// Context
class Context<TInput, TOutput> {
  constructor(private strategy: Strategy<TInput, TOutput>) {}

  setStrategy(strategy: Strategy<TInput, TOutput>): void {
    this.strategy = strategy;
  }

  executeStrategy(data: TInput): TOutput {
    return this.strategy.execute(data);
  }
}

// Usage
const context = new Context(new ConcreteStrategyA());
const result1 = context.executeStrategy("hello world");

context.setStrategy(new ConcreteStrategyB());
const result2 = context.executeStrategy("hello world");
```

### Go Template

```go
package main

// Strategy interface
type Strategy interface {
    Execute(data map[string]interface{}) (map[string]interface{}, error)
}

// Concrete strategy A
type ConcreteStrategyA struct{}

func (s *ConcreteStrategyA) Execute(data map[string]interface{}) (map[string]interface{}, error) {
    data["result"] = "Strategy A"
    return data, nil
}

// Concrete strategy B
type ConcreteStrategyB struct{}

func (s *ConcreteStrategyB) Execute(data map[string]interface{}) (map[string]interface{}, error) {
    data["result"] = "Strategy B"
    return data, nil
}

// Context
type Context struct {
    strategy Strategy
}

func NewContext(strategy Strategy) *Context {
    return &Context{strategy: strategy}
}

func (c *Context) SetStrategy(strategy Strategy) {
    c.strategy = strategy
}

func (c *Context) ExecuteStrategy(data map[string]interface{}) (map[string]interface{}, error) {
    return c.strategy.Execute(data)
}

// Usage
func main() {
    ctx := NewContext(&ConcreteStrategyA{})
    result, _ := ctx.ExecuteStrategy(map[string]interface{}{"input": "test"})

    ctx.SetStrategy(&ConcreteStrategyB{})
    result, _ = ctx.ExecuteStrategy(map[string]interface{}{"input": "test"})
    _ = result
}
```

## Observer Pattern

### Python Template

```python
from typing import Protocol, Callable
from dataclasses import dataclass, field
from weakref import WeakSet


# Observer protocol
class Observer(Protocol):
    def update(self, event: str, data: dict) -> None:
        ...


# Subject
class Subject:
    def __init__(self):
        self._observers: dict[str, WeakSet[Observer]] = {}

    def subscribe(self, event: str, observer: Observer) -> Callable[[], None]:
        if event not in self._observers:
            self._observers[event] = WeakSet()
        self._observers[event].add(observer)

        def unsubscribe():
            self._observers[event].discard(observer)
        return unsubscribe

    def notify(self, event: str, data: dict = None) -> None:
        if event in self._observers:
            for observer in list(self._observers[event]):
                observer.update(event, data or {})


# Concrete observer
class ConcreteObserver:
    def __init__(self, name: str):
        self.name = name

    def update(self, event: str, data: dict) -> None:
        print(f"{self.name} received {event}: {data}")


# Usage
subject = Subject()
observer1 = ConcreteObserver("Observer1")
observer2 = ConcreteObserver("Observer2")

unsubscribe1 = subject.subscribe("user.created", observer1)
subject.subscribe("user.created", observer2)

subject.notify("user.created", {"user_id": "123"})

unsubscribe1()
subject.notify("user.created", {"user_id": "456"})
```

### TypeScript Template

```typescript
type Listener<T> = (data: T) => void;
type Unsubscribe = () => void;

class EventEmitter<TEvents extends Record<string, unknown>> {
  private listeners = new Map<keyof TEvents, Set<Listener<any>>>();

  on<K extends keyof TEvents>(event: K, listener: Listener<TEvents[K]>): Unsubscribe {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(listener);

    return () => {
      this.listeners.get(event)?.delete(listener);
    };
  }

  emit<K extends keyof TEvents>(event: K, data: TEvents[K]): void {
    this.listeners.get(event)?.forEach(listener => listener(data));
  }

  off<K extends keyof TEvents>(event: K, listener: Listener<TEvents[K]>): void {
    this.listeners.get(event)?.delete(listener);
  }
}

// Type-safe events
interface AppEvents {
  'user.created': { userId: string; email: string };
  'user.deleted': { userId: string };
  'order.placed': { orderId: string; total: number };
}

// Usage
const emitter = new EventEmitter<AppEvents>();

const unsubscribe = emitter.on('user.created', (data) => {
  console.log(`User created: ${data.userId}`);
});

emitter.emit('user.created', { userId: '123', email: 'test@example.com' });

unsubscribe();
```

### Go Template

```go
package main

import (
    "sync"
)

// Observer interface
type Observer interface {
    Update(event string, data interface{})
}

// Subject
type Subject struct {
    mu        sync.RWMutex
    observers map[string][]Observer
}

func NewSubject() *Subject {
    return &Subject{
        observers: make(map[string][]Observer),
    }
}

func (s *Subject) Subscribe(event string, observer Observer) func() {
    s.mu.Lock()
    defer s.mu.Unlock()

    s.observers[event] = append(s.observers[event], observer)

    // Return unsubscribe function
    return func() {
        s.mu.Lock()
        defer s.mu.Unlock()
        for i, obs := range s.observers[event] {
            if obs == observer {
                s.observers[event] = append(s.observers[event][:i], s.observers[event][i+1:]...)
                break
            }
        }
    }
}

func (s *Subject) Notify(event string, data interface{}) {
    s.mu.RLock()
    defer s.mu.RUnlock()

    for _, observer := range s.observers[event] {
        observer.Update(event, data)
    }
}

// Concrete observer
type ConcreteObserver struct {
    Name string
}

func (o *ConcreteObserver) Update(event string, data interface{}) {
    println(o.Name, "received", event)
}

// Usage
func main() {
    subject := NewSubject()
    observer := &ConcreteObserver{Name: "Observer1"}

    unsubscribe := subject.Subscribe("user.created", observer)
    subject.Notify("user.created", map[string]string{"id": "123"})

    unsubscribe()
}
```

## Command Pattern

### Python Template

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


@dataclass
class Receiver:
    """The object that performs the actual work."""
    state: str = ""


@dataclass
class ConcreteCommand(Command):
    receiver: Receiver
    value: str
    previous_state: str = field(default="", init=False)

    def execute(self) -> None:
        self.previous_state = self.receiver.state
        self.receiver.state = self.value

    def undo(self) -> None:
        self.receiver.state = self.previous_state


class Invoker:
    def __init__(self):
        self._history: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()

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


# Usage
receiver = Receiver()
invoker = Invoker()

invoker.execute(ConcreteCommand(receiver, "State 1"))
invoker.execute(ConcreteCommand(receiver, "State 2"))

invoker.undo()  # Back to State 1
invoker.redo()  # Forward to State 2
```

### TypeScript Template

```typescript
interface Command {
  execute(): void;
  undo(): void;
}

class Receiver {
  state = '';

  setState(value: string): void {
    this.state = value;
  }
}

class ConcreteCommand implements Command {
  private previousState = '';

  constructor(
    private receiver: Receiver,
    private value: string
  ) {}

  execute(): void {
    this.previousState = this.receiver.state;
    this.receiver.setState(this.value);
  }

  undo(): void {
    this.receiver.setState(this.previousState);
  }
}

class Invoker {
  private history: Command[] = [];
  private redoStack: Command[] = [];

  execute(command: Command): void {
    command.execute();
    this.history.push(command);
    this.redoStack = [];
  }

  undo(): boolean {
    const command = this.history.pop();
    if (!command) return false;

    command.undo();
    this.redoStack.push(command);
    return true;
  }

  redo(): boolean {
    const command = this.redoStack.pop();
    if (!command) return false;

    command.execute();
    this.history.push(command);
    return true;
  }
}

// Usage
const receiver = new Receiver();
const invoker = new Invoker();

invoker.execute(new ConcreteCommand(receiver, 'State 1'));
invoker.execute(new ConcreteCommand(receiver, 'State 2'));

invoker.undo();
invoker.redo();
```

### Go Template

```go
package main

// Command interface
type Command interface {
    Execute()
    Undo()
}

// Receiver
type Receiver struct {
    State string
}

// Concrete command
type ConcreteCommand struct {
    receiver      *Receiver
    value         string
    previousState string
}

func NewConcreteCommand(receiver *Receiver, value string) *ConcreteCommand {
    return &ConcreteCommand{
        receiver: receiver,
        value:    value,
    }
}

func (c *ConcreteCommand) Execute() {
    c.previousState = c.receiver.State
    c.receiver.State = c.value
}

func (c *ConcreteCommand) Undo() {
    c.receiver.State = c.previousState
}

// Invoker
type Invoker struct {
    history   []Command
    redoStack []Command
}

func NewInvoker() *Invoker {
    return &Invoker{
        history:   make([]Command, 0),
        redoStack: make([]Command, 0),
    }
}

func (i *Invoker) Execute(cmd Command) {
    cmd.Execute()
    i.history = append(i.history, cmd)
    i.redoStack = nil
}

func (i *Invoker) Undo() bool {
    if len(i.history) == 0 {
        return false
    }
    cmd := i.history[len(i.history)-1]
    i.history = i.history[:len(i.history)-1]
    cmd.Undo()
    i.redoStack = append(i.redoStack, cmd)
    return true
}

func (i *Invoker) Redo() bool {
    if len(i.redoStack) == 0 {
        return false
    }
    cmd := i.redoStack[len(i.redoStack)-1]
    i.redoStack = i.redoStack[:len(i.redoStack)-1]
    cmd.Execute()
    i.history = append(i.history, cmd)
    return true
}

// Usage
func main() {
    receiver := &Receiver{}
    invoker := NewInvoker()

    invoker.Execute(NewConcreteCommand(receiver, "State 1"))
    invoker.Execute(NewConcreteCommand(receiver, "State 2"))

    invoker.Undo()
    invoker.Redo()
}
```

## State Pattern

### Python Template

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class State(ABC):
    @abstractmethod
    def handle(self, context: "Context") -> None:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class ConcreteStateA(State):
    name = "StateA"

    def handle(self, context: "Context") -> None:
        print(f"Handling in {self.name}, transitioning to StateB")
        context.state = ConcreteStateB()


class ConcreteStateB(State):
    name = "StateB"

    def handle(self, context: "Context") -> None:
        print(f"Handling in {self.name}, transitioning to StateA")
        context.state = ConcreteStateA()


@dataclass
class Context:
    state: State

    def request(self) -> None:
        self.state.handle(self)

    @property
    def current_state(self) -> str:
        return self.state.name


# Usage
context = Context(state=ConcreteStateA())
print(f"Current: {context.current_state}")

context.request()
print(f"Current: {context.current_state}")

context.request()
print(f"Current: {context.current_state}")
```

### TypeScript Template

```typescript
interface State {
  handle(context: Context): void;
  readonly name: string;
}

class ConcreteStateA implements State {
  readonly name = 'StateA';

  handle(context: Context): void {
    console.log(`Handling in ${this.name}, transitioning to StateB`);
    context.setState(new ConcreteStateB());
  }
}

class ConcreteStateB implements State {
  readonly name = 'StateB';

  handle(context: Context): void {
    console.log(`Handling in ${this.name}, transitioning to StateA`);
    context.setState(new ConcreteStateA());
  }
}

class Context {
  constructor(private state: State) {}

  setState(state: State): void {
    this.state = state;
  }

  request(): void {
    this.state.handle(this);
  }

  get currentState(): string {
    return this.state.name;
  }
}

// Usage
const context = new Context(new ConcreteStateA());
console.log(`Current: ${context.currentState}`);

context.request();
console.log(`Current: ${context.currentState}`);
```

### Go Template

```go
package main

import "fmt"

// State interface
type State interface {
    Handle(context *Context)
    Name() string
}

// Concrete state A
type ConcreteStateA struct{}

func (s *ConcreteStateA) Handle(context *Context) {
    fmt.Printf("Handling in %s, transitioning to StateB\n", s.Name())
    context.SetState(&ConcreteStateB{})
}

func (s *ConcreteStateA) Name() string {
    return "StateA"
}

// Concrete state B
type ConcreteStateB struct{}

func (s *ConcreteStateB) Handle(context *Context) {
    fmt.Printf("Handling in %s, transitioning to StateA\n", s.Name())
    context.SetState(&ConcreteStateA{})
}

func (s *ConcreteStateB) Name() string {
    return "StateB"
}

// Context
type Context struct {
    state State
}

func NewContext(state State) *Context {
    return &Context{state: state}
}

func (c *Context) SetState(state State) {
    c.state = state
}

func (c *Context) Request() {
    c.state.Handle(c)
}

func (c *Context) CurrentState() string {
    return c.state.Name()
}

// Usage
func main() {
    ctx := NewContext(&ConcreteStateA{})
    fmt.Println("Current:", ctx.CurrentState())

    ctx.Request()
    fmt.Println("Current:", ctx.CurrentState())
}
```

## Chain of Responsibility

### Python Template

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class Request:
    data: dict
    handled: bool = False


class Handler(ABC):
    def __init__(self):
        self._next: Handler | None = None

    def set_next(self, handler: "Handler") -> "Handler":
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request: Request) -> Request:
        pass

    def pass_to_next(self, request: Request) -> Request:
        if self._next:
            return self._next.handle(request)
        return request


class ConcreteHandlerA(Handler):
    def handle(self, request: Request) -> Request:
        if request.data.get("type") == "A":
            request.handled = True
            print("HandlerA processed the request")
            return request
        return self.pass_to_next(request)


class ConcreteHandlerB(Handler):
    def handle(self, request: Request) -> Request:
        if request.data.get("type") == "B":
            request.handled = True
            print("HandlerB processed the request")
            return request
        return self.pass_to_next(request)


class DefaultHandler(Handler):
    def handle(self, request: Request) -> Request:
        print("DefaultHandler: no handler found")
        return request


# Usage
handler_a = ConcreteHandlerA()
handler_b = ConcreteHandlerB()
default = DefaultHandler()

handler_a.set_next(handler_b).set_next(default)

# Process requests
handler_a.handle(Request(data={"type": "A"}))
handler_a.handle(Request(data={"type": "B"}))
handler_a.handle(Request(data={"type": "C"}))
```

### TypeScript Template

```typescript
interface Request {
  data: Record<string, unknown>;
  handled: boolean;
}

abstract class Handler {
  private next?: Handler;

  setNext(handler: Handler): Handler {
    this.next = handler;
    return handler;
  }

  abstract handle(request: Request): Request;

  protected passToNext(request: Request): Request {
    if (this.next) {
      return this.next.handle(request);
    }
    return request;
  }
}

class ConcreteHandlerA extends Handler {
  handle(request: Request): Request {
    if (request.data.type === 'A') {
      request.handled = true;
      console.log('HandlerA processed the request');
      return request;
    }
    return this.passToNext(request);
  }
}

class ConcreteHandlerB extends Handler {
  handle(request: Request): Request {
    if (request.data.type === 'B') {
      request.handled = true;
      console.log('HandlerB processed the request');
      return request;
    }
    return this.passToNext(request);
  }
}

class DefaultHandler extends Handler {
  handle(request: Request): Request {
    console.log('DefaultHandler: no handler found');
    return request;
  }
}

// Usage
const handlerA = new ConcreteHandlerA();
const handlerB = new ConcreteHandlerB();
const defaultHandler = new DefaultHandler();

handlerA.setNext(handlerB).setNext(defaultHandler);

handlerA.handle({ data: { type: 'A' }, handled: false });
handlerA.handle({ data: { type: 'B' }, handled: false });
handlerA.handle({ data: { type: 'C' }, handled: false });
```

### Go Template

```go
package main

import "fmt"

// Request
type Request struct {
    Data    map[string]interface{}
    Handled bool
}

// Handler interface
type Handler interface {
    SetNext(handler Handler) Handler
    Handle(request *Request) *Request
}

// Base handler
type BaseHandler struct {
    next Handler
}

func (h *BaseHandler) SetNext(handler Handler) Handler {
    h.next = handler
    return handler
}

func (h *BaseHandler) PassToNext(request *Request) *Request {
    if h.next != nil {
        return h.next.Handle(request)
    }
    return request
}

// Concrete handler A
type ConcreteHandlerA struct {
    BaseHandler
}

func (h *ConcreteHandlerA) Handle(request *Request) *Request {
    if request.Data["type"] == "A" {
        request.Handled = true
        fmt.Println("HandlerA processed the request")
        return request
    }
    return h.PassToNext(request)
}

// Concrete handler B
type ConcreteHandlerB struct {
    BaseHandler
}

func (h *ConcreteHandlerB) Handle(request *Request) *Request {
    if request.Data["type"] == "B" {
        request.Handled = true
        fmt.Println("HandlerB processed the request")
        return request
    }
    return h.PassToNext(request)
}

// Default handler
type DefaultHandler struct {
    BaseHandler
}

func (h *DefaultHandler) Handle(request *Request) *Request {
    fmt.Println("DefaultHandler: no handler found")
    return request
}

// Usage
func main() {
    handlerA := &ConcreteHandlerA{}
    handlerB := &ConcreteHandlerB{}
    defaultHandler := &DefaultHandler{}

    handlerA.SetNext(handlerB).SetNext(defaultHandler)

    handlerA.Handle(&Request{Data: map[string]interface{}{"type": "A"}})
    handlerA.Handle(&Request{Data: map[string]interface{}{"type": "B"}})
    handlerA.Handle(&Request{Data: map[string]interface{}{"type": "C"}})
}
```

## Template Method

### Python Template

```python
from abc import ABC, abstractmethod


class AbstractClass(ABC):
    def template_method(self) -> str:
        """The template method defines the skeleton of an algorithm."""
        result = []
        result.append(self.step_one())
        result.append(self.step_two())
        result.append(self.hook())
        result.append(self.step_three())
        return "\n".join(result)

    @abstractmethod
    def step_one(self) -> str:
        """Required step - must be implemented."""
        pass

    @abstractmethod
    def step_two(self) -> str:
        """Required step - must be implemented."""
        pass

    def hook(self) -> str:
        """Optional hook - can be overridden."""
        return "Default hook"

    @abstractmethod
    def step_three(self) -> str:
        """Required step - must be implemented."""
        pass


class ConcreteClassA(AbstractClass):
    def step_one(self) -> str:
        return "ConcreteA: Step 1"

    def step_two(self) -> str:
        return "ConcreteA: Step 2"

    def step_three(self) -> str:
        return "ConcreteA: Step 3"


class ConcreteClassB(AbstractClass):
    def step_one(self) -> str:
        return "ConcreteB: Step 1"

    def step_two(self) -> str:
        return "ConcreteB: Step 2"

    def hook(self) -> str:
        return "ConcreteB: Custom hook"

    def step_three(self) -> str:
        return "ConcreteB: Step 3"


# Usage
concrete_a = ConcreteClassA()
print(concrete_a.template_method())

concrete_b = ConcreteClassB()
print(concrete_b.template_method())
```

### TypeScript Template

```typescript
abstract class AbstractClass {
  // Template method
  templateMethod(): string {
    const result: string[] = [];
    result.push(this.stepOne());
    result.push(this.stepTwo());
    result.push(this.hook());
    result.push(this.stepThree());
    return result.join('\n');
  }

  protected abstract stepOne(): string;
  protected abstract stepTwo(): string;

  // Hook with default implementation
  protected hook(): string {
    return 'Default hook';
  }

  protected abstract stepThree(): string;
}

class ConcreteClassA extends AbstractClass {
  protected stepOne(): string {
    return 'ConcreteA: Step 1';
  }

  protected stepTwo(): string {
    return 'ConcreteA: Step 2';
  }

  protected stepThree(): string {
    return 'ConcreteA: Step 3';
  }
}

class ConcreteClassB extends AbstractClass {
  protected stepOne(): string {
    return 'ConcreteB: Step 1';
  }

  protected stepTwo(): string {
    return 'ConcreteB: Step 2';
  }

  protected hook(): string {
    return 'ConcreteB: Custom hook';
  }

  protected stepThree(): string {
    return 'ConcreteB: Step 3';
  }
}

// Usage
const concreteA = new ConcreteClassA();
console.log(concreteA.templateMethod());

const concreteB = new ConcreteClassB();
console.log(concreteB.templateMethod());
```

### Go Template

```go
package main

import (
    "fmt"
    "strings"
)

// Steps interface
type Steps interface {
    StepOne() string
    StepTwo() string
    Hook() string
    StepThree() string
}

// Template (uses embedding for default hooks)
type Template struct {
    steps Steps
}

func NewTemplate(steps Steps) *Template {
    return &Template{steps: steps}
}

func (t *Template) TemplateMethod() string {
    result := []string{
        t.steps.StepOne(),
        t.steps.StepTwo(),
        t.steps.Hook(),
        t.steps.StepThree(),
    }
    return strings.Join(result, "\n")
}

// Default hook implementation
type DefaultSteps struct{}

func (d *DefaultSteps) Hook() string {
    return "Default hook"
}

// Concrete implementation A
type ConcreteA struct {
    DefaultSteps
}

func (c *ConcreteA) StepOne() string   { return "ConcreteA: Step 1" }
func (c *ConcreteA) StepTwo() string   { return "ConcreteA: Step 2" }
func (c *ConcreteA) StepThree() string { return "ConcreteA: Step 3" }

// Concrete implementation B with custom hook
type ConcreteB struct{}

func (c *ConcreteB) StepOne() string   { return "ConcreteB: Step 1" }
func (c *ConcreteB) StepTwo() string   { return "ConcreteB: Step 2" }
func (c *ConcreteB) Hook() string      { return "ConcreteB: Custom hook" }
func (c *ConcreteB) StepThree() string { return "ConcreteB: Step 3" }

// Usage
func main() {
    templateA := NewTemplate(&ConcreteA{})
    fmt.Println(templateA.TemplateMethod())

    templateB := NewTemplate(&ConcreteB{})
    fmt.Println(templateB.TemplateMethod())
}
```

## Mediator Pattern

### Python Template

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Mediator(ABC):
    @abstractmethod
    def notify(self, sender: "Colleague", event: str) -> None:
        pass


class Colleague:
    def __init__(self, mediator: Mediator | None = None):
        self._mediator = mediator

    def set_mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator


class ConcreteColleagueA(Colleague):
    def do_a(self) -> None:
        print("ColleagueA does A")
        if self._mediator:
            self._mediator.notify(self, "A")


class ConcreteColleagueB(Colleague):
    def do_b(self) -> None:
        print("ColleagueB does B")
        if self._mediator:
            self._mediator.notify(self, "B")

    def do_c(self) -> None:
        print("ColleagueB does C")


class ConcreteMediator(Mediator):
    def __init__(self):
        self.colleague_a: ConcreteColleagueA | None = None
        self.colleague_b: ConcreteColleagueB | None = None

    def set_colleague_a(self, colleague: ConcreteColleagueA) -> None:
        self.colleague_a = colleague
        colleague.set_mediator(self)

    def set_colleague_b(self, colleague: ConcreteColleagueB) -> None:
        self.colleague_b = colleague
        colleague.set_mediator(self)

    def notify(self, sender: Colleague, event: str) -> None:
        if event == "A" and self.colleague_b:
            print("Mediator reacts to A and triggers B's do_c()")
            self.colleague_b.do_c()
        elif event == "B" and self.colleague_a:
            print("Mediator reacts to B")


# Usage
mediator = ConcreteMediator()

colleague_a = ConcreteColleagueA()
colleague_b = ConcreteColleagueB()

mediator.set_colleague_a(colleague_a)
mediator.set_colleague_b(colleague_b)

colleague_a.do_a()  # Triggers colleague_b.do_c() via mediator
```

### TypeScript Template

```typescript
interface Mediator {
  notify(sender: Colleague, event: string): void;
}

abstract class Colleague {
  protected mediator?: Mediator;

  setMediator(mediator: Mediator): void {
    this.mediator = mediator;
  }
}

class ConcreteColleagueA extends Colleague {
  doA(): void {
    console.log('ColleagueA does A');
    this.mediator?.notify(this, 'A');
  }
}

class ConcreteColleagueB extends Colleague {
  doB(): void {
    console.log('ColleagueB does B');
    this.mediator?.notify(this, 'B');
  }

  doC(): void {
    console.log('ColleagueB does C');
  }
}

class ConcreteMediator implements Mediator {
  private colleagueA?: ConcreteColleagueA;
  private colleagueB?: ConcreteColleagueB;

  setColleagueA(colleague: ConcreteColleagueA): void {
    this.colleagueA = colleague;
    colleague.setMediator(this);
  }

  setColleagueB(colleague: ConcreteColleagueB): void {
    this.colleagueB = colleague;
    colleague.setMediator(this);
  }

  notify(sender: Colleague, event: string): void {
    if (event === 'A' && this.colleagueB) {
      console.log("Mediator reacts to A and triggers B's doC()");
      this.colleagueB.doC();
    } else if (event === 'B' && this.colleagueA) {
      console.log('Mediator reacts to B');
    }
  }
}

// Usage
const mediator = new ConcreteMediator();

const colleagueA = new ConcreteColleagueA();
const colleagueB = new ConcreteColleagueB();

mediator.setColleagueA(colleagueA);
mediator.setColleagueB(colleagueB);

colleagueA.doA();
```

## Iterator Pattern

### Python Template (Generator-based)

```python
from typing import Iterator, Generic, TypeVar
from dataclasses import dataclass, field

T = TypeVar('T')


@dataclass
class Collection(Generic[T]):
    items: list[T] = field(default_factory=list)

    def add(self, item: T) -> None:
        self.items.append(item)

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def reverse_iterator(self) -> Iterator[T]:
        return reversed(self.items)

    def filtered_iterator(self, predicate) -> Iterator[T]:
        return (item for item in self.items if predicate(item))


# Usage
collection = Collection[int]()
collection.add(1)
collection.add(2)
collection.add(3)

# Forward iteration
for item in collection:
    print(item)

# Reverse iteration
for item in collection.reverse_iterator():
    print(item)

# Filtered iteration
for item in collection.filtered_iterator(lambda x: x > 1):
    print(item)
```

### TypeScript Template

```typescript
interface Iterator<T> {
  hasNext(): boolean;
  next(): T;
  reset(): void;
}

interface Iterable<T> {
  createIterator(): Iterator<T>;
}

class Collection<T> implements Iterable<T> {
  private items: T[] = [];

  add(item: T): void {
    this.items.push(item);
  }

  getItems(): T[] {
    return [...this.items];
  }

  createIterator(): Iterator<T> {
    return new ArrayIterator(this.items);
  }
}

class ArrayIterator<T> implements Iterator<T> {
  private index = 0;

  constructor(private items: T[]) {}

  hasNext(): boolean {
    return this.index < this.items.length;
  }

  next(): T {
    return this.items[this.index++];
  }

  reset(): void {
    this.index = 0;
  }
}

// Usage
const collection = new Collection<number>();
collection.add(1);
collection.add(2);
collection.add(3);

const iterator = collection.createIterator();
while (iterator.hasNext()) {
  console.log(iterator.next());
}
```

## Visitor Pattern

### Python Template

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Visitor(ABC):
    @abstractmethod
    def visit_element_a(self, element: "ConcreteElementA") -> None:
        pass

    @abstractmethod
    def visit_element_b(self, element: "ConcreteElementB") -> None:
        pass


class Element(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass


@dataclass
class ConcreteElementA(Element):
    value: str

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_element_a(self)


@dataclass
class ConcreteElementB(Element):
    value: int

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_element_b(self)


class ConcreteVisitor1(Visitor):
    def visit_element_a(self, element: ConcreteElementA) -> None:
        print(f"Visitor1 visiting ElementA: {element.value}")

    def visit_element_b(self, element: ConcreteElementB) -> None:
        print(f"Visitor1 visiting ElementB: {element.value}")


class ConcreteVisitor2(Visitor):
    def visit_element_a(self, element: ConcreteElementA) -> None:
        print(f"Visitor2 visiting ElementA: {element.value.upper()}")

    def visit_element_b(self, element: ConcreteElementB) -> None:
        print(f"Visitor2 visiting ElementB: {element.value * 2}")


# Usage
elements: list[Element] = [
    ConcreteElementA("hello"),
    ConcreteElementB(42),
]

visitor1 = ConcreteVisitor1()
visitor2 = ConcreteVisitor2()

for element in elements:
    element.accept(visitor1)

for element in elements:
    element.accept(visitor2)
```

### TypeScript Template

```typescript
interface Visitor {
  visitElementA(element: ConcreteElementA): void;
  visitElementB(element: ConcreteElementB): void;
}

interface Element {
  accept(visitor: Visitor): void;
}

class ConcreteElementA implements Element {
  constructor(public value: string) {}

  accept(visitor: Visitor): void {
    visitor.visitElementA(this);
  }
}

class ConcreteElementB implements Element {
  constructor(public value: number) {}

  accept(visitor: Visitor): void {
    visitor.visitElementB(this);
  }
}

class ConcreteVisitor1 implements Visitor {
  visitElementA(element: ConcreteElementA): void {
    console.log(`Visitor1 visiting ElementA: ${element.value}`);
  }

  visitElementB(element: ConcreteElementB): void {
    console.log(`Visitor1 visiting ElementB: ${element.value}`);
  }
}

class ConcreteVisitor2 implements Visitor {
  visitElementA(element: ConcreteElementA): void {
    console.log(`Visitor2 visiting ElementA: ${element.value.toUpperCase()}`);
  }

  visitElementB(element: ConcreteElementB): void {
    console.log(`Visitor2 visiting ElementB: ${element.value * 2}`);
  }
}

// Usage
const elements: Element[] = [
  new ConcreteElementA('hello'),
  new ConcreteElementB(42),
];

const visitor1 = new ConcreteVisitor1();
const visitor2 = new ConcreteVisitor2();

elements.forEach(e => e.accept(visitor1));
elements.forEach(e => e.accept(visitor2));
```

## Related

- [README.md](README.md) - Pattern overview
- [checklist.md](checklist.md) - Implementation checklist
- [examples.md](examples.md) - Real-world examples
- [llm-prompts.md](llm-prompts.md) - LLM prompts
