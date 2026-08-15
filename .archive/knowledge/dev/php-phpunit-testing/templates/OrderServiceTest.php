// purpose: PHPUnit test class with AAA + #[DataProvider] + constructor mocks
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~500 tokens when loaded as context

<?php

namespace Tests\Unit\Services;

use App\Models\Order;
use App\Models\OrderItem;
use App\Services\DiscountService;
use App\Services\OrderService;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\MockObject\MockObject;

final class OrderServiceTest extends TestCase
{
    private DiscountService&MockObject $discount;
    private OrderService $service;

    protected function setUp(): void
    {
        parent::setUp();
        $this->discount = $this->createMock(DiscountService::class);
        $this->service = new OrderService($this->discount);
    }

    #[DataProvider('totalCases')]
    public function test_calculates_total_for_various_baskets(array $items, int $discountCents, int $expectedCents): void
    {
        // Arrange
        $this->discount->method('apply')->willReturn($discountCents);

        // Act
        $total = $this->service->calculateTotal($items);

        // Assert
        self::assertSame($expectedCents, $total);
    }

    public static function totalCases(): array
    {
        return [
            'empty basket' => [[], 0, 0],
            'single item' => [[['cents' => 1000, 'qty' => 1]], 0, 1000],
            'multi-item with discount' => [[['cents' => 1000, 'qty' => 2], ['cents' => 500, 'qty' => 3]], 200, 3300],
        ];
    }
}
