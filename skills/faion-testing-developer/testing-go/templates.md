# Go Testing Templates

Copy-paste templates for common Go testing scenarios.

## Table-Driven Test Template

### Basic Template

```go
func TestFunctionName(t *testing.T) {
    tests := []struct {
        name    string
        input   InputType
        want    OutputType
        wantErr bool
    }{
        {
            name:    "description of test case",
            input:   InputType{},
            want:    OutputType{},
            wantErr: false,
        },
        // Add more test cases...
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := FunctionName(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("FunctionName() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("FunctionName() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

### Parallel Table-Driven Test

```go
func TestFunctionName_Parallel(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    string
        wantErr bool
    }{
        {"case 1", "input1", "output1", false},
        {"case 2", "input2", "output2", false},
        {"error case", "bad", "", true},
    }

    for _, tt := range tests {
        tt := tt // Capture range variable
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            got, err := FunctionName(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("got %v, want %v", got, tt.want)
            }
        })
    }
}
```

### With Custom Check Function

```go
func TestFunctionName_CustomCheck(t *testing.T) {
    tests := []struct {
        name  string
        input InputType
        check func(t *testing.T, result OutputType, err error)
    }{
        {
            name:  "custom validation",
            input: InputType{},
            check: func(t *testing.T, result OutputType, err error) {
                if err != nil {
                    t.Errorf("unexpected error: %v", err)
                }
                if result.Field < 0 {
                    t.Errorf("Field should be non-negative, got %d", result.Field)
                }
            },
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := FunctionName(tt.input)
            tt.check(t, result, err)
        })
    }
}
```

## Mock Templates

### Manual Mock Template

```go
// Interface to mock
type Repository interface {
    Create(item Item) (Item, error)
    FindByID(id int) (Item, error)
    Update(item Item) error
    Delete(id int) error
}

// Mock implementation
type MockRepository struct {
    CreateFunc   func(item Item) (Item, error)
    FindByIDFunc func(id int) (Item, error)
    UpdateFunc   func(item Item) error
    DeleteFunc   func(id int) error
}

func (m *MockRepository) Create(item Item) (Item, error) {
    if m.CreateFunc != nil {
        return m.CreateFunc(item)
    }
    return Item{}, nil
}

func (m *MockRepository) FindByID(id int) (Item, error) {
    if m.FindByIDFunc != nil {
        return m.FindByIDFunc(id)
    }
    return Item{}, nil
}

func (m *MockRepository) Update(item Item) error {
    if m.UpdateFunc != nil {
        return m.UpdateFunc(item)
    }
    return nil
}

func (m *MockRepository) Delete(id int) error {
    if m.DeleteFunc != nil {
        return m.DeleteFunc(id)
    }
    return nil
}
```

### testify/mock Template

```go
import (
    "github.com/stretchr/testify/mock"
)

type MockService struct {
    mock.Mock
}

func (m *MockService) GetByID(id int) (Entity, error) {
    args := m.Called(id)
    return args.Get(0).(Entity), args.Error(1)
}

func (m *MockService) Create(input CreateInput) (Entity, error) {
    args := m.Called(input)
    return args.Get(0).(Entity), args.Error(1)
}

// Usage in test
func TestHandler_GetByID(t *testing.T) {
    mockService := new(MockService)
    mockService.On("GetByID", 1).Return(Entity{ID: 1, Name: "Test"}, nil)
    mockService.On("GetByID", 999).Return(Entity{}, errors.New("not found"))

    handler := NewHandler(mockService)

    // Test code...

    mockService.AssertExpectations(t)
}
```

### Mock with Call Tracking

```go
type MockRepository struct {
    CreateFunc func(item Item) (Item, error)
    Calls      struct {
        Create []Item
    }
}

func (m *MockRepository) Create(item Item) (Item, error) {
    m.Calls.Create = append(m.Calls.Create, item)
    if m.CreateFunc != nil {
        return m.CreateFunc(item)
    }
    return item, nil
}

