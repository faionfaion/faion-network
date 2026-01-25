# Creational Design Patterns

Patterns for object creation mechanisms.

## Overview

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| Factory Method | Create objects without specifying class | Multiple related classes |
| Abstract Factory | Create families of objects | Platform-specific UIs |
| Builder | Construct complex objects step by step | Many optional parameters |
| Singleton | Single instance globally | Logging, config, connections |
| Prototype | Clone existing objects | Expensive to create |

## Factory Method

Delegate object creation to subclasses.

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str): pass

class EmailNotification(Notification):
    def send(self, message: str):
        print(f"Email: {message}")

class SMSNotification(Notification):
    def send(self, message: str):
        print(f"SMS: {message}")

class NotificationFactory:
    @staticmethod
    def create(type: str) -> Notification:
        if type == "email":
            return EmailNotification()
        elif type == "sms":
            return SMSNotification()
        raise ValueError(f"Unknown type: {type}")

# Usage
notification = NotificationFactory.create("email")
notification.send("Hello!")
```

## Abstract Factory

Create families of related objects.

```python
from abc import ABC, abstractmethod

# Abstract products
class Button(ABC):
    @abstractmethod
    def render(self): pass

class Checkbox(ABC):
    @abstractmethod
    def render(self): pass

# Concrete products
class WindowsButton(Button):
    def render(self): return "Windows Button"

class MacButton(Button):
    def render(self): return "Mac Button"

# Abstract factory
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: pass
    @abstractmethod
    def create_checkbox(self) -> Checkbox: pass

# Concrete factories
class WindowsFactory(UIFactory):
    def create_button(self): return WindowsButton()
    def create_checkbox(self): return WindowsCheckbox()

class MacFactory(UIFactory):
    def create_button(self): return MacButton()
    def create_checkbox(self): return MacCheckbox()
```

## Builder

Construct complex objects step by step.

```python
class User:
    def __init__(self):
        self.name = None
        self.email = None
        self.age = None
        self.address = None

class UserBuilder:
    def __init__(self):
        self.user = User()

    def with_name(self, name: str) -> 'UserBuilder':
        self.user.name = name
        return self

    def with_email(self, email: str) -> 'UserBuilder':
        self.user.email = email
        return self

    def with_age(self, age: int) -> 'UserBuilder':
        self.user.age = age
        return self

    def build(self) -> User:
        return self.user

# Usage
user = (UserBuilder()
    .with_name("John")
    .with_email("john@example.com")
    .with_age(30)
    .build())
```

## Singleton

Single instance globally accessible.

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Modern Python approach
class Config:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
```

**Warning:** Singletons can make testing difficult. Consider dependency injection instead.

## Prototype

Clone existing objects.

```python
import copy

class Prototype:
    def clone(self):
        return copy.deepcopy(self)

class Document(Prototype):
    def __init__(self, title, content):
        self.title = title
        self.content = content

# Usage
original = Document("Report", "Content...")
clone = original.clone()
clone.title = "Report Copy"
```

## When to Use

| Situation | Pattern |
|-----------|---------|
| "Create X based on type Y" | Factory Method |
| "Create themed/platform UI" | Abstract Factory |
| "Object has 10+ optional params" | Builder |
| "Need exactly one instance" | Singleton (carefully) |
| "Copy is cheaper than create" | Prototype |

## Related

- [structural-patterns.md](structural-patterns.md) - Object composition
- [behavioral-patterns.md](behavioral-patterns.md) - Object interaction
