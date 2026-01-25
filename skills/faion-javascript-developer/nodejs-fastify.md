# Fastify Framework Patterns

**High-performance TypeScript-first Node.js framework**

## When to Use

- Performance-critical APIs
- TypeScript-first projects
- Schema validation priority
- Microservices architecture

## Key Principles

1. **Plugin architecture** - Composable plugins
2. **Schema validation** - JSON Schema/TypeBox
3. **Type safety** - TypeScript-first
4. **Performance** - High throughput
5. **Graceful shutdown** - Clean termination

### Fastify Application Setup

```typescript
// app.ts
import Fastify, { FastifyInstance } from 'fastify';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import rateLimit from '@fastify/rate-limit';
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox';
import { userRoutes } from './routes/users.routes';
import { authRoutes } from './routes/auth.routes';
import { errorHandler } from './plugins/errorHandler';
import { config } from './config';

export async function createApp(): Promise<FastifyInstance> {
  const app = Fastify({
    logger: {
      level: config.logLevel,
      transport: config.isDevelopment
        ? { target: 'pino-pretty' }
        : undefined,
    },
  }).withTypeProvider<TypeBoxTypeProvider>();

  // Plugins
  await app.register(helmet);
  await app.register(cors, {
    origin: config.corsOrigins,
    credentials: true,
  });
  await app.register(rateLimit, {
    max: 100,
    timeWindow: '15 minutes',
  });

  // Custom error handler
  app.setErrorHandler(errorHandler);

  // Health check
  app.get('/health', async () => ({
    status: 'ok',
    timestamp: new Date().toISOString(),
  }));

  // Routes
  await app.register(authRoutes, { prefix: '/api/v1/auth' });
  await app.register(userRoutes, { prefix: '/api/v1/users' });

  return app;
}

// server.ts
import { createApp } from './app';
import { config } from './config';

async function start() {
  const app = await createApp();

  try {
    await app.listen({ port: config.port, host: '0.0.0.0' });
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
}

start();
```

### Fastify Routes with TypeBox

```typescript
// routes/users.routes.ts
import { FastifyPluginAsync } from 'fastify';
import { Type, Static } from '@sinclair/typebox';

const UserSchema = Type.Object({
  id: Type.String(),
  email: Type.String({ format: 'email' }),
  name: Type.String(),
  createdAt: Type.String({ format: 'date-time' }),
});

const CreateUserSchema = Type.Object({
  email: Type.String({ format: 'email' }),
  name: Type.String({ minLength: 1, maxLength: 100 }),
  password: Type.String({ minLength: 8 }),
});

const UpdateUserSchema = Type.Partial(
  Type.Object({
    email: Type.String({ format: 'email' }),
    name: Type.String({ minLength: 1, maxLength: 100 }),
  })
);

const ParamsSchema = Type.Object({
  id: Type.String(),
});

const QuerySchema = Type.Object({
  page: Type.Optional(Type.Number({ minimum: 1, default: 1 })),
  limit: Type.Optional(Type.Number({ minimum: 1, maximum: 100, default: 20 })),
  search: Type.Optional(Type.String()),
});

type User = Static<typeof UserSchema>;
type CreateUser = Static<typeof CreateUserSchema>;
type UpdateUser = Static<typeof UpdateUserSchema>;

export const userRoutes: FastifyPluginAsync = async (app) => {
  // GET /users
  app.get<{
    Querystring: Static<typeof QuerySchema>;
    Reply: { users: User[]; total: number; page: number; limit: number };
  }>(
    '/',
    {
      schema: {
        querystring: QuerySchema,
        response: {
          200: Type.Object({
            users: Type.Array(UserSchema),
            total: Type.Number(),
            page: Type.Number(),
            limit: Type.Number(),
          }),
        },
      },
      preHandler: [app.authenticate],
    },
    async (request, reply) => {
      const { page = 1, limit = 20, search } = request.query;
      const result = await app.userService.getUsers(page, limit, search);
      return result;
    }
  );

  // GET /users/:id
  app.get<{
    Params: Static<typeof ParamsSchema>;
    Reply: { data: User };
  }>(
    '/:id',
    {
      schema: {
        params: ParamsSchema,
        response: {
          200: Type.Object({ data: UserSchema }),
        },
      },
      preHandler: [app.authenticate],
    },
    async (request) => {
      const user = await app.userService.getUser(request.params.id);
      return { data: user };
    }
  );

  // POST /users
  app.post<{
    Body: CreateUser;
    Reply: { data: User };
  }>(
    '/',
    {
      schema: {
        body: CreateUserSchema,
        response: {
          201: Type.Object({ data: UserSchema }),
        },
      },
    },
    async (request, reply) => {
      const user = await app.userService.createUser(request.body);
      reply.status(201);
      return { data: user };
    }
  );

  // PATCH /users/:id
  app.patch<{
    Params: Static<typeof ParamsSchema>;
    Body: UpdateUser;
    Reply: { data: User };
  }>(
    '/:id',
    {
      schema: {
        params: ParamsSchema,
        body: UpdateUserSchema,
        response: {
          200: Type.Object({ data: UserSchema }),
        },
      },
      preHandler: [app.authenticate],
    },
    async (request) => {
      const user = await app.userService.updateUser(
        request.params.id,
        request.body
      );
      return { data: user };
    }
  );

  // DELETE /users/:id
  app.delete<{
    Params: Static<typeof ParamsSchema>;
  }>(
    '/:id',
    {
      schema: {
        params: ParamsSchema,
        response: {
          204: Type.Null(),
        },
      },
      preHandler: [app.authenticate],
    },
    async (request, reply) => {
      await app.userService.deleteUser(request.params.id);
      reply.status(204).send();
    }
  );
};
```

