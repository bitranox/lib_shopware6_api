"""Unit tests for the pure/offline parts of lib_shopware6_api (no Shopware needed)."""

from __future__ import annotations

import pytest
from lib_shopware6_api_base import ConfShopware6ApiBase, GrantType

from lib_shopware6_api import (
    Currency,
    DeliveryTime,
    Media,
    Product,
    ProductPicture,
    Shopware6API,
    Tax,
    Unit,
)
from lib_shopware6_api._conf_helper import get_docker_test_config, resolve_config
from lib_shopware6_api.lib_shopware6_api_cli import cli_info, cli_main, info


class TestProductPicture:
    @pytest.mark.os_agnostic
    def test_defaults(self) -> None:
        pic = ProductPicture()
        assert pic.position == 0
        assert pic.url == ""
        assert pic.media_alt is None
        assert pic.upload_media is True

    @pytest.mark.os_agnostic
    def test_construct(self) -> None:
        pic = ProductPicture(position=3, url="http://x/a.jpg", media_alt="alt", media_title="t", upload_media=False)
        assert pic.position == 3
        assert pic.url == "http://x/a.jpg"
        assert pic.media_alt == "alt"
        assert pic.upload_media is False


class TestProductPureFunctions:
    @pytest.mark.os_agnostic
    def test_calc_new_product_id_is_deterministic_md5(self) -> None:
        a = Product.calc_new_product_id(product_number="123")
        b = Product.calc_new_product_id(product_number="123")
        c = Product.calc_new_product_id(product_number="1234")
        assert len(a) == 32
        assert a == b
        assert a != c

    @pytest.mark.os_agnostic
    def test_calc_new_product_media_id_varies_by_position(self) -> None:
        a = Product.calc_new_product_media_id(product_id="123", position=0)
        b = Product.calc_new_product_media_id(product_id="123", position=1)
        assert len(a) == 32
        assert a != b


class TestMediaPureFunctions:
    @pytest.mark.os_agnostic
    def test_calc_media_filename_from_product_number(self) -> None:
        assert (
            Media.calc_media_filename_from_product_number(product_number=123456789, position=1, url="x.jpg") == "123456789_1.jpg"
        )

    @pytest.mark.os_agnostic
    def test_calc_new_media_id_requires_extension(self) -> None:
        assert len(Media.calc_new_media_id(media_filename="123.jpg")) == 32
        with pytest.raises(ValueError, match="must have an extension"):
            Media.calc_new_media_id(media_filename="123")

    @pytest.mark.os_agnostic
    def test_calc_path_media_folder_from_product_number(self) -> None:
        media = Media()
        path = media.calc_path_media_folder_from_product_number(product_number=456789)
        assert path.startswith("/Product Media/api_imported/")
        # md5 sharding: root/xx/xx/xx/<rest>
        assert path.count("/") >= 5


class TestConfHelper:
    @pytest.mark.os_agnostic
    def test_get_docker_test_config(self) -> None:
        config = get_docker_test_config()
        assert config.shopware_admin_api_url == "http://localhost/api"
        assert config.shopware_storefront_api_url == "http://localhost/store-api"
        assert config.grant_type == GrantType.USER_CREDENTIALS

    @pytest.mark.os_agnostic
    def test_resolve_config_explicit_wins(self) -> None:
        explicit = ConfShopware6ApiBase(shopware_admin_api_url="http://explicit/api")
        assert resolve_config(explicit, True) is explicit

    @pytest.mark.os_agnostic
    def test_resolve_config_docker(self) -> None:
        config = resolve_config(None, True)
        assert config.shopware_admin_api_url == "http://localhost/api"


