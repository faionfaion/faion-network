# M-GO-004: Go Error Handling

## Metadata
- **Category:** Development/Backend/Go
- **Difficulty:** Intermediate
- **Tags:** #dev, #go, #errors, #backend, #methodology
- **Agent:** faion-code-agent

---

## Problem

Go error handling feels verbose and repetitive. Errors lose context as they propagate up the call stack. Stack traces are missing. You need patterns that make errors informative and handling consistent.

## Promise

After this methodology, you will handle errors in Go that are easy to debug, well-structured, and maintain context. Your APIs will return meaningful error messages.

## Overview

Go 1.13+ introduced error wrapping with `errors.Is()` and `errors.As()`. This methodology covers modern patterns for error handling, custom error types, and API error responses.

---

## Framework

### Step 1: Error Wrapping

```go
import (
    "errors"
    "fmt"
)

// Wrap errors with context
func GetUser(id string) (*User, error) {
    user, err := db.FindByID(id)
    if err != nil {
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}

// Check wrapped errors
func HandleRequest(id string) {
    user, err := GetUser(id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            // Handle not found
        }
        if errors.Is(err, context.DeadlineExceeded) {
            // Handle timeout
        }
    }
}
```

### Step 2: Sentinel Errors

```go
// Define package-level error values
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrForbidden    = errors.New("forbidden")
    ErrConflict     = errors.New("conflict")
    ErrValidation   = errors.New("validation error")
)

// Use in code
func GetUser(id string) (*User, error) {
    user, err := repo.FindByID(id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, fmt.Errorf("user %s: %w", id, ErrNotFound)
        }
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}

// Check in handler
func (h *Handler) GetUser(c *gin.Context) {
    user, err := h.service.GetUser(c.Param("id"))
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            c.JSON(404, gin.H{"error": "user not found"})
            return
        }
        c.JSON(500, gin.H{"error": "internal error"})
        return
    }
    c.JSON(200, user)
}
```

### Step 3: Custom Error Types

```go
// Custom error with additional context
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

// Error with multiple fields
type ValidationErrors struct {
    Errors []ValidationError
}

func (e *ValidationErrors) Error() string {
    var msgs []string
    for _, err := range e.Errors {
        msgs = append(msgs, err.Error())
    }
    return strings.Join(msgs, "; ")
}

// Usage
func ValidateUser(input CreateUserInput) error {
    var errs ValidationErrors

    if input.Email == "" {
        errs.Errors = append(errs.Errors, ValidationError{
            Field:   "email",
            Message: "is required",
        })
    }

    if len(input.Password) < 8 {
        errs.Errors = append(errs.Errors, ValidationError{
            Field:   "password",
            Message: "must be at least 8 characters",
        })
    }

    if len(errs.Errors) > 0 {
        return &errs
    }

    return nil
}

// Check with errors.As
func HandleError(err error) {
    var validationErr *ValidationErrors
    if errors.As(err, &validationErr) {
        // Handle validation errors
        for _, e := range validationErr.Errors {
            fmt.Printf("Field %s: %s\n", e.Field, e.Message)
        }
    }
}
```

### Step 4: API Error Response

```go
// Structured API error
type APIError struct {
    Code       string            `json:"code"`
    Message    string            `json:"message"`
    Details    map[string]string `json:"details,omitempty"`
    StatusCode int               `json:"-"`
}

func (e *APIError) Error() string {
    return e.Message
}

// Error constructors
func NewNotFoundError(resource, id string) *APIError {
    return &APIError{
        Code:       "NOT_FOUND",
        Message:    fmt.Sprintf("%s with id %s not found", resource, id),
        StatusCode: 404,
    }
}

func NewValidationError(details map[string]string) *APIError {
    return &APIError{
        Code:       "VALIDATION_ERROR",
        Message:    "validation failed",
        Details:    details,
        StatusCode: 400,
    }
}

func NewInternalError(err error) *APIError {
    // Log the actual error
    log.Printf("internal error: %v", err)

    return &APIError{
        Code:       "INTERNAL_ERROR",
        Message:    "an internal error occurred",
        StatusCode: 500,
    }
}

// Error handler middleware (Gin)
func ErrorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()

        if len(c.Errors) > 0 {
            err := c.Errors.Last().Err

            var apiErr *APIError
            if errors.As(err, &apiErr) {
                c.JSON(apiErr.StatusCode, apiErr)
                return
            }

            // Default to internal error
            c.JSON(500, NewInternalError(err))
        }
    }
}
```

### Step 5: Error Context with Stack Traces

```bash
go get github.com/pkg/errors
```

```go
import "github.com/pkg/errors"

// Wrap with stack trace
func GetUser(id string) (*User, error) {
    user, err := repo.FindByID(id)
    if err != nil {
        return nil, errors.Wrap(err, "failed to get user")
    }
    return user, nil
}

// Print stack trace
func HandleError(err error) {
    fmt.Printf("Error: %v\n", err)
    fmt.Printf("Stack trace:\n%+v\n", err)
}
```

### Step 6: Domain Errors

