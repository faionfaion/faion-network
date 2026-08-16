# C4 Model for Architecture Visualization

## Summary

**One-sentence:** Hierarchical diagrams at four levels: System Context, Containers, Components, Code. Locked toolchain (Structurizr / Mermaid / PlantUML) and per-level audience.

**One-paragraph:** C4 (Simon Brown) gives architecture diagrams a hierarchy: Level 1 Context (system + users + external systems), Level 2 Containers (deployable units + tech), Level 3 Components (internals of one container), Level 4 Code (class diagrams, usually auto-generated). Output is a diagram pack at Levels 1-3 + a chosen toolchain + a sync-with-code policy.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Stakeholders ask 'how does this system fit together?' more than once a quarter.
- Onboarding a new engineer takes > 1 day on architecture alone.
- You have ≥1 external integration or ≥3 deployable containers.

## Skip If (ANY kills it)

- Single binary, single DB, no external integrations.
- No stakeholders beyond the implementing engineer.
- Architecture changes weekly — diagrams will stale before they ship.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| System inventory | list of containers + tech | tech lead |
| External integrations | list | tech lead |
| Toolchain decision | Structurizr / Mermaid / PlantUML | team consensus |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/architecture-decision-records` | Toolchain choice is recorded as an ADR. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the diagram pack + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: tool choice → L1 context → L2 containers → L3 components → sync policy | ~700 |
| `content/05-examples.xml` | medium | Worked example: Context + Containers diagrams for a SaaS shop | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-l1-context` | sonnet | Synthesize external systems + actors. |
| `draft-l2-containers` | sonnet | Per-container tech + relationships. |
| `audit-staleness` | opus | Compare diagrams against current repo + manifests. |

## Templates

| File | Purpose |
|------|---------|
| `templates/c4-diagram-pack.md` | C4 diagram-pack spec listing levels + toolchain + sync policy. |
| `templates/structurizr-workspace.dsl` | Structurizr DSL workspace skeleton: system + actors + container view scaffolding. |
| `templates/plantuml-context.puml` | PlantUML C4 Context-diagram template using `C4-PlantUML` includes. |
| `templates/mermaid-container.md.j2` | Mermaid Container-diagram template inside a Markdown fence for repo docs. |
| `templates/mermaid-container.md` | Mermaid Container-diagram template inside a Markdown fence for repo docs. Generated from `templates/mermaid-container.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-c4-model.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[architecture-decision-records]]
- [[arch-pattern-clean]]
- [[decision-tree-architecture-style]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/structurizr-workspace.dsl`

```text
workspace "{System Name}" "{Short system description}" {

    model {
        # --- Persons (users/personas) ---
        customer = person "Customer" "A user of the system" "External"
        admin    = person "Admin"    "Internal administrator" "Internal"

        # --- Your Software System ---
        mySystem = softwareSystem "{System Name}" "Brief description of what it does" {
            # --- Level 2: Containers ---
            webApp = container "Web Application" "React SPA; serves the single-page app" "React 18, TypeScript" {
                tags "Web Browser"
            }

            apiService = container "API Service" "Handles all business logic and data access" "Django 5, Python 3.12" {
                tags "Service"
                # --- Level 3: Components (optional, for complex containers) ---
                orderComponent   = component "Order Management" "Creates, tracks, and cancels orders"      "Django app: orders"
                paymentComponent = component "Payment Processing" "Charges cards and manages refunds"      "Django app: payments"
                authComponent    = component "Auth"               "JWT issuance and validation"             "djangorestframework-simplejwt"
            }

            database = container "Database" "Stores all application data" "PostgreSQL 16" {
                tags "Database"
            }

            cache = container "Cache" "Session store and hot-path caching" "Redis 7" {
                tags "Cache"
            }

            messageQueue = container "Message Queue" "Async inter-module communication" "Redis Streams" {
                tags "Queue"
            }
        }

        # --- External Software Systems ---
        emailProvider = softwareSystem "Email Provider" "Sends transactional email" "External"
        paymentGateway = softwareSystem "Payment Gateway" "Processes card payments" "External"

        # --- Relationships: Persons → System ---
        customer -> webApp "Uses" "HTTPS"
        admin    -> webApp "Manages" "HTTPS"

        # --- Relationships: Containers ---
        webApp       -> apiService   "Makes API calls" "HTTPS/REST, JSON"
        apiService   -> database     "Reads/writes"    "PostgreSQL protocol"
        apiService   -> cache        "Reads/writes"    "Redis protocol"
        apiService   -> messageQueue "Publishes events" "Redis Streams"

        # --- Relationships: Components ---
        orderComponent   -> paymentComponent "Triggers payment" "In-process call"
        paymentComponent -> paymentGateway   "Charges card"     "HTTPS/REST"
        apiService       -> emailProvider    "Sends email"      "SMTP/TLS"
    }

    views {
        # Level 1: System Context
        systemContext mySystem "SystemContext" "System Context diagram for {System Name}" {
            include *
            autoLayout lr
        }

        # Level 2: Container
        container mySystem "Containers" "Container diagram for {System Name}" {
            include *
            autoLayout lr
        }

        # Level 3: Component (for the API service)
        component apiService "APIComponents" "Component diagram for the API Service" {
            include *
            autoLayout lr
        }

        # Styles
        styles {
            element "External" {
                background #999999
                color #ffffff
            }
            element "Database" {
                shape Cylinder
            }
            element "Cache" {
                shape Cylinder
                background #f5a623
            }
            element "Queue" {
                shape Pipe
            }
            element "Web Browser" {
                shape WebBrowser
            }
        }
    }
}
```

### `templates/plantuml-context.puml`

```plantuml
' purpose: C4 Context diagram in PlantUML.
' consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
' produces: a c4-model artefact validating against scripts/validate-c4-model.py
' depends-on: content/01-core-rules.xml, content/02-output-contract.xml
' token-budget-impact: ~400-1500 tokens once filled
@startuml SystemContext

!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

' Optional: override default styling
' LAYOUT_WITH_LEGEND()
LAYOUT_LEFT_RIGHT()

title System Context — {System Name}

' Persons (users)
Person(customer, "Customer", "Uses the system to browse and purchase")
Person_Ext(partner, "Partner", "External partner with API access")

' Your system (in scope)
System(mySystem, "{System Name}", "Manages orders, users, payments, and notifications")

' External systems (out of scope)
System_Ext(emailSystem,   "Email Provider",   "Sends transactional and marketing email (SendGrid)")
System_Ext(paymentSystem, "Payment Gateway",  "Processes card payments (Stripe)")
System_Ext(authProvider,  "Identity Provider","Social login (Google OAuth 2.0)")

' Relationships
Rel(customer, mySystem, "Uses", "HTTPS")
Rel(partner,  mySystem, "Integrates with", "HTTPS / REST API")
Rel(mySystem, emailSystem,   "Sends email via",     "SMTP / REST API")
Rel(mySystem, paymentSystem, "Processes payments",  "HTTPS / REST API")
Rel(mySystem, authProvider,  "Authenticates via",   "OIDC / HTTPS")

@enduml
```
