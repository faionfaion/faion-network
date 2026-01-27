# Code Templates by Architectural Pattern

Ready-to-use templates for Clean, Hexagonal, Onion, and DDD implementations.

## Clean Architecture Templates

### Entity Template

```typescript
// src/domain/entities/{EntityName}.ts

import { DomainEvent } from '../events/DomainEvent';

export interface {EntityName}Props {
  id: string;
  // ... other properties
}

export class {EntityName} {
  private readonly id: string;
  private readonly events: DomainEvent[] = [];

  private constructor(props: {EntityName}Props) {
    this.id = props.id;
    // ... initialize other properties
  }

  // Factory method for creation
  static create(props: Omit<{EntityName}Props, 'id'>): {EntityName} {
    const id = crypto.randomUUID();
    const entity = new {EntityName}({ id, ...props });
    // entity.addEvent(new {EntityName}Created(id));
    return entity;
  }

  // Factory method for reconstitution (from DB)
  static reconstitute(props: {EntityName}Props): {EntityName} {
    return new {EntityName}(props);
  }

  // Getters
  get entityId(): string {
    return this.id;
  }

  // Domain behavior methods
  // ...

  // Event handling
  protected addEvent(event: DomainEvent): void {
    this.events.push(event);
  }

  pullEvents(): DomainEvent[] {
    const events = [...this.events];
    this.events.length = 0;
    return events;
  }
}
```

### Value Object Template

```typescript
// src/domain/value-objects/{ValueObjectName}.ts

export interface {ValueObjectName}Props {
  // ... value properties
}

export class {ValueObjectName} {
  private constructor(private readonly props: {ValueObjectName}Props) {
    this.validate();
  }

  static create(props: {ValueObjectName}Props): {ValueObjectName} {
    return new {ValueObjectName}(props);
  }

  private validate(): void {
    // Add validation logic
    // throw new Error('Invalid {ValueObjectName}') if invalid
  }

  // Getters for individual properties
  // ...

  // Value object equality
  equals(other: {ValueObjectName}): boolean {
    if (!(other instanceof {ValueObjectName})) return false;
    return JSON.stringify(this.props) === JSON.stringify(other.props);
  }

  // Immutable transformation methods
  // ...

  toString(): string {
    return JSON.stringify(this.props);
  }
}
```

### Repository Interface Template

```typescript
// src/domain/repositories/I{EntityName}Repository.ts

import { {EntityName} } from '../entities/{EntityName}';

export interface I{EntityName}Repository {
  save(entity: {EntityName}): Promise<void>;
  findById(id: string): Promise<{EntityName} | null>;
  findAll(): Promise<{EntityName}[]>;
  delete(id: string): Promise<void>;
  // Add domain-specific query methods
  // findByStatus(status: Status): Promise<{EntityName}[]>;
}
```

### Use Case Template

```typescript
// src/application/use-cases/{UseCaseName}.ts

import { I{EntityName}Repository } from '../../domain/repositories/I{EntityName}Repository';
import { {EntityName} } from '../../domain/entities/{EntityName}';
import { {UseCaseName}Request } from '../dto/{UseCaseName}Request';
import { {UseCaseName}Response } from '../dto/{UseCaseName}Response';

export class {UseCaseName} {
  constructor(
    private readonly repository: I{EntityName}Repository,
    // ... other dependencies
  ) {}

  async execute(request: {UseCaseName}Request): Promise<{UseCaseName}Response> {
    // 1. Validate request
    this.validate(request);

    // 2. Business logic
    const entity = {EntityName}.create({
      // ... map from request
    });

    // 3. Persist
    await this.repository.save(entity);

    // 4. Return response DTO
    return {UseCaseName}Response.from(entity);
  }

  private validate(request: {UseCaseName}Request): void {
    // Add validation logic
  }
}
```

### DTO Templates

```typescript
// src/application/dto/{UseCaseName}Request.ts

export interface {UseCaseName}Request {
  // Input properties
}

// src/application/dto/{UseCaseName}Response.ts

import { {EntityName} } from '../../domain/entities/{EntityName}';

export interface {UseCaseName}Response {
  // Output properties
}

export const {UseCaseName}Response = {
  from(entity: {EntityName}): {UseCaseName}Response {
    return {
      // Map entity to response
    };
  }
};
```

