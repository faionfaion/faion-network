// purpose: Legacy template for the go-concurrency-patterns methodology.
// consumes: inputs declared in go-concurrency-patterns/AGENTS.md prerequisites.
// produces: working code/config aligned with content/01-core-rules.xml.
// depends-on: content/02-output-contract.xml schema for output shape.
// token-budget-impact: ~600 tokens when loaded as reference.
// internal/worker/pool.go
// Generic worker pool: bounded parallelism, context cancellation, panic recovery.
package worker

import (
	"context"
	"log/slog"
	"sync"
)

// Job is a unit of work. Implementations must respect ctx cancellation.
type Job func(ctx context.Context) error

// Pool manages a fixed number of goroutines consuming from a buffered job queue.
type Pool struct {
	workers int
	jobs    chan Job
	wg      sync.WaitGroup
	logger  *slog.Logger
}

// New creates a Pool. buffer = job queue depth (size to upstream burst).
func New(workers, buffer int, logger *slog.Logger) *Pool {
	return &Pool{
		workers: workers,
		jobs:    make(chan Job, buffer),
		logger:  logger,
	}
}

// Start launches worker goroutines. Call Stop() to drain and shut down.
func (p *Pool) Start(ctx context.Context) {
	for range p.workers {
		p.wg.Add(1)
		go p.worker(ctx)
	}
}

func (p *Pool) worker(ctx context.Context) {
	defer p.wg.Done()
	for {
		select {
		case <-ctx.Done():
			return
		case job, ok := <-p.jobs:
			if !ok {
				return
			}
			p.run(ctx, job)
		}
	}
}

func (p *Pool) run(ctx context.Context, job Job) {
	defer func() {
		if r := recover(); r != nil {
			p.logger.ErrorContext(ctx, "worker panic", "recover", r)
		}
	}()
	if err := job(ctx); err != nil {
		p.logger.ErrorContext(ctx, "job error", "err", err)
	}
}

// Submit enqueues a job. Returns false and drops the job if ctx is cancelled.
func (p *Pool) Submit(ctx context.Context, job Job) bool {
	select {
	case p.jobs <- job:
		return true
	case <-ctx.Done():
		return false
	}
}

// Stop closes the job queue and waits for all workers to finish.
func (p *Pool) Stop() {
	close(p.jobs)
	p.wg.Wait()
}
