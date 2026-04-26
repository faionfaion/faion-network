// internal/api/server.go
// stdlib 1.22 muxer pattern: App struct, routes(), writeJSON, writeProblem.
// No framework dependency required for basic CRUD.
package api

import (
	"encoding/json"
	"log/slog"
	"net/http"
)

// App holds injected dependencies. Never use package-level globals.
type App struct {
	users  UserService
	logger *slog.Logger
}

func NewApp(users UserService, logger *slog.Logger) *App {
	return &App{users: users, logger: logger}
}

// Routes returns the HTTP handler with all routes registered.
// Middleware is applied via function wrapping (outermost = Recovery).
func (a *App) Routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /api/v1/users", a.listUsers)
	mux.HandleFunc("GET /api/v1/users/{id}", a.getUser)
	mux.HandleFunc("POST /api/v1/users", a.createUser)
	mux.HandleFunc("DELETE /api/v1/users/{id}", a.deleteUser)
	mux.HandleFunc("GET /health", func(w http.ResponseWriter, _ *http.Request) {
		w.Write([]byte("OK")) //nolint:errcheck
	})
	return withRecovery(withRequestID(withLogger(a.logger, mux)))
}

func (a *App) getUser(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	u, err := a.users.Get(r.Context(), id)
	if err != nil {
		writeProblem(w, r, a.logger, err)
		return
	}
	writeJSON(w, http.StatusOK, u)
}

func (a *App) listUsers(w http.ResponseWriter, r *http.Request) {
	users, err := a.users.List(r.Context())
	if err != nil {
		writeProblem(w, r, a.logger, err)
		return
	}
	writeJSON(w, http.StatusOK, users)
}

func (a *App) createUser(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()
	var req CreateUserRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeProblem(w, r, a.logger, err)
		return
	}
	u, err := a.users.Create(r.Context(), req)
	if err != nil {
		writeProblem(w, r, a.logger, err)
		return
	}
	writeJSON(w, http.StatusCreated, u)
}

func (a *App) deleteUser(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	if err := a.users.Delete(r.Context(), id); err != nil {
		writeProblem(w, r, a.logger, err)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func writeJSON(w http.ResponseWriter, code int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	_ = json.NewEncoder(w).Encode(v)
}

// writeProblem maps err to RFC 7807 — see error-handling/ methodology.
func writeProblem(w http.ResponseWriter, r *http.Request, logger *slog.Logger, err error) {
	logger.ErrorContext(r.Context(), "handler error", "err", err, "path", r.URL.Path)
	// TODO: map err type to ProblemDetail status + code using apperror.IsCode
	w.Header().Set("Content-Type", "application/problem+json")
	w.WriteHeader(http.StatusInternalServerError)
	_ = json.NewEncoder(w).Encode(map[string]any{
		"type":   "https://api.example.com/errors/v1/internal-error",
		"title":  "Internal Server Error",
		"status": 500,
	})
}
