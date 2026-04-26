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