### Repository Implementation Template

```typescript
// src/infrastructure/persistence/Postgres{EntityName}Repository.ts

import { Pool } from 'pg';
import { I{EntityName}Repository } from '../../domain/repositories/I{EntityName}Repository';
import { {EntityName} } from '../../domain/entities/{EntityName}';

export class Postgres{EntityName}Repository implements I{EntityName}Repository {
  constructor(private readonly pool: Pool) {}

  async save(entity: {EntityName}): Promise<void> {
    await this.pool.query(
      `INSERT INTO {table_name} (id, /* columns */)
       VALUES ($1, /* params */)
       ON CONFLICT (id) DO UPDATE SET /* updates */`,
      [entity.entityId, /* values */]
    );
  }

  async findById(id: string): Promise<{EntityName} | null> {
    const result = await this.pool.query(
      'SELECT * FROM {table_name} WHERE id = $1',
      [id]
    );
    if (result.rows.length === 0) return null;
    return this.toDomain(result.rows[0]);
  }

  async findAll(): Promise<{EntityName}[]> {
    const result = await this.pool.query('SELECT * FROM {table_name}');
    return result.rows.map(row => this.toDomain(row));
  }

  async delete(id: string): Promise<void> {
    await this.pool.query('DELETE FROM {table_name} WHERE id = $1', [id]);
  }

  private toDomain(row: any): {EntityName} {
    return {EntityName}.reconstitute({
      id: row.id,
      // ... map other fields
    });
  }
}
```

### Controller Template

```typescript
// src/presentation/api/{EntityName}Controller.ts

import { Request, Response, NextFunction } from 'express';
import { {UseCaseName} } from '../../application/use-cases/{UseCaseName}';

export class {EntityName}Controller {
  constructor(
    private readonly {useCaseName}: {UseCaseName},
    // ... other use cases
  ) {}

  async create(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const result = await this.{useCaseName}.execute(req.body);
      res.status(201).json(result);
    } catch (error) {
      next(error);
    }
  }

  // ... other methods
}
```

---

## Hexagonal Architecture Templates

### Port Interface Template (Inbound)

```typescript
// src/core/ports/inbound/{UseCaseName}Port.ts

export interface {UseCaseName}Command {
  // Input data
}

export interface {UseCaseName}Result {
  // Output data
}

export interface {UseCaseName}Port {
  execute(command: {UseCaseName}Command): Promise<{UseCaseName}Result>;
}
```

### Port Interface Template (Outbound)

```typescript
// src/core/ports/outbound/{ResourceName}Port.ts

import { {EntityName} } from '../../domain/{EntityName}';

export interface {ResourceName}Port {
  // Define operations the core needs from external world
  save(entity: {EntityName}): Promise<void>;
  findById(id: string): Promise<{EntityName} | null>;
  // ...
}
```

### Core Service Template

```typescript
// src/core/services/{EntityName}Service.ts

import { {UseCaseName}Port, {UseCaseName}Command, {UseCaseName}Result }
  from '../ports/inbound/{UseCaseName}Port';
import { {RepositoryName}Port } from '../ports/outbound/{RepositoryName}Port';
import { {EntityName} } from '../domain/{EntityName}';

export class {EntityName}Service implements {UseCaseName}Port {
  constructor(
    private readonly repository: {RepositoryName}Port,
    // ... other outbound ports
  ) {}

  async execute(command: {UseCaseName}Command): Promise<{UseCaseName}Result> {
    // Business logic using domain objects
    const entity = {EntityName}.create(/* ... */);
    await this.repository.save(entity);
    return { /* result */ };
  }
}
```

### Primary Adapter Template (REST)

```typescript
// src/adapters/inbound/rest/{EntityName}Controller.ts

import { Request, Response } from 'express';
import { {UseCaseName}Port } from '../../../core/ports/inbound/{UseCaseName}Port';

export class {EntityName}Controller {
  constructor(private readonly port: {UseCaseName}Port) {}

  async handle{UseCaseName}(req: Request, res: Response): Promise<void> {
    const result = await this.port.execute({
      // Map from HTTP request to command
    });
    res.status(201).json(result);
  }
}
```

