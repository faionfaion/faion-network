# Structural Patterns Examples

Real-world implementations in Python, TypeScript, and Go.

---

## 1. Adapter Pattern

### Use Case: Payment Gateway Integration

Integrating a legacy payment system with a new unified payment interface.

#### Python

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


@dataclass
class PaymentResult:
    success: bool
    transaction_id: str
    message: str


# Target Interface (what we want)
class PaymentProcessor(Protocol):
    def process_payment(self, amount: float, currency: str) -> PaymentResult:
        ...


# Adaptee 1: Legacy Stripe-like Gateway
class LegacyStripeGateway:
    def charge(self, cents: int, currency_code: str) -> dict:
        # Simulates legacy API
        return {
            "status": "succeeded",
            "id": f"ch_{cents}_{currency_code}",
            "error": None
        }


# Adaptee 2: PayPal-like Gateway
class PayPalAPI:
    def create_payment(self, value: str, currency: str) -> dict:
        return {
            "state": "approved",
            "id": f"PAY-{value}",
            "message": "Payment approved"
        }


# Adapter for Legacy Stripe
class StripeAdapter:
    def __init__(self, gateway: LegacyStripeGateway):
        self._gateway = gateway

    def process_payment(self, amount: float, currency: str) -> PaymentResult:
        # Convert dollars to cents, map response
        cents = int(amount * 100)
        result = self._gateway.charge(cents, currency.upper())

        return PaymentResult(
            success=result["status"] == "succeeded",
            transaction_id=result["id"],
            message=result.get("error") or "Payment processed"
        )


# Adapter for PayPal
class PayPalAdapter:
    def __init__(self, api: PayPalAPI):
        self._api = api

    def process_payment(self, amount: float, currency: str) -> PaymentResult:
        result = self._api.create_payment(f"{amount:.2f}", currency)

        return PaymentResult(
            success=result["state"] == "approved",
            transaction_id=result["id"],
            message=result["message"]
        )


# Usage: Client code works with any adapter
def checkout(processor: PaymentProcessor, amount: float) -> None:
    result = processor.process_payment(amount, "USD")
    if result.success:
        print(f"Payment successful: {result.transaction_id}")
    else:
        print(f"Payment failed: {result.message}")


# Test both adapters
stripe_adapter = StripeAdapter(LegacyStripeGateway())
paypal_adapter = PayPalAdapter(PayPalAPI())

checkout(stripe_adapter, 99.99)  # Payment successful: ch_9999_USD
checkout(paypal_adapter, 49.99)  # Payment successful: PAY-49.99
```

#### TypeScript

```typescript
interface PaymentResult {
  success: boolean;
  transactionId: string;
  message: string;
}

// Target Interface
interface PaymentProcessor {
  processPayment(amount: number, currency: string): PaymentResult;
}

// Adaptee: Legacy Gateway
class LegacyStripeGateway {
  charge(cents: number, currencyCode: string): Record<string, unknown> {
    return {
      status: "succeeded",
      id: `ch_${cents}_${currencyCode}`,
      error: null,
    };
  }
}

// Adapter
class StripeAdapter implements PaymentProcessor {
  constructor(private gateway: LegacyStripeGateway) {}

  processPayment(amount: number, currency: string): PaymentResult {
    const cents = Math.round(amount * 100);
    const result = this.gateway.charge(cents, currency.toUpperCase());

    return {
      success: result.status === "succeeded",
      transactionId: result.id as string,
      message: (result.error as string) || "Payment processed",
    };
  }
}

// Usage
const adapter = new StripeAdapter(new LegacyStripeGateway());
const result = adapter.processPayment(99.99, "USD");
console.log(result); // { success: true, transactionId: 'ch_9999_USD', ... }
```

#### Go

```go
package main

import "fmt"

// Target Interface
type PaymentProcessor interface {
    ProcessPayment(amount float64, currency string) PaymentResult
}

type PaymentResult struct {
    Success       bool
    TransactionID string
    Message       string
}

// Adaptee: Legacy Gateway
type LegacyStripeGateway struct{}

func (g *LegacyStripeGateway) Charge(cents int, currencyCode string) map[string]interface{} {
    return map[string]interface{}{
        "status": "succeeded",
        "id":     fmt.Sprintf("ch_%d_%s", cents, currencyCode),
        "error":  nil,
    }
}

// Adapter
type StripeAdapter struct {
    gateway *LegacyStripeGateway
}

func NewStripeAdapter(gateway *LegacyStripeGateway) *StripeAdapter {
    return &StripeAdapter{gateway: gateway}
}

func (a *StripeAdapter) ProcessPayment(amount float64, currency string) PaymentResult {
    cents := int(amount * 100)
    result := a.gateway.Charge(cents, currency)

    return PaymentResult{
        Success:       result["status"] == "succeeded",
        TransactionID: result["id"].(string),
        Message:       "Payment processed",
    }
}