// Verify in test
func TestService_Create(t *testing.T) {
    mock := &MockRepository{
        CreateFunc: func(item Item) (Item, error) {
            item.ID = 1
            return item, nil
        },
    }

    service := NewService(mock)
    service.Create(Item{Name: "Test"})

    if len(mock.Calls.Create) != 1 {
        t.Errorf("Create called %d times, want 1", len(mock.Calls.Create))
    }
    if mock.Calls.Create[0].Name != "Test" {
        t.Errorf("Create called with %v, want Name=Test", mock.Calls.Create[0])
    }
}
```

## HTTP Handler Templates

### Handler Test Template

```go
import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestHandler_Method(t *testing.T) {
    tests := []struct {
        name       string
        method     string
        path       string
        body       interface{}
        wantStatus int
        wantBody   string
    }{
        {
            name:       "successful request",
            method:     http.MethodGet,
            path:       "/api/items/1",
            body:       nil,
            wantStatus: http.StatusOK,
            wantBody:   `"id":1`,
        },
        {
            name:       "not found",
            method:     http.MethodGet,
            path:       "/api/items/999",
            body:       nil,
            wantStatus: http.StatusNotFound,
            wantBody:   `"error"`,
        },
    }

    handler := setupHandler() // Setup your handler with mocks

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            var body io.Reader
            if tt.body != nil {
                b, _ := json.Marshal(tt.body)
                body = bytes.NewReader(b)
            }

            req := httptest.NewRequest(tt.method, tt.path, body)
            if tt.body != nil {
                req.Header.Set("Content-Type", "application/json")
            }
            w := httptest.NewRecorder()

            handler.ServeHTTP(w, req)

            if w.Code != tt.wantStatus {
                t.Errorf("status = %d, want %d", w.Code, tt.wantStatus)
            }
            if tt.wantBody != "" && !strings.Contains(w.Body.String(), tt.wantBody) {
                t.Errorf("body = %s, want to contain %s", w.Body.String(), tt.wantBody)
            }
        })
    }
}
```

### Test Server for HTTP Client

```go
func TestClient_Integration(t *testing.T) {
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        switch {
        case r.Method == http.MethodGet && r.URL.Path == "/users/1":
            w.Header().Set("Content-Type", "application/json")
            json.NewEncoder(w).Encode(map[string]interface{}{
                "id":   1,
                "name": "Test User",
            })
        case r.Method == http.MethodPost && r.URL.Path == "/users":
            var input map[string]interface{}
            json.NewDecoder(r.Body).Decode(&input)
            input["id"] = 2
            w.WriteHeader(http.StatusCreated)
            json.NewEncoder(w).Encode(input)
        default:
            w.WriteHeader(http.StatusNotFound)
            json.NewEncoder(w).Encode(map[string]string{"error": "not found"})
        }
    }))
    defer server.Close()

    client := NewClient(server.URL)

    t.Run("GetUser", func(t *testing.T) {
        user, err := client.GetUser(1)
        if err != nil {
            t.Fatalf("unexpected error: %v", err)
        }
        if user.Name != "Test User" {
            t.Errorf("name = %s, want Test User", user.Name)
        }
    })
}
```

### Middleware Test Template

```go
func TestMiddleware_Auth(t *testing.T) {
    tests := []struct {
        name       string
        authHeader string
        wantStatus int
    }{
        {"valid token", "Bearer valid-token", http.StatusOK},
        {"invalid token", "Bearer invalid", http.StatusUnauthorized},
        {"missing token", "", http.StatusUnauthorized},
        {"malformed header", "NotBearer token", http.StatusUnauthorized},
    }

    nextHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    })

    middleware := AuthMiddleware(nextHandler)

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest(http.MethodGet, "/protected", nil)
            if tt.authHeader != "" {
                req.Header.Set("Authorization", tt.authHeader)
            }
            w := httptest.NewRecorder()

            middleware.ServeHTTP(w, req)

            if w.Code != tt.wantStatus {
                t.Errorf("status = %d, want %d", w.Code, tt.wantStatus)
            }
        })
    }
}
```

## testify/assert Templates

### Common Assertions

```go
import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestWithTestify(t *testing.T) {
    // Equality
    assert.Equal(t, expected, actual)
    assert.NotEqual(t, expected, actual)

    // Nil checks
    assert.Nil(t, value)
    assert.NotNil(t, value)

    // Boolean
    assert.True(t, condition)
    assert.False(t, condition)

    // Error checks
    assert.NoError(t, err)
    assert.Error(t, err)
    assert.ErrorIs(t, err, expectedErr)
    assert.ErrorContains(t, err, "substring")

    // Collections
    assert.Len(t, slice, 3)
    assert.Empty(t, slice)
    assert.NotEmpty(t, slice)
    assert.Contains(t, slice, element)
    assert.ElementsMatch(t, expected, actual) // Order doesn't matter

    // Strings
    assert.Contains(t, str, "substring")
    assert.HasPrefix(t, str, "prefix")
    assert.HasSuffix(t, str, "suffix")

    // Numbers
    assert.Greater(t, a, b)
    assert.GreaterOrEqual(t, a, b)
    assert.Less(t, a, b)
    assert.InDelta(t, expected, actual, delta)

    // require - stops test on failure
    require.NoError(t, err, "setup failed")
    require.NotNil(t, obj)
}
```

## go-cmp Templates

### Basic Comparison

```go
import (
    "testing"
    "github.com/google/go-cmp/cmp"
    "github.com/google/go-cmp/cmp/cmpopts"
)

