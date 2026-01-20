---
id: M-DEV-050
name: "Documentation"
domain: DEV
skill: faion-software-developer
category: "development"
---

# M-DEV-050: Documentation

## Overview

Documentation ensures code is understandable, maintainable, and usable by both current and future developers. This includes code comments, docstrings, API documentation, architecture docs, and user guides.

## When to Use

- Public APIs and libraries
- Complex business logic
- Architecture decisions (ADRs)
- Onboarding new team members
- Open source projects

## Key Principles

- **Document why, not what**: Code shows what, docs explain why
- **Keep it close to code**: Documentation should live with code
- **Automate generation**: Generate API docs from code
- **Keep it current**: Outdated docs are worse than no docs
- **Know your audience**: Different docs for different readers

## Best Practices

### Code Comments

```python
# BAD: Comments that describe WHAT (redundant)
# Increment counter by 1
counter += 1

# GOOD: Comments that explain WHY
# Offset by 1 because external API uses 1-based indexing
counter += 1

# BAD: Outdated comment
# Calculate tax at 5%
tax = price * 0.08  # Comment says 5%, code says 8%

# GOOD: Comment explaining non-obvious code
# Using bitwise AND for performance in hot path
# Equivalent to: index % BUFFER_SIZE
buffer_index = index & (BUFFER_SIZE - 1)

# GOOD: Warning comments
# WARNING: This function is not thread-safe. Use lock if calling
# from multiple threads.
def update_shared_state(value):
    pass

# GOOD: TODO with context
# TODO(username): Refactor to use connection pool once #1234 is merged
# Current implementation creates new connection per request
connection = create_connection()

# GOOD: Explaining business logic
# Premium users get 20% discount, applied before tax
# This matches the pricing model approved in PRD-2024-01
discount = 0.20 if user.is_premium else 0.0
```

### Python Docstrings (Google Style)

```python
def calculate_shipping_cost(
    weight: float,
    destination: str,
    expedited: bool = False
) -> Decimal:
    """Calculate shipping cost based on weight and destination.

    Uses the standard shipping rate table with surcharges for
    international destinations and expedited delivery.

    Args:
        weight: Package weight in kilograms. Must be positive.
        destination: Two-letter country code (ISO 3166-1 alpha-2).
        expedited: If True, uses express shipping (2x cost).

    Returns:
        The calculated shipping cost in USD.

    Raises:
        ValueError: If weight is not positive.
        InvalidDestinationError: If country code is not recognized.

    Example:
        >>> calculate_shipping_cost(2.5, "US")
        Decimal('12.50')
        >>> calculate_shipping_cost(2.5, "US", expedited=True)
        Decimal('25.00')

    Note:
        International shipping adds a flat $15 surcharge.
        Rates are updated quarterly; see SHIPPING_RATES constant.
    """
    if weight <= 0:
        raise ValueError(f"Weight must be positive, got {weight}")

    # Implementation...


class OrderService:
    """Service for managing customer orders.

    Handles order creation, status updates, and fulfillment tracking.
    Uses the repository pattern for data access.

    Attributes:
        repository: Data access layer for orders.
        payment_gateway: External payment processing service.
        notification_service: Service for sending customer notifications.

    Example:
        >>> service = OrderService(repo, payment, notifications)
        >>> order = service.create_order(customer_id="123", items=[...])
        >>> service.process_payment(order.id)
    """

    def __init__(
        self,
        repository: OrderRepository,
        payment_gateway: PaymentGateway,
        notification_service: NotificationService
    ):
        """Initialize OrderService with dependencies.

        Args:
            repository: Order data access object.
            payment_gateway: Payment processing integration.
            notification_service: Customer notification sender.
        """
        self.repository = repository
        self.payment_gateway = payment_gateway
        self.notification_service = notification_service
```

### TypeScript/JSDoc Documentation