### Secondary Adapter Template

```typescript
// src/adapters/outbound/persistence/{EntityName}RepositoryAdapter.ts

import { {RepositoryName}Port } from '../../../core/ports/outbound/{RepositoryName}Port';
import { {EntityName} } from '../../../core/domain/{EntityName}';
import { PrismaClient } from '@prisma/client';

export class {EntityName}RepositoryAdapter implements {RepositoryName}Port {
  constructor(private readonly prisma: PrismaClient) {}

  async save(entity: {EntityName}): Promise<void> {
    await this.prisma.{tableName}.upsert({
      where: { id: entity.id },
      update: this.toPersistence(entity),
      create: this.toPersistence(entity),
    });
  }

  async findById(id: string): Promise<{EntityName} | null> {
    const record = await this.prisma.{tableName}.findUnique({
      where: { id },
    });
    return record ? this.toDomain(record) : null;
  }

  private toPersistence(entity: {EntityName}): any {
    return { /* map to DB model */ };
  }

  private toDomain(record: any): {EntityName} {
    return {EntityName}.reconstitute({ /* map from DB model */ });
  }
}
```

---

## DDD Templates

### Aggregate Root Template

```typescript
// src/domain/aggregates/{AggregateName}/{AggregateName}.ts

import { AggregateRoot } from '../../shared/AggregateRoot';
import { {AggregateName}Id } from './{AggregateName}Id';
import { {DomainEvent} } from '../../events/{DomainEvent}';

interface {AggregateName}Props {
  // Aggregate properties
}

export class {AggregateName} extends AggregateRoot<{AggregateName}Id> {
  // Private properties
  private status: {AggregateName}Status;

  private constructor(id: {AggregateName}Id, props: {AggregateName}Props) {
    super(id);
    // Initialize properties
  }

  // Factory for new aggregates
  static create(props: Omit<{AggregateName}Props, 'status'>): {AggregateName} {
    const id = {AggregateName}Id.generate();
    const aggregate = new {AggregateName}(id, {
      ...props,
      status: {AggregateName}Status.INITIAL,
    });
    aggregate.addDomainEvent(new {AggregateName}Created(id));
    return aggregate;
  }

  // Factory for reconstitution
  static reconstitute(
    id: {AggregateName}Id,
    props: {AggregateName}Props
  ): {AggregateName} {
    return new {AggregateName}(id, props);
  }

  // Domain behavior (enforces invariants)
  public doSomething(): void {
    // Guard: check invariants
    if (!this.canDoSomething()) {
      throw new DomainException('Cannot do something in current state');
    }

    // Execute business logic
    this.status = {AggregateName}Status.SOMETHING_DONE;

    // Raise domain event
    this.addDomainEvent(new SomethingDone(this.id));
  }

  private canDoSomething(): boolean {
    return this.status === {AggregateName}Status.INITIAL;
  }
}
```

### Domain Event Template

```typescript
// src/domain/events/{EventName}.ts

import { DomainEvent } from '../shared/DomainEvent';

export class {EventName} extends DomainEvent {
  readonly aggregateId: string;
  readonly occurredOn: Date;
  // Event-specific data

  constructor(aggregateId: string, /* event data */) {
    super();
    this.aggregateId = aggregateId;
    this.occurredOn = new Date();
    // Initialize event data
  }

  get eventName(): string {
    return '{EventName}';
  }
}
```

### Domain Service Template

```typescript
// src/domain/services/{ServiceName}Service.ts

import { {EntityA} } from '../entities/{EntityA}';
import { {EntityB} } from '../entities/{EntityB}';

/**
 * Domain service for operations spanning multiple aggregates
 * or complex domain logic that doesn't belong to a single entity.
 */
export class {ServiceName}Service {
  // Pure domain logic - no infrastructure dependencies

  calculate{Something}(entityA: {EntityA}, entityB: {EntityB}): Result {
    // Cross-entity business logic
  }
}
```

