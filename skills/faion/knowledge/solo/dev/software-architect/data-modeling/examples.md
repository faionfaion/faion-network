# Data Modeling Examples

Real-world data model examples across different database paradigms and use cases.

## E-Commerce Platform

### Relational Model (PostgreSQL)

Normalized schema for transactional e-commerce.

```sql
-- Core entities
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE addresses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    type VARCHAR(20) CHECK (type IN ('billing', 'shipping')),
    street_line1 VARCHAR(255) NOT NULL,
    street_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    postal_code VARCHAR(20) NOT NULL,
    country_code CHAR(2) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id UUID REFERENCES categories(id),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    sort_order INT DEFAULT 0
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    compare_at_price DECIMAL(10, 2),
    cost_price DECIMAL(10, 2),
    stock_quantity INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    weight_grams INT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE product_categories (
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, category_id)
);

CREATE TABLE product_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    url VARCHAR(500) NOT NULL,
    alt_text VARCHAR(255),
    sort_order INT DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(20) UNIQUE NOT NULL,
    customer_id UUID REFERENCES customers(id),
    status VARCHAR(30) DEFAULT 'pending'
        CHECK (status IN ('pending', 'confirmed', 'processing',
                          'shipped', 'delivered', 'cancelled', 'refunded')),
    subtotal DECIMAL(10, 2) NOT NULL,
    tax_amount DECIMAL(10, 2) DEFAULT 0,
    shipping_amount DECIMAL(10, 2) DEFAULT 0,
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL,
    currency_code CHAR(3) DEFAULT 'USD',
    billing_address_id UUID REFERENCES addresses(id),
    shipping_address_id UUID REFERENCES addresses(id),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    product_name VARCHAR(255) NOT NULL,  -- Denormalized for history
    product_sku VARCHAR(50) NOT NULL,    -- Denormalized for history
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL
);

-- Indexes
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_active ON products(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created ON orders(created_at);
CREATE INDEX idx_order_items_order ON order_items(order_id);
```

### Document Model (MongoDB)

Denormalized for read-heavy catalog access.

```javascript
// Products collection
{
  "_id": ObjectId("..."),
  "sku": "PROD-001",
  "name": "Wireless Bluetooth Headphones",
  "slug": "wireless-bluetooth-headphones",
  "description": "Premium noise-cancelling headphones...",
  "price": {
    "amount": 149.99,
    "currency": "USD",
    "compareAt": 199.99
  },
  "inventory": {
    "quantity": 150,
    "lowStockThreshold": 10,
    "trackInventory": true
  },
  "categories": [
    { "id": "cat-electronics", "name": "Electronics", "slug": "electronics" },
    { "id": "cat-audio", "name": "Audio", "slug": "audio" }
  ],
  "images": [
    {
      "url": "https://cdn.example.com/img1.jpg",
      "alt": "Front view",
      "isPrimary": true
    },
    {
      "url": "https://cdn.example.com/img2.jpg",
      "alt": "Side view",
      "isPrimary": false
    }
  ],
  "attributes": {
    "brand": "AudioTech",
    "color": "Black",
    "connectivity": "Bluetooth 5.2",
    "batteryLife": "30 hours"
  },
  "reviews": {
    "averageRating": 4.5,
    "totalCount": 128
  },
  "isActive": true,
  "createdAt": ISODate("2025-01-15T10:00:00Z"),
  "updatedAt": ISODate("2025-01-20T14:30:00Z")
}

// Orders collection
{
  "_id": ObjectId("..."),
  "orderNumber": "ORD-2025-001234",
  "customer": {
    "id": ObjectId("..."),
    "email": "john@example.com",
    "name": "John Doe"
  },
  "status": "shipped",
  "statusHistory": [
    { "status": "pending", "timestamp": ISODate("2025-01-20T10:00:00Z") },
    { "status": "confirmed", "timestamp": ISODate("2025-01-20T10:05:00Z") },
    { "status": "processing", "timestamp": ISODate("2025-01-20T14:00:00Z") },
    { "status": "shipped", "timestamp": ISODate("2025-01-21T09:00:00Z") }
  ],
  "items": [
    {
      "productId": ObjectId("..."),
      "sku": "PROD-001",
      "name": "Wireless Bluetooth Headphones",
      "quantity": 1,
      "unitPrice": 149.99,
      "totalPrice": 149.99
    }
  ],
  "addresses": {
    "shipping": {
      "name": "John Doe",
      "street": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "postalCode": "94102",
      "country": "US"
    },
    "billing": {
      "name": "John Doe",
      "street": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "postalCode": "94102",
      "country": "US"
    }
  },
  "totals": {
    "subtotal": 149.99,
    "tax": 12.37,
    "shipping": 5.99,
    "discount": 0,
    "total": 168.35
  },
  "payment": {
    "method": "credit_card",
    "last4": "4242",
    "transactionId": "txn_abc123"
  },
  "createdAt": ISODate("2025-01-20T10:00:00Z"),
  "updatedAt": ISODate("2025-01-21T09:00:00Z")
}
```

