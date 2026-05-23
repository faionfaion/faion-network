"""
purpose: root conftest.py — register every factory via pytest_factoryboy.register().
consumes: factories declared in tests/factories/*.
produces: auto-created fixtures (user, user_factory, invoice, invoice_factory, ...).
depends-on: pytest-django, factory_boy, pytest-factoryboy.
token-budget-impact: ~180 tokens.
"""

from __future__ import annotations

from pytest_factoryboy import register

from tests.factories.accounts import CustomerFactory, UserFactory
from tests.factories.billing import InvoiceFactory

# Single register() per factory; do NOT manually add @pytest.fixture for the same name.
register(UserFactory)            # creates 'user' + 'user_factory'
register(CustomerFactory)        # creates 'customer' + 'customer_factory'
register(InvoiceFactory)         # creates 'invoice' + 'invoice_factory'

# Multi-factory registration for the same model: use _name to avoid collision.
# register(AdminUserFactory, _name="admin_user")