func main() {
    adapter := NewStripeAdapter(&LegacyStripeGateway{})
    result := adapter.ProcessPayment(99.99, "USD")
    fmt.Printf("%+v\n", result)
}
```

---

## 2. Bridge Pattern

### Use Case: Cross-Platform Notification System

Sending notifications across different platforms (email, SMS, push) with different urgency levels.

#### Python

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


# Implementor Interface
class NotificationSender(ABC):
    @abstractmethod
    def send(self, recipient: str, title: str, body: str) -> bool:
        pass


# Concrete Implementors
class EmailSender(NotificationSender):
    def send(self, recipient: str, title: str, body: str) -> bool:
        print(f"EMAIL to {recipient}: [{title}] {body}")
        return True


class SMSSender(NotificationSender):
    def send(self, recipient: str, title: str, body: str) -> bool:
        # SMS has length limits
        message = f"{title}: {body}"[:160]
        print(f"SMS to {recipient}: {message}")
        return True


class PushNotificationSender(NotificationSender):
    def send(self, recipient: str, title: str, body: str) -> bool:
        print(f"PUSH to {recipient}: {title} - {body[:100]}...")
        return True


# Abstraction
class Notification(ABC):
    def __init__(self, sender: NotificationSender):
        self._sender = sender

    @abstractmethod
    def notify(self, recipient: str, message: str) -> bool:
        pass


# Refined Abstractions
class UrgentNotification(Notification):
    def notify(self, recipient: str, message: str) -> bool:
        title = "[URGENT]"
        body = message.upper()
        return self._sender.send(recipient, title, body)


class RegularNotification(Notification):
    def notify(self, recipient: str, message: str) -> bool:
        return self._sender.send(recipient, "Notification", message)


class ScheduledNotification(Notification):
    def __init__(self, sender: NotificationSender, schedule_time: str):
        super().__init__(sender)
        self.schedule_time = schedule_time

    def notify(self, recipient: str, message: str) -> bool:
        title = f"[Scheduled for {self.schedule_time}]"
        return self._sender.send(recipient, title, message)


# Usage: Any notification type with any sender
email = EmailSender()
sms = SMSSender()
push = PushNotificationSender()

# Combine any abstraction with any implementor
urgent_email = UrgentNotification(email)
urgent_sms = UrgentNotification(sms)
regular_push = RegularNotification(push)

urgent_email.notify("user@example.com", "Server is down!")
urgent_sms.notify("+1234567890", "Server is down!")
regular_push.notify("user_123", "Your order has shipped")
```

#### TypeScript

```typescript
// Implementor Interface
interface NotificationSender {
  send(recipient: string, title: string, body: string): boolean;
}

// Concrete Implementors
class EmailSender implements NotificationSender {
  send(recipient: string, title: string, body: string): boolean {
    console.log(`EMAIL to ${recipient}: [${title}] ${body}`);
    return true;
  }
}

class SMSSender implements NotificationSender {
  send(recipient: string, title: string, body: string): boolean {
    const message = `${title}: ${body}`.slice(0, 160);
    console.log(`SMS to ${recipient}: ${message}`);
    return true;
  }
}

// Abstraction
abstract class Notification {
  constructor(protected sender: NotificationSender) {}
  abstract notify(recipient: string, message: string): boolean;
}

// Refined Abstractions
class UrgentNotification extends Notification {
  notify(recipient: string, message: string): boolean {
    return this.sender.send(recipient, "[URGENT]", message.toUpperCase());
  }
}

class RegularNotification extends Notification {
  notify(recipient: string, message: string): boolean {
    return this.sender.send(recipient, "Notification", message);
  }
}

// Usage
const urgentEmail = new UrgentNotification(new EmailSender());
const regularSms = new RegularNotification(new SMSSender());

urgentEmail.notify("user@example.com", "Server is down!");
regularSms.notify("+1234567890", "Your order shipped");
```

#### Go

```go
package main

import "fmt"

// Implementor Interface
type NotificationSender interface {
    Send(recipient, title, body string) bool
}

// Concrete Implementors
type EmailSender struct{}

func (e *EmailSender) Send(recipient, title, body string) bool {
    fmt.Printf("EMAIL to %s: [%s] %s\n", recipient, title, body)
    return true
}

type SMSSender struct{}

func (s *SMSSender) Send(recipient, title, body string) bool {
    message := fmt.Sprintf("%s: %s", title, body)
    if len(message) > 160 {
        message = message[:160]
    }
    fmt.Printf("SMS to %s: %s\n", recipient, message)
    return true
}

// Abstraction
type Notification interface {
    Notify(recipient, message string) bool
}

// Refined Abstraction
type UrgentNotification struct {
    sender NotificationSender
}

func (u *UrgentNotification) Notify(recipient, message string) bool {
    return u.sender.Send(recipient, "[URGENT]", message)
}

type RegularNotification struct {
    sender NotificationSender
}

func (r *RegularNotification) Notify(recipient, message string) bool {
    return r.sender.Send(recipient, "Notification", message)
}

func main() {
    urgentEmail := &UrgentNotification{sender: &EmailSender{}}
    regularSms := &RegularNotification{sender: &SMSSender{}}

    urgentEmail.Notify("user@example.com", "Server is down!")
    regularSms.Notify("+1234567890", "Your order shipped")
}
```

---

## 3. Composite Pattern

