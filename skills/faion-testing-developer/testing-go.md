---
name: faion-testing-go
user-invocable: false
description: "Go testing: table-driven tests, mocking, benchmarks, fuzzing"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(go test:*)
---

# Go Testing

## Overview

Go has built-in testing via `testing` package. No external dependencies required.

## Project Structure

```
project/
├── pkg/
│   └── user/
│       ├── user.go
│       └── user_test.go
├── internal/
│   └── service/
│       ├── service.go
│       └── service_test.go
└── go.mod
```

## Basic Test

```go
// user_test.go
package user

import "testing"

func TestCreateUser(t *testing.T) {
    // Arrange
    service := NewUserService()
    input := UserInput{Name: "John", Email: "john@example.com"}

    // Act
    user, err := service.Create(input)

    // Assert
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if user.Name != "John" {
        t.Errorf("expected name 'John', got '%s'", user.Name)
    }
}
```

## Table-Driven Tests

```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid email", "user@example.com", false},
        {"missing at symbol", "invalid", true},
        {"missing domain", "user@", true},
        {"empty string", "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateEmail(%q) error = %v, wantErr %v",
                    tt.email, err, tt.wantErr)
            }
        })
    }
}
```

## Subtests

```go
func TestUserService(t *testing.T) {
    service := NewUserService()

    t.Run("Create", func(t *testing.T) {
        t.Run("with valid data", func(t *testing.T) {
            user, err := service.Create(validInput)
            if err != nil {
                t.Fatal(err)
            }
            if user.ID == 0 {
                t.Error("expected non-zero ID")
            }
        })

        t.Run("with invalid email", func(t *testing.T) {
            _, err := service.Create(invalidInput)
            if err == nil {
                t.Error("expected error for invalid email")
            }
        })
    })
}
```

## Test Helpers

```go
// testutil/helpers.go
package testutil

import "testing"

func AssertNoError(t *testing.T, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}

func AssertEqual[T comparable](t *testing.T, got, want T) {
    t.Helper()
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}
```

## Mocking with Interfaces

```go
// Define interface
type UserRepository interface {
    Create(user User) (User, error)
    FindByID(id int) (User, error)
}

// Mock implementation
type MockUserRepository struct {
    CreateFunc   func(user User) (User, error)
    FindByIDFunc func(id int) (User, error)
}

func (m *MockUserRepository) Create(user User) (User, error) {
    if m.CreateFunc != nil {
        return m.CreateFunc(user)
    }
    return User{}, nil
}

// Test with mock
func TestUserService_Create(t *testing.T) {
    mockRepo := &MockUserRepository{
        CreateFunc: func(user User) (User, error) {
            user.ID = 1
            return user, nil
        },
    }

    service := NewUserService(mockRepo)
    user, err := service.Create(UserInput{Name: "John"})

    if err != nil {
        t.Fatal(err)
    }
    if user.ID != 1 {
        t.Errorf("expected ID 1, got %d", user.ID)
    }
}
```

## Setup and Teardown

```go
func TestMain(m *testing.M) {
    // Global setup
    setup()

    // Run tests
    code := m.Run()

    // Global teardown
    teardown()

    os.Exit(code)
}
```

## Benchmarks

```go
func BenchmarkProcessData(b *testing.B) {
    data := generateTestData(1000)

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        ProcessData(data)
    }
}

func BenchmarkProcessData_Parallel(b *testing.B) {
    data := generateTestData(1000)

    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            ProcessData(data)
        }
    })
}
```

## Fuzzing (Go 1.18+)

```go
func FuzzParseEmail(f *testing.F) {
    // Seed corpus
    f.Add("user@example.com")
    f.Add("invalid")
    f.Add("")

    f.Fuzz(func(t *testing.T, email string) {
        _, err := ParseEmail(email)
        // Verify no panic
        _ = err
    })
}
```

## Running Tests

```bash
go test ./...                    # Run all tests
go test -v ./...                 # Verbose
go test ./pkg/user               # Specific package
go test -run TestCreateUser      # Specific test
go test -cover ./...             # With coverage
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out # HTML report
go test -bench=. ./...           # Run benchmarks
go test -race ./...              # Race detection
```

## Sources

- [Go Testing Package](https://pkg.go.dev/testing) - official testing docs
- [Table Driven Tests](https://go.dev/wiki/TableDrivenTests) - table-driven test pattern
- [Go Fuzzing](https://go.dev/security/fuzz/) - fuzzing tutorial
- [Advanced Testing with Go](https://www.youtube.com/watch?v=8hQG7QlcLBk) - Mitchell Hashimoto talk
- [Testing Techniques](https://go.dev/doc/tutorial/add-a-test) - official testing tutorial
