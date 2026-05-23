// purpose: TBD-template-header
// consumes: input from methodology
// produces: output artefact
// depends-on: 01-core-rules.xml
// token-budget-impact: small

import { v4 as uuidv4 } from 'uuid';

interface Entity {
  id: string;
  name: string;
  email: string;
  status: 'pending' | 'active' | 'inactive';
  createdAt: Date;
  metadata?: Record<string, unknown>;
}

export class EntityBuilder {
  private entity: Entity;

  constructor() {
    this.entity = {
      id: uuidv4(),
      name: 'Default Name',
      email: 'default@example.com',
      status: 'pending',
      createdAt: new Date(),
    };
  }

  withId(id: string): EntityBuilder {
    this.entity.id = id;
    return this;
  }

  withName(name: string): EntityBuilder {
    this.entity.name = name;
    return this;
  }

  withEmail(email: string): EntityBuilder {
    this.entity.email = email;
    return this;
  }

  asActive(): EntityBuilder {
    this.entity.status = 'active';
    return this;
  }

  asInactive(): EntityBuilder {
    this.entity.status = 'inactive';
    return this;
  }

  withStatus(status: Entity['status']): EntityBuilder {
    this.entity.status = status;
    return this;
  }

  createdAt(date: Date): EntityBuilder {
    this.entity.createdAt = date;
    return this;
  }

  withMetadata(metadata: Record<string, unknown>): EntityBuilder {
    this.entity.metadata = metadata;
    return this;
  }

  build(): Entity {
    return { ...this.entity };
  }
}
