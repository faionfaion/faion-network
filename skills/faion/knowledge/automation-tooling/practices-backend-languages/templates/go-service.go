// purpose: Go service skeleton with consumer-side interface + worker pool
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for practices-backend-languages
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

package handlers

import (
    "context"
    "fmt"
)

// Consumer-side interface (declared where it is used)
type OrderRepo interface {
    Find(ctx context.Context, id string) (*Order, error)
    Save(ctx context.Context, o *Order) error
}

type OrderHandler struct {
    repo OrderRepo
}

func NewOrderHandler(repo OrderRepo) *OrderHandler {
    return &OrderHandler{repo: repo}
}

func (h *OrderHandler) Charge(ctx context.Context, id string) error {
    o, err := h.repo.Find(ctx, id)
    if err != nil {
        return fmt.Errorf("charge order %s: %w", id, err)
    }
    o.Status = "charged"
    if err := h.repo.Save(ctx, o); err != nil {
        return fmt.Errorf("save order %s: %w", id, err)
    }
    return nil
}