### Use Case: File System with Size Calculation

Tree structure for files and directories with recursive size calculation.

#### Python

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterator


class FileSystemItem(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        pass


@dataclass
class File(FileSystemItem):
    _name: str
    size: int

    @property
    def name(self) -> str:
        return self._name

    def get_size(self) -> int:
        return self.size

    def display(self, indent: int = 0) -> str:
        return f"{'  ' * indent}{self._name} ({self.size} bytes)"


@dataclass
class Directory(FileSystemItem):
    _name: str
    children: list[FileSystemItem] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self._name

    def add(self, item: FileSystemItem) -> "Directory":
        self.children.append(item)
        return self

    def remove(self, item: FileSystemItem) -> "Directory":
        self.children.remove(item)
        return self

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)

    def display(self, indent: int = 0) -> str:
        lines = [f"{'  ' * indent}{self._name}/ ({self.get_size()} bytes)"]
        for child in self.children:
            lines.append(child.display(indent + 1))
        return "\n".join(lines)

    def __iter__(self) -> Iterator[FileSystemItem]:
        return iter(self.children)


# Usage: Build a file system tree
root = Directory("project")
root.add(File("README.md", 1024))
root.add(File(".gitignore", 256))

src = Directory("src")
src.add(File("main.py", 2048))
src.add(File("utils.py", 1536))

tests = Directory("tests")
tests.add(File("test_main.py", 1024))

src.add(tests)
root.add(src)

# Treat uniformly
print(root.display())
print(f"\nTotal size: {root.get_size()} bytes")

# Output:
# project/ (5888 bytes)
#   README.md (1024 bytes)
#   .gitignore (256 bytes)
#   src/ (4608 bytes)
#     main.py (2048 bytes)
#     utils.py (1536 bytes)
#     tests/ (1024 bytes)
#       test_main.py (1024 bytes)
#
# Total size: 5888 bytes
```

#### TypeScript

```typescript
interface FileSystemItem {
  name: string;
  getSize(): number;
  display(indent?: number): string;
}

class File implements FileSystemItem {
  constructor(public name: string, private size: number) {}

  getSize(): number {
    return this.size;
  }

  display(indent = 0): string {
    return `${"  ".repeat(indent)}${this.name} (${this.size} bytes)`;
  }
}

class Directory implements FileSystemItem {
  private children: FileSystemItem[] = [];

  constructor(public name: string) {}

  add(item: FileSystemItem): this {
    this.children.push(item);
    return this;
  }

  getSize(): number {
    return this.children.reduce((sum, child) => sum + child.getSize(), 0);
  }

  display(indent = 0): string {
    const lines = [`${"  ".repeat(indent)}${this.name}/ (${this.getSize()} bytes)`];
    for (const child of this.children) {
      lines.push(child.display(indent + 1));
    }
    return lines.join("\n");
  }
}

// Usage
const root = new Directory("project");
root.add(new File("README.md", 1024));

const src = new Directory("src");
src.add(new File("main.ts", 2048));
root.add(src);

console.log(root.display());
console.log(`\nTotal: ${root.getSize()} bytes`);
```

#### Go

```go
package main

import (
    "fmt"
    "strings"
)

type FileSystemItem interface {
    Name() string
    GetSize() int
    Display(indent int) string
}

// File (Leaf)
type File struct {
    name string
    size int
}

func NewFile(name string, size int) *File {
    return &File{name: name, size: size}
}

func (f *File) Name() string { return f.name }
func (f *File) GetSize() int { return f.size }
func (f *File) Display(indent int) string {
    return fmt.Sprintf("%s%s (%d bytes)", strings.Repeat("  ", indent), f.name, f.size)
}

// Directory (Composite)
type Directory struct {
    name     string
    children []FileSystemItem
}

func NewDirectory(name string) *Directory {
    return &Directory{name: name, children: []FileSystemItem{}}
}

func (d *Directory) Name() string { return d.name }

func (d *Directory) Add(item FileSystemItem) *Directory {
    d.children = append(d.children, item)
    return d
}

func (d *Directory) GetSize() int {
    total := 0
    for _, child := range d.children {
        total += child.GetSize()
    }
    return total
}

func (d *Directory) Display(indent int) string {
    var lines []string
    lines = append(lines, fmt.Sprintf("%s%s/ (%d bytes)",
        strings.Repeat("  ", indent), d.name, d.GetSize()))
    for _, child := range d.children {
        lines = append(lines, child.Display(indent+1))
    }
    return strings.Join(lines, "\n")
}

