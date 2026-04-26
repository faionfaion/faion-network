<?php
// Feature test skeleton — HTTP-driven, uses RefreshDatabase
// Replace: User, UserControllerTest, /api/v1/users endpoints

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class UserControllerTest extends TestCase
{
    use RefreshDatabase;

    private User $admin;

    protected function setUp(): void
    {
        parent::setUp();
        $this->admin = User::factory()->create(['role' => 'admin']);
    }

    public function test_authenticated_user_can_list_users(): void
    {
        User::factory()->count(3)->create();

        $response = $this->actingAs($this->admin)->getJson('/api/v1/users');

        $response->assertOk()
            ->assertJsonCount(4, 'data') // 3 + admin
            ->assertJsonPath('meta.current_page', 1);
    }

    public function test_can_create_user_with_valid_data(): void
    {
        $response = $this->actingAs($this->admin)->postJson('/api/v1/users', [
            'name'     => 'John Doe',
            'email'    => 'john@example.com',
            'password' => 'password123',
        ]);

        $response->assertCreated()
            ->assertJsonPath('data.name', 'John Doe')
            ->assertJsonPath('data.email', 'john@example.com');

        $this->assertDatabaseHas('users', ['email' => 'john@example.com']);
    }

    public function test_create_returns_422_with_invalid_email(): void
    {
        $response = $this->actingAs($this->admin)->postJson('/api/v1/users', [
            'name'     => 'John',
            'email'    => 'not-an-email',
            'password' => 'password123',
        ]);

        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['email']);
    }

    public function test_can_soft_delete_user(): void
    {
        $user = User::factory()->create();

        $this->actingAs($this->admin)->deleteJson("/api/v1/users/{$user->id}")
            ->assertNoContent();

        $this->assertSoftDeleted('users', ['id' => $user->id]);
    }
}
