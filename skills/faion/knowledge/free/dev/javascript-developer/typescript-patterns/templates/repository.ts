// purpose: TBD-template-header
// consumes: input from methodology
// produces: output artefact
// depends-on: 01-core-rules.xml
// token-budget-impact: small

// Generic Repository interface — constrain T to have an id: string property
interface Repository<T extends { id: string }> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(data: Omit<T, 'id'>): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}
