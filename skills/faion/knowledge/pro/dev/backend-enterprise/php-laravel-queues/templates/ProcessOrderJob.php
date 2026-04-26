<?php
// Laravel Queue job skeleton — idempotent, ID-only, retry/backoff/timeout, failed()
// Replace: ProcessOrderJob, Order, OrderProcessor, NotifyCustomerJob

namespace App\Jobs;

use App\Models\Order;
use App\Services\OrderProcessor;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\Middleware\WithoutOverlapping;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;
use Throwable;

class ProcessOrderJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries   = 3;
    public int $backoff = 60;   // seconds between retries
    public int $timeout = 120;  // max seconds per attempt

    public function __construct(public readonly int $orderId) {}

    public function middleware(): array
    {
        return [new WithoutOverlapping($this->orderId)];
    }

    public function handle(OrderProcessor $processor): void
    {
        $order = Order::findOrFail($this->orderId);

        if ($order->isProcessed()) {
            return; // idempotency guard
        }

        $processor->process($order);

        NotifyCustomerJob::dispatch($this->orderId)->onQueue('notifications');
    }

    public function failed(Throwable $exception): void
    {
        Order::find($this->orderId)?->update(['status' => 'failed']);

        Log::error('Order processing failed', [
            'order_id' => $this->orderId,
            'error'    => $exception->getMessage(),
        ]);
    }

    public function retryUntil(): \DateTime
    {
        return now()->addHours(24);
    }
}

// Dispatch examples:
// ProcessOrderJob::dispatch($order->id)->onQueue('orders');
// ProcessOrderJob::dispatch($order->id)->delay(now()->addMinutes(5));