func TestWithGoCmp(t *testing.T) {
    want := Expected{}
    got := FunctionUnderTest()

    if diff := cmp.Diff(want, got); diff != "" {
        t.Errorf("mismatch (-want +got):\n%s", diff)
    }
}
```

### With Options

```go
func TestWithGoCmpOptions(t *testing.T) {
    want := Expected{}
    got := FunctionUnderTest()

    opts := []cmp.Option{
        // Ignore specific fields
        cmpopts.IgnoreFields(Type{}, "CreatedAt", "UpdatedAt"),

        // Ignore unexported fields
        cmpopts.IgnoreUnexported(Type{}),

        // Sort slices before comparison
        cmpopts.SortSlices(func(a, b Type) bool {
            return a.ID < b.ID
        }),

        // Approximate float comparison
        cmpopts.EquateApprox(0.01, 0),

        // Treat empty and nil slices as equal
        cmpopts.EquateEmpty(),
    }

    if diff := cmp.Diff(want, got, opts...); diff != "" {
        t.Errorf("mismatch (-want +got):\n%s", diff)
    }
}
```

## testcontainers-go Templates

### PostgreSQL Template

```go
//go:build integration

package repository

import (
    "context"
    "testing"

    "github.com/jackc/pgx/v5/pgxpool"
    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/modules/postgres"
    "github.com/testcontainers/testcontainers-go/wait"
)

var testDB *pgxpool.Pool

func TestMain(m *testing.M) {
    ctx := context.Background()

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
    if err != nil {
        panic(err)
    }
    defer container.Terminate(ctx)

    connStr, _ := container.ConnectionString(ctx, "sslmode=disable")
    testDB, _ = pgxpool.New(ctx, connStr)
    defer testDB.Close()

    // Run migrations
    testDB.Exec(ctx, `CREATE TABLE ...`)

    os.Exit(m.Run())
}

func TestRepository(t *testing.T) {
    repo := NewRepository(testDB)
    // Test code using testDB...
}
```

### Redis Template

```go
//go:build integration

package cache

import (
    "context"
    "os"
    "testing"

    "github.com/redis/go-redis/v9"
    "github.com/testcontainers/testcontainers-go/modules/redis"
)

var testClient *redis.Client

func TestMain(m *testing.M) {
    ctx := context.Background()

    container, err := redis.Run(ctx, "redis:7-alpine")
    if err != nil {
        panic(err)
    }
    defer container.Terminate(ctx)

    endpoint, _ := container.Endpoint(ctx, "")
    testClient = redis.NewClient(&redis.Options{Addr: endpoint})
    defer testClient.Close()

    os.Exit(m.Run())
}

func TestCache(t *testing.T) {
    cache := NewCache(testClient)
    // Test code using testClient...
}
```

### MongoDB Template

```go
//go:build integration

package repository

import (
    "context"
    "os"
    "testing"

    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
    "github.com/testcontainers/testcontainers-go/modules/mongodb"
)

var testDB *mongo.Database

func TestMain(m *testing.M) {
    ctx := context.Background()

    container, err := mongodb.Run(ctx, "mongo:7")
    if err != nil {
        panic(err)
    }
    defer container.Terminate(ctx)

    endpoint, _ := container.ConnectionString(ctx)
    client, _ := mongo.Connect(ctx, options.Client().ApplyURI(endpoint))
    defer client.Disconnect(ctx)

    testDB = client.Database("testdb")

    os.Exit(m.Run())
}
```

## Benchmark Templates

### Basic Benchmark

```go
func BenchmarkFunction(b *testing.B) {
    // Setup (not timed)
    input := prepareInput()

    b.ResetTimer() // Start timing

    for i := 0; i < b.N; i++ {
        Function(input)
    }
}

