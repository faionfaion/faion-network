// purpose: HTTP middleware translating returned-error AppError into JSON via errors.As.
// consumes: handlers of type `func(w,r) error`; AppError from pkg/apperror.
// produces: JSON response with Content-Type application/json (or problem+json if integrated with error-handling methodology).
// depends-on: pkg/apperror, encoding/json, net/http.
// token-budget-impact: ~70 lines; loaded once at boot.
// Package httpx provides HTTP handler wrappers including error translation middleware.
// Handler is a func(ResponseWriter, *Request) error variant of http.HandlerFunc.
// Wrap converts it to a standard HandlerFunc and translates *AppError to JSON responses.
package httpx

import (
	"encoding/json"
	"errors"
	"log/slog"
	"net/http"

	"yourmod/pkg/apperror"
)

type errBody struct {
	Code    string `json:"code"`
	Message string `json:"message"`
	TraceID string `json:"trace_id,omitempty"`
}

// Handler is like http.HandlerFunc but returns an error.
type Handler func(http.ResponseWriter, *http.Request) error

// Wrap converts a Handler to http.HandlerFunc with error translation.
func Wrap(h Handler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		err := h(w, r)
		if err == nil {
			return
		}
		var appErr *apperror.AppError
		if !errors.As(err, &appErr) {
			appErr = apperror.Wrap(err, "internal error")
		}
		if appErr.HTTPStatus >= 500 {
			slog.ErrorContext(r.Context(), "http error",
				"code", appErr.Code, "status", appErr.HTTPStatus, "err", err)
		} else {
			slog.InfoContext(r.Context(), "http client error",
				"code", appErr.Code, "status", appErr.HTTPStatus)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(appErr.HTTPStatus)
		if encErr := json.NewEncoder(w).Encode(errBody{
			Code:    appErr.Code,
			Message: appErr.Message,
			TraceID: TraceIDFromCtx(r.Context()),
		}); encErr != nil {
			slog.ErrorContext(r.Context(), "failed to encode error response", "err", encErr)
		}
	}
}

// TraceIDFromCtx extracts the trace ID from context — implement per project.
func TraceIDFromCtx(r interface{ Value(any) any }) string {
	if id, ok := r.Value("trace_id").(string); ok {
		return id
	}
	return ""
}
