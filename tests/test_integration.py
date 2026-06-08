"""Integration tests against a live dockware Shopware 6 container.

These exercise the resource clients end-to-end. The ``docker_container`` fixture
(see conftest.py) auto-starts/stops dockware; clients use
``use_docker_test_container=True`` to target ``http://localhost``.
"""

from __future__ import annotations

import uuid
from decimal import Decimal

import pytest

from lib_shopware6_api import Currency, DeliveryTime, Media, Product, Tax, Unit


@pytest.mark.integration
@pytest.mark.usefixtures("docker_container")
class TestReadResources:
    def test_currency_get_currencies(self) -> None:
        currencies = Currency(use_docker_test_container=True).get_currencies()
        assert isinstance(currencies, list)
        assert len(currencies) > 0

    def test_currency_id_by_iso_code(self) -> None:
        currency_id = Currency(use_docker_test_container=True).get_currency_id_by_iso_code("EUR")
        assert len(currency_id) == 32

    def test_tax_get_taxes_and_lookup(self) -> None:
        tax = Tax(use_docker_test_container=True)
        assert len(tax.get_taxes()) > 0
        assert len(tax.get_tax_id_by_name("Standard rate")) == 32
        assert isinstance(tax.get_tax_rate_by_name("Standard rate"), Decimal)

    def test_unit_get_units(self) -> None:
        assert isinstance(Unit(use_docker_test_container=True).get_units(), list)

    def test_delivery_times(self) -> None:
        dt = DeliveryTime(use_docker_test_container=True)
        assert isinstance(dt.get_delivery_times(), list)
        assert isinstance(dt.get_delivery_times_sorted_by_min_days(), list)


@pytest.mark.integration
@pytest.mark.usefixtures("docker_container")
class TestProductLifecycle:
    def test_insert_get_delete_product(self) -> None:
        product = Product(use_docker_test_container=True)
        product_number = f"itest-{uuid.uuid4().hex[:10]}"
        product_id = product.insert_product(
            name="lib_shopware6_api integration test",
            product_number=product_number,
            price_brutto=Decimal("9.99"),
            stock=1,
        )
        assert len(product_id) == 32
        try:
            assert product.get_product_id_by_product_number(product_number=product_number) == product_id
        finally:
            product.delete_product_by_id(product_id=product_id)


@pytest.mark.integration
@pytest.mark.usefixtures("docker_container")
class TestMediaFolderLifecycle:
    def test_upsert_get_delete_media_folder(self) -> None:
        media = Media(use_docker_test_container=True)
        path = f"/Product Media/itest_{uuid.uuid4().hex[:8]}"
        folder_id = media.upsert_media_folders_by_path(path)
        assert folder_id is not None
        try:
            assert media.get_media_folder_id_by_path(path_media_folder=path) == folder_id
        finally:
            media.delete_media_folder_by_path(path, force=True)


class TestCliIntegration:
    """The read-only CLI commands work end-to-end against the dockware container."""

    @pytest.mark.integration
    @pytest.mark.usefixtures("docker_container", "dockware_env")
    def test_test_connection_reports_ok(self) -> None:
        from click.testing import CliRunner

        from lib_shopware6_api.lib_shopware6_api_cli import cli_main

        result = CliRunner().invoke(cli_main, ["test-connection"])
        assert result.exit_code == 0, result.output
        assert "Admin API  OK" in result.output

    @pytest.mark.integration
    @pytest.mark.usefixtures("docker_container", "dockware_env")
    def test_list_currencies_returns_json(self) -> None:
        import json

        from click.testing import CliRunner

        from lib_shopware6_api.lib_shopware6_api_cli import cli_main

        result = CliRunner().invoke(cli_main, ["list", "currencies"])
        assert result.exit_code == 0, result.output
        assert isinstance(json.loads(result.output), list)