### Graph Model (Neo4j)

For product recommendations and customer behavior.

```cypher
// Create nodes
CREATE (c:Customer {
  id: 'cust-001',
  email: 'john@example.com',
  name: 'John Doe',
  createdAt: datetime()
})

CREATE (p1:Product {
  id: 'prod-001',
  sku: 'HEADPHONES-BT',
  name: 'Wireless Bluetooth Headphones',
  price: 149.99,
  category: 'Electronics'
})

CREATE (p2:Product {
  id: 'prod-002',
  sku: 'CASE-HP',
  name: 'Headphones Carrying Case',
  price: 29.99,
  category: 'Accessories'
})

CREATE (cat:Category {
  id: 'cat-electronics',
  name: 'Electronics',
  slug: 'electronics'
})

// Create relationships
CREATE (c)-[:PURCHASED {
  orderId: 'ord-001',
  quantity: 1,
  price: 149.99,
  purchasedAt: datetime()
}]->(p1)

CREATE (c)-[:VIEWED {
  viewedAt: datetime(),
  duration: 45
}]->(p1)

CREATE (c)-[:ADDED_TO_CART {
  addedAt: datetime()
}]->(p2)

CREATE (p1)-[:BELONGS_TO]->(cat)
CREATE (p2)-[:BELONGS_TO]->(cat)

CREATE (p1)-[:FREQUENTLY_BOUGHT_WITH {
  score: 0.85,
  count: 234
}]->(p2)

// Query: Recommend products based on purchase history
MATCH (c:Customer {id: 'cust-001'})-[:PURCHASED]->(p:Product)
      -[:FREQUENTLY_BOUGHT_WITH]->(rec:Product)
WHERE NOT (c)-[:PURCHASED]->(rec)
RETURN rec.name, rec.price
ORDER BY rec.price DESC
LIMIT 5
```

---

## IoT Sensor Data

### Time-Series Model (TimescaleDB)

