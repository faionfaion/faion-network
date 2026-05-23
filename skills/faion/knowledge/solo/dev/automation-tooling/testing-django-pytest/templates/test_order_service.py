# purpose: Parametrized pytest test with shallow mocks
# consumes: input artefacts described in AGENTS.md ## Prerequisites
# produces: artefact conforming to content/02-output-contract.xml for testing-django-pytest
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1200 tokens when loaded as context

import pytest
from unittest.mock import Mock
from orders.services import create_and_charge


@pytest.mark.django_db
@pytest.mark.parametrize('amount,currency,expected_status', [
    (1000, 'USD', 'charged'),
    (50,   'USD', 'charged'),
    (10000, 'EUR', 'charged'),
], ids=['default', 'small', 'large_eur'])
def test_create_and_charge_marks_charged(order, amount, currency, expected_status):
    payment = Mock()
    payment.charge.return_value = {'ok': True}
    result = create_and_charge(order.customer, amount, currency, payment=payment)
    assert result.status == expected_status