### Application Command Handler Template

```typescript
// src/application/commands/{CommandName}Handler.ts

import { I{Repository}Repository } from '../../domain/repositories/I{Repository}Repository';
import { IEventPublisher } from '../interfaces/IEventPublisher';

export interface {CommandName} {
  // Command data
}

export class {CommandName}Handler {
  constructor(
    private readonly repository: I{Repository}Repository,
    private readonly eventPublisher: IEventPublisher,
  ) {}

  async handle(command: {CommandName}): Promise<void> {
    // 1. Load aggregate
    const aggregate = await this.repository.findById(command.aggregateId);
    if (!aggregate) {
      throw new AggregateNotFoundError(command.aggregateId);
    }

    // 2. Execute domain logic
    aggregate.doSomething(/* command data */);

    // 3. Persist
    await this.repository.save(aggregate);

    // 4. Publish domain events
    const events = aggregate.pullDomainEvents();
    await this.eventPublisher.publishAll(events);
  }
}
```

### Application Query Handler Template

```typescript
// src/application/queries/{QueryName}Handler.ts

import { I{ReadModel}ReadModel } from '../read-models/I{ReadModel}ReadModel';

export interface {QueryName} {
  // Query parameters
}

export interface {QueryName}Result {
  // Query result
}

export class {QueryName}Handler {
  constructor(
    private readonly readModel: I{ReadModel}ReadModel,
  ) {}

  async handle(query: {QueryName}): Promise<{QueryName}Result> {
    // Direct read from optimized read model
    return this.readModel.find(query);
  }
}
```

---

## DI Container Templates

### Clean Architecture DI (TypeScript/TSyringe)

```typescript
// src/infrastructure/config/container.ts

import { container } from 'tsyringe';
import { I{EntityName}Repository } from '../../domain/repositories/I{EntityName}Repository';
import { Postgres{EntityName}Repository } from '../persistence/Postgres{EntityName}Repository';
import { {UseCaseName} } from '../../application/use-cases/{UseCaseName}';

// Register repositories
container.register<I{EntityName}Repository>(
  'I{EntityName}Repository',
  { useClass: Postgres{EntityName}Repository }
);

// Register use cases
container.register({UseCaseName}, {
  useFactory: (c) => new {UseCaseName}(
    c.resolve<I{EntityName}Repository>('I{EntityName}Repository'),
  ),
});

export { container };
```

### Hexagonal DI (Manual Composition)

```typescript
// src/config/composition.ts

import { Pool } from 'pg';
import { {EntityName}Service } from '../core/services/{EntityName}Service';
import { {EntityName}Controller } from '../adapters/inbound/rest/{EntityName}Controller';
import { {EntityName}RepositoryAdapter } from '../adapters/outbound/persistence/{EntityName}RepositoryAdapter';

export function compose(pool: Pool) {
  // Outbound adapters
  const repository = new {EntityName}RepositoryAdapter(pool);

  // Core services
  const service = new {EntityName}Service(repository);

  // Inbound adapters
  const controller = new {EntityName}Controller(service);

  return { controller };
}
```

---

## Test Templates

### Domain Entity Test

```typescript
// tests/unit/domain/{EntityName}.test.ts

import { {EntityName} } from '../../../src/domain/entities/{EntityName}';

describe('{EntityName}', () => {
  describe('create', () => {
    it('should create valid entity', () => {
      const entity = {EntityName}.create({ /* props */ });
      expect(entity.entityId).toBeDefined();
      // Assert initial state
    });

    it('should reject invalid props', () => {
      expect(() => {EntityName}.create({ /* invalid props */ }))
        .toThrow('Expected error message');
    });
  });

  describe('business method', () => {
    it('should change state correctly', () => {
      const entity = {EntityName}.create({ /* props */ });
      entity.doSomething();
      expect(entity.status).toBe(ExpectedStatus);
    });

    it('should raise domain event', () => {
      const entity = {EntityName}.create({ /* props */ });
      entity.doSomething();
      const events = entity.pullEvents();
      expect(events).toHaveLength(1);
      expect(events[0]).toBeInstanceOf(SomethingDone);
    });
  });
});
```