```go
// domain/errors.go
package domain

type DomainError struct {
    Code    string
    Message string
    Cause   error
}

func (e *DomainError) Error() string {
    if e.Cause != nil {
        return fmt.Sprintf("%s: %v", e.Message, e.Cause)
    }
    return e.Message
}

func (e *DomainError) Unwrap() error {
    return e.Cause
}

// Domain-specific errors
var (
    ErrUserNotFound = &DomainError{
        Code:    "USER_NOT_FOUND",
        Message: "user not found",
    }

    ErrEmailAlreadyExists = &DomainError{
        Code:    "EMAIL_EXISTS",
        Message: "email already registered",
    }

    ErrInvalidCredentials = &DomainError{
        Code:    "INVALID_CREDENTIALS",
        Message: "invalid email or password",
    }
)

// Create error with cause
func NewUserNotFoundError(id string) error {
    return &DomainError{
        Code:    "USER_NOT_FOUND",
        Message: fmt.Sprintf("user %s not found", id),
    }
}
```

---

## Templates

### Error Handling Layer

```go
// internal/apperror/errors.go
package apperror

import (
    "fmt"
    "net/http"
)

type AppError struct {
    Code       string            `json:"code"`
    Message    string            `json:"message"`
    Details    map[string]string `json:"details,omitempty"`
    HTTPStatus int               `json:"-"`
    Err        error             `json:"-"`
}

func (e *AppError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("%s: %v", e.Message, e.Err)
    }
    return e.Message
}

func (e *AppError) Unwrap() error {
    return e.Err
}

// Constructors
func NotFound(resource string) *AppError {
    return &AppError{
        Code:       "NOT_FOUND",
        Message:    resource + " not found",
        HTTPStatus: http.StatusNotFound,
    }
}

func BadRequest(message string) *AppError {
    return &AppError{
        Code:       "BAD_REQUEST",
        Message:    message,
        HTTPStatus: http.StatusBadRequest,
    }
}

func Validation(details map[string]string) *AppError {
    return &AppError{
        Code:       "VALIDATION_ERROR",
        Message:    "validation failed",
        Details:    details,
        HTTPStatus: http.StatusBadRequest,
    }
}

func Internal(err error) *AppError {
    return &AppError{
        Code:       "INTERNAL_ERROR",
        Message:    "internal server error",
        HTTPStatus: http.StatusInternalServerError,
        Err:        err,
    }
}

func Unauthorized(message string) *AppError {
    return &AppError{
        Code:       "UNAUTHORIZED",
        Message:    message,
        HTTPStatus: http.StatusUnauthorized,
    }
}

func Forbidden(message string) *AppError {
    return &AppError{
        Code:       "FORBIDDEN",
        Message:    message,
        HTTPStatus: http.StatusForbidden,
    }
}
```

---

## Examples

### Complete Error Flow

```go
// Repository layer
func (r *UserRepository) FindByID(ctx context.Context, id string) (*User, error) {
    var user User
    err := r.db.QueryRowContext(ctx, "SELECT * FROM users WHERE id = $1", id).
        Scan(&user.ID, &user.Email, &user.Name)

    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, nil // Not found, no error
        }
        return nil, fmt.Errorf("query user: %w", err)
    }

    return &user, nil
}

// Service layer
func (s *UserService) GetUser(ctx context.Context, id string) (*User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, apperror.Internal(err)
    }

    if user == nil {
        return nil, apperror.NotFound("user")
    }

    return user, nil
}

// Handler layer
func (h *UserHandler) GetUser(c *gin.Context) {
    user, err := h.service.GetUser(c.Request.Context(), c.Param("id"))
    if err != nil {
        var appErr *apperror.AppError
        if errors.As(err, &appErr) {
            c.JSON(appErr.HTTPStatus, appErr)
            return
        }
        c.JSON(500, apperror.Internal(err))
        return
    }

    c.JSON(200, user)
}
```

### Must Functions

```go
// For initialization that should never fail
func MustParseURL(rawURL string) *url.URL {
    u, err := url.Parse(rawURL)
    if err != nil {
        panic(fmt.Sprintf("invalid URL %q: %v", rawURL, err))
    }
    return u
}

func MustCompileRegex(pattern string) *regexp.Regexp {
    r, err := regexp.Compile(pattern)
    if err != nil {
        panic(fmt.Sprintf("invalid regex %q: %v", pattern, err))
    }
    return r
}

// Usage (only in init or main)
var emailRegex = MustCompileRegex(`^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$`)
```

---

## Common Mistakes

1. **Ignoring errors** - Check every error return
2. **Wrapping without context** - Add useful context
3. **Logging and returning** - Do one or the other
4. **Panicking on user input** - Only panic for programmer errors
5. **Comparing error strings** - Use errors.Is or errors.As

---

## Checklist

- [ ] All errors are checked
- [ ] Errors wrapped with context
- [ ] Sentinel errors for common cases
- [ ] Custom error types where needed
- [ ] API errors have consistent structure
- [ ] Internal errors not exposed to users
- [ ] Errors logged at appropriate level
- [ ] Stack traces for debugging

---

## Next Steps

- M-GO-001: Go Project Setup
- M-GO-003: Go Testing
- M-API-007: API Error Handling

---

*Methodology M-GO-004 v1.0*
