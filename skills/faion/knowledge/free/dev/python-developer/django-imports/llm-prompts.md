# LLM Prompts for Django Import Organization

Effective prompts for using Claude, Cursor, and other LLMs to organize Django imports.

## Quick Reference

| Task | Prompt Type |
|------|-------------|
| Organize single file | Single File Reorganization |
| Fix circular imports | Circular Import Detection |
| Configure Ruff | Configuration Generation |
| Review imports | Import Audit |
| Migrate to Ruff | Migration from isort |

## Single File Reorganization

### Basic Reorganization

```
Reorganize the imports in this Django file following these conventions:

1. Import order: __future__, stdlib, third-party (Django first), first-party, local
2. Cross-app imports use aliases (from apps.X import models as X_models)
3. Local imports use relative syntax (.models, .services)
4. TYPE_CHECKING block at end for type-only imports
5. Add `from __future__ import annotations` if Python 3.9+

File:
```python
[PASTE YOUR FILE HERE]
```

Python version: 3.11
Project structure: apps/{app_name}/
```

### With Context

```
Given this Django project structure:
- apps/users/ (User model)
- apps/orders/ (Order, OrderItem models)
- apps/catalog/ (Product, Category models)
- apps/payments/ (Payment model)

Reorganize imports in this file, using:
1. Aliases for cross-app model imports
2. String references for ForeignKey to other apps
3. TYPE_CHECKING for type annotations that would cause circular imports

File:
```python
[PASTE YOUR FILE HERE]
```
```

## Circular Import Detection

### Detect and Fix

```
Analyze these Django files for circular import issues:

File 1 (apps/orders/services.py):
```python
[PASTE FILE 1]
```

File 2 (apps/payments/services.py):
```python
[PASTE FILE 2]
```

For each circular import found:
1. Explain why it's circular
2. Suggest the best fix (TYPE_CHECKING, lazy import, apps.get_model, signals)
3. Provide the corrected code
```

### Architecture-Level Analysis

```
I have a Django project with these apps and their dependencies:

- users: no dependencies
- orders: depends on users, catalog
- catalog: no dependencies
- payments: depends on orders, users
- notifications: depends on users, orders, payments

Analyze this dependency graph for:
1. Potential circular import issues
2. Architectural improvements to reduce coupling
3. Recommended import patterns for each app

Provide a dependency diagram and corrected import structure.
```

## Configuration Generation

### Ruff Configuration

```
Generate a Ruff configuration for my Django project with:

- Python 3.11
- Django 5.x + DRF
- Celery for async tasks
- First-party apps in "apps/" directory
- Line length 88 (Black-compatible)
- Enable Django-specific rules
- Skip migrations folder

Include:
1. pyproject.toml [tool.ruff] section
2. Pre-commit configuration
3. VS Code settings for Ruff integration
```

### Project-Specific Configuration

```
Create a Ruff isort configuration for:

Project structure:
```
myproject/
  apps/
    users/
    orders/
    catalog/
  config/
    settings/
    urls.py
  core/
    models.py
    mixins.py
```

Third-party packages: django, rest_framework, celery, boto3, stripe

Requirements:
- Django imports grouped together
- DRF imports after Django
- apps/* as first-party
- config/* and core/* as first-party
```

## Import Audit

### Full Audit

```
Audit imports in this Django file for:

1. ❌ Wildcard imports (from X import *)
2. ❌ Direct class imports from other apps (should use aliases)
3. ❌ Multi-dot relative imports (../.. should be absolute)
4. ❌ Circular import risks
5. ❌ Missing TYPE_CHECKING for type-only imports
6. ❌ Wrong import order
7. ⚠️ Unnecessary imports
8. ⚠️ Duplicate imports

File:
```python
[PASTE YOUR FILE HERE]
```

For each issue, provide:
- Line number
- Problem description
- Corrected import
```

### Cross-File Audit

```
Audit these related Django files for import consistency:

models.py:
```python
[PASTE]
```

services.py:
```python
[PASTE]
```

serializers.py:
```python
[PASTE]
```

views.py:
```python
[PASTE]
```

Check for:
1. Consistent alias usage across files
2. Consistent import order
3. Circular import risks between these files
4. TYPE_CHECKING usage consistency
```