func main() {
    root := NewDirectory("project")
    root.Add(NewFile("README.md", 1024))

    src := NewDirectory("src")
    src.Add(NewFile("main.go", 2048))
    root.Add(src)

    fmt.Println(root.Display(0))
    fmt.Printf("\nTotal: %d bytes\n", root.GetSize())
}
```

---

## 4. Decorator Pattern

### Use Case: HTTP Middleware Chain

Adding logging, authentication, and rate limiting to HTTP handlers.

#### Python

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps
from typing import Callable, Any
import time


# Component Interface
@dataclass
class Request:
    path: str
    method: str
    headers: dict[str, str]
    body: str = ""


@dataclass
class Response:
    status: int
    body: str
    headers: dict[str, str] = None


class Handler(ABC):
    @abstractmethod
    def handle(self, request: Request) -> Response:
        pass


# Concrete Component
class ApiHandler(Handler):
    def handle(self, request: Request) -> Response:
        return Response(status=200, body='{"message": "success"}')


# Base Decorator
class HandlerDecorator(Handler):
    def __init__(self, handler: Handler):
        self._handler = handler

    def handle(self, request: Request) -> Response:
        return self._handler.handle(request)


# Concrete Decorators
class LoggingDecorator(HandlerDecorator):
    def handle(self, request: Request) -> Response:
        start = time.time()
        print(f"[LOG] {request.method} {request.path}")

        response = super().handle(request)

        duration = (time.time() - start) * 1000
        print(f"[LOG] Response: {response.status} ({duration:.2f}ms)")
        return response


class AuthDecorator(HandlerDecorator):
    def __init__(self, handler: Handler, api_key: str):
        super().__init__(handler)
        self._api_key = api_key

    def handle(self, request: Request) -> Response:
        auth = request.headers.get("Authorization", "")
        if auth != f"Bearer {self._api_key}":
            return Response(status=401, body='{"error": "Unauthorized"}')
        return super().handle(request)


class RateLimitDecorator(HandlerDecorator):
    def __init__(self, handler: Handler, max_requests: int = 100):
        super().__init__(handler)
        self._max_requests = max_requests
        self._request_count = 0

    def handle(self, request: Request) -> Response:
        self._request_count += 1
        if self._request_count > self._max_requests:
            return Response(status=429, body='{"error": "Rate limit exceeded"}')
        return super().handle(request)


class CacheDecorator(HandlerDecorator):
    def __init__(self, handler: Handler, ttl_seconds: int = 300):
        super().__init__(handler)
        self._cache: dict[str, tuple[Response, float]] = {}
        self._ttl = ttl_seconds

    def handle(self, request: Request) -> Response:
        if request.method != "GET":
            return super().handle(request)

        cache_key = f"{request.method}:{request.path}"
        cached = self._cache.get(cache_key)

        if cached:
            response, timestamp = cached
            if time.time() - timestamp < self._ttl:
                print(f"[CACHE] Hit for {cache_key}")
                return response

        response = super().handle(request)
        self._cache[cache_key] = (response, time.time())
        return response


# Usage: Stack decorators
handler = ApiHandler()
handler = CacheDecorator(handler, ttl_seconds=60)
handler = RateLimitDecorator(handler, max_requests=1000)
handler = AuthDecorator(handler, api_key="secret-key")
handler = LoggingDecorator(handler)

# Test request
request = Request(
    path="/api/users",
    method="GET",
    headers={"Authorization": "Bearer secret-key"}
)

response = handler.handle(request)
print(f"Response: {response.status} - {response.body}")
```

#### TypeScript

```typescript
interface Request {
  path: string;
  method: string;
  headers: Record<string, string>;
}

interface Response {
  status: number;
  body: string;
}

interface Handler {
  handle(request: Request): Response;
}

// Concrete Component
class ApiHandler implements Handler {
  handle(_request: Request): Response {
    return { status: 200, body: '{"message": "success"}' };
  }
}

// Base Decorator
abstract class HandlerDecorator implements Handler {
  constructor(protected handler: Handler) {}

  handle(request: Request): Response {
    return this.handler.handle(request);
  }
}

// Concrete Decorators
class LoggingDecorator extends HandlerDecorator {
  handle(request: Request): Response {
    console.log(`[LOG] ${request.method} ${request.path}`);
    const start = Date.now();

    const response = super.handle(request);

    console.log(`[LOG] Response: ${response.status} (${Date.now() - start}ms)`);
    return response;
  }
}

class AuthDecorator extends HandlerDecorator {
  constructor(handler: Handler, private apiKey: string) {
    super(handler);
  }

  handle(request: Request): Response {
    if (request.headers["Authorization"] !== `Bearer ${this.apiKey}`) {
      return { status: 401, body: '{"error": "Unauthorized"}' };
    }
    return super.handle(request);
  }
}

// Usage
let handler: Handler = new ApiHandler();
handler = new AuthDecorator(handler, "secret-key");
handler = new LoggingDecorator(handler);

const response = handler.handle({
  path: "/api/users",
  method: "GET",
  headers: { Authorization: "Bearer secret-key" },
});
console.log(response);
```

#### Python Function Decorators

