<!-- purpose: minimum viable layered-service skeleton reference for Spring Boot 3 -->
<!-- consumes: API contract + entity model -->
<!-- produces: file layout conforming to constructor-injection + dto-record-separate-from-entity rules -->
<!-- depends-on: content/01-core-rules.xml rules constructor-injection, dto-record-separate-from-entity, mapstruct-for-mapping -->
<!-- token-budget-impact: ~300 tokens when loaded as context -->

# Smoke-test layered service layout

```
src/main/java/com/acme/billing/
├── BillingApplication.java
├── feature/
│   └── invoices/
│       ├── InvoiceController.java          // thin: validate, delegate, return record
│       ├── InvoiceService.java             // @Service + @Transactional(readOnly=true)
│       ├── InvoiceRepository.java          // JpaRepository<Invoice, Long>
│       ├── InvoiceMapper.java              // @Mapper(componentModel="spring")
│       └── dto/
│           ├── CreateInvoiceRequest.java   // record
│           └── InvoiceResponse.java        // record
└── shared/
    ├── error/
    │   └── GlobalExceptionAdvice.java      // @RestControllerAdvice → ProblemDetail
    └── config/
        └── WebConfig.java
```

Endpoints:

- `GET /api/v1/invoices?page=0&size=20` → `Page<InvoiceResponse>`
- `POST /api/v1/invoices` → 201 + `InvoiceResponse`
- `GET /api/v1/invoices/{id}` → 200 / 404 via `ProblemDetail`