## Migration Prompts

### From isort to Ruff

```
I'm migrating from isort to Ruff. Convert my configuration:

Current .isort.cfg:
```ini
[settings]
profile = django
line_length = 88
known_first_party = apps
known_third_party = django,rest_framework,celery
skip = .venv,migrations
```

Provide:
1. Equivalent Ruff configuration in pyproject.toml
2. Any behavioral differences to be aware of
3. Commands to verify the migration
```

### From flake8 to Ruff

```
Convert my flake8 + isort setup to Ruff:

.flake8:
```ini
[flake8]
max-line-length = 88
exclude = .venv,migrations
extend-ignore = E203,W503
```

.isort.cfg:
```ini
[settings]
profile = black
known_first_party = apps
```

Provide complete Ruff configuration that replicates this behavior.
```

## Advanced Patterns

### TYPE_CHECKING Migration

```
Migrate these runtime imports to TYPE_CHECKING pattern:

Current:
```python
from apps.users.models import User
from apps.orders.models import Order
from apps.payments.models import Payment

def process_order(user: User, order: Order) -> Payment:
    ...
```

Conditions:
- User is used only in type hints
- Order is used in type hints AND at runtime (Order.objects.get())
- Payment is used only in type hints

Provide the corrected imports with TYPE_CHECKING.
```

### Lazy Import Refactoring

```
Refactor this file to use lazy imports where beneficial:

```python
# Heavy imports at module level
from apps.reports.generators import PDFGenerator, ExcelGenerator
from apps.analytics.calculators import ComplexMetricsCalculator
from apps.integrations.stripe import StripeClient

class OrderService:
    def generate_invoice(self, order):
        # PDFGenerator used only here
        return PDFGenerator().generate(order)

    def export_orders(self, orders, format):
        # Generators used conditionally
        if format == "pdf":
            return PDFGenerator().generate_batch(orders)
        return ExcelGenerator().generate_batch(orders)
```

Move imports to be lazy where it improves startup time without harming readability.
```

### Signal-Based Decoupling

```
Refactor these tightly coupled services to use Django signals:

apps/orders/services.py:
```python
from apps.payments.services import PaymentService
from apps.notifications.services import NotificationService
from apps.inventory.services import InventoryService

class OrderService:
    def complete_order(self, order):
        order.status = "completed"
        order.save()
        PaymentService.charge(order)
        NotificationService.send_order_complete(order)
        InventoryService.decrement_stock(order.items)
```

Provide:
1. Signal definitions for order events
2. Receiver functions in each app
3. Updated OrderService without direct imports
```

## Prompt Templates for Cursor/Copilot

### Inline Comment Prompt

```python
# Cursor: Reorganize imports following Django conventions,
# use aliases for cross-app imports, add TYPE_CHECKING block
from apps.users.models import User
from django.db import models
from apps.orders.models import Order
import logging
from .services import MyService
from rest_framework import serializers
```

### Selection Prompt

```
/edit Reorganize these imports:
1. __future__ first
2. stdlib, third-party (Django first), first-party with aliases, local
3. Add TYPE_CHECKING for type-only imports
```

### Chat Prompt

```
I have a circular import between apps/orders/models.py and apps/payments/models.py.
Both need to reference each other's models.

Options I know:
1. String references for ForeignKey
2. apps.get_model()
3. TYPE_CHECKING
4. Lazy imports

Which is best for my case where:
- Order has FK to Payment
- Payment has FK to Order
- Both are used in serializers
```

## Validation Prompts

### Verify Reorganization

```
Verify this import reorganization is correct:

Before:
```python
[PASTE BEFORE]
```

After:
```python
[PASTE AFTER]
```

Check:
1. No functionality changed
2. Import order correct
3. No new circular import risks
4. TYPE_CHECKING used correctly
5. Aliases consistent with project style
```

### Pre-PR Review

```
Review imports in this PR for Django best practices:

Changed files:
1. apps/orders/views.py
2. apps/orders/services.py
3. apps/payments/handlers.py

[PASTE DIFFS]

Flag any:
- Import order violations
- Missing TYPE_CHECKING
- Potential circular imports
- Inconsistent alias usage
```