```python
from functools import wraps
from typing import Callable, TypeVar, ParamSpec
import time

P = ParamSpec("P")
R = TypeVar("R")


def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    """Log function entry and exit with timing."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        print(f"Calling {func.__name__}")

        result = func(*args, **kwargs)

        duration = (time.perf_counter() - start) * 1000
        print(f"{func.__name__} completed in {duration:.2f}ms")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry function on failure."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator


def cache_result(ttl_seconds: int = 300):
    """Cache function results with TTL."""
    cache: dict[str, tuple[any, float]] = {}

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = str((args, tuple(sorted(kwargs.items()))))

            if key in cache:
                result, timestamp = cache[key]
                if time.time() - timestamp < ttl_seconds:
                    return result

            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator


# Usage: Stack decorators (bottom-up application)
@log_calls
@retry(max_attempts=3, delay=0.5)
@cache_result(ttl_seconds=60)
def fetch_user(user_id: int) -> dict:
    """Fetch user from database."""
    # Simulated database call
    return {"id": user_id, "name": "John Doe"}


user = fetch_user(123)  # Logged, retried if fails, cached
```

---

## 5. Facade Pattern

### Use Case: Video Conversion System

Simplifying a complex video processing subsystem.

#### Python

```python
from dataclasses import dataclass
from pathlib import Path


# Complex Subsystem Classes
class VideoDecoder:
    def decode(self, filename: str) -> bytes:
        print(f"Decoding video from {filename}")
        return b"raw_video_data"


class AudioDecoder:
    def decode(self, filename: str) -> bytes:
        print(f"Decoding audio from {filename}")
        return b"raw_audio_data"


class VideoEncoder:
    def encode(self, data: bytes, codec: str, quality: int) -> bytes:
        print(f"Encoding video with {codec} at quality {quality}")
        return b"encoded_video"


class AudioEncoder:
    def encode(self, data: bytes, codec: str, bitrate: int) -> bytes:
        print(f"Encoding audio with {codec} at {bitrate}kbps")
        return b"encoded_audio"


class Muxer:
    def mux(self, video: bytes, audio: bytes, container: str) -> bytes:
        print(f"Muxing video and audio into {container}")
        return b"final_output"


class FileWriter:
    def write(self, data: bytes, output_path: str) -> None:
        print(f"Writing {len(data)} bytes to {output_path}")


class Metadata:
    def add_metadata(self, data: bytes, info: dict) -> bytes:
        print(f"Adding metadata: {info}")
        return data + b"_metadata"


# Facade: Simple interface to complex subsystem
@dataclass
class ConversionOptions:
    video_codec: str = "h264"
    audio_codec: str = "aac"
    video_quality: int = 80
    audio_bitrate: int = 192
    container: str = "mp4"


class VideoConverter:
    """Facade for video conversion subsystem."""

    def __init__(self):
        self._video_decoder = VideoDecoder()
        self._audio_decoder = AudioDecoder()
        self._video_encoder = VideoEncoder()
        self._audio_encoder = AudioEncoder()
        self._muxer = Muxer()
        self._file_writer = FileWriter()
        self._metadata = Metadata()

    def convert(
        self,
        input_path: str,
        output_path: str,
        options: ConversionOptions | None = None
    ) -> None:
        """Convert video file with simple interface."""
        options = options or ConversionOptions()

        print(f"\n=== Converting {input_path} to {output_path} ===\n")

        # Decode
        raw_video = self._video_decoder.decode(input_path)
        raw_audio = self._audio_decoder.decode(input_path)

        # Encode
        encoded_video = self._video_encoder.encode(
            raw_video, options.video_codec, options.video_quality
        )
        encoded_audio = self._audio_encoder.encode(
            raw_audio, options.audio_codec, options.audio_bitrate
        )

        # Mux
        muxed = self._muxer.mux(encoded_video, encoded_audio, options.container)

        # Add metadata
        final = self._metadata.add_metadata(muxed, {
            "encoder": "VideoConverter Facade",
            "codec": options.video_codec
        })

        # Write
        self._file_writer.write(final, output_path)

        print(f"\n=== Conversion complete! ===\n")

    def convert_to_web(self, input_path: str, output_path: str) -> None:
        """Preset for web-optimized video."""
        options = ConversionOptions(
            video_codec="h264",
            audio_codec="aac",
            video_quality=70,
            audio_bitrate=128,
            container="mp4"
        )
        self.convert(input_path, output_path, options)

    def convert_to_archive(self, input_path: str, output_path: str) -> None:
        """Preset for archival quality."""
        options = ConversionOptions(
            video_codec="h265",
            audio_codec="flac",
            video_quality=100,
            audio_bitrate=320,
            container="mkv"
        )
        self.convert(input_path, output_path, options)


# Usage: Simple interface hides complexity
converter = VideoConverter()

# Default conversion
converter.convert("input.avi", "output.mp4")

# Web-optimized preset
converter.convert_to_web("video.mkv", "web_video.mp4")

# Custom options still available
converter.convert(
    "movie.mkv",
    "movie.webm",
    ConversionOptions(video_codec="vp9", container="webm")
)
```

#### TypeScript

