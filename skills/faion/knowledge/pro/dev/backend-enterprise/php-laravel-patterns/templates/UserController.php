<?php
// Thin controller skeleton — Route → FormRequest → Service → Resource
// Replace: User, UserService, StoreUserRequest, UpdateUserRequest, UserResource, UserCollection

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreUserRequest;
use App\Http\Requests\UpdateUserRequest;
use App\Http\Resources\UserCollection;
use App\Http\Resources\UserResource;
use App\Services\UserService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Response;

class UserController extends Controller
{
    public function __construct(private readonly UserService $userService) {}

    public function index(): UserCollection
    {
        $users = $this->userService->paginate(
            perPage: request()->integer('per_page', 20)
        );
        return new UserCollection($users);
    }

    public function store(StoreUserRequest $request): JsonResponse
    {
        $user = $this->userService->create($request->validated());
        return (new UserResource($user))->response()->setStatusCode(Response::HTTP_CREATED);
    }

    public function show(int $id): UserResource
    {
        return new UserResource($this->userService->findOrFail($id));
    }

    public function update(UpdateUserRequest $request, int $id): UserResource
    {
        return new UserResource($this->userService->update($id, $request->validated()));
    }

    public function destroy(int $id): JsonResponse
    {
        $this->userService->delete($id);
        return response()->json(null, Response::HTTP_NO_CONTENT);
    }
}
