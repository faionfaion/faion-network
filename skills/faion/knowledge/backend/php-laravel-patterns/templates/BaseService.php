<?php
// purpose: abstract Service base class with DB::transaction helper
// consumes: per-service model + repository dependencies
// produces: Service skeleton conforming to db-transaction-closure rule
// depends-on: content/01-core-rules.xml rule db-transaction-closure
// token-budget-impact: ~250 tokens when loaded as context
// Abstract base service — extend per resource to share paginate/find/delete
// Only use when ≥2 resources share the same CRUD shape

namespace App\Services;

use App\Repositories\BaseRepository;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\DB;

abstract class BaseService
{
    public function __construct(protected readonly BaseRepository $repository) {}

    public function paginate(int $perPage = 20): LengthAwarePaginator
    {
        return $this->repository->paginate($perPage);
    }

    public function findOrFail(int $id): Model
    {
        return $this->repository->findOrFail($id);
    }

    public function delete(int $id): bool
    {
        return DB::transaction(fn (): bool => $this->repository->delete($id));
    }
}
