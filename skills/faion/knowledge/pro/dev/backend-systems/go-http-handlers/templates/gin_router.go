// purpose: Legacy template for the go-http-handlers methodology.
// consumes: inputs declared in go-http-handlers/AGENTS.md prerequisites.
// produces: working code/config aligned with content/01-core-rules.xml.
// depends-on: content/02-output-contract.xml schema for output shape.
// token-budget-impact: ~600 tokens when loaded as reference.
// internal/router/router.go
// Gin router setup with middleware stack and user CRUD route group.
package router

import (
	"github.com/gin-gonic/gin"

	"project/internal/handler"
	"project/internal/middleware"
)

// New returns a configured Gin engine.
// Middleware order: Recovery (outermost) → RequestID → Logger → Auth (per group).
func New(users *handler.UserHandler) *gin.Engine {
	r := gin.New()

	// Global middleware — order is critical.
	r.Use(middleware.Recovery()) // outermost: catches panics before logger
	r.Use(middleware.RequestID())
	r.Use(middleware.Logger())

	// Health check (no auth).
	r.GET("/health", func(c *gin.Context) { c.String(200, "OK") })

	// Protected API group.
	v1 := r.Group("/api/v1")
	v1.Use(middleware.Auth())
	{
		u := v1.Group("/users")
		u.GET("", users.List)
		u.GET("/:id", users.Get)
		u.POST("", users.Create)
		u.PUT("/:id", users.Update)
		u.DELETE("/:id", users.Delete)
	}

	return r
}