// Go 1.24+ style
func BenchmarkFunction_Loop(b *testing.B) {
    input := prepareInput()

    for b.Loop() {
        Function(input)
    }
}
```

### Benchmark with Sub-benchmarks

```go
func BenchmarkFunction_Sizes(b *testing.B) {
    sizes := []int{10, 100, 1000, 10000}

    for _, size := range sizes {
        b.Run(fmt.Sprintf("size-%d", size), func(b *testing.B) {
            input := generateInput(size)
            b.ResetTimer()

            for i := 0; i < b.N; i++ {
                Function(input)
            }
        })
    }
}
```

### Parallel Benchmark

```go
func BenchmarkConcurrent(b *testing.B) {
    resource := setupSharedResource()

    b.ResetTimer()
    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            resource.Operation()
        }
    })
}
```

### Memory Allocation Benchmark

```go
func BenchmarkAllocations(b *testing.B) {
    b.ReportAllocs() // Include in all runs, not just -benchmem

    for i := 0; i < b.N; i++ {
        _ = FunctionThatAllocates()
    }
}
```

## Fuzzing Templates

### Basic Fuzz Test

```go
func FuzzParse(f *testing.F) {
    // Add seed corpus
    f.Add([]byte("valid input"))
    f.Add([]byte(""))
    f.Add([]byte("edge case"))

    f.Fuzz(func(t *testing.T, data []byte) {
        // Should not panic
        result, err := Parse(data)

        // If no error, result should be usable
        if err == nil {
            _ = result.String()
        }
    })
}
```

### Fuzz with Multiple Inputs

```go
func FuzzFormat(f *testing.F) {
    f.Add("hello", 42, true)
    f.Add("", 0, false)
    f.Add("test", -1, true)

    f.Fuzz(func(t *testing.T, s string, n int, b bool) {
        result := Format(s, n, b)
        if len(result) == 0 && s != "" {
            t.Error("expected non-empty result for non-empty input")
        }
    })
}
```

## Test Helper Templates

### Custom Assertion Helpers

```go
package testutil

import "testing"

func AssertNoError(t *testing.T, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}

func AssertError(t *testing.T, err error, msg string) {
    t.Helper()
    if err == nil {
        t.Fatalf("expected error: %s", msg)
    }
}

func AssertEqual[T comparable](t *testing.T, got, want T) {
    t.Helper()
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}

func AssertContains(t *testing.T, haystack, needle string) {
    t.Helper()
    if !strings.Contains(haystack, needle) {
        t.Errorf("%q does not contain %q", haystack, needle)
    }
}
```

### Fixture Helpers

```go
package testutil

import (
    "os"
    "path/filepath"
    "testing"
)

func LoadFixture(t *testing.T, name string) []byte {
    t.Helper()
    path := filepath.Join("testdata", name)
    data, err := os.ReadFile(path)
    if err != nil {
        t.Fatalf("failed to read fixture %s: %v", name, err)
    }
    return data
}

func TempDir(t *testing.T) string {
    t.Helper()
    dir, err := os.MkdirTemp("", "test-*")
    if err != nil {
        t.Fatalf("failed to create temp dir: %v", err)
    }
    t.Cleanup(func() { os.RemoveAll(dir) })
    return dir
}

func TempFile(t *testing.T, content string) string {
    t.Helper()
    f, err := os.CreateTemp("", "test-*")
    if err != nil {
        t.Fatalf("failed to create temp file: %v", err)
    }
    f.WriteString(content)
    f.Close()
    t.Cleanup(func() { os.Remove(f.Name()) })
    return f.Name()
}
```

### Eventually Helper (for async tests)

```go
package testutil

import (
    "testing"
    "time"
)

func Eventually(t *testing.T, condition func() bool, timeout, interval time.Duration) {
    t.Helper()
    deadline := time.Now().Add(timeout)
    for time.Now().Before(deadline) {
        if condition() {
            return
        }
        time.Sleep(interval)
    }
    t.Fatal("condition not met within timeout")
}

// Usage:
// testutil.Eventually(t, func() bool {
//     return cache.Has("key")
// }, 5*time.Second, 100*time.Millisecond)
```

## TestMain Template

```go
package mypackage

import (
    "os"
    "testing"
)

func TestMain(m *testing.M) {
    // Global setup
    if err := setup(); err != nil {
        os.Exit(1)
    }

    // Run tests
    code := m.Run()

    // Global teardown
    teardown()

    os.Exit(code)
}

func setup() error {
    // Initialize test database, config, etc.
    return nil
}

func teardown() {
    // Clean up resources
}
```

## Build Tags for Integration Tests

```go
//go:build integration

package repository

// This file only compiles with: go test -tags=integration ./...
```

## Coverage Report Generation

```bash
# Generate coverage profile
go test -coverprofile=coverage.out ./...

# View as HTML
go tool cover -html=coverage.out -o coverage.html

# View coverage by function
go tool cover -func=coverage.out
```
