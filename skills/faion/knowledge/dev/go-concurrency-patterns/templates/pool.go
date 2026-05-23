// purpose: Bounded worker pool with context cancellation + errgroup coordination
// consumes: See content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1000 tokens when loaded as context
// pkg/worker/pool.go
// Leak-safe bounded worker pool with context cancellation and error collection.
// Usage:
//   p := NewPool(ctx, 8, 100)
//   p.Submit(func(ctx context.Context) error { return doWork(ctx) })
//   p.Stop()
//   for err := range p.Errors() { log.Print(err) }
package worker

import (
	"context"
	"sync"
)

// Job is a unit of work. Must respect ctx cancellation.
type Job func(ctx context.Context) error

// Pool is a bounded goroutine pool with error collection.
type Pool struct {
	jobs   chan Job          // owned and closed by Stop()
	errs   chan error        // closed by Stop() after all workers finish
	wg     sync.WaitGroup
	cancel context.CancelFunc
}

// NewPool starts `workers` goroutines reading from a channel of capacity `buffer`.
func NewPool(ctx context.Context, workers, buffer int) *Pool {
	ctx, cancel := context.WithCancel(ctx)
	p := &Pool{
		jobs:   make(chan Job, buffer),
		errs:   make(chan error, buffer),
		cancel: cancel,
	}
	for i := 0; i < workers; i++ {
		p.wg.Add(1)
		go func() {
			defer p.wg.Done()
			defer func() { _ = recover() }() // prevent single-job panic from crashing pool
			for {
				select {
				case <-ctx.Done():
					return
				case job, ok := <-p.jobs:
					if !ok {
						return
					}
					if err := job(ctx); err != nil {
						select {
						case p.errs <- err:
						default: // drop if error buffer full; log if needed
						}
					}
				}
			}
		}()
	}
	return p
}

// Submit enqueues a job. Blocks if the buffer is full.
func (p *Pool) Submit(j Job) { p.jobs <- j }

// Errors returns the read-only error channel. Drain after Stop().
func (p *Pool) Errors() <-chan error { return p.errs }

// Stop closes the job channel, waits for all workers to finish, then closes the error channel.
func (p *Pool) Stop() {
	close(p.jobs)
	p.wg.Wait()
	close(p.errs)
	p.cancel()
}
