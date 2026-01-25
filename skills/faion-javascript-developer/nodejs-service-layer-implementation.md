# Node.js Service Layer Implementation

**Practical Controller-Service-Repository patterns**

## Repository Layer

```typescript
// repositories/users.repository.ts
import { PrismaClient, User, Prisma } from '@prisma/client';

export interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  findAll(params: FindAllParams): Promise<{ users: User[]; total: number }>;
  create(data: CreateUserData): Promise<User>;
  update(id: string, data: UpdateUserData): Promise<User>;
  delete(id: string): Promise<void>;
}

interface FindAllParams {
  page: number;
  limit: number;
  search?: string;
}

interface CreateUserData {
  email: string;
  name: string;
  hashedPassword: string;
}

interface UpdateUserData {
  email?: string;
  name?: string;
}

export class UserRepository implements IUserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { id },
    });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { email },
    });
  }

  async findAll(params: FindAllParams): Promise<{ users: User[]; total: number }> {
    const { page, limit, search } = params;
    const skip = (page - 1) * limit;

    const where: Prisma.UserWhereInput = search
      ? {
          OR: [
            { name: { contains: search, mode: 'insensitive' } },
            { email: { contains: search, mode: 'insensitive' } },
          ],
        }
      : {};

    const [users, total] = await Promise.all([
      this.prisma.user.findMany({
        where,
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
      }),
      this.prisma.user.count({ where }),
    ]);

    return { users, total };
  }

  async create(data: CreateUserData): Promise<User> {
    return this.prisma.user.create({ data });
  }

  async update(id: string, data: UpdateUserData): Promise<User> {
    return this.prisma.user.update({
      where: { id },
      data,
    });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({ where: { id } });
  }
}
```

## Service Layer

```typescript
// services/users.service.ts
import { User } from '@prisma/client';
import { IUserRepository } from '../repositories/users.repository';
import { hashPassword, comparePasswords } from '../utils/password';
import { NotFoundError, ConflictError, UnauthorizedError } from '../utils/errors';

export interface IUserService {
  getUser(id: string): Promise<User>;
  getUsers(page: number, limit: number, search?: string): Promise<PaginatedUsers>;
  createUser(data: CreateUserDto): Promise<User>;
  updateUser(id: string, data: UpdateUserDto): Promise<User>;
  deleteUser(id: string): Promise<void>;
  authenticateUser(email: string, password: string): Promise<User>;
}

interface CreateUserDto {
  email: string;
  name: string;
  password: string;
}

interface UpdateUserDto {
  email?: string;
  name?: string;
}

interface PaginatedUsers {
  users: User[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export class UserService implements IUserService {
  constructor(private userRepository: IUserRepository) {}

  async getUser(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);

    if (!user) {
      throw new NotFoundError(`User with id ${id} not found`);
    }

    return user;
  }

  async getUsers(
    page: number,
    limit: number,
    search?: string
  ): Promise<PaginatedUsers> {
    const { users, total } = await this.userRepository.findAll({
      page,
      limit,
      search,
    });

    return {
      users,
      total,
      page,
      limit,
      pages: Math.ceil(total / limit),
    };
  }

  async createUser(data: CreateUserDto): Promise<User> {
    // Check for existing user
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) {
      throw new ConflictError('User with this email already exists');
    }

    // Hash password
    const hashedPassword = await hashPassword(data.password);

    // Create user
    return this.userRepository.create({
      email: data.email,
      name: data.name,
      hashedPassword,
    });
  }

  async updateUser(id: string, data: UpdateUserDto): Promise<User> {
    // Verify user exists
    await this.getUser(id);

    // Check email uniqueness if updating email
    if (data.email) {
      const existing = await this.userRepository.findByEmail(data.email);
      if (existing && existing.id !== id) {
        throw new ConflictError('Email already in use');
      }
    }

    return this.userRepository.update(id, data);
  }

  async deleteUser(id: string): Promise<void> {
    await this.getUser(id); // Verify exists
    await this.userRepository.delete(id);
  }

  async authenticateUser(email: string, password: string): Promise<User> {
    const user = await this.userRepository.findByEmail(email);

    if (!user) {
      throw new UnauthorizedError('Invalid credentials');
    }

    const isValid = await comparePasswords(password, user.hashedPassword);

    if (!isValid) {
      throw new UnauthorizedError('Invalid credentials');
    }

    return user;
  }
}
```

## Controller Layer

```typescript
// controllers/users.controller.ts
import { Request, Response, NextFunction } from 'express';
import { IUserService } from '../services/users.service';
import { CreateUserSchema, UpdateUserSchema } from '../schemas/users';

export class UserController {
  constructor(private userService: IUserService) {}

  getUsers = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 20;
      const search = req.query.search as string | undefined;

      const result = await this.userService.getUsers(page, limit, search);

      res.json(result);
    } catch (error) {
      next(error);
    }
  };

  getUser = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const { id } = req.params;
      const user = await this.userService.getUser(id);

      res.json({ data: user });
    } catch (error) {
      next(error);
    }
  };

  createUser = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const data = CreateUserSchema.parse(req.body);
      const user = await this.userService.createUser(data);

      res.status(201).json({ data: user });
    } catch (error) {
      next(error);
    }
  };

  updateUser = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const { id } = req.params;
      const data = UpdateUserSchema.parse(req.body);
      const user = await this.userService.updateUser(id, data);

      res.json({ data: user });
    } catch (error) {
      next(error);
    }
  };

  deleteUser = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const { id } = req.params;
      await this.userService.deleteUser(id);

      res.status(204).send();
    } catch (error) {
      next(error);
    }
  };
}
```

## Key Points

- **Services** - Business logic and orchestration
- **Repositories** - Database operations
- **Controllers** - HTTP handling only
- **Dependency injection** - Testability
- **Domain errors** - Better debugging

## Sources

- [Service Layer Pattern](https://martinfowler.com/eaaCatalog/serviceLayer.html) - Martin Fowler pattern catalog
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html) - Data access abstraction
- [Prisma ORM](https://www.prisma.io/docs) - Type-safe database client
- [TypeScript Express Guide](https://blog.logrocket.com/how-to-set-up-node-typescript-express/) - Express with TypeScript
- [Node.js Testing Best Practices](https://github.com/goldbergyoni/javascript-testing-best-practices) - Testing patterns
