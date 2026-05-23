<?php
// purpose: Unit test skeleton without Laravel boot, Mockery for dependencies
// consumes: service class + collaborator interfaces
// produces: Unit test conforming to feature-vs-unit-boundary rule
// depends-on: content/01-core-rules.xml rule feature-vs-unit-boundary
// token-budget-impact: ~350 tokens when loaded as context
// Unit test skeleton — single class, no RefreshDatabase, Mockery for dependencies
// Replace: UserService, UserRepository, UserCreated event

namespace Tests\Unit\Services;

use App\Events\UserCreated;
use App\Repositories\UserRepository;
use App\Services\UserService;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Hash;
use Mockery;
use Tests\TestCase;

class UserServiceTest extends TestCase
{
    // NOTE: do NOT use RefreshDatabase here — it is a unit test

    private UserService    $service;
    private UserRepository $repository;

    protected function setUp(): void
    {
        parent::setUp();
        $this->repository = Mockery::mock(UserRepository::class);
        $this->service    = new UserService($this->repository);
    }

    public function test_create_dispatches_user_created_event(): void
    {
        Event::fake(); // BEFORE the action

        $this->repository->shouldReceive('create')->once()->andReturn(
            \App\Models\User::factory()->make()
        );

        $this->service->create([
            'name'     => 'Alice',
            'email'    => 'alice@example.com',
            'password' => 'password',
        ]);

        Event::assertDispatched(UserCreated::class);
    }

    public function test_create_hashes_password(): void
    {
        $this->repository->shouldReceive('create')
            ->once()
            ->andReturnUsing(fn (array $data) => \App\Models\User::factory()->make($data));

        $user = $this->service->create([
            'name'     => 'Alice',
            'email'    => 'alice@example.com',
            'password' => 'plaintext',
        ]);

        $this->assertNotEquals('plaintext', $user->password);
        $this->assertTrue(Hash::check('plaintext', $user->password));
    }

    protected function tearDown(): void
    {
        Mockery::close();
        parent::tearDown();
    }
}
