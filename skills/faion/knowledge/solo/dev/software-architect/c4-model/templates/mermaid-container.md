# C4 Container Diagram — {System Name}

Rendered natively in GitHub and GitLab. Requires Mermaid 10.3+.

```mermaid
C4Container
    title Container diagram — {System Name}

    Person(customer, "Customer", "Uses the system via browser or mobile")

    System_Boundary(mySystem, "{System Name}") {
        Container(webApp,     "Web Application",  "React 18, TypeScript",   "Single-page app served as static files")
        Container(apiService, "API Service",      "Django 5, Python 3.12",  "Business logic and data access. Exposes REST API")
        Container(worker,     "Background Worker","Celery, Python 3.12",    "Processes async jobs: email, export, webhooks")
        ContainerDb(database, "Database",         "PostgreSQL 16",          "Stores all application data")
        ContainerDb(cache,    "Cache",            "Redis 7",                "Session store, hot-path cache, Celery broker")
    }

    System_Ext(emailSystem,   "Email Provider",  "SendGrid — transactional email")
    System_Ext(paymentSystem, "Payment Gateway", "Stripe — card processing")

    Rel(customer,   webApp,      "Uses",                    "HTTPS")
    Rel(webApp,     apiService,  "Makes API calls",         "HTTPS / REST, JSON")
    Rel(apiService, database,    "Reads/writes",            "PostgreSQL protocol")
    Rel(apiService, cache,       "Reads/writes",            "Redis protocol")
    Rel(apiService, worker,      "Enqueues jobs",           "Celery / Redis")
    Rel(worker,     emailSystem, "Sends email",             "HTTPS / REST API")
    Rel(apiService, paymentSystem, "Processes payments",   "HTTPS / REST API")
```

## Notes

- Replace `{System Name}` with the actual system name.
- Each `Container()` shows: alias, name, technology, description.
- Each `Rel()` shows: from, to, label, protocol.
- Mermaid C4 does not support Deployment diagrams — use Structurizr DSL or PlantUML for those.
- For Level 3 (Component) diagrams use `C4Component` with `Component()` and `ComponentDb()` elements.
