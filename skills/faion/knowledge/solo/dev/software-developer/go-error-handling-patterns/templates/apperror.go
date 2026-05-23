// purpose: Sentinel error declarations + helper constructors
// consumes: See content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1000 tokens when loaded as context
// pkg/apperror/errors.go — Centralized error taxonomy for a Go service
// All sentinel errors live here. Repositories wrap low-level errors into these.
// Handlers map these to HTTP/gRPC codes at the transport edge only.

package apperror

import (
	"errors"
	"fmt"
	"net/http"
)

// Sentinel errors — checked with errors.Is throughout the codebase.
var (
	ErrNotFound     = errors.New("resource not found")
	ErrUnauthorized = errors.New("unauthorized")
	ErrForbidden    = errors.New("forbidden")
	ErrConflict     = errors.New("resource conflict")
	ErrValidation   = errors.New("validation failed")
	ErrInternal     = errors.New("internal error")
)

// AppError carries structured context for HTTP/gRPC edge mapping.
type AppError struct {
	Code    string            `json:"code"`
	Message string            `json:"message"`
	Status  int               `json:"-"`
	Details map[string]string `json:"details,omitempty"`
	Err     error             `json:"-"`
}

func (e *AppError) Error() string {
	if e.Err != nil {
		return fmt.Sprintf("%s: %v", e.Message, e.Err)
	}
	return e.Message
}

func (e *AppError) Unwrap() error { return e.Err }

// Constructor functions — use at repository/service layer for typed context.

func NotFound(resource, id string) *AppError {
	return &AppError{
		Code:    "NOT_FOUND",
		Message: fmt.Sprintf("%s %s not found", resource, id),
		Status:  http.StatusNotFound,
		Err:     ErrNotFound,
	}
}

func Validation(details map[string]string) *AppError {
	return &AppError{
		Code:    "VALIDATION_ERROR",
		Message: "validation failed",
		Status:  http.StatusBadRequest,
		Details: details,
		Err:     ErrValidation,
	}
}

func Unauthorized(message string) *AppError {
	return &AppError{
		Code:    "UNAUTHORIZED",
		Message: message,
		Status:  http.StatusUnauthorized,
		Err:     ErrUnauthorized,
	}
}

func Internal(err error) *AppError {
	return &AppError{
		Code:    "INTERNAL_ERROR",
		Message: "internal server error",
		Status:  http.StatusInternalServerError,
		Err:     err,
	}
}

// AsAppError extracts *AppError from an error chain.
func AsAppError(err error) (*AppError, bool) {
	var appErr *AppError
	return appErr, errors.As(err, &appErr)
}