```sql
-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create hypertable for sensor readings
CREATE TABLE sensor_readings (
    time TIMESTAMPTZ NOT NULL,
    sensor_id VARCHAR(50) NOT NULL,
    device_id VARCHAR(50) NOT NULL,
    location_id VARCHAR(50) NOT NULL,
    metric_type VARCHAR(30) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20) NOT NULL,
    quality_score SMALLINT DEFAULT 100
);

-- Convert to hypertable with 1-day chunks
SELECT create_hypertable('sensor_readings', 'time', chunk_time_interval => INTERVAL '1 day');

-- Create indexes
CREATE INDEX idx_sensor_readings_sensor ON sensor_readings (sensor_id, time DESC);
CREATE INDEX idx_sensor_readings_device ON sensor_readings (device_id, time DESC);
CREATE INDEX idx_sensor_readings_location ON sensor_readings (location_id, time DESC);
CREATE INDEX idx_sensor_readings_metric ON sensor_readings (metric_type, time DESC);

-- Create continuous aggregate for hourly rollups
CREATE MATERIALIZED VIEW sensor_readings_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    sensor_id,
    device_id,
    location_id,
    metric_type,
    AVG(value) AS avg_value,
    MIN(value) AS min_value,
    MAX(value) AS max_value,
    COUNT(*) AS sample_count
FROM sensor_readings
GROUP BY bucket, sensor_id, device_id, location_id, metric_type;

-- Create continuous aggregate for daily rollups
CREATE MATERIALIZED VIEW sensor_readings_daily
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', time) AS bucket,
    sensor_id,
    device_id,
    location_id,
    metric_type,
    AVG(value) AS avg_value,
    MIN(value) AS min_value,
    MAX(value) AS max_value,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY value) AS median_value,
    COUNT(*) AS sample_count
FROM sensor_readings
GROUP BY bucket, sensor_id, device_id, location_id, metric_type;

-- Data retention policy: keep raw data for 30 days
SELECT add_retention_policy('sensor_readings', INTERVAL '30 days');

-- Compression policy: compress chunks older than 7 days
ALTER TABLE sensor_readings SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'sensor_id, device_id',
    timescaledb.compress_orderby = 'time DESC'
);
SELECT add_compression_policy('sensor_readings', INTERVAL '7 days');

-- Device metadata (regular table)
CREATE TABLE devices (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    location_id VARCHAR(50) NOT NULL,
    installed_at TIMESTAMPTZ NOT NULL,
    firmware_version VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE
);

-- Sensor metadata
CREATE TABLE sensors (
    id VARCHAR(50) PRIMARY KEY,
    device_id VARCHAR(50) REFERENCES devices(id),
    type VARCHAR(50) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    min_value DOUBLE PRECISION,
    max_value DOUBLE PRECISION,
    calibrated_at TIMESTAMPTZ
);
```

### InfluxDB Model (Line Protocol)

```
# Measurement: sensor_data
# Tags: sensor_id, device_id, location, metric_type
# Fields: value, quality

sensor_data,sensor_id=temp-001,device_id=dev-001,location=warehouse-a,metric_type=temperature value=23.5,quality=100 1706100000000000000
sensor_data,sensor_id=hum-001,device_id=dev-001,location=warehouse-a,metric_type=humidity value=45.2,quality=100 1706100000000000000
sensor_data,sensor_id=temp-002,device_id=dev-002,location=warehouse-b,metric_type=temperature value=21.8,quality=98 1706100000000000000

# InfluxQL queries
SELECT MEAN(value) FROM sensor_data
WHERE metric_type = 'temperature'
  AND time > now() - 1h
GROUP BY time(5m), location

# Flux queries (InfluxDB 2.x+)
from(bucket: "iot_data")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "sensor_data")
  |> filter(fn: (r) => r.metric_type == "temperature")
  |> aggregateWindow(every: 5m, fn: mean)
  |> group(columns: ["location"])
```

---

## Social Network

### Graph Model (Neo4j)

