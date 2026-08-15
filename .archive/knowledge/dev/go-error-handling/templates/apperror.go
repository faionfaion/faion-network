// purpose: typed AppError package with Error()/Unwrap()/Wrap helpers — backs the methodology's r1/r9.
// consumes: nothing external; drop into pkg/apperror/.
// produces: AppError{Code,Message,HTTPStatus,Err} + constructors NewNotFound/NewBadRequest/etc.
// depends-on: stdlib errors + fmt only.
// token-budget-impact: ~60 lines; loaded once at boot.
// Package apperror defines a structured error type for HTTP services.
// Use constructors (NewNotFound, NewValidation, etc.); never modify package-level vars.
package apperror

import (
	"errors"
	"fmt"
	"net/http"
)

// AppError carries an API-stable code, human message, HTTP status, and optional wrapped error.
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

func NewNotFound(resource string) *AppError {
	return &AppError{
		Code:       "NOT_FOUND",
		Message:    fmt.Sprintf("%s not found", resource),
		HTTPStatus: http.StatusNotFound,
	}
}

func NewUnauthorized(msg string) *AppError {
	return &AppError{Code: "UNAUTHORIZED", Message: msg, HTTPStatus: http.StatusUnauthorized}
}

func NewValidation(msg string) *AppError {
	return &AppError{Code: "VALIDATION_ERROR", Message: msg, HTTPStatus: http.StatusBadRequest}
}

// Wrap preserves Code and HTTPStatus from an inner *AppError when present.
func Wrap(err error, msg string) *AppError {
	var inner *AppError
	if errors.As(err, &inner) {
		return &AppError{
			Code:       inner.Code,
			Message:    msg,
			HTTPStatus: inner.HTTPStatus,
			Err:        err,
		}
	}
	return &AppError{
		Code:       "INTERNAL_ERROR",
		Message:    msg,
		HTTPStatus: http.StatusInternalServerError,
		Err:        err,
	}
}