class TestConstruction:
    """Constructing the clients must not require a live Shopware (only the API calls do)."""

    @pytest.mark.os_agnostic
    def test_resource_clients_construct(self) -> None:
        for cls in (Currency, DeliveryTime, Media, Product, Tax, Unit):
            obj = cls(use_docker_test_container=True)
            assert obj._admin_client is not None

    @pytest.mark.os_agnostic
    def test_facade_constructs_all_resources(self) -> None:
        api = Shopware6API(use_docker_test_container=True)
        assert api.currency is not None
        assert api.delivery_time is not None
        assert api.media is not None
        assert api.product is not None
        assert api.tax is not None
        assert api.unit is not None


class TestCli:
    @pytest.mark.os_agnostic
    def test_info_prints_metadata(self, capsys: pytest.CaptureFixture[str]) -> None:
        info()
        out = capsys.readouterr().out
        assert "Info for lib_shopware6_api:" in out
        assert "version" in out

    @pytest.mark.os_agnostic
    def test_cli_callables_exist(self) -> None:
        # the click group + info command are wired
        assert callable(cli_main)
        assert callable(cli_info)

    @pytest.mark.os_agnostic
    def test_new_commands_registered(self) -> None:
        from click.testing import CliRunner

        out = CliRunner().invoke(cli_main, ["-h"]).output.lower()
        for command in ("test-connection", "get-product", "list", "config"):
            assert command in out

    @pytest.mark.os_agnostic
    def test_list_group_lists_resources(self) -> None:
        from click.testing import CliRunner

        out = CliRunner().invoke(cli_main, ["list", "-h"]).output.lower()
        for resource in ("currencies", "taxes", "units", "delivery-times", "products"):
            assert resource in out

    @pytest.mark.os_agnostic
    def test_config_paths_runs(self) -> None:
        from click.testing import CliRunner

        result = CliRunner().invoke(cli_main, ["config", "paths"])
        assert result.exit_code == 0
        assert "bundled" in result.output
        assert "LIB_SHOPWARE6_API_BASE___" in result.output

    @pytest.mark.os_agnostic
    def test_error_prints_diagnostic_message(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
        """A live error must print its message - run_cli's custom handler used to swallow it."""
        import lib_cli_exit_tools

        from lib_shopware6_api.exit_codes import ExitCode
        from lib_shopware6_api.lib_shopware6_api_cli import _get_exit_code

        # pin the terse format so the assertion does not depend on a leaked global --traceback state
        monkeypatch.setattr(lib_cli_exit_tools.config, "traceback", False)
        try:
            raise ValueError("diagnostic_marker_42")
        except ValueError as exc:
            code = _get_exit_code(exc)
        captured = capsys.readouterr()
        assert code == ExitCode.INVALID_ARGUMENT
        assert "diagnostic_marker_42" in (captured.out + captured.err)

    @pytest.mark.os_agnostic
    def test_configuration_error_prints_message(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A domain exception must also print its diagnostic, not just map an exit code."""
        import lib_cli_exit_tools
        from lib_shopware6_api_base import ConfigurationError

        from lib_shopware6_api.exit_codes import ExitCode
        from lib_shopware6_api.lib_shopware6_api_cli import _get_exit_code

        monkeypatch.setattr(lib_cli_exit_tools.config, "traceback", False)
        try:
            raise ConfigurationError("config_marker_99")
        except ConfigurationError as exc:
            code = _get_exit_code(exc)
        captured = capsys.readouterr()
        assert code == ExitCode.CONFIGURATION_ERROR
        assert "config_marker_99" in (captured.out + captured.err)

    @pytest.mark.os_agnostic
    def test_signal_exit_is_quiet(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Signals exit cleanly with no printed traceback, even with an active exception."""
        import lib_cli_exit_tools

        from lib_shopware6_api.exit_codes import ExitCode
        from lib_shopware6_api.lib_shopware6_api_cli import _get_exit_code

        try:
            raise lib_cli_exit_tools.SigIntInterrupt()
        except lib_cli_exit_tools.SigIntInterrupt as exc:
            code = _get_exit_code(exc)
        captured = capsys.readouterr()
        assert code == ExitCode.SIGINT
        assert captured.out == ""
        assert captured.err == ""