```cypher
// User nodes
CREATE (u1:User {
  id: 'user-001',
  username: 'johndoe',
  email: 'john@example.com',
  name: 'John Doe',
  bio: 'Software developer and coffee enthusiast',
  joinedAt: datetime('2024-01-15'),
  isVerified: false
})

CREATE (u2:User {
  id: 'user-002',
  username: 'janedoe',
  email: 'jane@example.com',
  name: 'Jane Doe',
  bio: 'Data scientist and book lover',
  joinedAt: datetime('2024-02-20'),
  isVerified: true
})

// Content nodes
CREATE (p1:Post {
  id: 'post-001',
  content: 'Just finished a great book on graph databases!',
  createdAt: datetime('2025-01-20T10:00:00'),
  likes: 45,
  shares: 12
})

CREATE (c1:Comment {
  id: 'comment-001',
  content: 'Which book? I want to read it too!',
  createdAt: datetime('2025-01-20T10:30:00'),
  likes: 5
})

// Hashtag nodes
CREATE (h1:Hashtag { name: 'graphdb', usageCount: 1250 })
CREATE (h2:Hashtag { name: 'tech', usageCount: 98000 })

// Relationships
CREATE (u1)-[:FOLLOWS { since: datetime('2024-03-01') }]->(u2)
CREATE (u2)-[:FOLLOWS { since: datetime('2024-03-15') }]->(u1)

CREATE (u2)-[:AUTHORED { publishedAt: datetime('2025-01-20T10:00:00') }]->(p1)
CREATE (u1)-[:LIKED { likedAt: datetime('2025-01-20T10:15:00') }]->(p1)
CREATE (u1)-[:AUTHORED]->(c1)
CREATE (c1)-[:COMMENT_ON]->(p1)

CREATE (p1)-[:TAGGED]->(h1)
CREATE (p1)-[:TAGGED]->(h2)

// Friend-of-friend recommendations
MATCH (u:User {id: 'user-001'})-[:FOLLOWS]->(friend)-[:FOLLOWS]->(foaf)
WHERE NOT (u)-[:FOLLOWS]->(foaf) AND u <> foaf
RETURN foaf.name, foaf.username, COUNT(friend) as mutualFriends
ORDER BY mutualFriends DESC
LIMIT 10

// Content feed query
MATCH (u:User {id: 'user-001'})-[:FOLLOWS]->(author)-[:AUTHORED]->(post:Post)
WHERE post.createdAt > datetime() - duration('P7D')
RETURN post, author
ORDER BY post.createdAt DESC
LIMIT 20
```

---

## Data Warehouse (Data Vault 2.0)

### Hub, Link, Satellite Structure

```sql
-- =============
-- HUBS
-- =============

-- Customer Hub
CREATE TABLE hub_customer (
    customer_hk CHAR(32) PRIMARY KEY,      -- Hash key (MD5 of business key)
    customer_bk VARCHAR(50) NOT NULL,       -- Business key (customer number)
    load_dts TIMESTAMPTZ NOT NULL,          -- Load timestamp
    record_source VARCHAR(100) NOT NULL     -- Source system
);

CREATE UNIQUE INDEX idx_hub_customer_bk ON hub_customer(customer_bk);

-- Product Hub
CREATE TABLE hub_product (
    product_hk CHAR(32) PRIMARY KEY,
    product_bk VARCHAR(50) NOT NULL,        -- SKU
    load_dts TIMESTAMPTZ NOT NULL,
    record_source VARCHAR(100) NOT NULL
);

CREATE UNIQUE INDEX idx_hub_product_bk ON hub_product(product_bk);

-- Order Hub
CREATE TABLE hub_order (
    order_hk CHAR(32) PRIMARY KEY,
    order_bk VARCHAR(50) NOT NULL,          -- Order number
    load_dts TIMESTAMPTZ NOT NULL,
    record_source VARCHAR(100) NOT NULL
);

CREATE UNIQUE INDEX idx_hub_order_bk ON hub_order(order_bk);

-- =============
-- LINKS
-- =============

-- Customer-Order Link
CREATE TABLE link_customer_order (
    customer_order_hk CHAR(32) PRIMARY KEY, -- Hash key (MD5 of composite)
    customer_hk CHAR(32) NOT NULL REFERENCES hub_customer(customer_hk),
    order_hk CHAR(32) NOT NULL REFERENCES hub_order(order_hk),
    load_dts TIMESTAMPTZ NOT NULL,
    record_source VARCHAR(100) NOT NULL
);

CREATE INDEX idx_link_customer_order_customer ON link_customer_order(customer_hk);
CREATE INDEX idx_link_customer_order_order ON link_customer_order(order_hk);

-- Order-Product Link (with quantity as degenerate dimension)
CREATE TABLE link_order_product (
    order_product_hk CHAR(32) PRIMARY KEY,
    order_hk CHAR(32) NOT NULL REFERENCES hub_order(order_hk),
    product_hk CHAR(32) NOT NULL REFERENCES hub_product(product_hk),
    quantity INT NOT NULL,                   -- Degenerate dimension
    load_dts TIMESTAMPTZ NOT NULL,
    record_source VARCHAR(100) NOT NULL
);

CREATE INDEX idx_link_order_product_order ON link_order_product(order_hk);
CREATE INDEX idx_link_order_product_product ON link_order_product(product_hk);

-- =============
-- SATELLITES
-- =============

-- Customer Satellite (descriptive attributes with history)
CREATE TABLE sat_customer (
    customer_hk CHAR(32) NOT NULL REFERENCES hub_customer(customer_hk),
    load_dts TIMESTAMPTZ NOT NULL,
    load_end_dts TIMESTAMPTZ DEFAULT '9999-12-31',
    hash_diff CHAR(32) NOT NULL,            -- Hash of attributes for CDC
    record_source VARCHAR(100) NOT NULL,

    -- Descriptive attributes
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    tier VARCHAR(20),                       -- gold, silver, bronze

    PRIMARY KEY (customer_hk, load_dts)
);

-- Product Satellite
CREATE TABLE sat_product (
    product_hk CHAR(32) NOT NULL REFERENCES hub_product(product_hk),
    load_dts TIMESTAMPTZ NOT NULL,
    load_end_dts TIMESTAMPTZ DEFAULT '9999-12-31',
    hash_diff CHAR(32) NOT NULL,
    record_source VARCHAR(100) NOT NULL,

    -- Descriptive attributes
    name VARCHAR(255),
    description TEXT,
    category VARCHAR(100),
    price DECIMAL(10, 2),
    cost DECIMAL(10, 2),

    PRIMARY KEY (product_hk, load_dts)
);

-- Order Satellite
CREATE TABLE sat_order (
    order_hk CHAR(32) NOT NULL REFERENCES hub_order(order_hk),
    load_dts TIMESTAMPTZ NOT NULL,
    load_end_dts TIMESTAMPTZ DEFAULT '9999-12-31',
    hash_diff CHAR(32) NOT NULL,
    record_source VARCHAR(100) NOT NULL,

    -- Descriptive attributes
    status VARCHAR(30),
    order_date DATE,
    ship_date DATE,
    total_amount DECIMAL(10, 2),
    currency CHAR(3),

    PRIMARY KEY (order_hk, load_dts)
);

-- =============
-- POINT-IN-TIME TABLE (Performance optimization)
-- =============

CREATE TABLE pit_customer (
    pit_customer_hk CHAR(32) PRIMARY KEY,
    customer_hk CHAR(32) NOT NULL,
    snapshot_dts TIMESTAMPTZ NOT NULL,

    -- Satellite load dates for fast lookup
    sat_customer_load_dts TIMESTAMPTZ,

    UNIQUE (customer_hk, snapshot_dts)
);
```

