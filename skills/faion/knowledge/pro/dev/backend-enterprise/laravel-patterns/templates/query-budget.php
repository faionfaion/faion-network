<?php
// Fail tests that exceed a query count budget (N+1 detector).
// Add to tests/TestCase.php and call $this->failOnNPlusOne() in setUp or per-test.
//
// Usage:
//   protected function setUp(): void {
//       parent::setUp();
//       $this->failOnNPlusOne(max: 10);
//   }

use Illuminate\Database\Events\QueryExecuted;
use Illuminate\Support\Facades\DB;

/**
 * Listen to queries and throw RuntimeException if the budget is exceeded.
 * Call this at the start of a test that should have bounded DB access.
 */
function failOnNPlusOne(int $max = 10): void
{
    $count = 0;
    DB::listen(function (QueryExecuted $event) use (&$count, $max) {
        if (++$count > $max) {
            throw new \RuntimeException(
                "Query budget exceeded: {$count} queries issued (max {$max}). "
                . "Last query: {$event->sql}"
            );
        }
    });
}
