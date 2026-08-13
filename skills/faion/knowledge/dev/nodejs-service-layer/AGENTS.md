# Node.js Service Layer

## Summary

**One-sentence:** Layer a Node.js TypeScript service into controller / service / repository with HTTP types confined to controller and persistence to repository.

**One-paragraph:** Controller-Service-Repository pattern for Node.js TypeScript services: controllers decode requests + encode responses; services hold business logic and orchestration; repositories own ORM/SQL. Controller never imports Prisma/Drizzle/Knex; service never imports Express/Fastify. Dependency injection via constructor + interfaces declared at the consumer side. Output is the layered package set + dependency graph + tests at each layer.

**Ефективно для:**

- Replacing fat-controller Node.js services with reviewable layers.
- Greenfield TypeScript backends adopting layered architecture.
- Onboarding engineers to consistent per-feature layout.
- Adding interface seams to enable unit testing service logic.

## Applies If (ALL must hold)

- Node.js >=20 + TypeScript project.
- Service has multi-step business logic (>=2 operations per feature).
- Persistence (Prisma, Drizzle, Knex, raw pg) exists.
- Tests target service logic directly, not only via HTTP integration.

## Skip If (ANY kills it)

- Thin CRUD service where layering adds overhead without payoff.
- Project follows a different architecture (CQRS, NestJS module conventions).
- Serverless functions where each function is the layer.
- Single-file experiment where one module holds everything intentionally.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature inventory: which aggregates need controller/service/repo | table | tech-lead |
| ORM choice (Prisma / Drizzle / Knex / pg) | ADR | tech-lead |
| HTTP framework (Express / Fastify / Hono / Koa) | config | platform |
| Test stack (vitest, jest, supertest) | config | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[monorepo-turborepo]] | Layered packages may live in workspaces. |
| [[logging-patterns]] | Each layer emits structured logs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (controller decodes/encodes, service has business logic, repo owns ORM, no HTTP in service, no ORM in controller) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for layered module spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: scaffold → interfaces → repo → service → controller | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `interface_design` | opus | Interface seams between layers. |
| `controller_authoring` | sonnet | Decode + call service + encode. |
| `repo_authoring` | sonnet | ORM/SQL + domain-type mapping. |

## Templates

| File | Purpose |
|------|---------|
| `templates/user-controller.ts` | Controller with decode + service call + encode |
| `templates/user-service.ts` | Service with business logic + interfaces |
| `templates/user-repository.ts` | Repository with ORM + domain-type mapping |
| `templates/errors.ts` | Domain error classes shared across layers |
| `templates/layer-check.sh` | Static check: no Prisma in controller, no Express in service |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nodejs-service-layer.py` | Validate layered module spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[go-standard-layout]]
- [[monorepo-turborepo]]
- [[logging-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps service complexity, persistence presence, and existing architecture to a rule from `01-core-rules.xml`, telling the agent whether to layer or skip for thin/CQRS cases. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/user-controller.ts`

```typescript
import { Request, Response, NextFunction } from 'express';
import { UserService } from './user-service';
import { CreateUserSchema, UpdateUserSchema } from '../schemas/users';

export class UserController {
  constructor(private userService: UserService) {}

  getUsers = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 20;
      const search = req.query.search as string | undefined;
      res.json(await this.userService.getUsers(page, limit, search));
    } catch (error) { next(error); }
  };

  getUser = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      res.json({ data: await this.userService.getUser(req.params.id) });
    } catch (error) { next(error); }
  };

  createUser = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const data = CreateUserSchema.parse(req.body);
      res.status(201).json({ data: await this.userService.createUser(data) });
    } catch (error) { next(error); }
  };

  updateUser = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const data = UpdateUserSchema.parse(req.body);
      res.json({ data: await this.userService.updateUser(req.params.id, data) });
    } catch (error) { next(error); }
  };

  deleteUser = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      await this.userService.deleteUser(req.params.id);
      res.status(204).send();
    } catch (error) { next(error); }
  };
}
```

### `templates/user-service.ts`

