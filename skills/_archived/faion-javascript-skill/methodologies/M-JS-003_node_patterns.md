# M-JS-003: Node.js Backend Patterns

## Metadata
- **Category:** Development/JavaScript
- **Difficulty:** Intermediate
- **Tags:** #dev, #javascript, #nodejs, #backend, #patterns, #methodology
- **Agent:** faion-code-agent

---

## Problem

Node.js backends can become unmaintainable spaghetti code. Async errors get swallowed, middleware chains become confusing, and scaling becomes impossible. You need patterns that keep code clean as projects grow.

## Promise

After this methodology, you will build Node.js backends that are scalable, maintainable, and production-ready. You will handle errors gracefully and structure code for teams.

## Overview

Modern Node.js uses ESM modules, async/await, and frameworks like Express, Fastify, or Hono. This methodology covers patterns applicable to any framework.

---

## Framework

### Step 1: Project Structure

```
src/
├── index.ts              # Entry point
├── app.ts                # App setup (middleware, routes)
├── config/
│   ├── index.ts          # Config aggregation
│   ├── env.ts            # Environment variables
│   └── database.ts       # Database config
├── routes/
│   ├── index.ts          # Route aggregation
│   ├── users.ts
│   └── products.ts
├── controllers/
│   ├── users.controller.ts
│   └── products.controller.ts
├── services/
│   ├── users.service.ts
│   └── products.service.ts
├── repositories/
│   ├── users.repository.ts
│   └── products.repository.ts
├── middleware/
│   ├── auth.ts
│   ├── error.ts
│   ├── validate.ts
│   └── rateLimit.ts
├── utils/
│   ├── logger.ts
│   ├── errors.ts
│   └── response.ts
├── types/
│   └── index.ts
└── tests/
    └── ...
```

### Step 2: Environment Configuration

```typescript
// config/env.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  REDIS_URL: z.string().url().optional(),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
});

const parsed = envSchema.safeParse(process.env);

if (!parsed.success) {
  console.error('Invalid environment variables:', parsed.error.flatten().fieldErrors);
  process.exit(1);
}

export const env = parsed.data;
```

### Step 3: Error Handling

```typescript
// utils/errors.ts
export class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public code?: string,
    public details?: unknown
  ) {
    super(message);
    this.name = 'AppError';
    Error.captureStackTrace(this, this.constructor);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id?: string) {
    super(404, `${resource}${id ? ` with id ${id}` : ''} not found`, 'NOT_FOUND');
  }
}

export class ValidationError extends AppError {
  constructor(details: unknown) {
    super(400, 'Validation failed', 'VALIDATION_ERROR', details);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(401, message, 'UNAUTHORIZED');
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Forbidden') {
    super(403, message, 'FORBIDDEN');
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super(409, message, 'CONFLICT');
  }
}
```

```typescript
// middleware/error.ts
import type { Request, Response, NextFunction } from 'express';
import { AppError } from '../utils/errors';
import { logger } from '../utils/logger';

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction
) {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      success: false,
      error: {
        code: err.code,
        message: err.message,
        details: err.details,
      },
    });
  }

  // Log unexpected errors
  logger.error('Unexpected error:', err);

  // Don't leak internal errors in production
  const message = process.env.NODE_ENV === 'production'
    ? 'Internal server error'
    : err.message;

  return res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message,
    },
  });
}
```

### Step 4: Controller-Service Pattern

```typescript
// controllers/users.controller.ts
import type { Request, Response, NextFunction } from 'express';
import { usersService } from '../services/users.service';
import { NotFoundError, ValidationError } from '../utils/errors';

export const usersController = {
  async getAll(req: Request, res: Response, next: NextFunction) {
    try {
      const { page = 1, limit = 10 } = req.query;
      const users = await usersService.findAll({
        page: Number(page),
        limit: Number(limit),
      });
      res.json({ success: true, data: users });
    } catch (error) {
      next(error);
    }
  },

  async getById(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await usersService.findById(req.params.id);
      if (!user) throw new NotFoundError('User', req.params.id);
      res.json({ success: true, data: user });
    } catch (error) {
      next(error);
    }
  },

  async create(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await usersService.create(req.body);
      res.status(201).json({ success: true, data: user });
    } catch (error) {
      next(error);
    }
  },

  async update(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await usersService.update(req.params.id, req.body);
      if (!user) throw new NotFoundError('User', req.params.id);
      res.json({ success: true, data: user });
    } catch (error) {
      next(error);
    }
  },

  async delete(req: Request, res: Response, next: NextFunction) {
    try {
      const deleted = await usersService.delete(req.params.id);
      if (!deleted) throw new NotFoundError('User', req.params.id);
      res.status(204).send();
    } catch (error) {
      next(error);
    }
  },
};
```

