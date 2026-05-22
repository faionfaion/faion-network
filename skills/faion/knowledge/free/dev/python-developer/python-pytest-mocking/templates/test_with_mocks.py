"""
purpose: Test skeleton: mocker.patch + autospec + AsyncMock + spy examples.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

from unittest.mock import AsyncMock


def test_mocker_patches_use_site(mocker):
    mock_send = mocker.patch(
        "apps.orders.services.send_mail", autospec=True
    )
    from apps.orders.services import confirm_order

    confirm_order(order_id=1)
    mock_send.assert_called_once()


async def test_async_callable_uses_asyncmock(mocker):
    mock_fetch = mocker.patch(
        "apps.users.services.fetch_profile",
        new=AsyncMock(return_value={"id": 1}),
    )
    from apps.users.services import load_user

    result = await load_user(1)
    assert result == {"id": 1}
    mock_fetch.assert_awaited_once_with(1)