### Fastify Authentication Plugin

```typescript
// plugins/auth.ts
import { FastifyPluginAsync, FastifyRequest } from 'fastify';
import fp from 'fastify-plugin';
import jwt from 'jsonwebtoken';

declare module 'fastify' {
  interface FastifyInstance {
    authenticate: (request: FastifyRequest) => Promise<void>;
  }
  interface FastifyRequest {
    user: { userId: string; email: string };
  }
}

const authPlugin: FastifyPluginAsync = async (app) => {
  app.decorate('authenticate', async (request: FastifyRequest) => {
    const authHeader = request.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
      throw app.httpErrors.unauthorized('Missing authorization');
    }

    try {
      const token = authHeader.slice(7);
      const payload = jwt.verify(token, app.config.jwtSecret);
      request.user = payload as { userId: string; email: string };
    } catch {
      throw app.httpErrors.unauthorized('Invalid token');
    }
  });
};

export default fp(authPlugin, { name: 'auth' });
```

### Fastify Custom Plugin

```typescript
// plugins/database.ts
import { FastifyPluginAsync } from 'fastify';
import fp from 'fastify-plugin';
import { Pool } from 'pg';

declare module 'fastify' {
  interface FastifyInstance {
    db: Pool;
  }
}

const databasePlugin: FastifyPluginAsync = async (app) => {
  const pool = new Pool({
    host: app.config.dbHost,
    port: app.config.dbPort,
    database: app.config.dbName,
    user: app.config.dbUser,
    password: app.config.dbPassword,
  });

  // Test connection
  await pool.query('SELECT 1');
  app.log.info('Database connected');

  // Decorate instance with pool
  app.decorate('db', pool);

  // Close pool on shutdown
  app.addHook('onClose', async (instance) => {
    await instance.db.end();
    instance.log.info('Database connection closed');
  });
};

export default fp(databasePlugin, { name: 'database' });
```

### Error Handler Plugin

```typescript
// plugins/errorHandler.ts
import { FastifyError, FastifyReply, FastifyRequest } from 'fastify';

export function errorHandler(
  error: FastifyError,
  request: FastifyRequest,
  reply: FastifyReply
) {
  request.log.error(error);

  // Validation errors
  if (error.validation) {
    return reply.status(400).send({
      error: 'Validation Error',
      message: error.message,
      details: error.validation,
    });
  }

  // HTTP errors
  if (error.statusCode) {
    return reply.status(error.statusCode).send({
      error: error.name,
      message: error.message,
    });
  }

  // Unknown errors
  return reply.status(500).send({
    error: 'Internal Server Error',
    message: 'An unexpected error occurred',
  });
}
```

## Anti-patterns

### Avoid: Not Awaiting Plugin Registration

```typescript
// BAD
export async function createApp() {
  const app = Fastify();
  app.register(cors); // Missing await
  app.register(helmet); // Missing await
  return app;
}

// GOOD
export async function createApp() {
  const app = Fastify();
  await app.register(cors);
  await app.register(helmet);
  return app;
}
```

### Avoid: Missing Type Safety

```typescript
// BAD - No type safety
app.get('/users/:id', async (request, reply) => {
  const id = request.params.id; // any type
  const user = await getUser(id);
  return user;
});

// GOOD - Full type safety
app.get<{
  Params: { id: string };
  Reply: { data: User };
}>(
  '/:id',
  {
    schema: {
      params: Type.Object({ id: Type.String() }),
      response: {
        200: Type.Object({ data: UserSchema }),
      },
    },
  },
  async (request) => {
    const id = request.params.id; // string type
    const user = await getUser(id);
    return { data: user };
  }
);
```

## Sources

- [Fastify Documentation](https://fastify.dev/docs/latest/) - Official docs
- [TypeBox](https://github.com/sinclairzx81/typebox) - Type-safe schema validation
- [Fastify Plugins Ecosystem](https://fastify.dev/ecosystem/) - Plugin directory
- [Fastify Best Practices](https://fastify.dev/docs/latest/Guides/Getting-Started/) - Getting started guide
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices) - Node.js patterns