```typescript
// Subsystem classes (simplified)
class VideoDecoder {
  decode(filename: string): Uint8Array {
    console.log(`Decoding video from ${filename}`);
    return new Uint8Array();
  }
}

class AudioDecoder {
  decode(filename: string): Uint8Array {
    console.log(`Decoding audio from ${filename}`);
    return new Uint8Array();
  }
}

class VideoEncoder {
  encode(data: Uint8Array, codec: string): Uint8Array {
    console.log(`Encoding video with ${codec}`);
    return new Uint8Array();
  }
}

interface ConversionOptions {
  videoCodec?: string;
  audioCodec?: string;
  container?: string;
}

// Facade
class VideoConverter {
  private videoDecoder = new VideoDecoder();
  private audioDecoder = new AudioDecoder();
  private videoEncoder = new VideoEncoder();

  convert(inputPath: string, outputPath: string, options: ConversionOptions = {}): void {
    const { videoCodec = "h264", container = "mp4" } = options;

    console.log(`\nConverting ${inputPath} to ${outputPath}\n`);

    const rawVideo = this.videoDecoder.decode(inputPath);
    const rawAudio = this.audioDecoder.decode(inputPath);
    const encodedVideo = this.videoEncoder.encode(rawVideo, videoCodec);

    console.log(`Writing ${container} file to ${outputPath}`);
    console.log("\nConversion complete!\n");
  }

  convertToWeb(inputPath: string, outputPath: string): void {
    this.convert(inputPath, outputPath, {
      videoCodec: "h264",
      container: "mp4"
    });
  }
}

// Usage
const converter = new VideoConverter();
converter.convert("input.avi", "output.mp4");
converter.convertToWeb("video.mkv", "web.mp4");
```

---

## 6. Proxy Pattern

### Use Case: Image Lazy Loading with Caching

Virtual proxy for expensive image loading with caching proxy.

#### Python

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import time


@dataclass
class ImageData:
    filename: str
    width: int
    height: int
    data: bytes


# Subject Interface
class Image(ABC):
    @abstractmethod
    def display(self) -> None:
        pass

    @abstractmethod
    def get_dimensions(self) -> tuple[int, int]:
        pass


# Real Subject: Expensive to create
class RealImage(Image):
    def __init__(self, filename: str):
        self.filename = filename
        self._data: ImageData | None = None
        self._load()

    def _load(self) -> None:
        """Expensive operation - loading from disk."""
        print(f"Loading image from disk: {self.filename}")
        time.sleep(0.5)  # Simulate I/O
        self._data = ImageData(
            filename=self.filename,
            width=1920,
            height=1080,
            data=b"image_bytes_here"
        )

    def display(self) -> None:
        print(f"Displaying {self._data.width}x{self._data.height} image: {self.filename}")

    def get_dimensions(self) -> tuple[int, int]:
        return (self._data.width, self._data.height)


# Virtual Proxy: Lazy loading
class LazyImageProxy(Image):
    """Delays image loading until actually needed."""

    def __init__(self, filename: str):
        self.filename = filename
        self._real_image: RealImage | None = None

    def _get_real_image(self) -> RealImage:
        if self._real_image is None:
            print(f"[PROXY] First access - loading image")
            self._real_image = RealImage(self.filename)
        return self._real_image

    def display(self) -> None:
        self._get_real_image().display()

    def get_dimensions(self) -> tuple[int, int]:
        return self._get_real_image().get_dimensions()


# Cache Proxy: Caches loaded images
class CachingImageProxy(Image):
    """Caches images to avoid repeated loading."""

    _cache: dict[str, RealImage] = {}

    def __init__(self, filename: str):
        self.filename = filename

    def _get_image(self) -> RealImage:
        if self.filename not in self._cache:
            print(f"[CACHE] Miss - loading: {self.filename}")
            self._cache[self.filename] = RealImage(self.filename)
        else:
            print(f"[CACHE] Hit: {self.filename}")
        return self._cache[self.filename]

    def display(self) -> None:
        self._get_image().display()

    def get_dimensions(self) -> tuple[int, int]:
        return self._get_image().get_dimensions()


# Protection Proxy: Access control
class ProtectedImageProxy(Image):
    """Controls access based on user permissions."""

    def __init__(self, filename: str, user_role: str):
        self.filename = filename
        self.user_role = user_role
        self._real_image: RealImage | None = None

    def _check_access(self) -> bool:
        allowed_roles = {"admin", "editor", "viewer"}
        if self.user_role not in allowed_roles:
            print(f"[ACCESS DENIED] Role '{self.user_role}' cannot view images")
            return False
        return True

    def _get_image(self) -> Optional[RealImage]:
        if not self._check_access():
            return None
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        return self._real_image

    def display(self) -> None:
        image = self._get_image()
        if image:
            image.display()

    def get_dimensions(self) -> tuple[int, int]:
        image = self._get_image()
        return image.get_dimensions() if image else (0, 0)


# Usage Examples
print("=== Virtual Proxy (Lazy Loading) ===")
lazy_image = LazyImageProxy("large_photo.jpg")
print("Proxy created - no loading yet")
lazy_image.display()  # Now it loads
lazy_image.display()  # Already loaded

print("\n=== Caching Proxy ===")
img1 = CachingImageProxy("photo1.jpg")
img2 = CachingImageProxy("photo1.jpg")  # Same file
img3 = CachingImageProxy("photo2.jpg")

img1.display()  # Cache miss
img2.display()  # Cache hit
img3.display()  # Cache miss

print("\n=== Protection Proxy ===")
admin_image = ProtectedImageProxy("secret.jpg", "admin")
guest_image = ProtectedImageProxy("secret.jpg", "guest")

