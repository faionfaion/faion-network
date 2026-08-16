# Backend Testing Across Languages

## Summary

**One-sentence:** Produces a test suite scaffold per backend language using the idiomatic runner (RSpec/Pest/xUnit/tokio::test/JUnit slices) with the right scope discipline (no @SpringBootTest by default; no WebApplicationFactory by default; #[tokio::test] for async Rust).

**One-paragraph:** Per-language test idioms: Ruby on Rails uses RSpec + factory_bot with let/let! discipline; Laravel uses Pest + RefreshDatabase + postJson/getJson; Spring Boot uses @ExtendWith(MockitoExtension.class) / @DataJpaTest / @WebMvcTest slices instead of @SpringBootTest by default; .NET uses xUnit + Moq + FluentAssertions, no WebApplicationFactory unless integration; Rust uses #[test] / #[tokio::test] in #[cfg(test)] mod tests {} blocks. Agent prompts include the runner name explicitly so LLMs don't default to the wrong API.

**Ефективно для:**

- Greenfield test setup in any of the five backend languages.
- Refactor passes replacing @SpringBootTest with proper slices.
- Adding async Rust tests under tokio::test instead of bare #[test].
- Cleaning up Minitest -> RSpec migrations.

## Applies If (ALL must hold)

- Backend language is one of: ruby_rails / laravel / spring / dotnet / rust.
- Project ships unit + integration tests as a quality gate.
- Tests run in CI and must complete in <10 minutes.
- Mocks/fakes are used for dependencies, not deep call graphs.

## Skip If (ANY kills it)

- Pure Python (use testing-django-pytest).
- Frontend tests (use testing-js-ts-frontend).
- End-to-end browser tests (use playwright-automation).
- Performance/load tests — separate methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Language | ruby_rails | laravel | spring | dotnet | rust | team decision |
| Test scope | unit | integration | slice | task brief |
| Dependencies the SUT uses | list of collaborators | service spec |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[practices-backend-languages]] | code-side patterns the tests verify |
| [[trunk-based-ci-gates]] | CI gate runs these tests on every push |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-runner` | haiku | lookup from language tag |
| `emit-test-scaffold` | sonnet | idiomatic test class with mocks + assertions |
| `scope-discipline-check` | sonnet | flag @SpringBootTest / WebApplicationFactory misuse |

## Templates

| File | Purpose |
|------|---------|
| `templates/OrderService.spec.rb` | RSpec test using factory_bot + let |
| `templates/OrderTest.php` | Pest test with RefreshDatabase + JSON assertion |
| `templates/OrderServiceTest.java` | Spring service unit test using MockitoExtension (no SpringBootTest) |
| `templates/OrderServiceTests.cs` | xUnit + Moq + FluentAssertions service test |
| `templates/order_test.rs` | Rust async unit test using tokio::test |
| `templates/artefact.json` | Sample artefact metadata for validator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testing-backend-languages.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[testing-django-pytest]]
- [[testing-js-ts-frontend]]
- [[practices-backend-languages]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/OrderService.spec.rb`

```ruby
require 'rails_helper'

RSpec.describe OrderService, type: :service do
  let(:customer) { create(:customer) }
  let!(:order) { create(:order, customer: customer) }

  describe '#charge' do
    it 'marks the order as charged on success' do
      result = described_class.new.charge(order)
      expect(result).to be_success
      expect(order.reload.status).to eq('charged')
    end
  end
end
```

### `templates/OrderTest.php`

```php
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
```

### `templates/OrderServiceTest.java`

```java
package com.example.orders;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    @Mock OrderRepository repo;
    @InjectMocks OrderService svc;

    @Test
    void charge_persists_charged_status() {
        Order o = Order.builder().amount(1000).build();
        when(repo.save(o)).thenReturn(o);
        Order result = svc.charge(o);
        assertThat(result.getStatus()).isEqualTo("charged");
    }
}
```

### `templates/OrderServiceTests.cs`

```csharp
using Moq;
using FluentAssertions;
using Xunit;

public class OrderServiceTests
{
    [Fact]
    public async Task Charge_Marks_Order_As_Charged()
    {
        var repo = new Mock<IOrderRepository>();
        var order = new Order { Amount = 1000 };
        repo.Setup(r => r.SaveAsync(order)).ReturnsAsync(order);
        var svc = new OrderService(repo.Object);

        var result = await svc.ChargeAsync(order);

        result.Status.Should().Be("charged");
    }
}
```

### `templates/order_test.rs`

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn charge_marks_order_as_charged() {
        let pool = test_pool().await;
        let order = create_order(&pool, 1000).await.unwrap();
        let result = charge_order(&pool, &order.id).await.unwrap();
        assert_eq!(result.status, "charged");
    }
}
```

### `templates/artefact.json`

```json
{
  "language": "spring",
  "runner": "junit5",
  "scope_discipline_ok": true,
  "mock_shallowness_ok": true,
  "ci_lt_10min": true,
  "spring_uses_slices": true
}
```
