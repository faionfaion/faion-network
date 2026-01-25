# Structural Design Patterns

Patterns for composing objects and classes.

## Overview

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| Adapter | Convert interface to another | Legacy integration |
| Bridge | Separate abstraction from implementation | Cross-platform |
| Composite | Tree structures | File systems, UI |
| Decorator | Add behavior dynamically | Middleware, streams |
| Facade | Simplified interface to subsystem | Complex libraries |
| Proxy | Placeholder for another object | Lazy loading, access control |

## Adapter

Convert one interface to another.

```python
# Old system
class OldPaymentGateway:
    def make_payment(self, amount):
        return f"Old: paid {amount}"

# New interface we need
class PaymentProcessor:
    def process(self, amount: float) -> str:
        raise NotImplementedError

# Adapter
class PaymentAdapter(PaymentProcessor):
    def __init__(self, old_gateway: OldPaymentGateway):
        self.old_gateway = old_gateway

    def process(self, amount: float) -> str:
        return self.old_gateway.make_payment(amount)

# Usage
old = OldPaymentGateway()
processor = PaymentAdapter(old)
processor.process(100.0)  # Works with new interface
```

## Decorator

Add behavior without modifying class.

```python
from functools import wraps

# Function decorator
def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_calls
def process_order(order_id):
    return f"Processed {order_id}"

# Class decorator pattern
class Component:
    def operation(self) -> str:
        return "Component"

class Decorator(Component):
    def __init__(self, component: Component):
        self._component = component

    def operation(self) -> str:
        return self._component.operation()

class LoggingDecorator(Decorator):
    def operation(self) -> str:
        print("Before operation")
        result = super().operation()
        print("After operation")
        return result
```

## Facade

Simplified interface to complex subsystem.

```python
# Complex subsystems
class VideoDecoder:
    def decode(self, file): pass

class AudioDecoder:
    def decode(self, file): pass

class VideoPlayer:
    def play(self, video, audio): pass

# Facade
class MediaFacade:
    def __init__(self):
        self.video_decoder = VideoDecoder()
        self.audio_decoder = AudioDecoder()
        self.player = VideoPlayer()

    def play_video(self, filename: str):
        """Simple interface hiding complexity"""
        video = self.video_decoder.decode(filename)
        audio = self.audio_decoder.decode(filename)
        self.player.play(video, audio)

# Usage
media = MediaFacade()
media.play_video("movie.mp4")  # Simple!
```

## Composite

Tree structures with uniform interface.

```python
from abc import ABC, abstractmethod

class FileSystemItem(ABC):
    @abstractmethod
    def get_size(self) -> int: pass

class File(FileSystemItem):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def get_size(self) -> int:
        return self.size

class Directory(FileSystemItem):
    def __init__(self, name: str):
        self.name = name
        self.children: list[FileSystemItem] = []

    def add(self, item: FileSystemItem):
        self.children.append(item)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)

# Usage
root = Directory("root")
root.add(File("a.txt", 100))
docs = Directory("docs")
docs.add(File("b.txt", 200))
root.add(docs)
root.get_size()  # 300
```

## Proxy

Control access to another object.

```python
class Image:
    def display(self): pass

class RealImage(Image):
    def __init__(self, filename: str):
        self.filename = filename
        self._load()  # Expensive operation

    def _load(self):
        print(f"Loading {self.filename}")

    def display(self):
        print(f"Displaying {self.filename}")

# Lazy loading proxy
class ImageProxy(Image):
    def __init__(self, filename: str):
        self.filename = filename
        self._real_image = None

    def display(self):
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()

# Usage
image = ImageProxy("large.jpg")  # No loading yet
# ... later ...
image.display()  # Now it loads
```

## Bridge

Separate abstraction from implementation.

```python
# Implementation hierarchy
class Renderer:
    def render_circle(self, x, y, radius): pass

class VectorRenderer(Renderer):
    def render_circle(self, x, y, radius):
        print(f"Vector circle at ({x},{y}) r={radius}")

class RasterRenderer(Renderer):
    def render_circle(self, x, y, radius):
        print(f"Raster circle at ({x},{y}) r={radius}")

# Abstraction
class Shape:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer

class Circle(Shape):
    def __init__(self, renderer: Renderer, x, y, radius):
        super().__init__(renderer)
        self.x, self.y, self.radius = x, y, radius

    def draw(self):
        self.renderer.render_circle(self.x, self.y, self.radius)

# Can combine any shape with any renderer
circle = Circle(VectorRenderer(), 5, 10, 3)
circle.draw()
```

## When to Use

| Situation | Pattern |
|-----------|---------|
| "Integrate legacy/3rd party" | Adapter |
| "Add features without subclassing" | Decorator |
| "Hide complex subsystem" | Facade |
| "Tree structures" | Composite |
| "Lazy loading, access control" | Proxy |
| "Multiple dimensions of variation" | Bridge |

## Related

- [creational-patterns.md](creational-patterns.md) - Object creation
- [behavioral-patterns.md](behavioral-patterns.md) - Object interaction
