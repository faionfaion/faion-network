# M-GO-003: Go Testing

## Metadata
- **Category:** Development/Backend/Go
- **Difficulty:** Intermediate
- **Tags:** #dev, #go, #testing, #backend, #methodology
- **Agent:** faion-test-agent

---

## Problem

Go testing can feel awkward without assertion libraries. Table-driven tests are powerful but unfamiliar. Mocking requires careful design. You need patterns that make tests readable and maintainable.

## Promise

After this methodology, you will write Go tests that are clear, comprehensive, and fast. You will use table-driven tests effectively and mock dependencies cleanly.

## Overview

Go has built-in testing with `go test`. This methodology covers patterns including table-driven tests, subtests, mocking with interfaces, and popular testing libraries.

---

## Framework

### Step 1: Basic Test Structure

**user_service_test.go:**

```go
package service_test

import (
    "testing"

    "github.com/username/project/internal/service"
)

func TestUserService_Create(t *testing.T) {
    // Arrange
    svc := service.NewUserService(mockRepo)
    input := service.CreateUserInput{
        Email: "test@example.com",
        Name:  "Test User",
    }

    // Act
    user, err := svc.Create(input)

    // Assert
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }

    if user.Email != input.Email {
        t.Errorf("got email %q, want %q", user.Email, input.Email)
    }
}
```

### Step 2: Table-Driven Tests

```go
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
            name:    "missing @",
            email:   "userexample.com",
            wantErr: true,
        },
        {
            name:    "missing domain",
            email:   "user@",
            wantErr: true,
        },
        {
            name:    "empty string",
            email:   "",
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

### Step 3: Subtests

```go
func TestUserService(t *testing.T) {
    svc := setupService(t)

    t.Run("Create", func(t *testing.T) {
        t.Run("with valid input", func(t *testing.T) {
            // Test valid creation
        })

        t.Run("with duplicate email", func(t *testing.T) {
            // Test duplicate handling
        })

        t.Run("with invalid email", func(t *testing.T) {
            // Test validation
        })
    })

    t.Run("Get", func(t *testing.T) {
        t.Run("existing user", func(t *testing.T) {
            // Test get existing
        })

        t.Run("non-existent user", func(t *testing.T) {
            // Test not found
        })
    })
}
```

### Step 4: Test Helpers

```go
// testutil/helpers.go
package testutil

import (
    "testing"
    "database/sql"
)

// Test helper for setup
func SetupTestDB(t *testing.T) *sql.DB {
    t.Helper()

    db, err := sql.Open("postgres", os.Getenv("TEST_DATABASE_URL"))
    if err != nil {
        t.Fatalf("failed to connect to test db: %v", err)
    }

    t.Cleanup(func() {
        db.Close()
    })

    return db
}

// Test helper for assertions
func AssertEqual[T comparable](t *testing.T, got, want T) {
    t.Helper()
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}

func AssertNoError(t *testing.T, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}

func AssertError(t *testing.T, err error) {
    t.Helper()
    if err == nil {
        t.Fatal("expected error, got nil")
    }
}
```

### Step 5: Mocking with Interfaces

**Define interface:**

```go
// repository/interfaces.go
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*User, error)
    FindByEmail(ctx context.Context, email string) (*User, error)
    Create(ctx context.Context, user *User) error
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id string) error
}
```

**Create mock:**

```go
// repository/mock_user_repository.go
type MockUserRepository struct {
    FindByIDFunc    func(ctx context.Context, id string) (*User, error)
    FindByEmailFunc func(ctx context.Context, email string) (*User, error)
    CreateFunc      func(ctx context.Context, user *User) error
    UpdateFunc      func(ctx context.Context, user *User) error
    DeleteFunc      func(ctx context.Context, id string) error
}

func (m *MockUserRepository) FindByID(ctx context.Context, id string) (*User, error) {
    if m.FindByIDFunc != nil {
        return m.FindByIDFunc(ctx, id)
    }
    return nil, nil
}

func (m *MockUserRepository) FindByEmail(ctx context.Context, email string) (*User, error) {
    if m.FindByEmailFunc != nil {
        return m.FindByEmailFunc(ctx, email)
    }
    return nil, nil
}

// ... other methods
```

**Use in tests:**

```go
func TestUserService_Create(t *testing.T) {
    mockRepo := &MockUserRepository{
        FindByEmailFunc: func(ctx context.Context, email string) (*User, error) {
            return nil, nil // No existing user
        },
        CreateFunc: func(ctx context.Context, user *User) error {
            user.ID = "generated-id"
            return nil
        },
    }

    svc := NewUserService(mockRepo)

    user, err := svc.Create(context.Background(), CreateUserInput{
        Email: "new@example.com",
        Name:  "New User",
    })

    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }

    if user.ID != "generated-id" {
        t.Errorf("got ID %q, want %q", user.ID, "generated-id")
    }
}
```

### Step 6: Using Testify

```bash
go get github.com/stretchr/testify
```

```go
import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "github.com/stretchr/testify/suite"
)

