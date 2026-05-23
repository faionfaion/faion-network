// purpose: Legacy template for the go-concurrency-patterns methodology.
// consumes: inputs declared in go-concurrency-patterns/AGENTS.md prerequisites.
// produces: working code/config aligned with content/01-core-rules.xml.
// depends-on: content/02-output-contract.xml schema for output shape.
// token-budget-impact: ~600 tokens when loaded as reference.
// internal/concurrent/process_all.go
// Bounded-parallel helper: errgroup + semaphore, fail-fast on first error.
// Requires Go 1.21+ (for range over integer), golang.org/x/sync.
package concurrent

import (
	"context"

	"golang.org/x/sync/errgroup"
	"golang.org/x/sync/semaphore"
)

// ProcessAll runs fn on each item in parallel, bounded to concurrency slots.
// Returns all results in input order, or the first non-nil error encountered.
// On error, sibling goroutines are cancelled via gctx.
func ProcessAll[T any, R any](
	ctx context.Context,
	items []T,
	concurrency int64,
	fn func(context.Context, T) (R, error),
) ([]R, error) {
	results := make([]R, len(items))
	sem := semaphore.NewWeighted(concurrency)
	g, gctx := errgroup.WithContext(ctx)

	for i, it := range items {
		i, it := i, it // capture loop variable (safe pre-Go1.22)
		if err := sem.Acquire(gctx, 1); err != nil {
			// Context cancelled before we could acquire a slot.
			return nil, err
		}
		g.Go(func() error {
			defer sem.Release(1)
			r, err := fn(gctx, it)
			if err != nil {
				return err
			}
			results[i] = r
			return nil
		})
	}

	if err := g.Wait(); err != nil {
		return nil, err
	}
	return results, nil
}
