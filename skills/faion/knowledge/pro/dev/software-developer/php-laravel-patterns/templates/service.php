// purpose: Service with DB::transaction + business rules
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~350 tokens when loaded as context

<?php

namespace App\Services;

use App\Models\Order;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\DB;

class OrderService
{
    public function listForCurrentUser(): Collection
    {
        return Order::where('user_id', auth()->id())->with('items')->latest()->get();
    }

    public function create(array $data): Order
    {
        return DB::transaction(function () use ($data) {
            $order = Order::create(['user_id' => auth()->id(), 'status' => 'pending']);
            foreach ($data['items'] as $item) {
                $order->items()->create($item);
            }
            return $order->load('items');
        });
    }

    public function cancel(Order $order): void
    {
        DB::transaction(function () use ($order) {
            $order->update(['status' => 'cancelled', 'cancelled_at' => now()]);
            event(new OrderCancelled($order));
        });
    }
}
