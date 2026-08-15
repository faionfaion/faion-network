// purpose: typed AppError package with Error()/Unwrap()/Wrap/IsCode — backs r-apperror-struct, r-constructors-not-mutable-globals and r-preserve-status-on-rewrap.
// consumes: nothing external; drop into internal/apperror/ (or pkg/apperror/).
// produces: AppError{Code,Message,HTTPStatus,Err} + immutable sentinels + fresh-instance constructors.
// depends-on: stdlib errors, fmt, net/http only.
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

// Sentinels are IMMUTABLE errors.New values, never *AppError pointers.
// An exported *AppError var is shared mutable state: one handler assigning
// .Message changes it for every subsequent request (r-constructors-not-mutable-globals).
var (
	ErrNotFound     = errors.New("resource not found")
	ErrUnauthorized = errors.New("authentication required")
	ErrValidation   = errors.New("invalid input")
	ErrConflict     = errors.New("resource conflict")
)

// Factory constructors — always return a fresh instance.

func NewNotFound(resource string) *AppError {
	return &AppError{
		Code: "NOT_FOUND", Message: fmt.Sprintf("%s not found", resource),
		HTTPStatus: http.StatusNotFound, Err: ErrNotFound,
	}
}

func NewUnauthorized(msg string) *AppError {
	return &AppError{
		Code: "UNAUTHORIZED", Message: msg,
		HTTPStatus: http.StatusUnauthorized, Err: ErrUnauthorized,
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

// Wrap adds context. It PRESERVES the inner *AppError's Code and HTTPStatus
// when one exists in the chain — a 404 must not become a 500 on rewrap
// (r-preserve-status-on-rewrap). Only an unrecognised error becomes a 500.
func Wrap(err error, message string) *AppError {
	var inner *AppError
	if errors.As(err, &inner) {
		return &AppError{
			Code: inner.Code, Message: message + ": " + inner.Message,
			HTTPStatus: inner.HTTPStatus, Err: err,
		}
	}
	return &AppError{
		Code: "INTERNAL_ERROR", Message: message,
		HTTPStatus: http.StatusInternalServerError, Err: err,
	}
}

// WrapWithStatus is the explicit override for the rare case where the caller
// genuinely needs to change the status rather than inherit it.
func WrapWithStatus(err error, message string, status int) *AppError {
	out := Wrap(err, message)
	out.HTTPStatus = status
	return out
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
