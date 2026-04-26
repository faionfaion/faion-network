import { faker } from '@faker-js/faker';

// ---- Type definitions (adapt to your domain models) ----

export interface UserData {
  email: string;
  name: string;
  password: string;
  role: 'user' | 'admin';
}

export interface ProductData {
  name: string;
  price: number;
  sku: string;
  inStock: boolean;
}

// ---- Factories ----

export function createUser(overrides: Partial<UserData> = {}): UserData {
  return {
    email: faker.internet.email(),
    name: faker.person.fullName(),
    password: faker.internet.password({ length: 12 }),
    role: 'user',
    ...overrides,
  };
}

export function createAdmin(overrides: Partial<UserData> = {}): UserData {
  return createUser({ role: 'admin', ...overrides });
}

export function createProduct(overrides: Partial<ProductData> = {}): ProductData {
  return {
    name: faker.commerce.productName(),
    price: parseFloat(faker.commerce.price({ min: 1, max: 500 })),
    sku: faker.string.alphanumeric(8).toUpperCase(),
    inStock: faker.datatype.boolean(),
    ...overrides,
  };
}

// ---- Builder pattern for complex objects ----

export class OrderBuilder {
  private data: Record<string, unknown> = {
    userId: faker.string.uuid(),
    items: [],
    status: 'pending',
  };

  withUser(userId: string): this {
    this.data.userId = userId;
    return this;
  }

  withItem(productId: string, quantity = 1): this {
    (this.data.items as unknown[]).push({ productId, quantity });
    return this;
  }

  withStatus(status: string): this {
    this.data.status = status;
    return this;
  }

  build() {
    return { ...this.data };
  }
}