---

## Slowly Changing Dimensions Example

### Type 2 SCD (Full History)

```sql
-- Customer dimension with Type 2 SCD
CREATE TABLE dim_customer (
    customer_sk SERIAL PRIMARY KEY,         -- Surrogate key
    customer_id VARCHAR(50) NOT NULL,       -- Natural/business key

    -- Descriptive attributes
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    customer_tier VARCHAR(20),              -- Tracked for history

    -- SCD Type 2 tracking columns
    valid_from TIMESTAMPTZ NOT NULL,
    valid_to TIMESTAMPTZ DEFAULT '9999-12-31 23:59:59',
    is_current BOOLEAN DEFAULT TRUE,

    -- Audit columns
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    hash_key CHAR(32)                       -- For change detection
);

-- Indexes for efficient queries
CREATE INDEX idx_dim_customer_id ON dim_customer(customer_id);
CREATE INDEX idx_dim_customer_current ON dim_customer(is_current) WHERE is_current = TRUE;
CREATE INDEX idx_dim_customer_valid ON dim_customer(valid_from, valid_to);

-- Example: Insert new customer
INSERT INTO dim_customer (
    customer_id, first_name, last_name, email, customer_tier,
    valid_from, is_current, hash_key
) VALUES (
    'CUST-001', 'John', 'Doe', 'john@example.com', 'Silver',
    NOW(), TRUE, MD5('John|Doe|john@example.com|Silver')
);

-- Example: Update customer tier (creates new version)
-- Step 1: Close current record
UPDATE dim_customer
SET valid_to = NOW(),
    is_current = FALSE,
    updated_at = NOW()
WHERE customer_id = 'CUST-001'
  AND is_current = TRUE;

-- Step 2: Insert new version
INSERT INTO dim_customer (
    customer_id, first_name, last_name, email, customer_tier,
    valid_from, is_current, hash_key
) VALUES (
    'CUST-001', 'John', 'Doe', 'john@example.com', 'Gold',
    NOW(), TRUE, MD5('John|Doe|john@example.com|Gold')
);

-- Query current state
SELECT * FROM dim_customer WHERE is_current = TRUE;

-- Query historical state at specific point in time
SELECT * FROM dim_customer
WHERE customer_id = 'CUST-001'
  AND '2025-01-15'::TIMESTAMPTZ BETWEEN valid_from AND valid_to;
```

