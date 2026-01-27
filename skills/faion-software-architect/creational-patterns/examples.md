# Creational Patterns Examples

> Real implementations in Python, TypeScript, and Go.

## Table of Contents

- [Factory Method](#factory-method)
- [Abstract Factory](#abstract-factory)
- [Builder](#builder)
- [Singleton and Alternatives](#singleton-and-alternatives)
- [Prototype](#prototype)
- [Dependency Injection](#dependency-injection)
- [Object Pool](#object-pool)

---

## Factory Method

### Use Case: Notification System

Create different notification types (email, SMS, push) based on user preferences.

### Python

```python
from abc import ABC, abstractmethod
from typing import Protocol
from dataclasses import dataclass

# Product interface
class Notification(Protocol):
    def send(self, recipient: str, message: str) -> bool: ...

# Concrete products
@dataclass
class EmailNotification:
    smtp_server: str = "smtp.example.com"

    def send(self, recipient: str, message: str) -> bool:
        print(f"Email to {recipient}: {message}")
        return True

@dataclass
class SMSNotification:
    api_key: str = "sms-api-key"

    def send(self, recipient: str, message: str) -> bool:
        print(f"SMS to {recipient}: {message}")
        return True

@dataclass
class PushNotification:
    app_id: str = "app-123"

    def send(self, recipient: str, message: str) -> bool:
        print(f"Push to {recipient}: {message}")
        return True

# Factory with registry pattern (modern approach)
class NotificationFactory:
    _registry: dict[str, type[Notification]] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator to register notification types."""
        def decorator(notification_cls: type[Notification]):
            cls._registry[name] = notification_cls
            return notification_cls
        return decorator

    @classmethod
    def create(cls, notification_type: str, **kwargs) -> Notification:
        if notification_type not in cls._registry:
            raise ValueError(f"Unknown notification type: {notification_type}")
        return cls._registry[notification_type](**kwargs)

# Register types (can be in separate files)
NotificationFactory.register("email")(EmailNotification)
NotificationFactory.register("sms")(SMSNotification)
NotificationFactory.register("push")(PushNotification)

# Usage
notification = NotificationFactory.create("email", smtp_server="custom.smtp.com")
notification.send("user@example.com", "Hello!")

# Extension: Just register new type
@NotificationFactory.register("slack")
@dataclass
class SlackNotification:
    webhook_url: str = "https://hooks.slack.com/..."

    def send(self, recipient: str, message: str) -> bool:
        print(f"Slack to {recipient}: {message}")
        return True
```

### TypeScript

```typescript
// Product interface
interface Notification {
  send(recipient: string, message: string): Promise<boolean>;
}

// Concrete products
class EmailNotification implements Notification {
  constructor(private smtpServer: string = "smtp.example.com") {}

  async send(recipient: string, message: string): Promise<boolean> {
    console.log(`Email to ${recipient}: ${message}`);
    return true;
  }
}

class SMSNotification implements Notification {
  constructor(private apiKey: string = "sms-api-key") {}

  async send(recipient: string, message: string): Promise<boolean> {
    console.log(`SMS to ${recipient}: ${message}`);
    return true;
  }
}

class PushNotification implements Notification {
  constructor(private appId: string = "app-123") {}

  async send(recipient: string, message: string): Promise<boolean> {
    console.log(`Push to ${recipient}: ${message}`);
    return true;
  }
}

// Factory with type-safe registry
type NotificationConfig = {
  email: { smtpServer?: string };
  sms: { apiKey?: string };
  push: { appId?: string };
};

type NotificationType = keyof NotificationConfig;

const notificationRegistry = {
  email: (config: NotificationConfig["email"]) => new EmailNotification(config.smtpServer),
  sms: (config: NotificationConfig["sms"]) => new SMSNotification(config.apiKey),
  push: (config: NotificationConfig["push"]) => new PushNotification(config.appId),
};

function createNotification<T extends NotificationType>(
  type: T,
  config: NotificationConfig[T]
): Notification {
  return notificationRegistry[type](config);
}

// Usage - type-safe!
const notification = createNotification("email", { smtpServer: "custom.smtp.com" });
await notification.send("user@example.com", "Hello!");
```

### Go

```go
package notification

import "fmt"

// Product interface
type Notification interface {
    Send(recipient, message string) error
}

// Concrete products
type EmailNotification struct {
    SMTPServer string
}

func (e *EmailNotification) Send(recipient, message string) error {
    fmt.Printf("Email to %s: %s\n", recipient, message)
    return nil
}

type SMSNotification struct {
    APIKey string
}

func (s *SMSNotification) Send(recipient, message string) error {
    fmt.Printf("SMS to %s: %s\n", recipient, message)
    return nil
}

// Factory function pattern (idiomatic Go)
type NotificationFactory func() Notification

var registry = map[string]NotificationFactory{}

func Register(name string, factory NotificationFactory) {
    registry[name] = factory
}

func Create(notificationType string) (Notification, error) {
    factory, ok := registry[notificationType]
    if !ok {
        return nil, fmt.Errorf("unknown notification type: %s", notificationType)
    }
    return factory(), nil
}

// Functional options for configuration
type EmailOption func(*EmailNotification)

func WithSMTPServer(server string) EmailOption {
    return func(e *EmailNotification) {
        e.SMTPServer = server
    }
}

func NewEmailNotification(opts ...EmailOption) Notification {
    e := &EmailNotification{SMTPServer: "smtp.example.com"}
    for _, opt := range opts {
        opt(e)
    }
    return e
}

// Register in init
func init() {
    Register("email", func() Notification {
        return NewEmailNotification()
    })
    Register("sms", func() Notification {
        return &SMSNotification{APIKey: "default-key"}
    })
}

// Usage
// notification, _ := Create("email")
// notification.Send("user@example.com", "Hello!")
```

---

## Abstract Factory

### Use Case: Cross-Platform UI Components

Create themed UI components (Button, Input, Modal) for different platforms.

### Python

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

# Abstract products
class Button(Protocol):
    def render(self) -> str: ...
    def click(self) -> None: ...

class Input(Protocol):
    def render(self) -> str: ...
    def get_value(self) -> str: ...

class Modal(Protocol):
    def render(self) -> str: ...
    def show(self) -> None: ...
    def hide(self) -> None: ...

# Material Design family
@dataclass
class MaterialButton:
    label: str

    def render(self) -> str:
        return f'<button class="md-button">{self.label}</button>'

    def click(self) -> None:
        print("Material ripple effect")

@dataclass
class MaterialInput:
    placeholder: str
    _value: str = ""

    def render(self) -> str:
        return f'<input class="md-input" placeholder="{self.placeholder}"/>'

    def get_value(self) -> str:
        return self._value

@dataclass
class MaterialModal:
    title: str

    def render(self) -> str:
        return f'<div class="md-modal"><h2>{self.title}</h2></div>'

    def show(self) -> None:
        print("Material slide-up animation")

    def hide(self) -> None:
        print("Material fade-out animation")

# iOS family
@dataclass
class IOSButton:
    label: str

    def render(self) -> str:
        return f'<button class="ios-button">{self.label}</button>'

    def click(self) -> None:
        print("iOS haptic feedback")

@dataclass
class IOSInput:
    placeholder: str
    _value: str = ""

    def render(self) -> str:
        return f'<input class="ios-input" placeholder="{self.placeholder}"/>'

    def get_value(self) -> str:
        return self._value

@dataclass
class IOSModal:
    title: str

    def render(self) -> str:
        return f'<div class="ios-modal"><h2>{self.title}</h2></div>'

    def show(self) -> None:
        print("iOS slide-from-bottom")

    def hide(self) -> None:
        print("iOS slide-to-bottom")

# Abstract factory
class UIFactory(ABC):
    @abstractmethod
    def create_button(self, label: str) -> Button: ...

    @abstractmethod
    def create_input(self, placeholder: str) -> Input: ...

    @abstractmethod
    def create_modal(self, title: str) -> Modal: ...

# Concrete factories
class MaterialUIFactory(UIFactory):
    def create_button(self, label: str) -> Button:
        return MaterialButton(label)

    def create_input(self, placeholder: str) -> Input:
        return MaterialInput(placeholder)

    def create_modal(self, title: str) -> Modal:
        return MaterialModal(title)

class IOSUIFactory(UIFactory):
    def create_button(self, label: str) -> Button:
        return IOSButton(label)

    def create_input(self, placeholder: str) -> Input:
        return IOSInput(placeholder)

    def create_modal(self, title: str) -> Modal:
        return IOSModal(title)

# Factory selector
def get_ui_factory(platform: str) -> UIFactory:
    factories = {
        "material": MaterialUIFactory(),
        "ios": IOSUIFactory(),
    }
    return factories.get(platform, MaterialUIFactory())

# Usage
factory = get_ui_factory("ios")
button = factory.create_button("Submit")
input_field = factory.create_input("Enter name...")
modal = factory.create_modal("Confirm")

print(button.render())  # <button class="ios-button">Submit</button>
```

### TypeScript

```typescript
// Abstract products
interface Button {
  render(): string;
  onClick(): void;
}

interface Input {
  render(): string;
  getValue(): string;
}

interface Modal {
  render(): string;
  show(): void;
  hide(): void;
}

// Material Design family
class MaterialButton implements Button {
  constructor(private label: string) {}

  render(): string {
    return `<button class="md-button">${this.label}</button>`;
  }

  onClick(): void {
    console.log("Material ripple effect");
  }
}

class MaterialInput implements Input {
  private value = "";
  constructor(private placeholder: string) {}

  render(): string {
    return `<input class="md-input" placeholder="${this.placeholder}"/>`;
  }

  getValue(): string {
    return this.value;
  }
}

class MaterialModal implements Modal {
  constructor(private title: string) {}

  render(): string {
    return `<div class="md-modal"><h2>${this.title}</h2></div>`;
  }

  show(): void { console.log("Material slide-up"); }
  hide(): void { console.log("Material fade-out"); }
}

// iOS family (similar structure)
class IOSButton implements Button {
  constructor(private label: string) {}
  render(): string { return `<button class="ios-button">${this.label}</button>`; }
  onClick(): void { console.log("iOS haptic feedback"); }
}

class IOSInput implements Input {
  private value = "";
  constructor(private placeholder: string) {}
  render(): string { return `<input class="ios-input" placeholder="${this.placeholder}"/>`; }
  getValue(): string { return this.value; }
}

class IOSModal implements Modal {
  constructor(private title: string) {}
  render(): string { return `<div class="ios-modal"><h2>${this.title}</h2></div>`; }
  show(): void { console.log("iOS slide-from-bottom"); }
  hide(): void { console.log("iOS slide-to-bottom"); }
}

// Abstract factory
interface UIFactory {
  createButton(label: string): Button;
  createInput(placeholder: string): Input;
  createModal(title: string): Modal;
}

// Concrete factories
class MaterialUIFactory implements UIFactory {
  createButton(label: string): Button { return new MaterialButton(label); }
  createInput(placeholder: string): Input { return new MaterialInput(placeholder); }
  createModal(title: string): Modal { return new MaterialModal(title); }
}

class IOSUIFactory implements UIFactory {
  createButton(label: string): Button { return new IOSButton(label); }
  createInput(placeholder: string): Input { return new IOSInput(placeholder); }
  createModal(title: string): Modal { return new IOSModal(title); }
}

// Factory selector with type safety
type Platform = "material" | "ios";

function getUIFactory(platform: Platform): UIFactory {
  const factories: Record<Platform, UIFactory> = {
    material: new MaterialUIFactory(),
    ios: new IOSUIFactory(),
  };
  return factories[platform];
}

// Usage
const factory = getUIFactory("ios");
const button = factory.createButton("Submit");
console.log(button.render()); // <button class="ios-button">Submit</button>
```

---

## Builder

### Use Case: HTTP Request Builder

Build complex HTTP requests with many optional parameters.

### Python

```python
from dataclasses import dataclass, field
from typing import Self
from enum import Enum

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

@dataclass(frozen=True)  # Immutable
class HTTPRequest:
    url: str
    method: HTTPMethod
    headers: dict[str, str] = field(default_factory=dict)
    query_params: dict[str, str] = field(default_factory=dict)
    body: str | dict | None = None
    timeout: int = 30
    retries: int = 3
    auth: tuple[str, str] | None = None

class HTTPRequestBuilder:
    def __init__(self, url: str):
        self._url = url
        self._method = HTTPMethod.GET
        self._headers: dict[str, str] = {}
        self._query_params: dict[str, str] = {}
        self._body: str | dict | None = None
        self._timeout = 30
        self._retries = 3
        self._auth: tuple[str, str] | None = None

    def method(self, method: HTTPMethod) -> Self:
        self._method = method
        return self

    def header(self, key: str, value: str) -> Self:
        self._headers[key] = value
        return self

    def headers(self, headers: dict[str, str]) -> Self:
        self._headers.update(headers)
        return self

    def query(self, key: str, value: str) -> Self:
        self._query_params[key] = value
        return self

    def body(self, body: str | dict) -> Self:
        self._body = body
        return self

    def json(self, data: dict) -> Self:
        self._body = data
        self._headers["Content-Type"] = "application/json"
        return self

    def timeout(self, seconds: int) -> Self:
        self._timeout = seconds
        return self

    def retries(self, count: int) -> Self:
        self._retries = count
        return self

    def basic_auth(self, username: str, password: str) -> Self:
        self._auth = (username, password)
        return self

    def bearer_token(self, token: str) -> Self:
        self._headers["Authorization"] = f"Bearer {token}"
        return self

    def build(self) -> HTTPRequest:
        # Validation
        if not self._url:
            raise ValueError("URL is required")
        if self._method in (HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH):
            if self._body is None:
                raise ValueError(f"{self._method.value} requires a body")

        return HTTPRequest(
            url=self._url,
            method=self._method,
            headers=self._headers.copy(),
            query_params=self._query_params.copy(),
            body=self._body,
            timeout=self._timeout,
            retries=self._retries,
            auth=self._auth,
        )

# Usage
request = (
    HTTPRequestBuilder("https://api.example.com/users")
    .method(HTTPMethod.POST)
    .header("X-Request-ID", "abc123")
    .bearer_token("eyJhbGciOiJIUzI1NiIs...")
    .json({"name": "John", "email": "john@example.com"})
    .timeout(10)
    .retries(5)
    .build()
)

print(request.url)     # https://api.example.com/users
print(request.method)  # HTTPMethod.POST
print(request.headers) # {'X-Request-ID': 'abc123', 'Content-Type': 'application/json', ...}
```

### TypeScript

```typescript
// Immutable request type
interface HTTPRequest {
  readonly url: string;
  readonly method: HTTPMethod;
  readonly headers: Readonly<Record<string, string>>;
  readonly queryParams: Readonly<Record<string, string>>;
  readonly body?: string | object;
  readonly timeout: number;
  readonly retries: number;
  readonly auth?: { username: string; password: string };
}

type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";

class HTTPRequestBuilder {
  private _url: string;
  private _method: HTTPMethod = "GET";
  private _headers: Record<string, string> = {};
  private _queryParams: Record<string, string> = {};
  private _body?: string | object;
  private _timeout = 30;
  private _retries = 3;
  private _auth?: { username: string; password: string };

  constructor(url: string) {
    this._url = url;
  }

  method(method: HTTPMethod): this {
    this._method = method;
    return this;
  }

  header(key: string, value: string): this {
    this._headers[key] = value;
    return this;
  }

  headers(headers: Record<string, string>): this {
    Object.assign(this._headers, headers);
    return this;
  }

  query(key: string, value: string): this {
    this._queryParams[key] = value;
    return this;
  }

  body(body: string | object): this {
    this._body = body;
    return this;
  }

  json(data: object): this {
    this._body = data;
    this._headers["Content-Type"] = "application/json";
    return this;
  }

  timeout(seconds: number): this {
    this._timeout = seconds;
    return this;
  }

  retries(count: number): this {
    this._retries = count;
    return this;
  }

  basicAuth(username: string, password: string): this {
    this._auth = { username, password };
    return this;
  }

  bearerToken(token: string): this {
    this._headers["Authorization"] = `Bearer ${token}`;
    return this;
  }

  build(): HTTPRequest {
    // Validation
    if (!this._url) {
      throw new Error("URL is required");
    }
    if (["POST", "PUT", "PATCH"].includes(this._method) && !this._body) {
      throw new Error(`${this._method} requires a body`);
    }

    return Object.freeze({
      url: this._url,
      method: this._method,
      headers: Object.freeze({ ...this._headers }),
      queryParams: Object.freeze({ ...this._queryParams }),
      body: this._body,
      timeout: this._timeout,
      retries: this._retries,
      auth: this._auth,
    });
  }
}

// Usage
const request = new HTTPRequestBuilder("https://api.example.com/users")
  .method("POST")
  .header("X-Request-ID", "abc123")
  .bearerToken("eyJhbGciOiJIUzI1NiIs...")
  .json({ name: "John", email: "john@example.com" })
  .timeout(10)
  .retries(5)
  .build();
```

### Go (Functional Options Pattern)

```go
package http

import (
    "errors"
    "time"
)

type HTTPMethod string

const (
    GET    HTTPMethod = "GET"
    POST   HTTPMethod = "POST"
    PUT    HTTPMethod = "PUT"
    DELETE HTTPMethod = "DELETE"
    PATCH  HTTPMethod = "PATCH"
)

type HTTPRequest struct {
    URL         string
    Method      HTTPMethod
    Headers     map[string]string
    QueryParams map[string]string
    Body        interface{}
    Timeout     time.Duration
    Retries     int
    Auth        *BasicAuth
}

type BasicAuth struct {
    Username string
    Password string
}

// Functional option type
type RequestOption func(*HTTPRequest) error

// Option functions
func WithMethod(method HTTPMethod) RequestOption {
    return func(r *HTTPRequest) error {
        r.Method = method
        return nil
    }
}

func WithHeader(key, value string) RequestOption {
    return func(r *HTTPRequest) error {
        if r.Headers == nil {
            r.Headers = make(map[string]string)
        }
        r.Headers[key] = value
        return nil
    }
}

func WithHeaders(headers map[string]string) RequestOption {
    return func(r *HTTPRequest) error {
        if r.Headers == nil {
            r.Headers = make(map[string]string)
        }
        for k, v := range headers {
            r.Headers[k] = v
        }
        return nil
    }
}

func WithQuery(key, value string) RequestOption {
    return func(r *HTTPRequest) error {
        if r.QueryParams == nil {
            r.QueryParams = make(map[string]string)
        }
        r.QueryParams[key] = value
        return nil
    }
}

func WithBody(body interface{}) RequestOption {
    return func(r *HTTPRequest) error {
        r.Body = body
        return nil
    }
}

func WithJSON(data interface{}) RequestOption {
    return func(r *HTTPRequest) error {
        r.Body = data
        if r.Headers == nil {
            r.Headers = make(map[string]string)
        }
        r.Headers["Content-Type"] = "application/json"
        return nil
    }
}

func WithTimeout(d time.Duration) RequestOption {
    return func(r *HTTPRequest) error {
        r.Timeout = d
        return nil
    }
}

func WithRetries(count int) RequestOption {
    return func(r *HTTPRequest) error {
        if count < 0 {
            return errors.New("retries must be non-negative")
        }
        r.Retries = count
        return nil
    }
}

func WithBasicAuth(username, password string) RequestOption {
    return func(r *HTTPRequest) error {
        r.Auth = &BasicAuth{Username: username, Password: password}
        return nil
    }
}

func WithBearerToken(token string) RequestOption {
    return func(r *HTTPRequest) error {
        if r.Headers == nil {
            r.Headers = make(map[string]string)
        }
        r.Headers["Authorization"] = "Bearer " + token
        return nil
    }
}

// Constructor with functional options
func NewRequest(url string, opts ...RequestOption) (*HTTPRequest, error) {
    r := &HTTPRequest{
        URL:     url,
        Method:  GET,
        Timeout: 30 * time.Second,
        Retries: 3,
    }

    for _, opt := range opts {
        if err := opt(r); err != nil {
            return nil, err
        }
    }

    // Validation
    if r.URL == "" {
        return nil, errors.New("URL is required")
    }
    if r.Method == POST || r.Method == PUT || r.Method == PATCH {
        if r.Body == nil {
            return nil, errors.New("body required for " + string(r.Method))
        }
    }

    return r, nil
}

// Usage
// request, err := NewRequest("https://api.example.com/users",
//     WithMethod(POST),
//     WithHeader("X-Request-ID", "abc123"),
//     WithBearerToken("eyJhbGciOiJIUzI1NiIs..."),
//     WithJSON(map[string]string{"name": "John"}),
//     WithTimeout(10*time.Second),
//     WithRetries(5),
// )
```

---

## Singleton and Alternatives

### Modern Alternative: Module-Level Instance

### Python

```python
# config.py - Module-level singleton (Pythonic approach)
from dataclasses import dataclass
from functools import lru_cache
import os

@dataclass(frozen=True)  # Immutable
class Config:
    database_url: str
    api_key: str
    debug: bool
    max_connections: int

@lru_cache(maxsize=1)  # Ensures single instance
def get_config() -> Config:
    """Load configuration once and cache it."""
    return Config(
        database_url=os.getenv("DATABASE_URL", "sqlite:///db.sqlite3"),
        api_key=os.getenv("API_KEY", ""),
        debug=os.getenv("DEBUG", "false").lower() == "true",
        max_connections=int(os.getenv("MAX_CONNECTIONS", "10")),
    )

# Usage
config = get_config()
print(config.database_url)

# Alternative: Class-based singleton for complex cases
class DatabaseConnection:
    _instance: "DatabaseConnection | None" = None

    def __new__(cls) -> "DatabaseConnection":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        # Expensive initialization
        print("Initializing database connection...")
        self.connection = self._connect()

    def _connect(self):
        # Actual connection logic
        return "connection"

    # Thread-safe alternative using __init_subclass__
    @classmethod
    def get_instance(cls) -> "DatabaseConnection":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
```

### TypeScript

```typescript
// config.ts - Module-level singleton
interface Config {
  readonly databaseUrl: string;
  readonly apiKey: string;
  readonly debug: boolean;
  readonly maxConnections: number;
}

// Lazy initialization with closure
const getConfig = (() => {
  let config: Config | null = null;

  return (): Config => {
    if (config === null) {
      config = Object.freeze({
        databaseUrl: process.env.DATABASE_URL || "sqlite:///db.sqlite3",
        apiKey: process.env.API_KEY || "",
        debug: process.env.DEBUG === "true",
        maxConnections: parseInt(process.env.MAX_CONNECTIONS || "10", 10),
      });
    }
    return config;
  };
})();

// Usage
const config = getConfig();
console.log(config.databaseUrl);

// Alternative: Class-based singleton
class Logger {
  private static instance: Logger | null = null;
  private logs: string[] = [];

  private constructor() {
    // Private constructor prevents direct instantiation
  }

  static getInstance(): Logger {
    if (Logger.instance === null) {
      Logger.instance = new Logger();
    }
    return Logger.instance;
  }

  log(message: string): void {
    const timestamp = new Date().toISOString();
    this.logs.push(`[${timestamp}] ${message}`);
    console.log(`[${timestamp}] ${message}`);
  }

  getLogs(): readonly string[] {
    return Object.freeze([...this.logs]);
  }

  // For testing: allow reset
  static resetInstance(): void {
    Logger.instance = null;
  }
}

// Usage
const logger = Logger.getInstance();
logger.log("Application started");
```

### Go

```go
package config

import (
    "os"
    "strconv"
    "sync"
)

type Config struct {
    DatabaseURL    string
    APIKey         string
    Debug          bool
    MaxConnections int
}

var (
    instance *Config
    once     sync.Once
)

// GetConfig returns singleton config instance
func GetConfig() *Config {
    once.Do(func() {
        maxConn, _ := strconv.Atoi(getEnv("MAX_CONNECTIONS", "10"))
        instance = &Config{
            DatabaseURL:    getEnv("DATABASE_URL", "sqlite:///db.sqlite3"),
            APIKey:         getEnv("API_KEY", ""),
            Debug:          getEnv("DEBUG", "false") == "true",
            MaxConnections: maxConn,
        }
    })
    return instance
}

func getEnv(key, defaultValue string) string {
    if value := os.Getenv(key); value != "" {
        return value
    }
    return defaultValue
}

// Usage
// config := GetConfig()
// fmt.Println(config.DatabaseURL)
```

---

## Prototype

### Use Case: Document Template System

Clone document templates with variations.

### Python

```python
from __future__ import annotations
import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

class Cloneable(Protocol):
    def clone(self) -> "Cloneable": ...

@dataclass
class Style:
    font_family: str = "Arial"
    font_size: int = 12
    color: str = "#000000"
    bold: bool = False
    italic: bool = False

@dataclass
class Paragraph:
    text: str
    style: Style = field(default_factory=Style)

@dataclass
class Document:
    title: str
    author: str
    created_at: datetime = field(default_factory=datetime.now)
    paragraphs: list[Paragraph] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)

    def clone(self) -> Document:
        """Create a deep copy of the document."""
        return copy.deepcopy(self)

    def shallow_clone(self) -> Document:
        """Create a shallow copy (paragraphs are shared)."""
        return Document(
            title=self.title,
            author=self.author,
            created_at=datetime.now(),  # New timestamp
            paragraphs=self.paragraphs,  # Shared reference
            metadata=self.metadata.copy(),  # Shallow copy of dict
        )

# Prototype registry
class DocumentRegistry:
    _templates: dict[str, Document] = {}

    @classmethod
    def register(cls, name: str, template: Document) -> None:
        cls._templates[name] = template

    @classmethod
    def create(cls, template_name: str) -> Document:
        if template_name not in cls._templates:
            raise ValueError(f"Unknown template: {template_name}")
        return cls._templates[template_name].clone()

# Setup templates
invoice_template = Document(
    title="Invoice",
    author="System",
    paragraphs=[
        Paragraph("Invoice Number: [NUMBER]", Style(font_size=16, bold=True)),
        Paragraph("Date: [DATE]"),
        Paragraph("Bill To: [CUSTOMER]"),
    ],
    metadata={"type": "invoice", "version": "1.0"},
)

report_template = Document(
    title="Report",
    author="System",
    paragraphs=[
        Paragraph("Executive Summary", Style(font_size=18, bold=True)),
        Paragraph("[SUMMARY]"),
        Paragraph("Details", Style(font_size=16, bold=True)),
        Paragraph("[DETAILS]"),
    ],
    metadata={"type": "report", "version": "1.0"},
)

DocumentRegistry.register("invoice", invoice_template)
DocumentRegistry.register("report", report_template)

# Usage
new_invoice = DocumentRegistry.create("invoice")
new_invoice.title = "Invoice #12345"
new_invoice.author = "John Doe"
new_invoice.paragraphs[0].text = "Invoice Number: 12345"

print(new_invoice.title)  # Invoice #12345
print(invoice_template.title)  # Invoice (unchanged)
```

### TypeScript

```typescript
// Modern approach using structuredClone (Node 17+, modern browsers)
interface Style {
  fontFamily: string;
  fontSize: number;
  color: string;
  bold: boolean;
  italic: boolean;
}

interface Paragraph {
  text: string;
  style: Style;
}

interface Document {
  title: string;
  author: string;
  createdAt: Date;
  paragraphs: Paragraph[];
  metadata: Record<string, string>;
}

// Clone function using structuredClone
function cloneDocument(doc: Document): Document {
  const cloned = structuredClone(doc);
  cloned.createdAt = new Date(); // Reset timestamp
  return cloned;
}

// Prototype registry
class DocumentRegistry {
  private static templates = new Map<string, Document>();

  static register(name: string, template: Document): void {
    this.templates.set(name, template);
  }

  static create(templateName: string): Document {
    const template = this.templates.get(templateName);
    if (!template) {
      throw new Error(`Unknown template: ${templateName}`);
    }
    return cloneDocument(template);
  }
}

// Default style factory
const createDefaultStyle = (): Style => ({
  fontFamily: "Arial",
  fontSize: 12,
  color: "#000000",
  bold: false,
  italic: false,
});

// Setup templates
const invoiceTemplate: Document = {
  title: "Invoice",
  author: "System",
  createdAt: new Date(),
  paragraphs: [
    { text: "Invoice Number: [NUMBER]", style: { ...createDefaultStyle(), fontSize: 16, bold: true } },
    { text: "Date: [DATE]", style: createDefaultStyle() },
    { text: "Bill To: [CUSTOMER]", style: createDefaultStyle() },
  ],
  metadata: { type: "invoice", version: "1.0" },
};

DocumentRegistry.register("invoice", invoiceTemplate);

// Usage
const newInvoice = DocumentRegistry.create("invoice");
newInvoice.title = "Invoice #12345";
newInvoice.author = "John Doe";
console.log(newInvoice.title); // Invoice #12345
console.log(invoiceTemplate.title); // Invoice (unchanged)
```

---

## Dependency Injection

### Use Case: User Service with Repository

### Python (with dependency-injector)

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol
from dependency_injector import containers, providers

# Domain models
@dataclass
class User:
    id: int
    email: str
    name: str

# Repository interface
class UserRepository(Protocol):
    def get_by_id(self, user_id: int) -> User | None: ...
    def save(self, user: User) -> User: ...
    def delete(self, user_id: int) -> bool: ...

# Concrete implementations
class PostgresUserRepository:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def get_by_id(self, user_id: int) -> User | None:
        # Actual DB query would go here
        print(f"PostgreSQL: Getting user {user_id}")
        return User(id=user_id, email="user@example.com", name="John")

    def save(self, user: User) -> User:
        print(f"PostgreSQL: Saving user {user.id}")
        return user

    def delete(self, user_id: int) -> bool:
        print(f"PostgreSQL: Deleting user {user_id}")
        return True

class InMemoryUserRepository:
    """For testing."""
    def __init__(self):
        self._users: dict[int, User] = {}

    def get_by_id(self, user_id: int) -> User | None:
        return self._users.get(user_id)

    def save(self, user: User) -> User:
        self._users[user.id] = user
        return user

    def delete(self, user_id: int) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

# Service
class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def get_user(self, user_id: int) -> User | None:
        return self._repository.get_by_id(user_id)

    def create_user(self, email: str, name: str) -> User:
        user = User(id=0, email=email, name=name)
        return self._repository.save(user)

# DI Container
class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    user_repository = providers.Singleton(
        PostgresUserRepository,
        connection_string=config.database_url,
    )

    user_service = providers.Factory(
        UserService,
        repository=user_repository,
    )

# Production setup
container = Container()
container.config.database_url.from_env("DATABASE_URL", "postgresql://localhost/db")

user_service = container.user_service()
user = user_service.get_user(1)

# Testing setup
def test_get_user():
    # Override with mock
    test_container = Container()
    test_container.user_repository.override(
        providers.Singleton(InMemoryUserRepository)
    )

    service = test_container.user_service()

    # Setup test data
    repo = test_container.user_repository()
    repo.save(User(id=1, email="test@example.com", name="Test"))

    # Test
    user = service.get_user(1)
    assert user is not None
    assert user.email == "test@example.com"
```

### TypeScript (with TSyringe)

```typescript
import "reflect-metadata";
import { container, injectable, inject, singleton } from "tsyringe";

// Domain models
interface User {
  id: number;
  email: string;
  name: string;
}

// Repository interface (as abstract class for DI)
abstract class UserRepository {
  abstract getById(userId: number): Promise<User | null>;
  abstract save(user: User): Promise<User>;
  abstract delete(userId: number): Promise<boolean>;
}

// Concrete implementation
@injectable()
class PostgresUserRepository extends UserRepository {
  constructor(@inject("DATABASE_URL") private connectionString: string) {
    super();
  }

  async getById(userId: number): Promise<User | null> {
    console.log(`PostgreSQL: Getting user ${userId}`);
    return { id: userId, email: "user@example.com", name: "John" };
  }

  async save(user: User): Promise<User> {
    console.log(`PostgreSQL: Saving user ${user.id}`);
    return user;
  }

  async delete(userId: number): Promise<boolean> {
    console.log(`PostgreSQL: Deleting user ${userId}`);
    return true;
  }
}

// In-memory for testing
@injectable()
class InMemoryUserRepository extends UserRepository {
  private users = new Map<number, User>();

  async getById(userId: number): Promise<User | null> {
    return this.users.get(userId) || null;
  }

  async save(user: User): Promise<User> {
    this.users.set(user.id, user);
    return user;
  }

  async delete(userId: number): Promise<boolean> {
    return this.users.delete(userId);
  }
}

// Service
@injectable()
class UserService {
  constructor(private repository: UserRepository) {}

  async getUser(userId: number): Promise<User | null> {
    return this.repository.getById(userId);
  }

  async createUser(email: string, name: string): Promise<User> {
    const user: User = { id: Date.now(), email, name };
    return this.repository.save(user);
  }
}

// Production setup
container.register("DATABASE_URL", { useValue: process.env.DATABASE_URL || "postgresql://localhost/db" });
container.register(UserRepository, { useClass: PostgresUserRepository });

const userService = container.resolve(UserService);
const user = await userService.getUser(1);

// Testing setup
function createTestContainer() {
  const testContainer = container.createChildContainer();
  testContainer.register(UserRepository, { useClass: InMemoryUserRepository });
  return testContainer;
}

// In test
const testContainer = createTestContainer();
const testService = testContainer.resolve(UserService);
```

### Go (with Wire)

```go
// user.go
package user

import "context"

type User struct {
    ID    int
    Email string
    Name  string
}

// Repository interface
type Repository interface {
    GetByID(ctx context.Context, id int) (*User, error)
    Save(ctx context.Context, user *User) (*User, error)
    Delete(ctx context.Context, id int) error
}

// Service
type Service struct {
    repo Repository
}

func NewService(repo Repository) *Service {
    return &Service{repo: repo}
}

func (s *Service) GetUser(ctx context.Context, id int) (*User, error) {
    return s.repo.GetByID(ctx, id)
}

func (s *Service) CreateUser(ctx context.Context, email, name string) (*User, error) {
    user := &User{Email: email, Name: name}
    return s.repo.Save(ctx, user)
}

// postgres.go
package postgres

import (
    "context"
    "database/sql"
    "user"
)

type UserRepository struct {
    db *sql.DB
}

func NewUserRepository(db *sql.DB) user.Repository {
    return &UserRepository{db: db}
}

func (r *UserRepository) GetByID(ctx context.Context, id int) (*user.User, error) {
    // Actual implementation
    return &user.User{ID: id, Email: "user@example.com", Name: "John"}, nil
}

func (r *UserRepository) Save(ctx context.Context, u *user.User) (*user.User, error) {
    // Actual implementation
    return u, nil
}

func (r *UserRepository) Delete(ctx context.Context, id int) error {
    return nil
}

// wire.go - Wire configuration
//go:build wireinject

package main

import (
    "database/sql"
    "user"
    "postgres"
    "github.com/google/wire"
)

func InitializeUserService(db *sql.DB) *user.Service {
    wire.Build(
        postgres.NewUserRepository,
        user.NewService,
    )
    return nil
}

// main.go
package main

import (
    "context"
    "database/sql"
    "fmt"
    _ "github.com/lib/pq"
)

func main() {
    db, _ := sql.Open("postgres", "postgresql://localhost/db")

    // Wire generates this function
    service := InitializeUserService(db)

    user, _ := service.GetUser(context.Background(), 1)
    fmt.Printf("User: %v\n", user)
}
```

---

## Object Pool

### Use Case: Database Connection Pool

### Python

```python
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from queue import Queue, Empty
from typing import Generator
import uuid

@dataclass
class Connection:
    """Simulated database connection."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: float = field(default_factory=time.time)
    _in_use: bool = False

    def query(self, sql: str) -> list:
        print(f"Connection {self.id}: Executing {sql}")
        return []

    def reset(self) -> None:
        """Reset connection state for reuse."""
        print(f"Connection {self.id}: Reset")

    def is_valid(self) -> bool:
        """Check if connection is still valid."""
        return time.time() - self.created_at < 3600  # 1 hour max age

class ConnectionPool:
    def __init__(
        self,
        min_size: int = 5,
        max_size: int = 20,
        timeout: float = 30.0,
    ):
        self._min_size = min_size
        self._max_size = max_size
        self._timeout = timeout
        self._pool: Queue[Connection] = Queue()
        self._size = 0
        self._lock = threading.Lock()

        # Pre-create minimum connections
        for _ in range(min_size):
            self._create_connection()

    def _create_connection(self) -> Connection:
        """Create new connection and add to pool."""
        conn = Connection()
        self._pool.put(conn)
        self._size += 1
        print(f"Pool: Created connection {conn.id} (total: {self._size})")
        return conn

    def acquire(self) -> Connection:
        """Get a connection from the pool."""
        try:
            conn = self._pool.get(timeout=self._timeout)

            # Validate connection
            if not conn.is_valid():
                print(f"Pool: Connection {conn.id} expired, creating new")
                with self._lock:
                    self._size -= 1
                return self.acquire()

            conn._in_use = True
            return conn

        except Empty:
            # Pool exhausted, try to create new connection
            with self._lock:
                if self._size < self._max_size:
                    conn = Connection()
                    conn._in_use = True
                    self._size += 1
                    print(f"Pool: Created connection {conn.id} on demand (total: {self._size})")
                    return conn
            raise TimeoutError("Connection pool exhausted")

    def release(self, conn: Connection) -> None:
        """Return connection to the pool."""
        conn.reset()
        conn._in_use = False
        self._pool.put(conn)
        print(f"Pool: Released connection {conn.id}")

    @contextmanager
    def connection(self) -> Generator[Connection, None, None]:
        """Context manager for automatic release."""
        conn = self.acquire()
        try:
            yield conn
        finally:
            self.release(conn)

    @property
    def stats(self) -> dict:
        """Get pool statistics."""
        return {
            "total": self._size,
            "available": self._pool.qsize(),
            "in_use": self._size - self._pool.qsize(),
        }

# Usage
pool = ConnectionPool(min_size=3, max_size=10)

# Manual acquire/release
conn = pool.acquire()
conn.query("SELECT * FROM users")
pool.release(conn)

# Context manager (recommended)
with pool.connection() as conn:
    conn.query("SELECT * FROM products")

print(pool.stats)  # {'total': 3, 'available': 3, 'in_use': 0}
```

### Go

```go
package pool

import (
    "context"
    "errors"
    "sync"
    "time"
)

var (
    ErrPoolExhausted = errors.New("connection pool exhausted")
    ErrPoolClosed    = errors.New("connection pool is closed")
)

type Connection struct {
    ID        string
    CreatedAt time.Time
    inUse     bool
}

func (c *Connection) Query(sql string) ([]map[string]interface{}, error) {
    // Simulated query
    return nil, nil
}

func (c *Connection) Reset() {
    // Reset connection state
}

func (c *Connection) IsValid() bool {
    return time.Since(c.CreatedAt) < time.Hour
}

type Pool struct {
    minSize     int
    maxSize     int
    timeout     time.Duration
    connections chan *Connection
    size        int
    mu          sync.Mutex
    closed      bool
    factory     func() (*Connection, error)
}

type PoolConfig struct {
    MinSize int
    MaxSize int
    Timeout time.Duration
    Factory func() (*Connection, error)
}

func NewPool(cfg PoolConfig) (*Pool, error) {
    if cfg.MinSize > cfg.MaxSize {
        return nil, errors.New("minSize cannot exceed maxSize")
    }

    p := &Pool{
        minSize:     cfg.MinSize,
        maxSize:     cfg.MaxSize,
        timeout:     cfg.Timeout,
        connections: make(chan *Connection, cfg.MaxSize),
        factory:     cfg.Factory,
    }

    // Pre-create minimum connections
    for i := 0; i < cfg.MinSize; i++ {
        conn, err := p.factory()
        if err != nil {
            return nil, err
        }
        p.connections <- conn
        p.size++
    }

    return p, nil
}

func (p *Pool) Acquire(ctx context.Context) (*Connection, error) {
    if p.closed {
        return nil, ErrPoolClosed
    }

    select {
    case conn := <-p.connections:
        if !conn.IsValid() {
            p.mu.Lock()
            p.size--
            p.mu.Unlock()
            return p.Acquire(ctx)
        }
        conn.inUse = true
        return conn, nil

    case <-time.After(p.timeout):
        // Try to create new connection
        p.mu.Lock()
        defer p.mu.Unlock()

        if p.size < p.maxSize {
            conn, err := p.factory()
            if err != nil {
                return nil, err
            }
            conn.inUse = true
            p.size++
            return conn, nil
        }
        return nil, ErrPoolExhausted

    case <-ctx.Done():
        return nil, ctx.Err()
    }
}

func (p *Pool) Release(conn *Connection) {
    if p.closed {
        return
    }
    conn.Reset()
    conn.inUse = false
    p.connections <- conn
}

// WithConnection provides a connection for the duration of the function
func (p *Pool) WithConnection(ctx context.Context, fn func(*Connection) error) error {
    conn, err := p.Acquire(ctx)
    if err != nil {
        return err
    }
    defer p.Release(conn)
    return fn(conn)
}

func (p *Pool) Stats() map[string]int {
    return map[string]int{
        "total":     p.size,
        "available": len(p.connections),
        "in_use":    p.size - len(p.connections),
    }
}

func (p *Pool) Close() {
    p.mu.Lock()
    defer p.mu.Unlock()

    p.closed = true
    close(p.connections)

    for conn := range p.connections {
        // Cleanup connection
        _ = conn
    }
}

// Usage example in main.go:
//
// pool, _ := NewPool(PoolConfig{
//     MinSize: 5,
//     MaxSize: 20,
//     Timeout: 30 * time.Second,
//     Factory: func() (*Connection, error) {
//         return &Connection{
//             ID:        uuid.New().String()[:8],
//             CreatedAt: time.Now(),
//         }, nil
//     },
// })
// defer pool.Close()
//
// err := pool.WithConnection(ctx, func(conn *Connection) error {
//     return conn.Query("SELECT * FROM users")
// })
```

---

## Related Files

| File | Description |
|------|-------------|
| [README.md](README.md) | Pattern overview and selection guide |
| [checklist.md](checklist.md) | Step-by-step implementation checklist |
| [templates.md](templates.md) | Copy-paste pattern templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM-assisted design |
