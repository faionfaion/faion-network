<?php
// app/Jobs/ProcessOrderJob.php
// Required: ShouldQueue, idempotency check, primitive args, failed(), retryUntil().

namespace App\Jobs;

use App\Models\Order;
use App\Services\OrderProcessor;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Queue\Middleware\WithoutOverlapping;
use Throwable;

class ProcessOrderJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $backoff = 60;
    public int $timeout = 120;

    public function __construct(
        public readonly Order $order
    ) {}

    public function middleware(): array
    {
        // WithoutOverlapping requires Redis or database cache — not file/array.
        return [new WithoutOverlapping($this->order->id)];
    }

    public function handle(OrderProcessor $processor): void
    {
        if ($this->order->isProcessed()) {
            return; // idempotency: already done
        }

        $processor->process($this->order);

        NotifyCustomerJob::dispatch($this->order)->onQueue('notifications');
    }

    public function failed(Throwable $exception): void
    {
        $this->order->update(['status' => 'failed']);

        \Log::error('Order processing failed', [
            'order_id' => $this->order->id,
            'error' => $exception->getMessage(),
        ]);
    }

    public function retryUntil(): \DateTime
    {
        return now()->addHours(24);
    }
}

// Dispatch examples:
// ProcessOrderJob::dispatch($order)->onQueue('orders');
// ProcessOrderJob::dispatch($order)->delay(now()->addMinutes(10));
// ProcessOrderJob::dispatch($order)->afterCommit(); // safe inside DB::transaction
