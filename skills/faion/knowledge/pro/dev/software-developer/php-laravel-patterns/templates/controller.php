// purpose: Thin layered controller skeleton
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~350 tokens when loaded as context

<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreOrderRequest;
use App\Http\Requests\UpdateOrderRequest;
use App\Http\Resources\OrderResource;
use App\Models\Order;
use App\Services\OrderService;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;

class OrderController extends Controller
{
    public function __construct(private readonly OrderService $service)
    {
        $this->authorizeResource(Order::class, 'order');
    }

    public function index(): AnonymousResourceCollection
    {
        return OrderResource::collection($this->service->listForCurrentUser());
    }

    public function store(StoreOrderRequest $request): OrderResource
    {
        return new OrderResource($this->service->create($request->validated()));
    }

    public function update(UpdateOrderRequest $request, Order $order): OrderResource
    {
        return new OrderResource($this->service->update($order, $request->validated()));
    }

    public function destroy(Order $order): void
    {
        $this->service->cancel($order);
    }
}