---

## Wide-Column Model (Cassandra/ScyllaDB)

### User Activity Tracking

```cql
-- Keyspace creation
CREATE KEYSPACE analytics
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'dc1': 3, 'dc2': 3
};

USE analytics;

-- User activity by date (query: get user's activity for a date)
CREATE TABLE user_activity_by_date (
    user_id UUID,
    activity_date DATE,
    activity_time TIMESTAMP,
    activity_type TEXT,
    page_url TEXT,
    session_id UUID,
    device_type TEXT,
    ip_address TEXT,
    metadata MAP<TEXT, TEXT>,
    PRIMARY KEY ((user_id, activity_date), activity_time)
) WITH CLUSTERING ORDER BY (activity_time DESC);

-- Activity by page (query: get all activity on a page)
CREATE TABLE activity_by_page (
    page_url TEXT,
    activity_date DATE,
    activity_time TIMESTAMP,
    user_id UUID,
    activity_type TEXT,
    session_id UUID,
    PRIMARY KEY ((page_url, activity_date), activity_time)
) WITH CLUSTERING ORDER BY (activity_time DESC);

-- User sessions (query: get user's sessions)
CREATE TABLE user_sessions (
    user_id UUID,
    session_id UUID,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    device_type TEXT,
    ip_address TEXT,
    page_count INT,
    total_duration INT,
    PRIMARY KEY (user_id, started_at)
) WITH CLUSTERING ORDER BY (started_at DESC);

-- Daily aggregates (query: get daily stats)
CREATE TABLE daily_stats (
    metric_type TEXT,
    date DATE,
    hour INT,
    value COUNTER,
    PRIMARY KEY ((metric_type, date), hour)
);

-- Example queries
-- Get user activity for specific date
SELECT * FROM user_activity_by_date
WHERE user_id = 550e8400-e29b-41d4-a716-446655440000
  AND activity_date = '2025-01-20';

-- Get last 100 activities on a page
SELECT * FROM activity_by_page
WHERE page_url = '/products/headphones'
  AND activity_date = '2025-01-20'
LIMIT 100;

-- Increment counter
UPDATE daily_stats
SET value = value + 1
WHERE metric_type = 'page_view'
  AND date = '2025-01-20'
  AND hour = 14;
```

---

## Polyglot Persistence Architecture

### Fintech Application Example

```
Data Store Architecture:

┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ PostgreSQL   │  │ Redis        │  │ Elasticsearch        │  │
│  │              │  │              │  │                      │  │
│  │ - Accounts   │  │ - Sessions   │  │ - Transaction search │  │
│  │ - Users      │  │ - Rate limits│  │ - Audit logs search  │  │
│  │ - Transactions│  │ - Cache     │  │ - Full-text queries  │  │
│  │ - Balances   │  │ - Pub/Sub    │  │                      │  │
│  │              │  │              │  │                      │  │
│  │ ACID         │  │ Sub-ms       │  │ Search & Analytics   │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ TimescaleDB  │  │ Neo4j        │  │ S3 + Parquet         │  │
│  │              │  │              │  │                      │  │
│  │ - Price feeds │  │ - Fraud graph│  │ - Historical data    │  │
│  │ - Metrics    │  │ - Network    │  │ - Compliance archive │  │
│  │ - Trading    │  │   analysis   │  │ - ML training data   │  │
│  │   history    │  │ - Customer   │  │                      │  │
│  │              │  │   360 view   │  │                      │  │
│  │ Time-series  │  │ Relationships│  │ Cold Storage         │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Data Flow:
1. Real-time transactions -> PostgreSQL (source of truth)
2. Transaction events -> Kafka -> Elasticsearch (search index)
3. Price updates -> TimescaleDB (time-series)
4. Transaction patterns -> Neo4j (fraud detection)
5. Nightly batch -> S3/Parquet (archive)
6. Frequently accessed data -> Redis (cache)
```

