# Data Modeling

Designing database schemas and data structures.

## Process

```
1. Identify Entities → What are the main objects?
2. Define Attributes → What properties do they have?
3. Establish Relationships → How do entities connect?
4. Normalize → Reduce redundancy
5. Denormalize → Optimize for queries (if needed)
```

## Entity-Relationship Diagram (ERD)

### Relationships

```
One-to-One (1:1)
User ────────── Profile
  │               │
  PK              FK

One-to-Many (1:N)
User ────────◀── Orders
  │               │
  PK              FK

Many-to-Many (M:N)
Students ◀────▶ Courses
    │       │       │
    PK    Junction  PK
          Table
```

### ERD Notation

```
┌─────────────────┐
│     ENTITY      │
├─────────────────┤
│ PK id           │
│    attribute1   │
│ FK foreign_key  │
└─────────────────┘
```

## Normalization

### 1NF (First Normal Form)
- No repeating groups
- Atomic values

```
❌ WRONG
| user_id | phones              |
|---------|---------------------|
| 1       | "123,456,789"       |

✅ RIGHT
| user_id | phone |
|---------|-------|
| 1       | 123   |
| 1       | 456   |
| 1       | 789   |
```

### 2NF (Second Normal Form)
- 1NF + No partial dependencies

```
❌ WRONG: course_name depends only on course_id
| student_id | course_id | course_name | grade |
|------------|-----------|-------------|-------|

✅ RIGHT: Separate tables
Students_Courses: student_id, course_id, grade
Courses: course_id, course_name
```

### 3NF (Third Normal Form)
- 2NF + No transitive dependencies

```
❌ WRONG: city depends on zip_code, not directly on id
| id | zip_code | city      |
|----|----------|-----------|

✅ RIGHT: Separate tables
Users: id, zip_code
ZipCodes: zip_code, city
```

## Denormalization

Add redundancy for query performance.

**When to denormalize:**
- Frequent joins are slow
- Read-heavy workloads
- Reporting/analytics

```sql
-- Normalized (slow reads, fast writes)
SELECT o.*, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id;

-- Denormalized (fast reads, slower writes)
-- Store customer_name directly in orders
SELECT * FROM orders;
```

## Common Patterns

### Polymorphic Associations

```sql
-- Single Table Inheritance
CREATE TABLE content (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20),  -- 'post', 'video', 'image'
    title VARCHAR(255),
    body TEXT,         -- for posts
    url VARCHAR(500),  -- for videos/images
    duration INT       -- for videos
);

-- OR: Separate tables with common interface
```

### Self-Referential

```sql
-- Tree structure (categories, org chart)
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    parent_id INT REFERENCES categories(id)
);
```

### Audit Trail

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    -- ... columns ...
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by INT REFERENCES users(id),
    updated_by INT REFERENCES users(id)
);
```

### Soft Delete

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    deleted_at TIMESTAMP NULL  -- NULL = active
);

-- Query only active
SELECT * FROM users WHERE deleted_at IS NULL;
```

## Index Strategy

```sql
-- Primary key (automatic)
-- Foreign keys (recommended)
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Partial index
CREATE INDEX idx_active_orders ON orders(status)
WHERE status = 'active';

-- Unique constraint
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

## Schema Example

```sql
-- E-commerce schema
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending',
    total DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL
);
```

## Related

- [database-selection.md](database-selection.md) - Choosing database
- [caching-architecture.md](caching-architecture.md) - Performance layer
