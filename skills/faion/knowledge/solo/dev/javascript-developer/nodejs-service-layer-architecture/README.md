# Node.js Service Layer Architecture

**Separation of concerns for enterprise Node.js**

## When to Use

- REST APIs (Express/Fastify)
- Complex business logic
- High testability requirements
- Microservices architecture
- Clear layer separation needed

## Key Principles

1. **Thin controllers** - HTTP only
2. **Fat services** - Business logic
3. **Repository pattern** - Data access
4. **Dependency injection** - Testability
5. **Single responsibility** - One job per layer

### Layer Responsibilities

- **Controllers**: HTTP handling, validation (Request → Response)
- **Services**: Business logic, orchestration
- **Repositories**: Data access, queries
- **Database**: Data storage

### Project Structure

```
src/
├── app.ts                  # Express app setup
├── server.ts               # Server entry point
├── config/
│   ├── index.ts           # Configuration
│   └── database.ts        # DB connection
│
├── controllers/
│   ├── index.ts
│   ├── users.controller.ts
│   └── orders.controller.ts
│
├── services/
│   ├── index.ts
│   ├── users.service.ts
│   └── orders.service.ts
│
├── repositories/
│   ├── index.ts
│   ├── users.repository.ts
│   └── orders.repository.ts
│
├── models/
│   ├── user.model.ts
│   └── order.model.ts
│
├── middleware/
│   ├── auth.ts
│   ├── errorHandler.ts
│   └── validate.ts
│
├── routes/
│   ├── index.ts
│   └── users.routes.ts
│
├── types/
│   └── index.ts
│
└── utils/
    ├── errors.ts
    └── logger.ts
```

### Dependency Injection

```typescript
// container.ts
import { PrismaClient } from '@prisma/client';
import { UserRepository } from './repositories/users.repository';
import { UserService } from './services/users.service';
import { UserController } from './controllers/users.controller';

// Database client
const prisma = new PrismaClient();

// Repositories
const userRepository = new UserRepository(prisma);

// Services
const userService = new UserService(userRepository);

// Controllers
const userController = new UserController(userService);

export { prisma, userRepository, userService, userController };

// routes/users.routes.ts
import { Router } from 'express';
import { userController } from '../container';
import { authenticate } from '../middleware/auth';

const router = Router();

router.get('/', authenticate, userController.getUsers);
router.get('/:id', authenticate, userController.getUser);
router.post('/', userController.createUser);
router.patch('/:id', authenticate, userController.updateUser);
router.delete('/:id', authenticate, userController.deleteUser);

export default router;
```

### Error Handling

```typescript
// utils/errors.ts
export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code: string = 'INTERNAL_ERROR',
    public isOperational: boolean = true
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class NotFoundError extends AppError {
  constructor(message = 'Resource not found') {
    super(message, 404, 'NOT_FOUND');
  }
}

export class ConflictError extends AppError {
  constructor(message = 'Resource conflict') {
    super(message, 409, 'CONFLICT');
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
  }
}

export class ValidationError extends AppError {
  constructor(
    message = 'Validation failed',
    public errors: Record<string, string[]> = {}
  ) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}

// middleware/errorHandler.ts
import { ErrorRequestHandler } from 'express';
import { ZodError } from 'zod';
import { AppError } from '../utils/errors';
import { logger } from '../utils/logger';

export const errorHandler: ErrorRequestHandler = (err, req, res, _next) => {
  logger.error({ err, path: req.path, method: req.method });

  if (err instanceof ZodError) {
    return res.status(400).json({
      error: 'Validation failed',
      code: 'VALIDATION_ERROR',
      details: err.flatten().fieldErrors,
    });
  }

  if (err instanceof AppError && err.isOperational) {
    return res.status(err.statusCode).json({
      error: err.message,
      code: err.code,
    });
  }

  // Unknown error
  return res.status(500).json({
    error: 'Internal server error',
    code: 'INTERNAL_ERROR',
  });
};
```

## Anti-patterns

### Avoid: Business Logic in Controllers

```typescript
// BAD
app.post('/users', async (req, res) => {
  const existing = await prisma.user.findUnique({ where: { email: req.body.email }});
  if (existing) return res.status(409).json({ error: 'Exists' });
  const hashedPassword = await bcrypt.hash(req.body.password, 10);
  const user = await prisma.user.create({ data: { ...req.body, hashedPassword }});
  res.json(user);
});

// GOOD - delegate to service
app.post('/users', async (req, res, next) => {
  try {
    const user = await userService.createUser(req.body);
    res.json(user);
  } catch (error) {
    next(error);
  }
});
```

### Avoid: Direct Database Access in Services

```typescript
// BAD - service uses Prisma directly
class UserService {
  async getUser(id: string) {
    return prisma.user.findUnique({ where: { id }});
  }
}

// GOOD - service uses repository
class UserService {
  constructor(private userRepository: IUserRepository) {}

  async getUser(id: string) {
    return this.userRepository.findById(id);
  }
}
```

## Testing Strategy

### Unit Tests

```typescript
// services/users.service.test.ts
describe('UserService', () => {
  let userService: UserService;
  let mockRepository: jest.Mocked<IUserRepository>;

  beforeEach(() => {
    mockRepository = {
      findById: jest.fn(),
      findByEmail: jest.fn(),
      findAll: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
    };
    userService = new UserService(mockRepository);
  });

  describe('createUser', () => {
    it('should create user with hashed password', async () => {
      mockRepository.findByEmail.mockResolvedValue(null);
      mockRepository.create.mockResolvedValue(mockUser);

      const result = await userService.createUser({
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123',
      });

      expect(result).toEqual(mockUser);
      expect(mockRepository.create).toHaveBeenCalledWith(
        expect.objectContaining({
          email: 'test@example.com',
          name: 'Test User',
          hashedPassword: expect.any(String),
        })
      );
    });

    it('should throw ConflictError if email exists', async () => {
      mockRepository.findByEmail.mockResolvedValue(mockUser);

      await expect(
        userService.createUser({
          email: 'existing@example.com',
          name: 'Test',
          password: 'pass',
        })
      ).rejects.toThrow(ConflictError);
    });
  });
});
```


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Service layer design | sonnet | Architecture planning |
| Dependency injection setup | sonnet | DI pattern expertise |

## Sources

- [Clean Architecture - Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - Architecture principles
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices) - Node.js patterns
- [Prisma Documentation](https://www.prisma.io/docs) - Type-safe ORM
- [Dependency Injection in Node.js](https://khalilstemmler.com/articles/software-design-architecture/dependency-injection/) - DI patterns
- [Service Layer Pattern](https://martinfowler.com/eaaCatalog/serviceLayer.html) - Martin Fowler's pattern catalog
