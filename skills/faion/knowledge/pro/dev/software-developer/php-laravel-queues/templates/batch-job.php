// purpose: Bus::batch fan-out for parallel processing of N records
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~350 tokens when loaded as context

<?php

namespace App\Services;

use App\Jobs\ProcessOrderItemJob;
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;
use Throwable;

class OrderItemProcessor
{
    public function dispatchBatch(array $orderItemIds): string
    {
        $jobs = array_map(fn (int $id) => new ProcessOrderItemJob($id), $orderItemIds);

        $batch = Bus::batch($jobs)
            ->name('process-order-items')
            ->onQueue('low')
            ->allowFailures()
            ->then(function (Batch $batch) {
                // all jobs completed (with or without failures since allowFailures)
            })
            ->catch(function (Batch $batch, Throwable $e) {
                // first failure callback
            })
            ->finally(function (Batch $batch) {
                // cleanup
            })
            ->dispatch();

        return $batch->id;
    }
}
