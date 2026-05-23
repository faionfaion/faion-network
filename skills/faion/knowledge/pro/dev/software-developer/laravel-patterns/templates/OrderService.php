// purpose: Service owning DB::transaction + business rules
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~350 tokens when loaded as context

<?php

namespace App\Services;

use App\Models\Order;
use Illuminate\Support\Facades\DB;

class OrderService
{
    public function create(array $data): Order
    {
        return DB::transaction(function () use ($data) {
            $order = Order::create([
                'user_id' => auth()->id(),
                'status' => 'pending',
            ]);
            foreach ($data['items'] as $item) {
                $order->items()->create($item);
            }
            return $order->load('items');
        });
    }

    public function update(Order $order, array $data): Order
    {
        return DB::transaction(function () use ($order, $data) {
            $order->update(array_filter($data, fn($k) => $k !== 'items', ARRAY_FILTER_USE_KEY));
            if (isset($data['items'])) {
                $order->items()->delete();
                foreach ($data['items'] as $item) {
                    $order->items()->create($item);
                }
            }
            return $order->fresh('items');
        });
    }
}