### Implementation Example

```python
# Python service with polyglot persistence
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import asyncpg
import redis.asyncio as redis
from elasticsearch import AsyncElasticsearch
from neo4j import AsyncGraphDatabase

@dataclass
class Transaction:
    id: str
    account_id: str
    amount: float
    currency: str
    type: str
    status: str
    created_at: datetime
    metadata: dict

class TransactionService:
    def __init__(self):
        self.pg_pool = None
        self.redis_client = None
        self.es_client = None
        self.neo4j_driver = None

    async def create_transaction(self, tx: Transaction):
        # 1. Write to PostgreSQL (source of truth)
        async with self.pg_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO transactions
                (id, account_id, amount, currency, type, status, created_at, metadata)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """, tx.id, tx.account_id, tx.amount, tx.currency,
                tx.type, tx.status, tx.created_at, tx.metadata)

        # 2. Index in Elasticsearch (for search)
        await self.es_client.index(
            index="transactions",
            id=tx.id,
            document={
                "account_id": tx.account_id,
                "amount": tx.amount,
                "currency": tx.currency,
                "type": tx.type,
                "status": tx.status,
                "created_at": tx.created_at.isoformat(),
                "metadata": tx.metadata
            }
        )

        # 3. Update Neo4j graph (for fraud detection)
        async with self.neo4j_driver.session() as session:
            await session.run("""
                MATCH (a:Account {id: $account_id})
                CREATE (t:Transaction {
                    id: $tx_id,
                    amount: $amount,
                    type: $type,
                    created_at: $created_at
                })
                CREATE (a)-[:MADE]->(t)
            """, account_id=tx.account_id, tx_id=tx.id,
                amount=tx.amount, type=tx.type,
                created_at=tx.created_at.isoformat())

        # 4. Invalidate cache
        await self.redis_client.delete(f"account:{tx.account_id}:balance")
        await self.redis_client.delete(f"account:{tx.account_id}:recent_tx")

    async def get_recent_transactions(self, account_id: str, limit: int = 10):
        # Try cache first
        cache_key = f"account:{account_id}:recent_tx"
        cached = await self.redis_client.get(cache_key)
        if cached:
            return cached

        # Fall back to database
        async with self.pg_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT * FROM transactions
                WHERE account_id = $1
                ORDER BY created_at DESC
                LIMIT $2
            """, account_id, limit)

        # Cache for 5 minutes
        await self.redis_client.setex(cache_key, 300, rows)
        return rows

    async def search_transactions(self, query: str, filters: dict):
        # Use Elasticsearch for complex searches
        return await self.es_client.search(
            index="transactions",
            query={
                "bool": {
                    "must": [{"match": {"metadata": query}}],
                    "filter": [{"term": {k: v}} for k, v in filters.items()]
                }
            }
        )

    async def detect_fraud_patterns(self, account_id: str):
        # Use Neo4j for graph-based fraud detection
        async with self.neo4j_driver.session() as session:
            result = await session.run("""
                MATCH (a:Account {id: $account_id})-[:MADE]->(t:Transaction)
                      -[:TO]->(recipient:Account)
                WITH recipient, COUNT(t) as tx_count, SUM(t.amount) as total
                WHERE tx_count > 10 AND total > 50000
                RETURN recipient.id, tx_count, total
                ORDER BY total DESC
            """, account_id=account_id)
            return await result.data()
```