```typescript
/**
 * Service for managing user authentication and sessions.
 *
 * @example
 * ```typescript
 * const authService = new AuthService(userRepo, tokenService);
 * const result = await authService.login('user@example.com', 'password');
 * if (result.success) {
 *   console.log('Token:', result.token);
 * }
 * ```
 */
class AuthService {
  /**
   * Creates an instance of AuthService.
   * @param userRepository - Repository for user data access
   * @param tokenService - Service for JWT token management
   */
  constructor(
    private readonly userRepository: UserRepository,
    private readonly tokenService: TokenService
  ) {}

  /**
   * Authenticates a user and returns a session token.
   *
   * @param email - User's email address
   * @param password - User's password (will be hashed for comparison)
   * @returns Authentication result with token if successful
   * @throws {InvalidCredentialsError} When email or password is incorrect
   * @throws {AccountLockedError} When account is locked due to failed attempts
   *
   * @example
   * ```typescript
   * try {
   *   const result = await authService.login('user@example.com', 'secret');
   *   localStorage.setItem('token', result.token);
   * } catch (error) {
   *   if (error instanceof InvalidCredentialsError) {
   *     showError('Invalid email or password');
   *   }
   * }
   * ```
   */
  async login(email: string, password: string): Promise<AuthResult> {
    // Implementation
  }

  /**
   * Validates a session token and returns the associated user.
   *
   * @param token - JWT token to validate
   * @returns User associated with the token, or null if invalid
   *
   * @remarks
   * This method checks both token signature and expiration.
   * Expired tokens return null rather than throwing.
   */
  async validateToken(token: string): Promise<User | null> {
    // Implementation
  }
}

/**
 * Configuration options for the API client.
 */
interface ApiClientConfig {
  /** Base URL for API requests */
  baseUrl: string;

  /** Request timeout in milliseconds (default: 30000) */
  timeout?: number;

  /** Custom headers to include in all requests */
  headers?: Record<string, string>;

  /**
   * Retry configuration for failed requests.
   * @default { maxRetries: 3, backoffMs: 1000 }
   */
  retry?: {
    /** Maximum number of retry attempts */
    maxRetries: number;
    /** Initial backoff delay in milliseconds */
    backoffMs: number;
  };
}
```

### API Documentation with OpenAPI

```python
# FastAPI automatically generates OpenAPI docs

from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field

app = FastAPI(
    title="E-Commerce API",
    description="""
    API for managing products, orders, and customers.

    ## Authentication
    All endpoints require Bearer token authentication.
    Obtain a token via `/auth/login`.

    ## Rate Limiting
    - Standard endpoints: 100 requests/minute
    - Search endpoints: 30 requests/minute
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "api@example.com",
    },
    license_info={
        "name": "MIT",
    },
)


class ProductCreate(BaseModel):
    """Schema for creating a new product."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Product name",
        example="Wireless Headphones"
    )
    price: Decimal = Field(
        ...,
        gt=0,
        description="Price in USD",
        example=79.99
    )
    description: str | None = Field(
        None,
        max_length=2000,
        description="Detailed product description"
    )
    category_id: int = Field(
        ...,
        description="ID of the product category"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Wireless Headphones",
                "price": 79.99,
                "description": "High-quality wireless headphones with noise cancellation",
                "category_id": 5
            }
        }


@app.post(
    "/api/products",
    response_model=Product,
    status_code=201,
    summary="Create a new product",
    description="""
    Creates a new product in the catalog.

    Requires admin authentication.
    """,
    responses={
        201: {"description": "Product created successfully"},
        400: {"description": "Invalid input data"},
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized (admin required)"},
        409: {"description": "Product with same SKU already exists"},
    },
    tags=["Products"],
)
async def create_product(
    product: ProductCreate,
    current_user: User = Depends(get_current_admin_user),
):
    """Create a new product.

    - **name**: Product display name
    - **price**: Price in USD (must be positive)
    - **description**: Optional detailed description
    - **category_id**: Must reference existing category
    """
    return await product_service.create(product)


@app.get(
    "/api/products/{product_id}",
    response_model=Product,
    summary="Get product by ID",
    tags=["Products"],
)
async def get_product(
    product_id: int = Path(..., description="Unique product identifier", ge=1),
):
    """Retrieve a product by its unique identifier."""
    product = await product_service.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get(
    "/api/products",
    response_model=PaginatedResponse[Product],
    summary="List products",
    tags=["Products"],
)
async def list_products(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    category: int | None = Query(None, description="Filter by category ID"),
    search: str | None = Query(None, min_length=2, description="Search in name"),
    sort: str = Query("created_at", description="Sort field"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
):
    """
    List products with pagination and filtering.

    Supports filtering by category and text search in product names.
    Results are paginated with configurable page size.
    """
    return await product_service.list(
        page=page,
        limit=limit,
        category=category,
        search=search,
        sort=sort,
        order=order,
    )
```

