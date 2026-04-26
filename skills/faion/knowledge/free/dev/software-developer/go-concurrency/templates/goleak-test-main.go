package mypkg_test

import (
	"testing"

	"go.uber.org/goleak"
)

// TestMain verifies no goroutine leaks after every test in this package.
// Add this to every package with concurrency-heavy code.
func TestMain(m *testing.M) {
	goleak.VerifyTestMain(m)
}
