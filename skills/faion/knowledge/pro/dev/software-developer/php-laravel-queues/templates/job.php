// purpose: Queue job skeleton with tries+timeout+backoff+failed+idempotent handle
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~450 tokens when loaded as context

<?php

namespace App\Jobs;

use App\Models\Order;
use App\Services\MailService;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\Middleware\WithoutOverlapping;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;
use Sentry\Laravel\Integration;
use Throwable;

class SendOrderConfirmationJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 5;
    public int $timeout = 30;

    public function __construct(
        public readonly int $orderId,
        public readonly string $idempotencyKey,
    ) {}

    public function backoff(): array
    {
        return [10, 30, 60, 120, 240];
    }

    public function middleware(): array
    {
        return [(new WithoutOverlapping($this->idempotencyKey))->expireAfter(300)];
    }

    public function handle(MailService $mail): void
    {
        $order = Order::findOrFail($this->orderId);
        if ($order->confirmation_sent_at !== null) {
            return; // idempotent: already processed
        }
        $mail->send($order->customer->email, "Order #{$order->id} confirmed", view('mail.order-confirmation', ['order' => $order])->render());
        $order->update(['confirmation_sent_at' => now()]);
    }

    public function failed(Throwable $e): void
    {
        Log::error('SendOrderConfirmationJob failed', ['order_id' => $this->orderId, 'exception' => $e->getMessage()]);
        Integration::captureUnhandledException($e);
    }
}
