---
id: go-channels
name: "Go Channels & Pipeline Patterns"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Go Channels & Pipeline Patterns

## Overview

Channels are Go's primary mechanism for communication between goroutines. This methodology covers channel patterns, pipelines, fan-out/fan-in, and select operations for building concurrent data processing systems.

## When to Use

- Data pipeline processing
- Event-driven systems
- Coordinating multiple goroutines
- Building producer-consumer patterns
- Implementing pub-sub systems

## Key Principles

1. **Channels are first-class values** - Pass them as parameters
2. **Close channels from sender side** - Receivers detect closure
3. **Buffered channels for async** - Use buffering to decouple sender/receiver
4. **Select for multiplexing** - Handle multiple channel operations
5. **Use context for cancellation** - Graceful shutdown

## Best Practices

### Pipeline Pattern

```go
package pipeline

import "context"

// Stage 1: Generate numbers
func generate(ctx context.Context, nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            select {
            case out <- n:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

// Stage 2: Square numbers
func square(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case out <- n * n:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

// Stage 3: Filter even numbers
func filterEven(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            if n%2 == 0 {
                select {
                case out <- n:
                case <-ctx.Done():
                    return
                }
            }
        }
    }()
    return out
}

// Fan-out: Distribute work to multiple goroutines
func fanOut(ctx context.Context, in <-chan int, n int) []<-chan int {
    outs := make([]<-chan int, n)
    for i := 0; i < n; i++ {
        outs[i] = square(ctx, in)
    }
    return outs
}

// Fan-in: Merge multiple channels into one
func fanIn(ctx context.Context, channels ...<-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup

    output := func(c <-chan int) {
        defer wg.Done()
        for n := range c {
            select {
            case out <- n:
            case <-ctx.Done():
                return
            }
        }
    }

    wg.Add(len(channels))
    for _, c := range channels {
        go output(c)
    }

    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}

// Usage
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // Build pipeline
    nums := generate(ctx, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    squared := square(ctx, nums)
    even := filterEven(ctx, squared)

    for n := range even {
        fmt.Println(n)
    }
}
```

### Select with Timeout

```go
package main

import (
    "context"
    "fmt"
    "time"
)

// Timeout pattern
func fetchWithTimeout(url string, timeout time.Duration) (string, error) {
    ctx, cancel := context.WithTimeout(context.Background(), timeout)
    defer cancel()

    resultCh := make(chan string, 1)
    errCh := make(chan error, 1)

    go func() {
        result, err := doFetch(ctx, url)
        if err != nil {
            errCh <- err
            return
        }
        resultCh <- result
    }()

    select {
    case result := <-resultCh:
        return result, nil
    case err := <-errCh:
        return "", err
    case <-ctx.Done():
        return "", fmt.Errorf("timeout after %v", timeout)
    }
}

// First response wins
func fetchFirst(ctx context.Context, urls []string) (string, error) {
    ctx, cancel := context.WithCancel(ctx)
    defer cancel() // Cancel remaining requests

    resultCh := make(chan string, len(urls))

    for _, url := range urls {
        go func(u string) {
            result, err := doFetch(ctx, u)
            if err == nil {
                resultCh <- result
            }
        }(url)
    }

    select {
    case result := <-resultCh:
        return result, nil
    case <-ctx.Done():
        return "", ctx.Err()
    }
}
```

### Buffered Channels

```go
package buffer

import (
    "context"
    "time"
)

// Producer with buffered channel
func producer(ctx context.Context, buffer int) <-chan int {
    out := make(chan int, buffer)
    go func() {
        defer close(out)
        for i := 0; ; i++ {
            select {
            case out <- i:
                // Non-blocking send up to buffer size
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

// Consumer with processing delay
func consumer(ctx context.Context, in <-chan int) {
    for {
        select {
        case n, ok := <-in:
            if !ok {
                return
            }
            // Process with delay
            time.Sleep(100 * time.Millisecond)
            fmt.Println(n)
        case <-ctx.Done():
            return
        }
    }
}
```

### Broadcast Pattern

