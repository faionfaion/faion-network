# M-GO-001: Go Project Setup

## Metadata
- **Category:** Development/Backend/Go
- **Difficulty:** Beginner
- **Tags:** #dev, #go, #backend, #setup, #methodology
- **Agent:** faion-code-agent

---

## Problem

Go projects can become disorganized without proper structure. Module management, dependency handling, and project layout confuse newcomers. You need a standard approach that the Go community expects.

## Promise

After this methodology, you will have a professional Go project with proper module structure, dependency management, and layout that scales from CLI tools to large services.

## Overview

Go uses modules for dependency management since Go 1.11+. This methodology covers project setup following Go community conventions and the official project layout recommendations.

---

## Framework

### Step 1: Initialize Module

```bash
# Create project directory
mkdir my-project && cd my-project

# Initialize Go module
go mod init github.com/username/my-project

# This creates go.mod file
```

**go.mod:**

```go
module github.com/username/my-project

go 1.22

require (
    // Dependencies will be added here
)
```

### Step 2: Project Layout

**Standard Layout:**

```
my-project/
├── go.mod
├── go.sum
├── README.md
├── Makefile
├── .gitignore
├── cmd/                  # Main applications
│   ├── api/
│   │   └── main.go       # API server entry point
│   └── cli/
│       └── main.go       # CLI tool entry point
├── internal/             # Private application code
│   ├── config/
│   │   └── config.go
│   ├── handler/
│   │   └── user.go
│   ├── service/
│   │   └── user.go
│   ├── repository/
│   │   └── user.go
│   └── model/
│       └── user.go
├── pkg/                  # Public library code
│   └── validator/
│       └── validator.go
├── api/                  # API definitions (OpenAPI, proto)
│   └── openapi.yaml
├── configs/              # Configuration files
│   ├── config.yaml
│   └── config.example.yaml
├── scripts/              # Build and CI scripts
├── test/                 # Additional test files
│   └── integration/
└── docs/
```

### Step 3: Main Entry Point

**cmd/api/main.go:**

```go
package main

import (
    "context"
    "log/slog"
    "os"
    "os/signal"
    "syscall"

    "github.com/username/my-project/internal/config"
    "github.com/username/my-project/internal/handler"
    "github.com/username/my-project/internal/server"
)

func main() {
    // Initialize logger
    logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
    slog.SetDefault(logger)

    // Load configuration
    cfg, err := config.Load()
    if err != nil {
        slog.Error("failed to load config", "error", err)
        os.Exit(1)
    }

    // Create server
    srv := server.New(cfg)

    // Graceful shutdown
    ctx, stop := signal.NotifyContext(context.Background(),
        syscall.SIGINT, syscall.SIGTERM)
    defer stop()

    // Start server
    go func() {
        if err := srv.Start(); err != nil {
            slog.Error("server error", "error", err)
        }
    }()

    slog.Info("server started", "port", cfg.Port)

    <-ctx.Done()
    slog.Info("shutting down...")

    if err := srv.Shutdown(context.Background()); err != nil {
        slog.Error("shutdown error", "error", err)
    }
}
```

### Step 4: Dependency Management

```bash
# Add dependency
go get github.com/gin-gonic/gin

# Add specific version
go get github.com/gin-gonic/gin@v1.9.1

# Update all dependencies
go get -u ./...

# Tidy up (remove unused)
go mod tidy

# Vendor dependencies (optional)
go mod vendor

# List dependencies
go list -m all
```

### Step 5: Configuration

**internal/config/config.go:**

```go
package config

import (
    "os"
    "strconv"
    "time"
)

type Config struct {
    Port         int
    Environment  string
    DatabaseURL  string
    JWTSecret    string
    ReadTimeout  time.Duration
    WriteTimeout time.Duration
}

func Load() (*Config, error) {
    return &Config{
        Port:         getEnvInt("PORT", 8080),
        Environment:  getEnv("ENVIRONMENT", "development"),
        DatabaseURL:  mustGetEnv("DATABASE_URL"),
        JWTSecret:    mustGetEnv("JWT_SECRET"),
        ReadTimeout:  time.Duration(getEnvInt("READ_TIMEOUT_SECONDS", 5)) * time.Second,
        WriteTimeout: time.Duration(getEnvInt("WRITE_TIMEOUT_SECONDS", 10)) * time.Second,
    }, nil
}

func getEnv(key, defaultValue string) string {
    if value := os.Getenv(key); value != "" {
        return value
    }
    return defaultValue
}

func mustGetEnv(key string) string {
    value := os.Getenv(key)
    if value == "" {
        panic("required environment variable not set: " + key)
    }
    return value
}

func getEnvInt(key string, defaultValue int) int {
    if value := os.Getenv(key); value != "" {
        if i, err := strconv.Atoi(value); err == nil {
            return i
        }
    }
    return defaultValue
}
```

### Step 6: Makefile

```makefile
.PHONY: build run test lint clean

# Variables
BINARY_NAME=api
BUILD_DIR=./bin
MAIN_PATH=./cmd/api

# Build
build:
	go build -o $(BUILD_DIR)/$(BINARY_NAME) $(MAIN_PATH)

# Run
run:
	go run $(MAIN_PATH)

# Test
test:
	go test -v ./...

test-coverage:
	go test -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

# Lint
lint:
	golangci-lint run

# Format
fmt:
	go fmt ./...
	goimports -w .

# Clean
clean:
	rm -rf $(BUILD_DIR)
	rm -f coverage.out coverage.html

# All
all: fmt lint test build
```

---

## Templates

### .gitignore

```
# Binaries
bin/
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test
*.test
coverage.out
coverage.html

# Vendor
vendor/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db
```

### Dockerfile

```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o /bin/api ./cmd/api

# Production stage
FROM alpine:3.19

RUN apk --no-cache add ca-certificates

WORKDIR /app

COPY --from=builder /bin/api .

EXPOSE 8080

CMD ["./api"]
```

---

## Examples

### Simple HTTP Server

```go
package main

import (
    "encoding/json"
    "log"
    "net/http"
)

type Response struct {
    Message string `json:"message"`
}

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(Response{Message: "Hello, World!"})
    })

    log.Println("Server starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

### CLI Application

```go
package main

import (
    "flag"
    "fmt"
    "os"
)

func main() {
    name := flag.String("name", "World", "Name to greet")
    flag.Parse()

    fmt.Printf("Hello, %s!\n", *name)
}
```

---

## Common Mistakes

1. **Not using go mod tidy** - Run after changing dependencies
2. **Importing internal packages** - internal/ is private to your module
3. **Using global variables** - Pass dependencies explicitly
4. **Ignoring error returns** - Always handle errors
5. **Not vendoring in CI** - Use go mod vendor for reproducible builds

---

## Checklist

- [ ] go.mod initialized with proper module path
- [ ] Project follows standard layout
- [ ] cmd/ contains main packages
- [ ] internal/ for private code
- [ ] Makefile with common commands
- [ ] .gitignore configured
- [ ] README.md with setup instructions

---

## Next Steps

- M-GO-002: Go Web Frameworks
- M-GO-003: Go Testing
- M-GO-004: Go Error Handling

---

*Methodology M-GO-001 v1.0*
