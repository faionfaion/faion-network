// internal/apperror/apperror.go — typed application errors with HTTP mapping
package apperror

import (
	"fmt"
	"net/http"
)

// AppError carries a machine-readable code, human message, HTTP status, and optional cause.
type AppError struct {
	Code       string `json:"code"`
	Message    string `json:"message"`
	HTTPStatus int    `json:"-"`
	Err        error  `json:"-"`
}

func (e *AppError) Error() string {
	if e.Err != nil {
		return fmt.Sprintf("%s: %v", e.Message, e.Err)
	}
	return e.Message
}

// Unwrap enables errors.Is / errors.As traversal.
func (e *AppError) Unwrap() error { return e.Err }

// Sentinel errors — use errors.Is to check.
var (
	ErrNotFound = &AppError{
		Code: "NOT_FOUND", Message: "Resource not found", HTTPStatus: http.StatusNotFound,
	}
	ErrUnauthorized = &AppError{
		Code: "UNAUTHORIZED", Message: "Authentication required", HTTPStatus: http.StatusUnauthorized,
	}
	ErrBadRequest = &AppError{
		Code: "BAD_REQUEST", Message: "Invalid request", HTTPStatus: http.StatusBadRequest,
	}
)

// NewNotFound creates a dynamic not-found error with resource name.
func NewNotFound(resource string) *AppError {
	return &AppError{
		Code:       "NOT_FOUND",
		Message:    fmt.Sprintf("%s not found", resource),
		HTTPStatus: http.StatusNotFound,
	}
}

// Wrap wraps a cause error with an internal error message.
func Wrap(err error, message string) *AppError {
	return &AppError{
		Code:       "INTERNAL_ERROR",
		Message:    message,
		HTTPStatus: http.StatusInternalServerError,
		Err:        err,
	}
}