admin_image.display()  # Allowed
guest_image.display()  # Denied
```

#### TypeScript

```typescript
interface Image {
  display(): void;
  getDimensions(): [number, number];
}

// Real Subject
class RealImage implements Image {
  private data: { width: number; height: number } | null = null;

  constructor(private filename: string) {
    this.load();
  }

  private load(): void {
    console.log(`Loading image from disk: ${this.filename}`);
    this.data = { width: 1920, height: 1080 };
  }

  display(): void {
    console.log(`Displaying ${this.data!.width}x${this.data!.height}: ${this.filename}`);
  }

  getDimensions(): [number, number] {
    return [this.data!.width, this.data!.height];
  }
}

// Virtual Proxy
class LazyImageProxy implements Image {
  private realImage: RealImage | null = null;

  constructor(private filename: string) {}

  private getImage(): RealImage {
    if (!this.realImage) {
      console.log("[PROXY] First access - loading");
      this.realImage = new RealImage(this.filename);
    }
    return this.realImage;
  }

  display(): void {
    this.getImage().display();
  }

  getDimensions(): [number, number] {
    return this.getImage().getDimensions();
  }
}

// Usage
const image = new LazyImageProxy("large.jpg");
console.log("Proxy created - no loading yet");
image.display(); // Now loads
image.display(); // Already loaded
```

---

## 7. Flyweight Pattern

### Use Case: Text Editor Character Rendering

Sharing character formatting objects to save memory.

#### Python

```python
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass(frozen=True)  # Immutable for thread safety
class CharacterStyle:
    """Flyweight: Shared intrinsic state."""
    font_family: str
    font_size: int
    bold: bool = False
    italic: bool = False
    color: str = "black"


class CharacterStyleFactory:
    """Flyweight Factory: Manages shared instances."""

    _styles: ClassVar[dict[tuple, CharacterStyle]] = {}
    _created_count: ClassVar[int] = 0
    _reused_count: ClassVar[int] = 0

    @classmethod
    def get_style(
        cls,
        font_family: str = "Arial",
        font_size: int = 12,
        bold: bool = False,
        italic: bool = False,
        color: str = "black"
    ) -> CharacterStyle:
        """Return cached style or create new one."""
        key = (font_family, font_size, bold, italic, color)

        if key not in cls._styles:
            cls._styles[key] = CharacterStyle(
                font_family, font_size, bold, italic, color
            )
            cls._created_count += 1
        else:
            cls._reused_count += 1

        return cls._styles[key]

    @classmethod
    def stats(cls) -> dict:
        return {
            "unique_styles": len(cls._styles),
            "created": cls._created_count,
            "reused": cls._reused_count,
            "memory_saved": f"{cls._reused_count * 64}+ bytes"
        }


@dataclass
class Character:
    """Context: Contains extrinsic state + reference to flyweight."""
    char: str  # Extrinsic
    position: tuple[int, int]  # Extrinsic
    style: CharacterStyle  # Flyweight (shared)

    def render(self) -> str:
        x, y = self.position
        return (
            f"'{self.char}' at ({x}, {y}) "
            f"[{self.style.font_family} {self.style.font_size}pt "
            f"{'bold ' if self.style.bold else ''}"
            f"{'italic ' if self.style.italic else ''}"
            f"{self.style.color}]"
        )


class TextDocument:
    """Client that uses flyweights."""

    def __init__(self):
        self.characters: list[Character] = []

    def add_text(
        self,
        text: str,
        start_x: int,
        y: int,
        font_family: str = "Arial",
        font_size: int = 12,
        bold: bool = False,
        italic: bool = False,
        color: str = "black"
    ) -> None:
        # Get shared style from factory
        style = CharacterStyleFactory.get_style(
            font_family, font_size, bold, italic, color
        )

        for i, char in enumerate(text):
            self.characters.append(
                Character(char, (start_x + i * 10, y), style)
            )

    def render(self) -> list[str]:
        return [char.render() for char in self.characters]


# Usage: Document with 1000+ characters, only a few unique styles
doc = TextDocument()

# Add text with different styles
doc.add_text("Hello ", 0, 0, "Arial", 14, bold=True)
doc.add_text("World!", 60, 0, "Arial", 14)
doc.add_text("This is normal text. ", 0, 20, "Arial", 12)
doc.add_text("This is also normal text. ", 0, 40, "Arial", 12)  # Same style
doc.add_text("Important! ", 0, 60, "Arial", 12, bold=True, color="red")
doc.add_text("Also important! ", 110, 60, "Arial", 12, bold=True, color="red")

# Render first few characters
print("Sample rendered characters:")
for rendered in doc.render()[:10]:
    print(f"  {rendered}")

# Show memory savings
print(f"\nFlyweight Statistics:")
stats = CharacterStyleFactory.stats()
for key, value in stats.items():
    print(f"  {key}: {value}")

# Output shows: 5 unique styles created, many reused
# Without flyweight: Each of 50+ characters would have its own style object
```

#### TypeScript

```typescript
// Flyweight: Shared intrinsic state
interface CharacterStyle {
  fontFamily: string;
  fontSize: number;
  bold: boolean;
  italic: boolean;
  color: string;
}

