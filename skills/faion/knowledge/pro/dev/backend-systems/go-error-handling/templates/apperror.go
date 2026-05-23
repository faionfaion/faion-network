// purpose: Legacy template for the go-error-handling methodology.
// consumes: inputs declared in go-error-handling/AGENTS.md prerequisites.
// produces: working code/config aligned with content/01-core-rules.xml.
// depends-on: content/02-output-contract.xml schema for output shape.
// token-budget-impact: ~600 tokens when loaded as reference.
// internal/apperror/apperror.go
// Project-wide typed error subsystem for Go HTTP services.
package apperror

import (
	"errors"
	"fmt"
	"net/http"
)

// AppError carries a machine-readable Code, a client-safe Message,
// an HTTP status, and an optional wrapped error chain.
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

func (e *AppError) Unwrap() error { return e.Err }

// Sentinel variables — use for errors.Is comparison; never mutate.
var (
	ErrNotFound = &AppError{
		Code: "NOT_FOUND", Message: "Resource not found",
		HTTPStatus: http.StatusNotFound,
	}
	ErrUnauthorized = &AppError{
		Code: "UNAUTHORIZED", Message: "Authentication required",
		HTTPStatus: http.StatusUnauthorized,
	}
	ErrValidation = &AppError{
		Code: "VALIDATION_ERROR", Message: "Invalid input",
		HTTPStatus: http.StatusBadRequest,
	}
)

// Factory constructors — always return a fresh instance.

func NewNotFound(resource string) *AppError {
	return &AppError{
		Code: "NOT_FOUND", Message: fmt.Sprintf("%s not found", resource),
		HTTPStatus: http.StatusNotFound,
	}
}

func AsValidation(msg string) *AppError {
	return &AppError{
		Code: "VALIDATION_ERROR", Message: msg,
		HTTPStatus: http.StatusBadRequest,
	}
}

func AsConflict(msg string) *AppError {
	return &AppError{
		Code: "CONFLICT", Message: msg,
		HTTPStatus: http.StatusConflict,
	}
}

// Wrap is for UNEXPECTED internal errors only (produces 500).
// Do not use for domain errors that have a typed constructor above.
func Wrap(err error, message string) *AppError {
	return &AppError{
		Code: "INTERNAL_ERROR", Message: message,
		HTTPStatus: http.StatusInternalServerError, Err: err,
	}
}

// Code predicate — classification via errors.As, not pointer identity.
type Code string

const (
	CodeNotFound     Code = "NOT_FOUND"
	CodeUnauthorized Code = "UNAUTHORIZED"
	CodeValidation   Code = "VALIDATION_ERROR"
	CodeConflict     Code = "CONFLICT"
)

// IsCode returns true when err (or any error in its chain) is an *AppError
// with the given code. Works after fmt.Errorf("%w", ...) wrapping.
func IsCode(err error, code Code) bool {
	var ae *AppError
	if !errors.As(err, &ae) {
		return false
	}
	return Code(ae.Code) == code
}
