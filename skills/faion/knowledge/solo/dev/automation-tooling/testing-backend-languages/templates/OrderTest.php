// purpose: Pest test with RefreshDatabase + JSON assertion
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for testing-backend-languages
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

<?php

use App\Models\Order;
use function Pest\Laravel\postJson;

uses(\Illuminate\Foundation\Testing\RefreshDatabase::class);

it('creates an order via the API', function () {
    postJson('/api/orders', ['amount' => 1000])
        ->assertCreated()
        ->assertJsonPath('data.amount', 1000);
    expect(Order::count())->toBe(1);
});