```typescript
import { User } from '@prisma/client';
import { IUserRepository } from './user-repository';
import { NotFoundError, ConflictError, UnauthorizedError } from './errors';
import { hashPassword, comparePasswords } from '../utils/password';

interface CreateUserDto { email: string; name: string; password: string }
interface UpdateUserDto { email?: string; name?: string }
interface PaginatedUsers { users: User[]; total: number; page: number; limit: number; pages: number }

export class UserService {
  constructor(private userRepository: IUserRepository) {}

  async getUser(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) throw new NotFoundError(`User ${id} not found`);
    return user;
  }

  async getUsers(page: number, limit: number, search?: string): Promise<PaginatedUsers> {
    const { users, total } = await this.userRepository.findAll({ page, limit, search });
    return { users, total, page, limit, pages: Math.ceil(total / limit) };
  }

  async createUser(data: CreateUserDto): Promise<User> {
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) throw new ConflictError('User with this email already exists');
    const hashedPassword = await hashPassword(data.password);
    return this.userRepository.create({ email: data.email, name: data.name, hashedPassword });
  }

  async updateUser(id: string, data: UpdateUserDto): Promise<User> {
    await this.getUser(id);
    if (data.email) {
      const existing = await this.userRepository.findByEmail(data.email);
      if (existing && existing.id !== id) throw new ConflictError('Email already in use');
    }
    return this.userRepository.update(id, data);
  }

  async deleteUser(id: string): Promise<void> {
    await this.getUser(id);
    await this.userRepository.delete(id);
  }

  async authenticateUser(email: string, password: string): Promise<User> {
    const user = await this.userRepository.findByEmail(email);
    if (!user) throw new UnauthorizedError('Invalid credentials');
    const valid = await comparePasswords(password, user.hashedPassword);
    if (!valid) throw new UnauthorizedError('Invalid credentials');
    return user;
  }
}
```

### `templates/user-repository.ts`

```typescript
import { PrismaClient, User, Prisma } from '@prisma/client';

export interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  findAll(params: FindAllParams): Promise<{ users: User[]; total: number }>;
  create(data: CreateUserData): Promise<User>;
  update(id: string, data: UpdateUserData): Promise<User>;
  delete(id: string): Promise<void>;
}

interface FindAllParams { page: number; limit: number; search?: string }
interface CreateUserData { email: string; name: string; hashedPassword: string }
interface UpdateUserData { email?: string; name?: string }

export class UserRepository implements IUserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { email } });
  }

  async findAll({ page, limit, search }: FindAllParams) {
    const skip = (page - 1) * limit;
    const where: Prisma.UserWhereInput = search
      ? { OR: [{ name: { contains: search, mode: 'insensitive' } },
                { email: { contains: search, mode: 'insensitive' } }] }
      : {};
    const [users, total] = await Promise.all([
      this.prisma.user.findMany({ where, skip, take: limit, orderBy: { createdAt: 'desc' } }),
      this.prisma.user.count({ where }),
    ]);
    return { users, total };
  }

  async create(data: CreateUserData): Promise<User> {
    return this.prisma.user.create({ data });
  }

  async update(id: string, data: UpdateUserData): Promise<User> {
    return this.prisma.user.update({ where: { id }, data });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({ where: { id } });
  }
}
```

### `templates/errors.ts`

```typescript
import { ErrorRequestHandler } from 'express';
import { ZodError } from 'zod';

export class AppError extends Error {
  constructor(
    message: string,
    public statusCode = 500,
    public code = 'INTERNAL_ERROR',
    public isOperational = true,
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class NotFoundError extends AppError {
  constructor(message = 'Resource not found') { super(message, 404, 'NOT_FOUND'); }
}

export class ConflictError extends AppError {
  constructor(message = 'Resource conflict') { super(message, 409, 'CONFLICT'); }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') { super(message, 401, 'UNAUTHORIZED'); }
}

export class ValidationError extends AppError {
  constructor(message = 'Validation failed', public errors: Record<string, string[]> = {}) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}

export const errorHandler: ErrorRequestHandler = (err, req, res, _next) => {
  if (err instanceof ZodError) {
    return res.status(400).json({ error: 'Validation failed', code: 'VALIDATION_ERROR',
      details: err.flatten().fieldErrors });
  }
  if (err instanceof AppError && err.isOperational) {
    return res.status(err.statusCode).json({ error: err.message, code: err.code });
  }
  return res.status(500).json({ error: 'Internal server error', code: 'INTERNAL_ERROR' });
};
```

### `templates/layer-check.sh`

```bash
# layer-check.sh — fail CI if controllers depend on repos or services depend on framework.
# Usage: bash layer-check.sh [src-dir]
set -euo pipefail
ROOT="${1:-src}"

# 1. ESLint with eslint-plugin-boundaries (assumes config in repo)
npx --yes eslint "$ROOT/**/*.ts" --max-warnings=0

# 2. dependency-cruiser custom rules
cat > /tmp/dc.json <<'JSON'
{
  "forbidden": [
    {
      "name": "ctrl-no-repo",
      "from": { "path": "controllers" },
      "to": { "path": "repositories" },
      "comment": "Controllers must call services, not repositories."
    },
    {
      "name": "svc-no-framework",
      "from": { "path": "services" },
      "to": { "path": "node_modules/(express|fastify|@nestjs/core)" },
      "comment": "Services are framework-agnostic."
    },
    {
      "name": "no-circular",
      "severity": "error",
      "from": {},
      "to": { "circular": true }
    }
  ]
}
JSON
npx --yes dependency-cruiser --config /tmp/dc.json --output-type err "$ROOT"

# 3. Circular dependency check
npx --yes madge --circular --extensions ts "$ROOT"

echo "Layer check OK"
```
