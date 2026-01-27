# Go Testing Examples

Real-world examples demonstrating Go testing patterns and best practices.

## Table-Driven Tests

### Basic Table-Driven Test

```go
package user

import "testing"

func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {
            name:    "valid email",
            email:   "user@example.com",
            wantErr: false,
        },
        {
            name:    "valid email with subdomain",
            email:   "user@mail.example.com",
            wantErr: false,
        },
        {
            name:    "missing at symbol",
            email:   "invalid",
            wantErr: true,
        },
        {
            name:    "missing domain",
            email:   "user@",
            wantErr: true,
        },
        {
            name:    "missing local part",
            email:   "@example.com",
            wantErr: true,
        },
        {
            name:    "empty string",
            email:   "",
            wantErr: true,
        },
        {
            name:    "spaces only",
            email:   "   ",
            wantErr: true,
        },
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

### Parallel Table-Driven Tests

```go
func TestProcessOrder(t *testing.T) {
    tests := []struct {
        name     string
        order    Order
        wantErr  bool
        wantCode string
    }{
        {
            name:     "valid order",
            order:    Order{ID: "123", Amount: 100},
            wantErr:  false,
            wantCode: "OK",
        },
        {
            name:     "zero amount",
            order:    Order{ID: "456", Amount: 0},
            wantErr:  true,
            wantCode: "",
        },
    }

    for _, tt := range tests {
        tt := tt // Capture range variable for parallel execution
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // Run subtests in parallel

            result, err := ProcessOrder(tt.order)
            if (err != nil) != tt.wantErr {
                t.Errorf("ProcessOrder() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if result.Code != tt.wantCode {
                t.Errorf("ProcessOrder() code = %v, want %v", result.Code, tt.wantCode)
            }
        })
    }
}
```

### Table Tests with Maps (Random Order)

```go
func TestParseConfig(t *testing.T) {
    // Using map for random test order - helps detect order dependencies
    tests := map[string]struct {
        input   string
        want    Config
        wantErr bool
    }{
        "valid json": {
            input:   `{"port": 8080, "host": "localhost"}`,
            want:    Config{Port: 8080, Host: "localhost"},
            wantErr: false,
        },
        "empty json": {
            input:   `{}`,
            want:    Config{},
            wantErr: false,
        },
        "invalid json": {
            input:   `{invalid}`,
            want:    Config{},
            wantErr: true,
        },
    }

    for name, tt := range tests {
        t.Run(name, func(t *testing.T) {
            got, err := ParseConfig(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("ParseConfig() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("ParseConfig() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

## Subtests with t.Run

### Hierarchical Test Organization

```go
func TestUserService(t *testing.T) {
    // Setup shared across all subtests
    service := NewUserService(NewMockRepository())

    t.Run("Create", func(t *testing.T) {
        t.Run("with valid data creates user", func(t *testing.T) {
            input := UserInput{
                Name:  "John Doe",
                Email: "john@example.com",
            }

            user, err := service.Create(input)

            if err != nil {
                t.Fatalf("unexpected error: %v", err)
            }
            if user.ID == 0 {
                t.Error("expected non-zero ID")
            }
            if user.Name != input.Name {
                t.Errorf("name = %q, want %q", user.Name, input.Name)
            }
        })

        t.Run("with invalid email returns error", func(t *testing.T) {
            input := UserInput{
                Name:  "Jane Doe",
                Email: "invalid-email",
            }

            _, err := service.Create(input)

            if err == nil {
                t.Error("expected error for invalid email")
            }
        })

        t.Run("with empty name returns error", func(t *testing.T) {
            input := UserInput{
                Name:  "",
                Email: "jane@example.com",
            }

            _, err := service.Create(input)

            if err == nil {
                t.Error("expected error for empty name")
            }
        })
    })

    t.Run("FindByID", func(t *testing.T) {
        t.Run("existing user returns user", func(t *testing.T) {
            user, err := service.FindByID(1)

            if err != nil {
                t.Fatalf("unexpected error: %v", err)
            }
            if user.ID != 1 {
                t.Errorf("ID = %d, want 1", user.ID)
            }
        })

        t.Run("non-existing user returns not found error", func(t *testing.T) {
            _, err := service.FindByID(9999)

            if err == nil {
                t.Error("expected error for non-existing user")
            }
            if !errors.Is(err, ErrNotFound) {
                t.Errorf("error = %v, want %v", err, ErrNotFound)
            }
        })
    })
}
```

## Interface-Based Mocking

### Manual Mock Implementation

```go
// repository.go
type UserRepository interface {
    Create(user User) (User, error)
    FindByID(id int) (User, error)
    Update(user User) error
    Delete(id int) error
}

// mock_repository_test.go
type MockUserRepository struct {
    CreateFunc   func(user User) (User, error)
    FindByIDFunc func(id int) (User, error)
    UpdateFunc   func(user User) error
    DeleteFunc   func(id int) error

    // Track calls for verification
    CreateCalls   []User
    FindByIDCalls []int
}

func (m *MockUserRepository) Create(user User) (User, error) {
    m.CreateCalls = append(m.CreateCalls, user)
    if m.CreateFunc != nil {
        return m.CreateFunc(user)
    }
    return User{}, nil
}

func (m *MockUserRepository) FindByID(id int) (User, error) {
    m.FindByIDCalls = append(m.FindByIDCalls, id)
    if m.FindByIDFunc != nil {
        return m.FindByIDFunc(id)
    }
    return User{}, nil
}

// service_test.go
func TestUserService_Create(t *testing.T) {
    mockRepo := &MockUserRepository{
        CreateFunc: func(user User) (User, error) {
            user.ID = 42
            user.CreatedAt = time.Now()
            return user, nil
        },
    }

    service := NewUserService(mockRepo)
    input := UserInput{Name: "John", Email: "john@example.com"}

    user, err := service.Create(input)

    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if user.ID != 42 {
        t.Errorf("ID = %d, want 42", user.ID)
    }
    if len(mockRepo.CreateCalls) != 1 {
        t.Errorf("Create called %d times, want 1", len(mockRepo.CreateCalls))
    }
}
```

## testify/assert and testify/mock

### Using testify/assert

```go
package user

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestCalculateDiscount(t *testing.T) {
    tests := []struct {
        name     string
        price    float64
        quantity int
        want     float64
    }{
        {"no discount under 5 items", 100.0, 3, 300.0},
        {"5% discount for 5+ items", 100.0, 5, 475.0},
        {"10% discount for 10+ items", 100.0, 10, 900.0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := CalculateDiscount(tt.price, tt.quantity)
            assert.Equal(t, tt.want, got, "discount calculation mismatch")
        })
    }
}

func TestCreateOrder(t *testing.T) {
    // require stops test on failure - use for preconditions
    service := NewOrderService()
    require.NotNil(t, service, "service should not be nil")

    order, err := service.Create(OrderInput{
        CustomerID: 1,
        Items:      []Item{{SKU: "ABC", Quantity: 2}},
    })

    // assert continues test on failure - use for assertions
    assert.NoError(t, err)
    assert.NotEmpty(t, order.ID)
    assert.Equal(t, 1, order.CustomerID)
    assert.Len(t, order.Items, 1)
    assert.Equal(t, "pending", order.Status)
}

func TestParseResponse(t *testing.T) {
    response := `{"status": "success", "data": {"id": 1}}`

    result, err := ParseResponse(response)

    assert.NoError(t, err)
    assert.Equal(t, "success", result.Status)
    assert.Contains(t, result.Data, "id")
    assert.NotContains(t, result.Data, "error")
}
```

### Using testify/mock

```go
package order

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// MockPaymentService implements PaymentService interface
type MockPaymentService struct {
    mock.Mock
}

func (m *MockPaymentService) Charge(amount float64, customerID int) (string, error) {
    args := m.Called(amount, customerID)
    return args.String(0), args.Error(1)
}

func (m *MockPaymentService) Refund(transactionID string) error {
    args := m.Called(transactionID)
    return args.Error(0)
}

func TestOrderService_ProcessPayment(t *testing.T) {
    t.Run("successful payment", func(t *testing.T) {
        mockPayment := new(MockPaymentService)
        mockPayment.On("Charge", 100.0, 1).Return("tx_123", nil)

        service := NewOrderService(mockPayment)
        order := Order{ID: "order_1", Amount: 100.0, CustomerID: 1}

        err := service.ProcessPayment(order)

        assert.NoError(t, err)
        mockPayment.AssertExpectations(t)
        mockPayment.AssertCalled(t, "Charge", 100.0, 1)
    })

    t.Run("payment failure triggers refund", func(t *testing.T) {
        mockPayment := new(MockPaymentService)
        mockPayment.On("Charge", mock.AnythingOfType("float64"), mock.AnythingOfType("int")).
            Return("", errors.New("insufficient funds"))

        service := NewOrderService(mockPayment)
        order := Order{ID: "order_2", Amount: 500.0, CustomerID: 2}

        err := service.ProcessPayment(order)

        assert.Error(t, err)
        assert.Contains(t, err.Error(), "insufficient funds")
        mockPayment.AssertExpectations(t)
    })
}
```

## go-cmp for Comparisons

### Basic go-cmp Usage

```go
package user

import (
    "testing"
    "time"

    "github.com/google/go-cmp/cmp"
    "github.com/google/go-cmp/cmp/cmpopts"
)

func TestGetUser(t *testing.T) {
    service := NewUserService()

    got, err := service.GetUser(1)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }

    want := User{
        ID:    1,
        Name:  "John Doe",
        Email: "john@example.com",
    }

    if diff := cmp.Diff(want, got); diff != "" {
        t.Errorf("GetUser() mismatch (-want +got):\n%s", diff)
    }
}

func TestListUsers(t *testing.T) {
    service := NewUserService()
    got, _ := service.ListUsers()

    want := []User{
        {ID: 1, Name: "Alice"},
        {ID: 2, Name: "Bob"},
    }

    // Sort slices before comparison (order doesn't matter)
    sortOpt := cmpopts.SortSlices(func(a, b User) bool {
        return a.ID < b.ID
    })

    if diff := cmp.Diff(want, got, sortOpt); diff != "" {
        t.Errorf("ListUsers() mismatch (-want +got):\n%s", diff)
    }
}

func TestUserWithTimestamp(t *testing.T) {
    service := NewUserService()
    user, _ := service.Create(UserInput{Name: "Test"})

    want := User{
        ID:        1,
        Name:      "Test",
        CreatedAt: time.Now(), // Will differ slightly
    }

    // Ignore time fields that vary
    opts := cmpopts.IgnoreFields(User{}, "CreatedAt", "UpdatedAt")

    if diff := cmp.Diff(want, user, opts); diff != "" {
        t.Errorf("Create() mismatch (-want +got):\n%s", diff)
    }

    // Or use approximate time comparison
    timeOpt := cmp.Comparer(func(a, b time.Time) bool {
        return a.Sub(b).Abs() < time.Second
    })

    if diff := cmp.Diff(want, user, timeOpt); diff != "" {
        t.Errorf("Create() mismatch (-want +got):\n%s", diff)
    }
}

func TestConfigWithUnexported(t *testing.T) {
    got := LoadConfig("test.json")
    want := Config{
        Port: 8080,
        Host: "localhost",
    }

    // Allow comparison of unexported fields
    opts := cmp.AllowUnexported(Config{})

    // Or ignore unexported fields
    ignoreOpts := cmpopts.IgnoreUnexported(Config{})

    if diff := cmp.Diff(want, got, ignoreOpts); diff != "" {
        t.Errorf("LoadConfig() mismatch (-want +got):\n%s", diff)
    }
}
```

## HTTP Handler Testing with httptest

### Testing HTTP Handlers

```go
package api

import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/stretchr/testify/assert"
)

func TestGetUserHandler(t *testing.T) {
    // Setup
    mockService := &MockUserService{
        GetFunc: func(id int) (User, error) {
            return User{ID: id, Name: "Test User"}, nil
        },
    }
    handler := NewUserHandler(mockService)

    tests := []struct {
        name       string
        path       string
        wantStatus int
        wantBody   string
    }{
        {
            name:       "valid user ID",
            path:       "/users/1",
            wantStatus: http.StatusOK,
            wantBody:   `"name":"Test User"`,
        },
        {
            name:       "invalid user ID",
            path:       "/users/abc",
            wantStatus: http.StatusBadRequest,
            wantBody:   `"error"`,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest(http.MethodGet, tt.path, nil)
            w := httptest.NewRecorder()

            handler.ServeHTTP(w, req)

            assert.Equal(t, tt.wantStatus, w.Code)
            assert.Contains(t, w.Body.String(), tt.wantBody)
        })
    }
}

func TestCreateUserHandler(t *testing.T) {
    mockService := &MockUserService{
        CreateFunc: func(input UserInput) (User, error) {
            return User{ID: 1, Name: input.Name, Email: input.Email}, nil
        },
    }
    handler := NewUserHandler(mockService)

    input := UserInput{Name: "John", Email: "john@example.com"}
    body, _ := json.Marshal(input)

    req := httptest.NewRequest(http.MethodPost, "/users", bytes.NewReader(body))
    req.Header.Set("Content-Type", "application/json")
    w := httptest.NewRecorder()

    handler.ServeHTTP(w, req)

    assert.Equal(t, http.StatusCreated, w.Code)

    var response User
    json.Unmarshal(w.Body.Bytes(), &response)
    assert.Equal(t, "John", response.Name)
    assert.Equal(t, 1, response.ID)
}

func TestMiddleware(t *testing.T) {
    // Test authentication middleware
    handler := AuthMiddleware(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("success"))
    }))

    t.Run("with valid token", func(t *testing.T) {
        req := httptest.NewRequest(http.MethodGet, "/protected", nil)
        req.Header.Set("Authorization", "Bearer valid-token")
        w := httptest.NewRecorder()

        handler.ServeHTTP(w, req)

        assert.Equal(t, http.StatusOK, w.Code)
    })

    t.Run("without token", func(t *testing.T) {
        req := httptest.NewRequest(http.MethodGet, "/protected", nil)
        w := httptest.NewRecorder()

        handler.ServeHTTP(w, req)

        assert.Equal(t, http.StatusUnauthorized, w.Code)
    })
}
```

### Testing HTTP Clients with Test Server

```go
func TestAPIClient(t *testing.T) {
    // Create test server
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        switch r.URL.Path {
        case "/users/1":
            w.Header().Set("Content-Type", "application/json")
            json.NewEncoder(w).Encode(User{ID: 1, Name: "Test"})
        case "/users/999":
            w.WriteHeader(http.StatusNotFound)
            json.NewEncoder(w).Encode(map[string]string{"error": "not found"})
        default:
            w.WriteHeader(http.StatusNotFound)
        }
    }))
    defer server.Close()

    // Create client with test server URL
    client := NewAPIClient(server.URL)

    t.Run("get existing user", func(t *testing.T) {
        user, err := client.GetUser(1)
        assert.NoError(t, err)
        assert.Equal(t, "Test", user.Name)
    })

    t.Run("get non-existing user", func(t *testing.T) {
        _, err := client.GetUser(999)
        assert.Error(t, err)
        assert.Contains(t, err.Error(), "not found")
    })
}
```

## Integration Tests with testcontainers-go

### PostgreSQL Integration Test

```go
//go:build integration

package repository

import (
    "context"
    "testing"

    "github.com/jackc/pgx/v5/pgxpool"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/modules/postgres"
    "github.com/testcontainers/testcontainers-go/wait"
)

func TestUserRepository_Integration(t *testing.T) {
    ctx := context.Background()

    // Start PostgreSQL container
    container, err := postgres.Run(ctx,
        "postgres:16-alpine",
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("test"),
        postgres.WithPassword("test"),
        testcontainers.WithWaitStrategy(
            wait.ForLog("database system is ready to accept connections").
                WithOccurrence(2),
        ),
    )
    require.NoError(t, err)
    defer container.Terminate(ctx)

    // Get connection string
    connStr, err := container.ConnectionString(ctx, "sslmode=disable")
    require.NoError(t, err)

    // Connect to database
    pool, err := pgxpool.New(ctx, connStr)
    require.NoError(t, err)
    defer pool.Close()

    // Run migrations
    _, err = pool.Exec(ctx, `
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    `)
    require.NoError(t, err)

    // Create repository
    repo := NewUserRepository(pool)

    t.Run("Create", func(t *testing.T) {
        user, err := repo.Create(ctx, User{
            Name:  "Test User",
            Email: "test@example.com",
        })

        assert.NoError(t, err)
        assert.NotZero(t, user.ID)
        assert.Equal(t, "Test User", user.Name)
    })

    t.Run("FindByEmail", func(t *testing.T) {
        user, err := repo.FindByEmail(ctx, "test@example.com")

        assert.NoError(t, err)
        assert.Equal(t, "Test User", user.Name)
    })

    t.Run("FindByEmail not found", func(t *testing.T) {
        _, err := repo.FindByEmail(ctx, "nonexistent@example.com")

        assert.Error(t, err)
    })
}
```

### Redis Integration Test

```go
//go:build integration

package cache

import (
    "context"
    "testing"
    "time"

    "github.com/redis/go-redis/v9"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/modules/redis"
)

func TestCache_Integration(t *testing.T) {
    ctx := context.Background()

    container, err := redis.Run(ctx, "redis:7-alpine")
    require.NoError(t, err)
    defer container.Terminate(ctx)

    endpoint, err := container.Endpoint(ctx, "")
    require.NoError(t, err)

    client := redis.NewClient(&redis.Options{
        Addr: endpoint,
    })
    defer client.Close()

    cache := NewCache(client)

    t.Run("Set and Get", func(t *testing.T) {
        err := cache.Set(ctx, "key1", "value1", time.Minute)
        assert.NoError(t, err)

        value, err := cache.Get(ctx, "key1")
        assert.NoError(t, err)
        assert.Equal(t, "value1", value)
    })

    t.Run("Get non-existing key", func(t *testing.T) {
        _, err := cache.Get(ctx, "nonexistent")
        assert.Error(t, err)
    })

    t.Run("TTL expiration", func(t *testing.T) {
        err := cache.Set(ctx, "shortlived", "value", 100*time.Millisecond)
        assert.NoError(t, err)

        time.Sleep(150 * time.Millisecond)

        _, err = cache.Get(ctx, "shortlived")
        assert.Error(t, err)
    })
}
```

## Benchmarks

### Basic Benchmark

```go
package algorithm

import "testing"

func BenchmarkFibonacci(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Fibonacci(20)
    }
}

// Go 1.24+ style with b.Loop()
func BenchmarkFibonacciLoop(b *testing.B) {
    for b.Loop() {
        Fibonacci(20)
    }
}

func BenchmarkFibonacci_WithSetup(b *testing.B) {
    // Setup code (not measured)
    input := prepareInput()

    b.ResetTimer() // Reset timer after setup

    for i := 0; i < b.N; i++ {
        ProcessInput(input)
    }
}
```

### Benchmark with Sub-benchmarks

```go
func BenchmarkSort(b *testing.B) {
    sizes := []int{100, 1000, 10000, 100000}

    for _, size := range sizes {
        b.Run(fmt.Sprintf("size-%d", size), func(b *testing.B) {
            data := generateRandomSlice(size)
            b.ResetTimer()

            for i := 0; i < b.N; i++ {
                dataCopy := make([]int, len(data))
                copy(dataCopy, data)
                sort.Ints(dataCopy)
            }
        })
    }
}
```

### Parallel Benchmark

```go
func BenchmarkConcurrentMap(b *testing.B) {
    m := NewConcurrentMap()

    // Populate map
    for i := 0; i < 1000; i++ {
        m.Set(fmt.Sprintf("key-%d", i), i)
    }

    b.ResetTimer()
    b.RunParallel(func(pb *testing.PB) {
        i := 0
        for pb.Next() {
            key := fmt.Sprintf("key-%d", i%1000)
            m.Get(key)
            i++
        }
    })
}
```

### Memory Allocation Benchmark

```go
func BenchmarkStringConcat(b *testing.B) {
    b.Run("plus operator", func(b *testing.B) {
        for i := 0; i < b.N; i++ {
            s := ""
            for j := 0; j < 100; j++ {
                s += "x"
            }
        }
    })

    b.Run("strings.Builder", func(b *testing.B) {
        for i := 0; i < b.N; i++ {
            var sb strings.Builder
            for j := 0; j < 100; j++ {
                sb.WriteString("x")
            }
            _ = sb.String()
        }
    })
}

// Run with: go test -bench=. -benchmem
// Output shows B/op (bytes per operation) and allocs/op
```

## Fuzzing

### Basic Fuzz Test

```go
package parser

import "testing"

func FuzzParseJSON(f *testing.F) {
    // Seed corpus with valid inputs
    f.Add([]byte(`{"name": "test"}`))
    f.Add([]byte(`{"id": 123, "active": true}`))
    f.Add([]byte(`[]`))
    f.Add([]byte(`null`))
    f.Add([]byte(`"string"`))

    // Add edge cases
    f.Add([]byte(`{}`))
    f.Add([]byte(``))
    f.Add([]byte(`{{{`))

    f.Fuzz(func(t *testing.T, data []byte) {
        // ParseJSON should not panic on any input
        result, err := ParseJSON(data)

        // If parsing succeeds, result should be valid
        if err == nil && result == nil {
            t.Error("ParseJSON returned nil result without error")
        }
    })
}
```

### Fuzz Test with Multiple Inputs

```go
func FuzzURLParser(f *testing.F) {
    f.Add("https", "example.com", "/path", "query=value")
    f.Add("http", "localhost", "/", "")
    f.Add("", "", "", "")

    f.Fuzz(func(t *testing.T, scheme, host, path, query string) {
        url := fmt.Sprintf("%s://%s%s?%s", scheme, host, path, query)

        parsed, err := ParseURL(url)
        if err != nil {
            return // Invalid URLs are expected
        }

        // Verify round-trip
        if parsed.String() != url {
            // Allow normalized differences
            reparsed, err := ParseURL(parsed.String())
            if err != nil {
                t.Errorf("failed to reparse: %v", err)
            }
            if reparsed.Host != parsed.Host {
                t.Errorf("host mismatch: %s vs %s", reparsed.Host, parsed.Host)
            }
        }
    })
}
```

## Test Helpers

### Custom Assertions

```go
package testutil

import (
    "testing"
    "time"
)

// AssertNoError fails the test if err is not nil
func AssertNoError(t *testing.T, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}

// AssertError fails the test if err is nil
func AssertError(t *testing.T, err error) {
    t.Helper()
    if err == nil {
        t.Fatal("expected error, got nil")
    }
}

// AssertEqual fails the test if got != want
func AssertEqual[T comparable](t *testing.T, got, want T) {
    t.Helper()
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}

// AssertEventually retries assertion until timeout
func AssertEventually(t *testing.T, condition func() bool, timeout time.Duration) {
    t.Helper()
    deadline := time.Now().Add(timeout)
    for time.Now().Before(deadline) {
        if condition() {
            return
        }
        time.Sleep(10 * time.Millisecond)
    }
    t.Fatal("condition not met within timeout")
}
```

### Test Fixtures

```go
package testutil

import (
    "os"
    "path/filepath"
    "testing"
)

// LoadFixture reads a file from testdata directory
func LoadFixture(t *testing.T, name string) []byte {
    t.Helper()
    path := filepath.Join("testdata", name)
    data, err := os.ReadFile(path)
    if err != nil {
        t.Fatalf("failed to load fixture %s: %v", name, err)
    }
    return data
}

// TempDir creates a temporary directory for the test
func TempDir(t *testing.T) string {
    t.Helper()
    dir, err := os.MkdirTemp("", "test-*")
    if err != nil {
        t.Fatalf("failed to create temp dir: %v", err)
    }
    t.Cleanup(func() {
        os.RemoveAll(dir)
    })
    return dir
}
```

## Setup and Teardown

### TestMain for Global Setup

```go
package database

import (
    "os"
    "testing"
)

var testDB *Database

func TestMain(m *testing.M) {
    // Global setup
    var err error
    testDB, err = SetupTestDatabase()
    if err != nil {
        panic(err)
    }

    // Run all tests
    code := m.Run()

    // Global teardown
    testDB.Close()

    os.Exit(code)
}
```

### Cleanup with t.Cleanup

```go
func TestWithCleanup(t *testing.T) {
    // Create resource
    file, err := os.CreateTemp("", "test-*")
    if err != nil {
        t.Fatal(err)
    }

    // Register cleanup (runs after test, even on failure)
    t.Cleanup(func() {
        os.Remove(file.Name())
    })

    // Test code...
}
```
