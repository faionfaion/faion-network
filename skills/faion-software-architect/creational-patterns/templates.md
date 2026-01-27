# Creational Patterns Templates

> Copy-paste templates for quick implementation.

## Table of Contents

- [Factory Method](#factory-method)
- [Abstract Factory](#abstract-factory)
- [Builder](#builder)
- [Singleton](#singleton)
- [Prototype](#prototype)
- [Dependency Injection](#dependency-injection)
- [Object Pool](#object-pool)

---

## Factory Method

### Python Template

```python
from abc import ABC, abstractmethod
from typing import Protocol, TypeVar

# Product protocol
class Product(Protocol):
    def operation(self) -> str: ...

# Concrete products
class ConcreteProductA:
    def operation(self) -> str:
        return "ProductA"

class ConcreteProductB:
    def operation(self) -> str:
        return "ProductB"

# Factory with registry (recommended)
T = TypeVar("T", bound=Product)

class Factory:
    _registry: dict[str, type[Product]] = {}

    @classmethod
    def register(cls, key: str):
        def decorator(product_cls: type[T]) -> type[T]:
            cls._registry[key] = product_cls
            return product_cls
        return decorator

    @classmethod
    def create(cls, key: str, **kwargs) -> Product:
        if key not in cls._registry:
            raise ValueError(f"Unknown product: {key}")
        return cls._registry[key](**kwargs)

# Register products
Factory.register("a")(ConcreteProductA)
Factory.register("b")(ConcreteProductB)

# Usage
product = Factory.create("a")
print(product.operation())
```

### TypeScript Template

```typescript
// Product interface
interface Product {
  operation(): string;
}

// Concrete products
class ConcreteProductA implements Product {
  operation(): string {
    return "ProductA";
  }
}

class ConcreteProductB implements Product {
  operation(): string {
    return "ProductB";
  }
}

// Factory with type-safe registry
type ProductKey = "a" | "b";

const productRegistry: Record<ProductKey, () => Product> = {
  a: () => new ConcreteProductA(),
  b: () => new ConcreteProductB(),
};

function createProduct(key: ProductKey): Product {
  return productRegistry[key]();
}

// Usage
const product = createProduct("a");
console.log(product.operation());
```

### Go Template

```go
package factory

import "fmt"

// Product interface
type Product interface {
    Operation() string
}

// Concrete products
type ConcreteProductA struct{}

func (p *ConcreteProductA) Operation() string {
    return "ProductA"
}

type ConcreteProductB struct{}

func (p *ConcreteProductB) Operation() string {
    return "ProductB"
}

// Factory with registry
type ProductFactory func() Product

var registry = map[string]ProductFactory{}

func Register(key string, factory ProductFactory) {
    registry[key] = factory
}

func Create(key string) (Product, error) {
    factory, ok := registry[key]
    if !ok {
        return nil, fmt.Errorf("unknown product: %s", key)
    }
    return factory(), nil
}

func init() {
    Register("a", func() Product { return &ConcreteProductA{} })
    Register("b", func() Product { return &ConcreteProductB{} })
}
```

---

## Abstract Factory

### Python Template

```python
from abc import ABC, abstractmethod

# Abstract products
class AbstractProductA(ABC):
    @abstractmethod
    def feature_a(self) -> str: ...

class AbstractProductB(ABC):
    @abstractmethod
    def feature_b(self) -> str: ...

# Concrete product family 1
class ProductA1(AbstractProductA):
    def feature_a(self) -> str:
        return "A1"

class ProductB1(AbstractProductB):
    def feature_b(self) -> str:
        return "B1"

# Concrete product family 2
class ProductA2(AbstractProductA):
    def feature_a(self) -> str:
        return "A2"

class ProductB2(AbstractProductB):
    def feature_b(self) -> str:
        return "B2"

# Abstract factory
class AbstractFactory(ABC):
    @abstractmethod
    def create_product_a(self) -> AbstractProductA: ...

    @abstractmethod
    def create_product_b(self) -> AbstractProductB: ...

# Concrete factories
class ConcreteFactory1(AbstractFactory):
    def create_product_a(self) -> AbstractProductA:
        return ProductA1()

    def create_product_b(self) -> AbstractProductB:
        return ProductB1()

class ConcreteFactory2(AbstractFactory):
    def create_product_a(self) -> AbstractProductA:
        return ProductA2()

    def create_product_b(self) -> AbstractProductB:
        return ProductB2()

# Factory selector
def get_factory(variant: str) -> AbstractFactory:
    factories = {
        "1": ConcreteFactory1(),
        "2": ConcreteFactory2(),
    }
    return factories.get(variant, ConcreteFactory1())
```

### TypeScript Template

```typescript
// Abstract products
interface AbstractProductA {
  featureA(): string;
}

interface AbstractProductB {
  featureB(): string;
}

// Concrete product family 1
class ProductA1 implements AbstractProductA {
  featureA(): string { return "A1"; }
}

class ProductB1 implements AbstractProductB {
  featureB(): string { return "B1"; }
}

// Concrete product family 2
class ProductA2 implements AbstractProductA {
  featureA(): string { return "A2"; }
}

class ProductB2 implements AbstractProductB {
  featureB(): string { return "B2"; }
}

// Abstract factory
interface AbstractFactory {
  createProductA(): AbstractProductA;
  createProductB(): AbstractProductB;
}

// Concrete factories
class ConcreteFactory1 implements AbstractFactory {
  createProductA(): AbstractProductA { return new ProductA1(); }
  createProductB(): AbstractProductB { return new ProductB1(); }
}

class ConcreteFactory2 implements AbstractFactory {
  createProductA(): AbstractProductA { return new ProductA2(); }
  createProductB(): AbstractProductB { return new ProductB2(); }
}

// Factory selector
type FactoryVariant = "1" | "2";

function getFactory(variant: FactoryVariant): AbstractFactory {
  const factories: Record<FactoryVariant, AbstractFactory> = {
    "1": new ConcreteFactory1(),
    "2": new ConcreteFactory2(),
  };
  return factories[variant];
}
```

---

## Builder

### Python Template

```python
from dataclasses import dataclass, field
from typing import Self

@dataclass(frozen=True)
class Product:
    """Immutable product."""
    required_field: str
    optional_field_a: str = ""
    optional_field_b: int = 0
    optional_field_c: list[str] = field(default_factory=list)

class ProductBuilder:
    def __init__(self, required_field: str):
        self._required_field = required_field
        self._optional_field_a = ""
        self._optional_field_b = 0
        self._optional_field_c: list[str] = []

    def with_field_a(self, value: str) -> Self:
        self._optional_field_a = value
        return self

    def with_field_b(self, value: int) -> Self:
        self._optional_field_b = value
        return self

    def with_field_c(self, value: list[str]) -> Self:
        self._optional_field_c = value.copy()
        return self

    def add_to_field_c(self, item: str) -> Self:
        self._optional_field_c.append(item)
        return self

    def build(self) -> Product:
        # Validation
        if not self._required_field:
            raise ValueError("required_field cannot be empty")

        return Product(
            required_field=self._required_field,
            optional_field_a=self._optional_field_a,
            optional_field_b=self._optional_field_b,
            optional_field_c=self._optional_field_c.copy(),
        )

# Usage
product = (
    ProductBuilder("required")
    .with_field_a("optional a")
    .with_field_b(42)
    .add_to_field_c("item1")
    .add_to_field_c("item2")
    .build()
)
```

### TypeScript Template

```typescript
interface Product {
  readonly requiredField: string;
  readonly optionalFieldA: string;
  readonly optionalFieldB: number;
  readonly optionalFieldC: readonly string[];
}

class ProductBuilder {
  private _requiredField: string;
  private _optionalFieldA = "";
  private _optionalFieldB = 0;
  private _optionalFieldC: string[] = [];

  constructor(requiredField: string) {
    this._requiredField = requiredField;
  }

  withFieldA(value: string): this {
    this._optionalFieldA = value;
    return this;
  }

  withFieldB(value: number): this {
    this._optionalFieldB = value;
    return this;
  }

  withFieldC(value: string[]): this {
    this._optionalFieldC = [...value];
    return this;
  }

  addToFieldC(item: string): this {
    this._optionalFieldC.push(item);
    return this;
  }

  build(): Product {
    if (!this._requiredField) {
      throw new Error("requiredField cannot be empty");
    }

    return Object.freeze({
      requiredField: this._requiredField,
      optionalFieldA: this._optionalFieldA,
      optionalFieldB: this._optionalFieldB,
      optionalFieldC: Object.freeze([...this._optionalFieldC]),
    });
  }
}

// Usage
const product = new ProductBuilder("required")
  .withFieldA("optional a")
  .withFieldB(42)
  .addToFieldC("item1")
  .addToFieldC("item2")
  .build();
```

### Go Template (Functional Options)

```go
package builder

import "errors"

type Product struct {
    RequiredField  string
    OptionalFieldA string
    OptionalFieldB int
    OptionalFieldC []string
}

type ProductOption func(*Product) error

func WithFieldA(value string) ProductOption {
    return func(p *Product) error {
        p.OptionalFieldA = value
        return nil
    }
}

func WithFieldB(value int) ProductOption {
    return func(p *Product) error {
        if value < 0 {
            return errors.New("field B must be non-negative")
        }
        p.OptionalFieldB = value
        return nil
    }
}

func WithFieldC(values ...string) ProductOption {
    return func(p *Product) error {
        p.OptionalFieldC = append(p.OptionalFieldC, values...)
        return nil
    }
}

func NewProduct(requiredField string, opts ...ProductOption) (*Product, error) {
    if requiredField == "" {
        return nil, errors.New("requiredField cannot be empty")
    }

    p := &Product{
        RequiredField:  requiredField,
        OptionalFieldC: []string{},
    }

    for _, opt := range opts {
        if err := opt(p); err != nil {
            return nil, err
        }
    }

    return p, nil
}

// Usage
// product, err := NewProduct("required",
//     WithFieldA("optional a"),
//     WithFieldB(42),
//     WithFieldC("item1", "item2"),
// )
```

---

## Singleton

### Python Template (Module-Level)

```python
# config.py - Recommended approach
from dataclasses import dataclass
from functools import lru_cache
import os

@dataclass(frozen=True)
class Config:
    setting_a: str
    setting_b: int
    setting_c: bool

@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config(
        setting_a=os.getenv("SETTING_A", "default"),
        setting_b=int(os.getenv("SETTING_B", "0")),
        setting_c=os.getenv("SETTING_C", "false").lower() == "true",
    )

# Usage
config = get_config()
```

### Python Template (Class-Based)

```python
class Singleton:
    _instance: "Singleton | None" = None
    _initialized: bool = False

    def __new__(cls) -> "Singleton":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        # Initialize here
        self.value = "initialized"

    @classmethod
    def reset(cls) -> None:
        """For testing only."""
        cls._instance = None
        cls._initialized = False
```

### TypeScript Template

```typescript
// Module-level singleton (recommended)
interface Config {
  readonly settingA: string;
  readonly settingB: number;
  readonly settingC: boolean;
}

const getConfig = (() => {
  let instance: Config | null = null;

  return (): Config => {
    if (instance === null) {
      instance = Object.freeze({
        settingA: process.env.SETTING_A || "default",
        settingB: parseInt(process.env.SETTING_B || "0", 10),
        settingC: process.env.SETTING_C === "true",
      });
    }
    return instance;
  };
})();

export { getConfig };
```

### Go Template

```go
package singleton

import "sync"

type Config struct {
    SettingA string
    SettingB int
    SettingC bool
}

var (
    instance *Config
    once     sync.Once
)

func GetConfig() *Config {
    once.Do(func() {
        instance = &Config{
            SettingA: getEnvOrDefault("SETTING_A", "default"),
            SettingB: getEnvIntOrDefault("SETTING_B", 0),
            SettingC: getEnvOrDefault("SETTING_C", "false") == "true",
        }
    })
    return instance
}

func getEnvOrDefault(key, defaultValue string) string {
    if value := os.Getenv(key); value != "" {
        return value
    }
    return defaultValue
}

func getEnvIntOrDefault(key string, defaultValue int) int {
    if value := os.Getenv(key); value != "" {
        if i, err := strconv.Atoi(value); err == nil {
            return i
        }
    }
    return defaultValue
}
```

---

## Prototype

### Python Template

```python
from __future__ import annotations
import copy
from dataclasses import dataclass, field
from typing import Self

@dataclass
class Prototype:
    field_a: str
    field_b: int
    nested: dict[str, str] = field(default_factory=dict)

    def clone(self) -> Self:
        """Deep clone."""
        return copy.deepcopy(self)

    def shallow_clone(self) -> Prototype:
        """Shallow clone (nested objects shared)."""
        return Prototype(
            field_a=self.field_a,
            field_b=self.field_b,
            nested=self.nested,  # Shared reference
        )

# Registry for prototypes
class PrototypeRegistry:
    _prototypes: dict[str, Prototype] = {}

    @classmethod
    def register(cls, key: str, prototype: Prototype) -> None:
        cls._prototypes[key] = prototype

    @classmethod
    def create(cls, key: str) -> Prototype:
        if key not in cls._prototypes:
            raise ValueError(f"Unknown prototype: {key}")
        return cls._prototypes[key].clone()

# Usage
PrototypeRegistry.register("default", Prototype("a", 1, {"key": "value"}))
clone = PrototypeRegistry.create("default")
```

### TypeScript Template

```typescript
interface Prototype<T> {
  clone(): T;
}

interface ProductData {
  fieldA: string;
  fieldB: number;
  nested: Record<string, string>;
}

class Product implements Prototype<Product> {
  fieldA: string;
  fieldB: number;
  nested: Record<string, string>;

  constructor(data: ProductData) {
    this.fieldA = data.fieldA;
    this.fieldB = data.fieldB;
    this.nested = data.nested;
  }

  clone(): Product {
    // Using structuredClone for deep copy (Node 17+)
    return new Product(structuredClone({
      fieldA: this.fieldA,
      fieldB: this.fieldB,
      nested: this.nested,
    }));
  }
}

// Registry
class PrototypeRegistry {
  private static prototypes = new Map<string, Prototype<any>>();

  static register<T extends Prototype<T>>(key: string, prototype: T): void {
    this.prototypes.set(key, prototype);
  }

  static create<T extends Prototype<T>>(key: string): T {
    const prototype = this.prototypes.get(key);
    if (!prototype) {
      throw new Error(`Unknown prototype: ${key}`);
    }
    return prototype.clone() as T;
  }
}
```

---

## Dependency Injection

### Python Template (Manual)

```python
from abc import ABC, abstractmethod
from typing import Protocol

# Interface
class Repository(Protocol):
    def get(self, id: int) -> dict | None: ...
    def save(self, data: dict) -> dict: ...

# Implementation
class PostgresRepository:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def get(self, id: int) -> dict | None:
        return {"id": id}

    def save(self, data: dict) -> dict:
        return data

# Service with injected dependency
class Service:
    def __init__(self, repository: Repository):
        self._repository = repository

    def get_item(self, id: int) -> dict | None:
        return self._repository.get(id)

# Composition root
def create_service() -> Service:
    repo = PostgresRepository("postgresql://localhost/db")
    return Service(repo)

# For testing
class InMemoryRepository:
    def __init__(self):
        self._data: dict[int, dict] = {}

    def get(self, id: int) -> dict | None:
        return self._data.get(id)

    def save(self, data: dict) -> dict:
        self._data[data["id"]] = data
        return data

def create_test_service() -> Service:
    return Service(InMemoryRepository())
```

### TypeScript Template (Manual)

```typescript
// Interface
interface Repository {
  get(id: number): Promise<Record<string, any> | null>;
  save(data: Record<string, any>): Promise<Record<string, any>>;
}

// Implementation
class PostgresRepository implements Repository {
  constructor(private connectionString: string) {}

  async get(id: number): Promise<Record<string, any> | null> {
    return { id };
  }

  async save(data: Record<string, any>): Promise<Record<string, any>> {
    return data;
  }
}

// Service
class Service {
  constructor(private repository: Repository) {}

  async getItem(id: number): Promise<Record<string, any> | null> {
    return this.repository.get(id);
  }
}

// Composition root
function createService(): Service {
  const repo = new PostgresRepository("postgresql://localhost/db");
  return new Service(repo);
}

// For testing
class InMemoryRepository implements Repository {
  private data = new Map<number, Record<string, any>>();

  async get(id: number): Promise<Record<string, any> | null> {
    return this.data.get(id) || null;
  }

  async save(data: Record<string, any>): Promise<Record<string, any>> {
    this.data.set(data.id, data);
    return data;
  }
}

function createTestService(): Service {
  return new Service(new InMemoryRepository());
}
```

### Go Template

```go
package di

import "context"

// Interface
type Repository interface {
    Get(ctx context.Context, id int) (map[string]any, error)
    Save(ctx context.Context, data map[string]any) (map[string]any, error)
}

// Implementation
type PostgresRepository struct {
    connectionString string
}

func NewPostgresRepository(connStr string) *PostgresRepository {
    return &PostgresRepository{connectionString: connStr}
}

func (r *PostgresRepository) Get(ctx context.Context, id int) (map[string]any, error) {
    return map[string]any{"id": id}, nil
}

func (r *PostgresRepository) Save(ctx context.Context, data map[string]any) (map[string]any, error) {
    return data, nil
}

// Service
type Service struct {
    repo Repository
}

func NewService(repo Repository) *Service {
    return &Service{repo: repo}
}

func (s *Service) GetItem(ctx context.Context, id int) (map[string]any, error) {
    return s.repo.Get(ctx, id)
}

// Composition root
func CreateService(connStr string) *Service {
    repo := NewPostgresRepository(connStr)
    return NewService(repo)
}

// For testing
type InMemoryRepository struct {
    data map[int]map[string]any
}

func NewInMemoryRepository() *InMemoryRepository {
    return &InMemoryRepository{data: make(map[int]map[string]any)}
}

func (r *InMemoryRepository) Get(ctx context.Context, id int) (map[string]any, error) {
    if data, ok := r.data[id]; ok {
        return data, nil
    }
    return nil, nil
}

func (r *InMemoryRepository) Save(ctx context.Context, data map[string]any) (map[string]any, error) {
    if id, ok := data["id"].(int); ok {
        r.data[id] = data
    }
    return data, nil
}

func CreateTestService() *Service {
    return NewService(NewInMemoryRepository())
}
```

---

## Object Pool

### Python Template

```python
from contextlib import contextmanager
from queue import Queue, Empty
from typing import Callable, Generator, TypeVar
import threading

T = TypeVar("T")

class ObjectPool[T]:
    def __init__(
        self,
        factory: Callable[[], T],
        reset: Callable[[T], None],
        validate: Callable[[T], bool] = lambda x: True,
        min_size: int = 5,
        max_size: int = 20,
        timeout: float = 30.0,
    ):
        self._factory = factory
        self._reset = reset
        self._validate = validate
        self._min_size = min_size
        self._max_size = max_size
        self._timeout = timeout
        self._pool: Queue[T] = Queue()
        self._size = 0
        self._lock = threading.Lock()

        for _ in range(min_size):
            self._pool.put(self._factory())
            self._size += 1

    def acquire(self) -> T:
        try:
            obj = self._pool.get(timeout=self._timeout)
            if not self._validate(obj):
                with self._lock:
                    self._size -= 1
                return self.acquire()
            return obj
        except Empty:
            with self._lock:
                if self._size < self._max_size:
                    self._size += 1
                    return self._factory()
            raise TimeoutError("Pool exhausted")

    def release(self, obj: T) -> None:
        self._reset(obj)
        self._pool.put(obj)

    @contextmanager
    def get(self) -> Generator[T, None, None]:
        obj = self.acquire()
        try:
            yield obj
        finally:
            self.release(obj)

    @property
    def stats(self) -> dict[str, int]:
        return {
            "total": self._size,
            "available": self._pool.qsize(),
            "in_use": self._size - self._pool.qsize(),
        }

# Usage example
# pool = ObjectPool(
#     factory=lambda: create_connection(),
#     reset=lambda conn: conn.reset(),
#     validate=lambda conn: conn.is_valid(),
#     min_size=5,
#     max_size=20,
# )
# with pool.get() as conn:
#     conn.query("SELECT 1")
```

### Go Template

```go
package pool

import (
    "context"
    "errors"
    "sync"
    "time"
)

var (
    ErrPoolExhausted = errors.New("pool exhausted")
    ErrPoolClosed    = errors.New("pool closed")
)

type Pool[T any] struct {
    factory  func() (T, error)
    reset    func(T)
    validate func(T) bool
    items    chan T
    size     int
    maxSize  int
    timeout  time.Duration
    mu       sync.Mutex
    closed   bool
}

type PoolConfig[T any] struct {
    Factory  func() (T, error)
    Reset    func(T)
    Validate func(T) bool
    MinSize  int
    MaxSize  int
    Timeout  time.Duration
}

func NewPool[T any](cfg PoolConfig[T]) (*Pool[T], error) {
    p := &Pool[T]{
        factory:  cfg.Factory,
        reset:    cfg.Reset,
        validate: cfg.Validate,
        items:    make(chan T, cfg.MaxSize),
        maxSize:  cfg.MaxSize,
        timeout:  cfg.Timeout,
    }

    if p.validate == nil {
        p.validate = func(T) bool { return true }
    }

    for i := 0; i < cfg.MinSize; i++ {
        item, err := p.factory()
        if err != nil {
            return nil, err
        }
        p.items <- item
        p.size++
    }

    return p, nil
}

func (p *Pool[T]) Acquire(ctx context.Context) (T, error) {
    var zero T
    if p.closed {
        return zero, ErrPoolClosed
    }

    select {
    case item := <-p.items:
        if !p.validate(item) {
            p.mu.Lock()
            p.size--
            p.mu.Unlock()
            return p.Acquire(ctx)
        }
        return item, nil
    case <-time.After(p.timeout):
        p.mu.Lock()
        defer p.mu.Unlock()
        if p.size < p.maxSize {
            p.size++
            return p.factory()
        }
        return zero, ErrPoolExhausted
    case <-ctx.Done():
        return zero, ctx.Err()
    }
}

func (p *Pool[T]) Release(item T) {
    if p.closed {
        return
    }
    if p.reset != nil {
        p.reset(item)
    }
    p.items <- item
}

func (p *Pool[T]) With(ctx context.Context, fn func(T) error) error {
    item, err := p.Acquire(ctx)
    if err != nil {
        return err
    }
    defer p.Release(item)
    return fn(item)
}

func (p *Pool[T]) Stats() map[string]int {
    return map[string]int{
        "total":     p.size,
        "available": len(p.items),
        "in_use":    p.size - len(p.items),
    }
}

func (p *Pool[T]) Close() {
    p.mu.Lock()
    defer p.mu.Unlock()
    p.closed = true
    close(p.items)
}
```

---

## Quick Reference

### Pattern Selection

| Need | Pattern |
|------|---------|
| Create based on type | Factory Method |
| Create product families | Abstract Factory |
| Many optional params | Builder |
| Single global instance | Singleton (or DI) |
| Clone objects | Prototype |
| Testable, loose coupling | Dependency Injection |
| Reuse expensive objects | Object Pool |

### Common Mistakes to Avoid

| Mistake | Better Approach |
|---------|-----------------|
| Factory for one type | Simple constructor |
| Builder for 2 params | Constructor |
| Singleton everywhere | Dependency Injection |
| No reset in pool | Always reset before reuse |
| Shallow clone when deep needed | Use `deepcopy`/`structuredClone` |

---

## Related Files

| File | Description |
|------|-------------|
| [README.md](README.md) | Pattern overview |
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Full examples |
| [llm-prompts.md](llm-prompts.md) | LLM prompts |
