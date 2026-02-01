# Node.js Patterns

**Backend patterns for Express and modern Node.js**

---

## Express Application Structure

```
src/
├── app.ts               # Express app setup
├── server.ts            # Server entry point
├── config/
│   └── env.ts           # Environment variables
├── routes/
│   ├── index.ts         # Route aggregator
│   ├── users.ts
│   └── products.ts
├── controllers/
│   ├── users.controller.ts
│   └── products.controller.ts
├── services/
│   ├── users.service.ts
│   └── products.service.ts
├── middleware/
│   ├── auth.ts
│   ├── errorHandler.ts
│   └── validate.ts
├── models/
│   └── user.model.ts
├── types/
│   └── express.d.ts     # Express type extensions
└── utils/
    ├── logger.ts
    └── errors.ts
```

---

## Express Setup

```typescript
// app.ts
import express, { type Express } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { errorHandler } from './middleware/errorHandler';
import { requestLogger } from './middleware/requestLogger';
import routes from './routes';

export function createApp(): Express {
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

  // Routes
  app.use('/api/v1', routes);

  // Health check
  app.get('/health', (_req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
  });

  // Error handling (MUST be last)
  app.use(errorHandler);

  return app;
}
```

---

## Middleware Pattern

```typescript
// middleware/auth.ts
import { type RequestHandler } from 'express';
import { verifyToken } from '../utils/jwt';
import { UnauthorizedError } from '../utils/errors';

export const authenticate: RequestHandler = async (req, _res, next) => {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
      throw new UnauthorizedError('Missing authorization header');
    }

    const token = authHeader.slice(7);
    const payload = await verifyToken(token);

    req.user = payload;
    next();
  } catch (error) {
    next(error);
  }
};

// Extend Express Request type
declare global {
  namespace Express {
    interface Request {
      user?: TokenPayload;
    }
  }
}
```

---

## Controller Pattern

```typescript
// controllers/users.controller.ts
import { type Request, type Response, type NextFunction } from 'express';
import * as usersService from '../services/users.service';
import { CreateUserSchema, UpdateUserSchema } from '../schemas/users';

export async function getUsers(
  req: Request,
  res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    const users = await usersService.findAll();
    res.json({ data: users });
  } catch (error) {
    next(error);
  }
}

export async function createUser(
  req: Request,
  res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    const data = CreateUserSchema.parse(req.body);
    const user = await usersService.create(data);
    res.status(201).json({ data: user });
  } catch (error) {
    next(error);
  }
}
```

---

## Error Handling

```typescript
// utils/errors.ts
export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code: string = 'INTERNAL_ERROR',
    public isOperational: boolean = true,
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

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
  }
}

export class ValidationError extends AppError {
  constructor(
    message = 'Validation failed',
    public errors: Record<string, string[]> = {},
  ) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}

// middleware/errorHandler.ts
import { type ErrorRequestHandler } from 'express';
import { AppError } from '../utils/errors';
import { ZodError } from 'zod';
import { logger } from '../utils/logger';

export const errorHandler: ErrorRequestHandler = (err, _req, res, _next) => {
  // Log error
  logger.error(err);

  // Zod validation error
  if (err instanceof ZodError) {
    res.status(400).json({
      error: 'Validation failed',
      code: 'VALIDATION_ERROR',
      details: err.flatten().fieldErrors,
    });
    return;
  }

  // Known operational error
  if (err instanceof AppError && err.isOperational) {
    res.status(err.statusCode).json({
      error: err.message,
      code: err.code,
    });
    return;
  }

  // Unknown error - don't leak details
  res.status(500).json({
    error: 'Internal server error',
    code: 'INTERNAL_ERROR',
  });
};
```

---

## Logging with Pino

```typescript
// utils/logger.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty', options: { colorize: true } }
    : undefined,
  formatters: {
    level: (label) => ({ level: label }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

// Request logger middleware
import { type RequestHandler } from 'express';
import { randomUUID } from 'crypto';

export const requestLogger: RequestHandler = (req, res, next) => {
  const requestId = randomUUID();
  req.id = requestId;

  const start = Date.now();

  res.on('finish', () => {
    logger.info({
      requestId,
      method: req.method,
      url: req.originalUrl,
      statusCode: res.statusCode,
      duration: Date.now() - start,
    });
  });

  next();
};
```

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Event emitter patterns | sonnet | Async pattern expertise |
| Stream handling | sonnet | Data flow design |
| Worker threads usage | sonnet | Concurrency decisions |

## Sources

- [Node.js Documentation](https://nodejs.org/docs/) - Official Node.js docs
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices) - Comprehensive guide (90k+ stars)
- [Express.js](https://expressjs.com/) - Minimalist web framework
- [Pino Logger](https://getpino.io/) - Fast logging library
- [Error Handling in Node.js](https://nodejs.org/en/learn/asynchronous-work/javascript-asynchronous-programming-and-callbacks) - Async patterns
