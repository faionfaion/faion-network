<?php
// tests/Feature/UserControllerTest.php
// Skeleton: five required scenarios per endpoint.

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Mail;
use Tests\TestCase;

class UserControllerTest extends TestCase
{
    use RefreshDatabase;

    // 1. Happy path
    public function test_can_create_user(): void
    {
        Mail::fake();

        $response = $this->actingAs(User::factory()->create())
            ->postJson('/api/v1/users', [
                'name' => 'John Doe',
                'email' => 'john@example.com',
                'password' => 'password123',
            ]);

        $response->assertCreated()
            ->assertJsonPath('data.name', 'John Doe')
            ->assertJsonPath('data.email', 'john@example.com')
            ->assertJsonMissing(['password']); // never expose password

        $this->assertDatabaseHas('users', ['email' => 'john@example.com']);
    }

    // 2. Validation failure
    public function test_create_user_validates_email(): void
    {
        $response = $this->actingAs(User::factory()->create())
            ->postJson('/api/v1/users', [
                'name' => 'John Doe',
                'email' => 'not-an-email',
                'password' => 'password123',
            ]);

        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['email']);
    }

    // 3. Missing required field
    public function test_create_user_requires_name(): void
    {
        $response = $this->actingAs(User::factory()->create())
            ->postJson('/api/v1/users', ['email' => 'john@example.com', 'password' => 'pass']);

        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['name']);
    }

    // 4. Unauthenticated
    public function test_create_user_requires_authentication(): void
    {
        $response = $this->postJson('/api/v1/users', [
            'name' => 'John', 'email' => 'john@example.com', 'password' => 'pass',
        ]);

        $response->assertUnauthorized();
    }

    // 5. Not found
    public function test_show_returns_404_for_missing_user(): void
    {
        $response = $this->actingAs(User::factory()->create())
            ->getJson('/api/v1/users/99999');

        $response->assertNotFound();
    }
}
