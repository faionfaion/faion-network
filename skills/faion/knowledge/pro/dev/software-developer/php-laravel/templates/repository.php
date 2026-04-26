<?php
// app/Repositories/UserRepository.php
// Only add this class if you have a real second backing implementation.
// For standard Eloquent, use the model directly from the service.
namespace App\Repositories;

use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Pagination\LengthAwarePaginator;

class UserRepository
{
    public function __construct(private readonly User $model) {}

    public function paginate(int $perPage = 20): LengthAwarePaginator
    {
        return $this->model->with(['roles'])->latest()->paginate($perPage);
    }

    public function findOrFail(int $id): User
    {
        return $this->model->with(['roles', 'orders'])->findOrFail($id);
    }

    public function create(array $data): User
    {
        return $this->model->create($data);
    }

    public function update(int $id, array $data): User
    {
        $user = $this->model->findOrFail($id);
        $user->update($data);
        return $user->fresh();
    }

    public function delete(int $id): bool
    {
        return $this->model->findOrFail($id)->delete();
    }

    public function findByEmail(string $email): ?User
    {
        return $this->model->where('email', $email)->first();
    }
}