```go
package broadcast

import (
    "sync"
)

type Broadcaster struct {
    mu          sync.RWMutex
    subscribers map[int]chan interface{}
    nextID      int
}

func New() *Broadcaster {
    return &Broadcaster{
        subscribers: make(map[int]chan interface{}),
    }
}

func (b *Broadcaster) Subscribe() (int, <-chan interface{}) {
    b.mu.Lock()
    defer b.mu.Unlock()

    id := b.nextID
    b.nextID++

    ch := make(chan interface{}, 1)
    b.subscribers[id] = ch

    return id, ch
}

func (b *Broadcaster) Unsubscribe(id int) {
    b.mu.Lock()
    defer b.mu.Unlock()

    if ch, exists := b.subscribers[id]; exists {
        close(ch)
        delete(b.subscribers, id)
    }
}

func (b *Broadcaster) Broadcast(msg interface{}) {
    b.mu.RLock()
    defer b.mu.RUnlock()

    for _, ch := range b.subscribers {
        select {
        case ch <- msg:
        default:
            // Skip slow subscriber
        }
    }
}

// Usage
func main() {
    bc := New()

    // Subscriber 1
    id1, ch1 := bc.Subscribe()
    go func() {
        for msg := range ch1 {
            fmt.Printf("Sub1: %v\n", msg)
        }
    }()

    // Subscriber 2
    id2, ch2 := bc.Subscribe()
    go func() {
        for msg := range ch2 {
            fmt.Printf("Sub2: %v\n", msg)
        }
    }()

    // Broadcast messages
    bc.Broadcast("message 1")
    bc.Broadcast("message 2")

    // Cleanup
    bc.Unsubscribe(id1)
    bc.Unsubscribe(id2)
}
```

### Done Channel Pattern

```go
package done

import (
    "fmt"
    "time"
)

func worker(done <-chan struct{}) {
    for {
        select {
        case <-done:
            fmt.Println("Worker stopping")
            return
        default:
            // Do work
            time.Sleep(100 * time.Millisecond)
            fmt.Println("Working...")
        }
    }
}

func main() {
    done := make(chan struct{})

    go worker(done)
    go worker(done)

    time.Sleep(1 * time.Second)

    // Signal all workers to stop
    close(done)

    time.Sleep(200 * time.Millisecond)
}
```

### Or-Done Channel

```go
package ordone

// Wraps channel to simplify select with done
func orDone(done <-chan struct{}, c <-chan interface{}) <-chan interface{} {
    out := make(chan interface{})
    go func() {
        defer close(out)
        for {
            select {
            case <-done:
                return
            case v, ok := <-c:
                if !ok {
                    return
                }
                select {
                case out <- v:
                case <-done:
                    return
                }
            }
        }
    }()
    return out
}

// Usage
func main() {
    done := make(chan struct{})
    defer close(done)

    data := make(chan interface{})
    go func() {
        for i := 0; i < 10; i++ {
            data <- i
        }
        close(data)
    }()

    // Simplified iteration with orDone
    for val := range orDone(done, data) {
        fmt.Println(val)
    }
}
```

### Tee Channel (Split Stream)

```go
package tee

func tee(done <-chan struct{}, in <-chan interface{}) (<-chan interface{}, <-chan interface{}) {
    out1 := make(chan interface{})
    out2 := make(chan interface{})

    go func() {
        defer close(out1)
        defer close(out2)

        for val := range orDone(done, in) {
            // Send to both outputs
            var out1, out2 = out1, out2
            for i := 0; i < 2; i++ {
                select {
                case <-done:
                    return
                case out1 <- val:
                    out1 = nil
                case out2 <- val:
                    out2 = nil
                }
            }
        }
    }()

    return out1, out2
}
```

## Anti-patterns

### Avoid: Sending on Closed Channel

```go
// BAD - panic: send on closed channel
ch := make(chan int)
close(ch)
ch <- 1 // PANIC!

// GOOD - check if should send before closing
done := make(chan struct{})
ch := make(chan int)

go func() {
    for {
        select {
        case <-done:
            return
        case ch <- getValue():
        }
    }
}()

close(done) // Signal goroutine to stop
```

### Avoid: Closing Receive-Only Channel

```go
// BAD - cannot close receive-only channel
func consumer(ch <-chan int) {
    close(ch) // Compile error
}

// GOOD - close from sender side
func producer() <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)
        ch <- 1
    }()
    return ch
}
```

### Avoid: Range on Unbuffered Channel Without Close

```go
// BAD - range waits for close, but sender never closes
func process() {
    ch := make(chan int)
    go func() {
        ch <- 1
        // Missing close(ch)
    }()

    for val := range ch { // Blocks forever after receiving 1
        fmt.Println(val)
    }
}

// GOOD - close channel when done
func process() {
    ch := make(chan int)
    go func() {
        ch <- 1
        close(ch)
    }()

    for val := range ch {
        fmt.Println(val)
    }
}
```

## References

- [Go Concurrency Patterns: Pipelines](https://go.dev/blog/pipelines)
- [Go Concurrency Patterns: Context](https://go.dev/blog/context)
- [Go by Example: Channels](https://gobyexample.com/channels)
- [Effective Go: Channels](https://go.dev/doc/effective_go#channels)
