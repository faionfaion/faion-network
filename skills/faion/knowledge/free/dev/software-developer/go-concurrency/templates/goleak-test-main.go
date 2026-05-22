// purpose: TestMain that verifies no goroutines leak past test completion.
// consumes: drop into any concurrency-heavy test package; rename `mypkg_test` to your package.
// produces: any leak fails the test run with the leaked goroutine stack.
// depends-on: go.uber.org/goleak (add to go.mod).
// token-budget-impact: ~15 lines per package; loaded only at test time.
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
