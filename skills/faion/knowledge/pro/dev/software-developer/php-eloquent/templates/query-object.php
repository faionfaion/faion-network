<?php
// app/Queries/UsersQuery.php
// Fluent Query Object — replace User and field names for other models.
namespace App\Queries;

use App\Models\User;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Builder;

class UsersQuery
{
    public function __construct(private Builder $query) {}

    public static function make(): self
    {
        return new self(User::query());
    }

    public function active(): self
    {
        $this->query->where('is_active', true);
        return $this;
    }

    public function withRole(string $role): self
    {
        $this->query->whereHas('roles', fn($q) => $q->where('name', $role));
        return $this;
    }

    public function search(?string $term): self
    {
        if (filled($term)) {
            $this->query->whereAny(['name', 'email'], 'LIKE', "%$term%");
        }
        return $this;
    }

    public function paginate(int $perPage = 20): LengthAwarePaginator
    {
        return $this->query->with('roles')->latest()->paginate($perPage);
    }
}