```typescript
// services/users.service.ts
import { usersRepository } from '../repositories/users.repository';
import { hashPassword, verifyPassword } from '../utils/crypto';
import { ConflictError, ValidationError } from '../utils/errors';
import type { CreateUserDTO, UpdateUserDTO, User } from '../types';

export const usersService = {
  async findAll(options: { page: number; limit: number }) {
    return usersRepository.findAll(options);
  },

  async findById(id: string): Promise<User | null> {
    return usersRepository.findById(id);
  },

  async findByEmail(email: string): Promise<User | null> {
    return usersRepository.findByEmail(email);
  },

  async create(data: CreateUserDTO): Promise<User> {
    // Check for existing user
    const existing = await this.findByEmail(data.email);
    if (existing) {
      throw new ConflictError('User with this email already exists');
    }

    // Hash password
    const hashedPassword = await hashPassword(data.password);

    // Create user
    return usersRepository.create({
      ...data,
      password: hashedPassword,
    });
  },

  async update(id: string, data: UpdateUserDTO): Promise<User | null> {
    if (data.password) {
      data.password = await hashPassword(data.password);
    }
    return usersRepository.update(id, data);
  },

  async delete(id: string): Promise<boolean> {
    return usersRepository.delete(id);
  },
};
```

### Step 5: Validation Middleware

```typescript
// middleware/validate.ts
import type { Request, Response, NextFunction } from 'express';
import { z, ZodSchema } from 'zod';
import { ValidationError } from '../utils/errors';

type ValidationTarget = 'body' | 'query' | 'params';

export function validate(schema: ZodSchema, target: ValidationTarget = 'body') {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req[target]);

    if (!result.success) {
      throw new ValidationError(result.error.flatten());
    }

    req[target] = result.data;
    next();
  };
}

// Usage in routes
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(2).max(100),
});

router.post('/users', validate(createUserSchema), usersController.create);
```

### Step 6: Async Handler Wrapper

```typescript
// utils/asyncHandler.ts
import type { Request, Response, NextFunction, RequestHandler } from 'express';

type AsyncHandler = (
  req: Request,
  res: Response,
  next: NextFunction
) => Promise<void>;

export function asyncHandler(fn: AsyncHandler): RequestHandler {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// Usage - cleaner controllers
export const usersController = {
  getAll: asyncHandler(async (req, res) => {
    const users = await usersService.findAll(req.query);
    res.json({ success: true, data: users });
  }),

  getById: asyncHandler(async (req, res) => {
    const user = await usersService.findById(req.params.id);
    if (!user) throw new NotFoundError('User', req.params.id);
    res.json({ success: true, data: user });
  }),
};
```

---

## Templates

### Express App Setup

```typescript
// app.ts
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import { routes } from './routes';
import { errorHandler } from './middleware/error';
import { requestLogger } from './middleware/logging';

const app = express();

// Security
app.use(helmet());
app.use(cors({ origin: process.env.CORS_ORIGIN }));

// Parsing
app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ extended: true }));

// Compression
app.use(compression());

// Logging
app.use(requestLogger);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Routes
app.use('/api/v1', routes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: { code: 'NOT_FOUND', message: 'Route not found' },
  });
});

// Error handler
app.use(errorHandler);

export { app };
```

### Graceful Shutdown

```typescript
// index.ts
import { app } from './app';
import { env } from './config/env';
import { logger } from './utils/logger';
import { closeDatabase } from './config/database';

const server = app.listen(env.PORT, () => {
  logger.info(`Server running on port ${env.PORT}`);
});

// Graceful shutdown
const shutdown = async (signal: string) => {
  logger.info(`${signal} received. Shutting down gracefully...`);

  server.close(async () => {
    logger.info('HTTP server closed');
    await closeDatabase();
    logger.info('Database connection closed');
    process.exit(0);
  });

  // Force shutdown after 10 seconds
  setTimeout(() => {
    logger.error('Forced shutdown after timeout');
    process.exit(1);
  }, 10000);
};

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

// Handle uncaught errors
process.on('uncaughtException', (error) => {
  logger.error('Uncaught exception:', error);
  process.exit(1);
});

process.on('unhandledRejection', (reason) => {
  logger.error('Unhandled rejection:', reason);
  process.exit(1);
});
```

---

## Examples

### Rate Limiting

```typescript
// middleware/rateLimit.ts
import rateLimit from 'express-rate-limit';

export const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    success: false,
    error: { code: 'RATE_LIMIT', message: 'Too many requests' },
  },
});

export const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5, // 5 login attempts
  message: {
    success: false,
    error: { code: 'RATE_LIMIT', message: 'Too many login attempts' },
  },
});
```

### Logger Setup

```typescript
// utils/logger.ts
import pino from 'pino';
import { env } from '../config/env';

export const logger = pino({
  level: env.LOG_LEVEL,
  transport:
    env.NODE_ENV === 'development'
      ? { target: 'pino-pretty', options: { colorize: true } }
      : undefined,
});
```

---

## Common Mistakes

1. **Not handling async errors** - Use asyncHandler or try/catch in every route
2. **Leaking stack traces** - Hide internal errors in production
3. **No input validation** - Always validate before processing
4. **Synchronous operations** - Use async alternatives for I/O
5. **Not closing connections** - Implement graceful shutdown

---

## Checklist

- [ ] Environment variables validated at startup
- [ ] Custom error classes for business errors
- [ ] Global error handler catches all errors
- [ ] Input validation on all routes
- [ ] Logging configured for all environments
- [ ] Graceful shutdown implemented
- [ ] Rate limiting on sensitive endpoints
- [ ] Security headers (helmet) enabled

---

## Next Steps

- M-JS-004: TypeScript Patterns
- M-JS-005: Testing with Jest/Vitest
- M-DO-003: Docker Basics

---

*Methodology M-JS-003 v1.0*
