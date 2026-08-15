// purpose: server.go skeleton — Wire(cfg) -> *http.Server with timeouts, Run() with graceful shutdown.
// consumes: *Config (Addr, timeouts), *Deps (handlers, logger).
// produces: *http.Server with all four timeouts; Run blocks until SIGINT/SIGTERM and drains.
// depends-on: stdlib net/http, os/signal, time, errgroup.
// token-budget-impact: ~60 lines; loaded once at boot.
// server/server.go — graceful shutdown wrapper for Go HTTP services.
// Usage: server.Run(srv, 15*time.Second, log)
// Blocks until SIGINT or SIGTERM, then drains for `grace` duration.
package server

import (
	"context"
	"errors"
	"net/http"
	"os/signal"
	"syscall"
	"time"

	"go.uber.org/zap"
)

// Run starts srv and blocks until SIGINT/SIGTERM, then drains for grace.
// Returns an error if the server fails to start or shutdown times out.
func Run(srv *http.Server, grace time.Duration, log *zap.Logger) error {
	ctx, stop := signal.NotifyContext(context.Background(),
		syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	errCh := make(chan error, 1)
	go func() {
		log.Info("listen", zap.String("addr", srv.Addr))
		if err := srv.ListenAndServe(); err != nil &&
			!errors.Is(err, http.ErrServerClosed) {
			errCh <- err
		}
	}()

	select {
	case err := <-errCh:
		return err
	case <-ctx.Done():
		log.Info("shutdown signal received")
	}

	shutCtx, cancel := context.WithTimeout(context.Background(), grace)
	defer cancel()
	if err := srv.Shutdown(shutCtx); err != nil {
		return err
	}
	log.Info("shutdown complete")
	return nil
}

// Wire from main.go:
// srv := &http.Server{
//     Addr:              ":8080",
//     Handler:           r,
//     ReadHeaderTimeout: 5 * time.Second,
//     ReadTimeout:       30 * time.Second,
//     WriteTimeout:      30 * time.Second,
//     IdleTimeout:       120 * time.Second,
// }
// if err := server.Run(srv, 15*time.Second, log); err != nil {
//     log.Fatal("server error", zap.Error(err))
// }