// Flyweight Factory
class CharacterStyleFactory {
  private static styles = new Map<string, CharacterStyle>();
  private static createdCount = 0;
  private static reusedCount = 0;

  static getStyle(
    fontFamily = "Arial",
    fontSize = 12,
    bold = false,
    italic = false,
    color = "black"
  ): CharacterStyle {
    const key = `${fontFamily}-${fontSize}-${bold}-${italic}-${color}`;

    if (!this.styles.has(key)) {
      this.styles.set(key, { fontFamily, fontSize, bold, italic, color });
      this.createdCount++;
    } else {
      this.reusedCount++;
    }

    return this.styles.get(key)!;
  }

  static getStats() {
    return {
      uniqueStyles: this.styles.size,
      created: this.createdCount,
      reused: this.reusedCount,
    };
  }
}

// Context with extrinsic state
interface Character {
  char: string;
  x: number;
  y: number;
  style: CharacterStyle; // Reference to flyweight
}

// Client
class TextDocument {
  private characters: Character[] = [];

  addText(
    text: string,
    startX: number,
    y: number,
    fontFamily?: string,
    fontSize?: number,
    bold?: boolean
  ): void {
    const style = CharacterStyleFactory.getStyle(
      fontFamily,
      fontSize,
      bold
    );

    for (let i = 0; i < text.length; i++) {
      this.characters.push({
        char: text[i],
        x: startX + i * 10,
        y,
        style, // Shared reference
      });
    }
  }
}

// Usage
const doc = new TextDocument();
doc.addText("Hello ", 0, 0, "Arial", 14, true);
doc.addText("World!", 60, 0, "Arial", 14);
doc.addText("Normal text repeated many times.", 0, 20, "Arial", 12);
doc.addText("More normal text with same style.", 0, 40, "Arial", 12);

console.log("Stats:", CharacterStyleFactory.getStats());
```

#### Go

```go
package main

import (
    "fmt"
    "sync"
)

// Flyweight: Shared intrinsic state (immutable)
type CharacterStyle struct {
    FontFamily string
    FontSize   int
    Bold       bool
    Color      string
}

// Flyweight Factory with thread safety
type StyleFactory struct {
    mu     sync.RWMutex
    styles map[string]*CharacterStyle
    stats  struct {
        created int
        reused  int
    }
}

func NewStyleFactory() *StyleFactory {
    return &StyleFactory{
        styles: make(map[string]*CharacterStyle),
    }
}

func (f *StyleFactory) GetStyle(fontFamily string, fontSize int, bold bool, color string) *CharacterStyle {
    key := fmt.Sprintf("%s-%d-%t-%s", fontFamily, fontSize, bold, color)

    f.mu.RLock()
    if style, exists := f.styles[key]; exists {
        f.mu.RUnlock()
        f.mu.Lock()
        f.stats.reused++
        f.mu.Unlock()
        return style
    }
    f.mu.RUnlock()

    f.mu.Lock()
    defer f.mu.Unlock()

    // Double-check after acquiring write lock
    if style, exists := f.styles[key]; exists {
        f.stats.reused++
        return style
    }

    style := &CharacterStyle{
        FontFamily: fontFamily,
        FontSize:   fontSize,
        Bold:       bold,
        Color:      color,
    }
    f.styles[key] = style
    f.stats.created++

    return style
}

func (f *StyleFactory) Stats() map[string]int {
    f.mu.RLock()
    defer f.mu.RUnlock()
    return map[string]int{
        "unique":  len(f.styles),
        "created": f.stats.created,
        "reused":  f.stats.reused,
    }
}

// Context with extrinsic state
type Character struct {
    Char  rune
    X, Y  int
    Style *CharacterStyle // Flyweight reference
}

func main() {
    factory := NewStyleFactory()

    // Create many characters, few styles
    style1 := factory.GetStyle("Arial", 14, true, "black")
    style2 := factory.GetStyle("Arial", 12, false, "black")
    style3 := factory.GetStyle("Arial", 14, true, "black")  // Reused
    style4 := factory.GetStyle("Arial", 12, false, "black") // Reused

    fmt.Printf("style1 == style3: %v\n", style1 == style3)
    fmt.Printf("style2 == style4: %v\n", style2 == style4)
    fmt.Printf("Stats: %+v\n", factory.Stats())
}
```

---

## Summary

| Pattern | Best Use Case | Key Implementation Detail |
|---------|---------------|---------------------------|
| Adapter | Legacy/third-party integration | Wrap adaptee, implement target interface |
| Bridge | Multiple independent variations | Separate abstraction and implementation hierarchies |
| Composite | Tree structures | Uniform interface for leaves and composites |
| Decorator | Dynamic behavior addition | Stack wrappers implementing same interface |
| Facade | Complex subsystem simplification | Single entry point delegating to subsystem |
| Proxy | Access control, lazy loading, caching | Same interface as real subject |
| Flyweight | Many similar objects, memory constrained | Separate intrinsic (shared) and extrinsic state |
