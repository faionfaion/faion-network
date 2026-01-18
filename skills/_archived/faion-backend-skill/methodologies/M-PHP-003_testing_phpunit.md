# M-PHP-003: PHP Testing with PHPUnit

## Metadata
- **Category:** Development/Backend/PHP
- **Difficulty:** Intermediate
- **Tags:** #dev, #php, #testing, #phpunit, #methodology
- **Agent:** faion-test-agent

---

## Problem

PHP applications without tests break in production. Manual testing is slow and unreliable. You need automated tests that catch bugs early and give confidence in deployments.

## Promise

After this methodology, you will write PHPUnit tests that are fast, maintainable, and catch real bugs. You will test units, integrations, and HTTP endpoints effectively.

## Overview

PHPUnit is the PHP testing standard. Combined with Laravel's testing helpers and Pest syntax, it enables comprehensive coverage.

---

## Framework

### Step 1: PHPUnit Setup

**composer.json:**

```json
{
  "require-dev": {
    "phpunit/phpunit": "^10.0",
    "mockery/mockery": "^1.6"
  }
}
```

**phpunit.xml:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/autoload.php"
         colors="true"
         cacheDirectory=".phpunit.cache">
    <testsuites>
        <testsuite name="Unit">
            <directory>tests/Unit</directory>
        </testsuite>
        <testsuite name="Feature">
            <directory>tests/Feature</directory>
        </testsuite>
    </testsuites>
    <source>
        <include>
            <directory>src</directory>
        </include>
    </source>
    <coverage>
        <report>
            <html outputDirectory="coverage"/>
            <text outputFile="php://stdout"/>
        </report>
    </coverage>
    <php>
        <env name="APP_ENV" value="testing"/>
        <env name="DB_DATABASE" value="testing"/>
    </php>
</phpunit>
```

### Step 2: Basic Test Structure

**tests/Unit/UserServiceTest.php:**

```php
<?php

declare(strict_types=1);

namespace Tests\Unit;

use App\Services\UserService;
use App\Repositories\UserRepository;
use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\MockObject\MockObject;

class UserServiceTest extends TestCase
{
    private UserService $service;
    private MockObject $repository;

    protected function setUp(): void
    {
        parent::setUp();

        $this->repository = $this->createMock(UserRepository::class);
        $this->service = new UserService($this->repository);
    }

    public function testCreateUserWithValidData(): void
    {
        // Arrange
        $data = ['email' => 'test@example.com', 'name' => 'Test'];

        $this->repository
            ->expects($this->once())
            ->method('create')
            ->with($data)
            ->willReturn((object) ['id' => 1, ...$data]);

        // Act
        $result = $this->service->create($data);

        // Assert
        $this->assertEquals('test@example.com', $result->email);
        $this->assertEquals('Test', $result->name);
    }

    public function testCreateUserThrowsOnDuplicateEmail(): void
    {
        // Arrange
        $this->repository
            ->method('findByEmail')
            ->willReturn((object) ['id' => 1]);

        // Assert
        $this->expectException(\DomainException::class);
        $this->expectExceptionMessage('Email already exists');

        // Act
        $this->service->create(['email' => 'existing@example.com']);
    }
}
```

### Step 3: Data Providers

```php
<?php

class ValidatorTest extends TestCase
{
    /**
     * @dataProvider validEmailProvider
     */
    public function testAcceptsValidEmails(string $email): void
    {
        $this->assertTrue(Validator::isEmail($email));
    }

    public static function validEmailProvider(): array
    {
        return [
            'simple' => ['test@example.com'],
            'with subdomain' => ['test@mail.example.com'],
            'with plus' => ['test+tag@example.com'],
            'with dots' => ['test.user@example.com'],
        ];
    }

    /**
     * @dataProvider invalidEmailProvider
     */
    public function testRejectsInvalidEmails(string $email): void
    {
        $this->assertFalse(Validator::isEmail($email));
    }

    public static function invalidEmailProvider(): array
    {
        return [
            'no at sign' => ['testexample.com'],
            'no domain' => ['test@'],
            'spaces' => ['test @example.com'],
            'empty' => [''],
        ];
    }
}
```

### Step 4: Mocking

**With PHPUnit:**

```php
<?php

public function testWithMock(): void
{
    // Create mock
    $paymentGateway = $this->createMock(PaymentGateway::class);

    // Configure behavior
    $paymentGateway
        ->expects($this->once())
        ->method('charge')
        ->with(
            $this->equalTo(1000),
            $this->stringContains('tok_')
        )
        ->willReturn(['id' => 'ch_123', 'status' => 'succeeded']);

    // Inject mock
    $service = new PaymentService($paymentGateway);

    // Act
    $result = $service->processPayment(1000, 'tok_test');

    // Assert
    $this->assertEquals('succeeded', $result['status']);
}
```

**With Mockery:**

```php
<?php

use Mockery;