### README Structure

```markdown
# Project Name

Brief description of what this project does and why it exists.

[![CI](https://github.com/org/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/org/repo/actions)
[![Coverage](https://codecov.io/gh/org/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/org/repo)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features

- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description

## Quick Start

```bash
# Install
pip install project-name

# Basic usage
from project import Client

client = Client(api_key="your-key")
result = client.do_something()
```

## Installation

### Requirements

- Python 3.11+
- PostgreSQL 15+

### From PyPI

```bash
pip install project-name
```

### From Source

```bash
git clone https://github.com/org/repo.git
cd repo
pip install -e .
```

## Usage

### Basic Example

```python
# Code example with comments
```

### Advanced Configuration

```python
# More complex example
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | Your API key | Required |
| `TIMEOUT` | Request timeout (seconds) | 30 |
| `DEBUG` | Enable debug logging | False |

## API Reference

See [API Documentation](https://docs.example.com) for full reference.

## Development

### Setup

```bash
# Clone and install dev dependencies
git clone https://github.com/org/repo.git
cd repo
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- [Documentation](https://docs.example.com)
- [Issue Tracker](https://github.com/org/repo/issues)
- [Discussions](https://github.com/org/repo/discussions)
```

### Architecture Decision Records (ADRs)

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status

Accepted

## Context

We need to choose a primary database for our e-commerce platform.
The system requires:
- ACID transactions for order processing
- Complex queries for reporting
- JSON support for flexible product attributes
- Horizontal read scaling capability

Candidates considered:
- PostgreSQL
- MySQL
- MongoDB
- CockroachDB

## Decision

We will use PostgreSQL as our primary database.

## Rationale

1. **ACID Compliance**: Critical for financial transactions
2. **JSON Support**: JSONB provides flexible schema when needed
3. **Read Replicas**: Native support for scaling reads
4. **Ecosystem**: Excellent tooling, ORMs, and community support
5. **Team Experience**: Team has PostgreSQL expertise

MongoDB was rejected due to:
- Eventual consistency model doesn't fit our needs
- Complex aggregations are harder to express

## Consequences

### Positive
- Strong data integrity guarantees
- Familiar SQL interface
- Excellent query performance with proper indexing

### Negative
- Vertical scaling for writes has limits
- Need to manage schema migrations carefully

### Risks
- May need to shard for very high write volumes
- Mitigation: Design with sharding keys in mind

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- PRD-2024-01: E-Commerce Platform Requirements
```

## Anti-patterns

- **Documentation debt**: Writing none, planning to add "later"
- **Stale documentation**: Docs that don't match code
- **Over-documentation**: Documenting obvious code
- **Wrong audience**: Technical docs for end users
- **No examples**: API docs without code samples
- **Duplicate information**: Same info in multiple places

## References

- [Google Style Guide - Python](https://google.github.io/styleguide/pyguide.html)
- [JSDoc Documentation](https://jsdoc.app/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Architecture Decision Records](https://adr.github.io/)
- [Write the Docs](https://www.writethedocs.org/)