### Use Case Test

```typescript
// tests/unit/application/{UseCaseName}.test.ts

import { {UseCaseName} } from '../../../src/application/use-cases/{UseCaseName}';
import { I{EntityName}Repository } from '../../../src/domain/repositories/I{EntityName}Repository';

describe('{UseCaseName}', () => {
  let useCase: {UseCaseName};
  let mockRepository: jest.Mocked<I{EntityName}Repository>;

  beforeEach(() => {
    mockRepository = {
      save: jest.fn(),
      findById: jest.fn(),
      // ... other methods
    };
    useCase = new {UseCaseName}(mockRepository);
  });

  it('should execute successfully', async () => {
    const request = { /* valid request */ };
    const result = await useCase.execute(request);

    expect(result).toBeDefined();
    expect(mockRepository.save).toHaveBeenCalledTimes(1);
  });

  it('should handle error case', async () => {
    const request = { /* error-triggering request */ };
    await expect(useCase.execute(request)).rejects.toThrow('Expected error');
  });
});
```

### Repository Integration Test

```typescript
// tests/integration/persistence/{EntityName}Repository.test.ts

import { Pool } from 'pg';
import { Postgres{EntityName}Repository } from '../../../src/infrastructure/persistence/Postgres{EntityName}Repository';
import { {EntityName} } from '../../../src/domain/entities/{EntityName}';

describe('Postgres{EntityName}Repository', () => {
  let pool: Pool;
  let repository: Postgres{EntityName}Repository;

  beforeAll(async () => {
    pool = new Pool({ connectionString: process.env.TEST_DATABASE_URL });
    repository = new Postgres{EntityName}Repository(pool);
  });

  afterAll(async () => {
    await pool.end();
  });

  beforeEach(async () => {
    await pool.query('DELETE FROM {table_name}');
  });

  it('should save and retrieve entity', async () => {
    const entity = {EntityName}.create({ /* props */ });
    await repository.save(entity);

    const retrieved = await repository.findById(entity.entityId);

    expect(retrieved).not.toBeNull();
    expect(retrieved!.entityId).toBe(entity.entityId);
  });
});
```

---

## Folder Structure Generator Script

```bash
#!/bin/bash
# generate-clean-architecture.sh

PROJECT_NAME=$1
BASE_DIR=${2:-.}

mkdir -p "$BASE_DIR/$PROJECT_NAME/src/domain/entities"
mkdir -p "$BASE_DIR/$PROJECT_NAME/src/domain/value-objects"
mkdir -p "$BASE_DIR/$PROJECT_NAME/src/domain/repositories"
mkdir -p "$BASE_DIR/$PROJECT_NAME/src/domain/events"

mkdir -p "$BASE_DIR/$PROJECT_NAME/src/application/use-cases"
mkdir -p "$BASE_DIR/$PROJECT_NAME/src/application/dto"
mkdir -p "$BASE_DIR/$PROJECT_NAME/src/application/interfaces"

mkdir -p "$BASE_DIR/$PROJECT_NAME/src/infrastructure/persistence"
mkdir -p "$BASE_DIR/$PROJECT_NAME/src/infrastructure/services"
mkdir -p "$BASE_DIR/$PROJECT_NAME/src/infrastructure/config"

mkdir -p "$BASE_DIR/$PROJECT_NAME/src/presentation/api"
mkdir -p "$BASE_DIR/$PROJECT_NAME/src/presentation/middleware"

mkdir -p "$BASE_DIR/$PROJECT_NAME/tests/unit/domain"
mkdir -p "$BASE_DIR/$PROJECT_NAME/tests/unit/application"
mkdir -p "$BASE_DIR/$PROJECT_NAME/tests/integration"

echo "Clean Architecture structure created at $BASE_DIR/$PROJECT_NAME"
```

---

## Usage Notes

1. **Replace placeholders:** All `{PlaceholderName}` should be replaced with actual names
2. **Adapt to language:** Templates are TypeScript, adapt to your language
3. **Don't over-engineer:** Start with minimum structure, add as needed
4. **Consistency matters:** Pick one style and stick with it across the project
