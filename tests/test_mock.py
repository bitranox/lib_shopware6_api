"""Mock-based unit tests for the resource read/lookup logic (no Shopware needed).

The resource methods are thin wrappers over the base admin client; here we inject a
mock client so the payload-building and response-parsing logic is exercised offline.
End-to-end behaviour is covered by the dockware integration suite.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from lib_shopware6_api import Currency, DeliveryTime, Tax, Unit


def _mock_client(data: list[dict[str, Any]]) -> MagicMock:
    """A mock admin client whose request_* methods all return ``{"data": data}``."""
    client = MagicMock()
    response = {"data": data}
    for method in ("request_get", "request_get_paginated", "request_post", "request_post_paginated"):
        getattr(client, method).return_value = response
    return client


class TestCurrencyMocked:
    @pytest.mark.os_agnostic
    def test_get_currencies(self) -> None:
        assert Currency(admin_client=_mock_client([{"id": "a"}])).get_currencies() == [{"id": "a"}]

    @pytest.mark.os_agnostic
    def test_get_currency_id_by_iso_code(self) -> None:
        assert Currency(admin_client=_mock_client([{"id": "cur-id"}])).get_currency_id_by_iso_code("EUR") == "cur-id"

    @pytest.mark.os_agnostic
    def test_get_currency_id_not_found(self) -> None:
        with pytest.raises(FileNotFoundError, match="not found"):
            Currency(admin_client=_mock_client([])).get_currency_id_by_iso_code("nope")


class TestTaxMocked:
    @pytest.mark.os_agnostic
    def test_get_taxes(self) -> None:
        assert Tax(admin_client=_mock_client([{"id": "t"}])).get_taxes() == [{"id": "t"}]

    @pytest.mark.os_agnostic
    def test_get_tax_id_by_name(self) -> None:
        assert Tax(admin_client=_mock_client([{"id": "tax-id"}])).get_tax_id_by_name("Standard rate") == "tax-id"

    @pytest.mark.os_agnostic
    def test_get_tax_id_not_found(self) -> None:
        with pytest.raises(FileNotFoundError, match="not found"):
            Tax(admin_client=_mock_client([])).get_tax_id_by_name("nope")


class TestUnitMocked:
    @pytest.mark.os_agnostic
    def test_get_units(self) -> None:
        assert Unit(admin_client=_mock_client([{"id": "u"}])).get_units() == [{"id": "u"}]


class TestDeliveryTimeMocked:
    @pytest.mark.os_agnostic
    def test_get_delivery_times(self) -> None:
        assert DeliveryTime(admin_client=_mock_client([{"id": "d"}])).get_delivery_times() == [{"id": "d"}]
