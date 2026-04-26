// internal/handler/<resource>.go
// Template: inject a service interface, handle one GET endpoint.
package handler

import (
	"context"
	"net/http"

	"github.com/gin-gonic/gin"
)

// <Resource>Service is the minimal interface this handler needs.
// Define it here (consumer side), not in the service package.
type <Resource>Service interface {
	GetByID(ctx context.Context, id string) (*<Model>, error)
}

type <Resource>Handler struct {
	svc <Resource>Service
}

func New<Resource>Handler(svc <Resource>Service) *<Resource>Handler {
	return &<Resource>Handler{svc: svc}
}

// Get<Resource> handles GET /<resources>/:id
func (h *<Resource>Handler) Get<Resource>(c *gin.Context) {
	id := c.Param("id")
	item, err := h.svc.GetByID(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "<Resource> not found"})
		return
	}
	c.JSON(http.StatusOK, item)
}