public function testWithMockery(): void
{
    // Create mock
    $mailer = Mockery::mock(Mailer::class);

    // Configure expectations
    $mailer->shouldReceive('send')
           ->once()
           ->with('test@example.com', Mockery::type('string'))
           ->andReturn(true);

    // Use mock
    $service = new NotificationService($mailer);
    $result = $service->notify('test@example.com', 'Hello');

    $this->assertTrue($result);
}

protected function tearDown(): void
{
    Mockery::close();
    parent::tearDown();
}
```

### Step 5: Laravel Feature Tests

**tests/Feature/UserApiTest.php:**

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class UserApiTest extends TestCase
{
    use RefreshDatabase;

    public function testListUsers(): void
    {
        // Arrange
        User::factory()->count(3)->create();

        // Act
        $response = $this->getJson('/api/users');

        // Assert
        $response
            ->assertOk()
            ->assertJsonCount(3, 'data')
            ->assertJsonStructure([
                'data' => [
                    '*' => ['id', 'email', 'name', 'created_at'],
                ],
            ]);
    }

    public function testCreateUser(): void
    {
        // Act
        $response = $this->postJson('/api/users', [
            'email' => 'new@example.com',
            'name' => 'New User',
            'password' => 'password123',
            'password_confirmation' => 'password123',
        ]);

        // Assert
        $response
            ->assertCreated()
            ->assertJsonPath('data.email', 'new@example.com');

        $this->assertDatabaseHas('users', [
            'email' => 'new@example.com',
        ]);
    }

    public function testCreateUserValidation(): void
    {
        $response = $this->postJson('/api/users', [
            'email' => 'invalid',
        ]);

        $response
            ->assertUnprocessable()
            ->assertJsonValidationErrors(['email', 'name', 'password']);
    }

    public function testShowUserRequiresAuth(): void
    {
        $user = User::factory()->create();

        $this->getJson("/api/users/{$user->id}")
            ->assertUnauthorized();
    }

    public function testAuthenticatedUserCanViewOwnProfile(): void
    {
        $user = User::factory()->create();

        $this->actingAs($user)
            ->getJson("/api/users/{$user->id}")
            ->assertOk()
            ->assertJsonPath('data.id', $user->id);
    }
}
```

### Step 6: Factories

**database/factories/UserFactory.php:**

```php
<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;

class UserFactory extends Factory
{
    protected $model = User::class;

    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'password' => Hash::make('password'),
            'email_verified_at' => now(),
        ];
    }

    public function unverified(): static
    {
        return $this->state(fn (array $attributes) => [
            'email_verified_at' => null,
        ]);
    }

    public function admin(): static
    {
        return $this->state(fn (array $attributes) => [
            'role' => 'admin',
        ]);
    }

    public function withOrders(int $count = 3): static
    {
        return $this->has(Order::factory()->count($count));
    }
}
```

---

## Templates

### Test Case Base

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication;

    protected function setUp(): void
    {
        parent::setUp();

        // Global setup
    }

    protected function assertJsonApiError(
        $response,
        int $status,
        string $message
    ): void {
        $response
            ->assertStatus($status)
            ->assertJson([
                'error' => [
                    'message' => $message,
                ],
            ]);
    }
}
```

### Pest Syntax (Optional)

```php
<?php
// tests/Unit/UserServiceTest.php

use App\Services\UserService;

beforeEach(function () {
    $this->service = new UserService(mock(UserRepository::class));
});

it('creates user with valid data', function () {
    $result = $this->service->create([
        'email' => 'test@example.com',
        'name' => 'Test',
    ]);

    expect($result)->toHaveProperty('email', 'test@example.com');
});

it('throws on duplicate email', function () {
    $this->service->create(['email' => 'existing@example.com']);
})->throws(DomainException::class, 'Email already exists');
```

---

## Examples

### Testing Jobs

```php
<?php

use Illuminate\Support\Facades\Queue;

public function testOrderCreationQueuesEmail(): void
{
    Queue::fake();

    // Act
    $this->postJson('/api/orders', $orderData);

    // Assert
    Queue::assertPushed(SendOrderConfirmationEmail::class, function ($job) {
        return $job->order->id === 1;
    });
}
```

### Testing Events

```php
<?php

use Illuminate\Support\Facades\Event;

public function testUserCreationFiresEvent(): void
{
    Event::fake();

    // Act
    User::factory()->create();

    // Assert
    Event::assertDispatched(UserCreated::class);
}
```

---

## Common Mistakes

1. **Testing implementation** - Test behavior, not internals
2. **Shared test state** - Use RefreshDatabase or DatabaseTransactions
3. **Slow tests** - Use unit tests where possible
4. **No assertions** - Every test must assert something
5. **Mystery data** - Be explicit about test data

---

## Checklist

- [ ] PHPUnit configured
- [ ] Unit tests for services
- [ ] Feature tests for API endpoints
- [ ] Factories for all models
- [ ] Mocks for external dependencies
- [ ] Database refresh between tests
- [ ] CI runs tests on every PR
- [ ] Coverage reports generated

---

## Next Steps

- M-PHP-004: PHP Code Quality
- M-PHP-002: Laravel Patterns
- M-DO-001: CI/CD with GitHub Actions

---

*Methodology M-PHP-003 v1.0*