func TestValidateEmail(t *testing.T) {
    // Assert continues on failure
    assert.True(t, isValid("user@example.com"))
    assert.False(t, isValid("invalid"))

    // Require stops on failure
    user, err := getUser("123")
    require.NoError(t, err)
    require.NotNil(t, user)

    assert.Equal(t, "John", user.Name)
}

// Test Suite
type UserServiceTestSuite struct {
    suite.Suite
    service *UserService
    mockRepo *MockUserRepository
}

func (s *UserServiceTestSuite) SetupTest() {
    s.mockRepo = &MockUserRepository{}
    s.service = NewUserService(s.mockRepo)
}

func (s *UserServiceTestSuite) TestCreate() {
    s.mockRepo.CreateFunc = func(ctx context.Context, user *User) error {
        return nil
    }

    user, err := s.service.Create(context.Background(), input)

    s.NoError(err)
    s.NotNil(user)
}

func TestUserServiceSuite(t *testing.T) {
    suite.Run(t, new(UserServiceTestSuite))
}
```

### Step 7: HTTP Testing

```go
import (
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"
)

func TestUserHandler_Create(t *testing.T) {
    // Setup
    handler := NewUserHandler(mockService)
    router := gin.Default()
    router.POST("/users", handler.Create)

    // Create request
    body := `{"email":"test@example.com","name":"Test"}`
    req := httptest.NewRequest(http.MethodPost, "/users",
        strings.NewReader(body))
    req.Header.Set("Content-Type", "application/json")

    // Record response
    rec := httptest.NewRecorder()

    // Execute
    router.ServeHTTP(rec, req)

    // Assert
    if rec.Code != http.StatusCreated {
        t.Errorf("got status %d, want %d", rec.Code, http.StatusCreated)
    }

    var response User
    json.Unmarshal(rec.Body.Bytes(), &response)

    if response.Email != "test@example.com" {
        t.Errorf("got email %q, want %q", response.Email, "test@example.com")
    }
}
```

---

## Templates

### Test File Organization

```
service/
├── user_service.go
├── user_service_test.go
├── product_service.go
└── product_service_test.go

testutil/
├── helpers.go
├── fixtures.go
└── mocks/
    ├── user_repository.go
    └── product_repository.go
```

### Golden Files

```go
func TestRenderTemplate(t *testing.T) {
    got := RenderTemplate(data)

    golden := filepath.Join("testdata", t.Name()+".golden")

    if *update {
        os.WriteFile(golden, []byte(got), 0644)
    }

    want, _ := os.ReadFile(golden)

    if got != string(want) {
        t.Errorf("output mismatch:\n%s", diff(want, got))
    }
}
```

---

## Examples

### Testing Context Cancellation

```go
func TestService_WithTimeout(t *testing.T) {
    ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
    defer cancel()

    svc := NewSlowService()

    _, err := svc.Process(ctx)

    if !errors.Is(err, context.DeadlineExceeded) {
        t.Errorf("expected deadline exceeded, got %v", err)
    }
}
```

### Benchmarks

```go
func BenchmarkParseJSON(b *testing.B) {
    data := []byte(`{"name":"test","value":123}`)

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        ParseJSON(data)
    }
}

func BenchmarkParseJSON_Large(b *testing.B) {
    data := loadLargeJSON()

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        ParseJSON(data)
    }
}

// Run: go test -bench=. -benchmem
```

---

## Common Mistakes

1. **Not using t.Helper()** - Marks function as test helper
2. **Testing implementation** - Test behavior, not internals
3. **Shared state between tests** - Use t.Parallel() carefully
4. **Long setup code** - Extract to helpers
5. **Not testing errors** - Test error cases explicitly

---

## Checklist

- [ ] Tests follow naming convention (*_test.go)
- [ ] Table-driven tests for multiple cases
- [ ] Subtests for organization
- [ ] Interfaces for mocking
- [ ] t.Helper() in helper functions
- [ ] t.Cleanup() for teardown
- [ ] HTTP tests use httptest
- [ ] Benchmarks for performance-critical code

---

## Next Steps

- M-GO-004: Go Error Handling
- M-GO-001: Go Project Setup
- M-DO-001: CI/CD with GitHub Actions

---

*Methodology M-GO-003 v1.0*
