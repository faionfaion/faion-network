<?php
// purpose: Service skeleton — constructor injection + DB::transaction + DTO/primitive inputs
// consumes: model + repository (optional)
// produces: service conforming to service-no-request-globals + db-transaction-closure
// depends-on: content/01-core-rules.xml rules service-no-request-globals, db-transaction-closure
// token-budget-impact: ~400 tokens when loaded as context
// Service layer skeleton — no request(), no JsonResponse, no Eloquent in controller
// Replace: User, UserRepository

namespace App\Services;

use App\Events\UserCreated;
use App\Models\User;
use App\Repositories\UserRepository;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

class UserService
{
    public function __construct(private readonly UserRepository $repository) {}

    public function paginate(int $perPage = 20): LengthAwarePaginator
    {
        return $this->repository->paginate($perPage);
    }

    public function findOrFail(int $id): User
    {
        return $this->repository->findOrFail($id);
    }

    public function create(array $data): User
    {
        return DB::transaction(function () use ($data): User {
            $data['password'] = Hash::make($data['password']);
            $user = $this->repository->create($data);
            event(new UserCreated($user));
            return $user;
        });
    }

    public function update(int $id, array $data): User
    {
        return DB::transaction(function () use ($id, $data): User {
            if (isset($data['password'])) {
                $data['password'] = Hash::make($data['password']);
            }
            return $this->repository->update($id, $data);
        });
    }

    public function delete(int $id): bool
    {
        return DB::transaction(fn (): bool => $this->repository->delete($id));
    }
}
