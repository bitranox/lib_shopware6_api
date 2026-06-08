"""CLI for lib_shopware6_api."""

# STDLIB
import json
import os
import platform
import socket
import sys
from pathlib import Path
from typing import Any

# OWN
import lib_cli_exit_tools

# EXT
import rich_click as click
from lib_layered_config import is_sensitive
from lib_shopware6_api_base import (
    ConfigurationError,
    Shopware6AdminAPIClientBase,
    ShopwareAPIError,
    require_config_from_env,
)
from lib_shopware6_api_base import __init__conf__ as base_conf
from lib_shopware6_api_base.config import get_config, get_default_config_path

# PROJ
from . import __init__conf__
from .exit_codes import ExitCode
from .lib_shopware6_api import Shopware6API
from .logging_setup import init_logging, shutdown_logging

# CONSTANTS
CLICK_CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}

# Connection-test endpoint: returns {"version": "6.x.y.z", ...} on any reachable shop.
_VERSION_ENDPOINT = "_info/version"

# Secrets masked in `config show`. lib_layered_config flags password/client_secret;
# the Store access key and OAuth client_id are credential material it does not catch.
_MASK = "***REDACTED***"
_EXTRA_SENSITIVE_KEYS = frozenset({"store_api_sw_access_key", "client_id"})


def _get_exit_code(exc: BaseException) -> int:
    """Map exceptions to exit codes, printing the diagnostic the user needs to see.

    run_cli installs this in place of its default exception handler, so it must also
    emit the message the default would have printed - otherwise every error exits with
    a bare code and no output. Signals exit cleanly and quietly (no traceback); all
    other errors print the message (terse, or a full traceback when --traceback is set)
    before the mapped exit code is returned.
    """
    if isinstance(exc, lib_cli_exit_tools.SigIntInterrupt):
        return ExitCode.SIGINT
    if isinstance(exc, lib_cli_exit_tools.SigTermInterrupt):
        return ExitCode.SIGTERM
    if isinstance(exc, BrokenPipeError):
        return ExitCode.SIGPIPE
    lib_cli_exit_tools.print_exception_message()
    if isinstance(exc, ConfigurationError):
        return ExitCode.CONFIGURATION_ERROR
    if isinstance(exc, ShopwareAPIError):
        return ExitCode.API_ERROR
    if isinstance(exc, ValueError):
        return ExitCode.INVALID_ARGUMENT
    return lib_cli_exit_tools.get_system_exit_code(exc)


def _build_api() -> Shopware6API:
    """Build a Shopware6API from the layered config (raises ConfigurationError if unconfigured)."""
    return Shopware6API(config=require_config_from_env())


def _echo_json(data: object) -> None:
    """Print a value as indented JSON."""
    click.echo(json.dumps(data, indent=2, default=str, sort_keys=False))


def _mask_section(section: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of a config section with non-empty secret values masked."""
    masked: dict[str, Any] = {}
    for key, value in section.items():
        secret = is_sensitive(key) or key in _EXTRA_SENSITIVE_KEYS
        masked[key] = _MASK if secret and value not in ("", None) else value
    return masked


def _config_locations() -> list[tuple[str, Path]]:
    """Return the (layer, file) config lookup locations for the current platform.

    Configuration is loaded by lib_shopware6_api_base, so these use its vendor / app / slug.
    """
    vendor = base_conf.LAYEREDCONF_VENDOR
    app = base_conf.LAYEREDCONF_APP
    slug = base_conf.LAYEREDCONF_SLUG
    hostname = socket.gethostname()
    system = platform.system()
    if system == "Windows":
        system_base = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / vendor / app
        user_base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / vendor / app
    elif system == "Darwin":
        system_base = Path("/Library/Application Support") / vendor / app
        user_base = Path.home() / "Library" / "Application Support" / vendor / app
    else:  # Linux / other POSIX (XDG)
        system_base = Path("/etc/xdg") / slug
        user_base = Path.home() / ".config" / slug
    return [
        ("app", system_base / "config.toml"),
        ("host", system_base / "hosts" / f"{hostname}.toml"),
        ("user", user_base / "config.toml"),
    ]


def info() -> None:
    """
    >>> info()
    Info for ...

    """
    __init__conf__.print_info()


@click.group(help=__init__conf__.title, context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
@click.version_option(
    version=__init__conf__.version,
    prog_name=__init__conf__.shell_command,
    message=f"{__init__conf__.shell_command} version {__init__conf__.version}",
)
@click.option("--traceback/--no-traceback", is_flag=True, type=bool, default=None, help="return traceback information on cli")
def cli_main(traceback: bool | None = None) -> None:
    """Main CLI entry point."""
    if traceback is not None:
        lib_cli_exit_tools.config.traceback = traceback


@cli_main.command("info", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
def cli_info() -> None:
    """Get program information."""
    info()


@cli_main.command("test-connection", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
def cli_test_connection() -> None:
    """Check that the configured credentials can reach Shopware.

    Authenticates against the Admin API and reports the grant type and shop version.
    Reads the configuration from the layered config / .env (via lib_shopware6_api_base).
    """
    config = require_config_from_env()
    with Shopware6AdminAPIClientBase(config=config) as admin:
        version = admin.request_get(_VERSION_ENDPOINT).model_dump().get("version", "unknown")
    click.echo(f"Admin API  OK    {config.shopware_admin_api_url}  (grant_type={config.grant_type.name}, shopware {version})")


@cli_main.command("get-product", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
@click.argument("product_number")
def cli_get_product(product_number: str) -> None:
    """Resolve a product's id by its product number and print it as JSON."""
    product_id = _build_api().product.get_product_id_by_product_number(product_number)
    _echo_json({"product_number": product_number, "product_id": product_id})


@cli_main.group("list", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
def cli_list() -> None:
    """List records (read-only)."""


@cli_list.command("currencies", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
def cli_list_currencies() -> None:
    """List all currencies."""
    _echo_json(_build_api().currency.get_currencies())


@cli_list.command("taxes", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
def cli_list_taxes() -> None:
    """List all tax rates."""
    _echo_json(_build_api().tax.get_taxes())


@cli_list.command("units", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
def cli_list_units() -> None:
    """List all units."""
    _echo_json(_build_api().unit.get_units())


@cli_list.command("delivery-times", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
def cli_list_delivery_times() -> None:
    """List all delivery times."""
    _echo_json(_build_api().delivery_time.get_delivery_times())


@cli_list.command("products", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
@click.option("--limit", type=int, default=10, show_default=True, help="maximum number of products to fetch")
def cli_list_products(limit: int) -> None:
    """List products (limited)."""
    _echo_json(_build_api().product.get_products(payload={"limit": limit}))


@cli_main.group("config", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
def cli_config() -> None:
    """Inspect the layered configuration (managed by lib_shopware6_api_base)."""


@cli_config.command("show", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
@click.option(
    "--section",
    type=click.Choice(["shopware", "lib_log_rich", "all"]),
    default="all",
    help="which section to print",
)
def cli_config_show(section: str) -> None:
    """Print the effective merged configuration, with secrets masked."""
    config = get_config()
    sections = ["shopware", "lib_log_rich"] if section == "all" else [section]
    out = {name: _mask_section(dict(config.get(name, default={}) or {})) for name in sections}
    _echo_json(out)


@cli_config.command("paths", context_settings=CLICK_CONTEXT_SETTINGS)  # type: ignore
def cli_config_paths() -> None:
    """Show where configuration is loaded from on this machine.

    Higher layers override lower ones:
    bundled defaults -> app -> host -> user -> .env -> environment.
    """
    default_path = get_default_config_path()
    click.echo(f"bundled    {default_path}  ({'present' if default_path.exists() else 'missing'})")
    for layer, path in _config_locations():
        marker = "present" if path.exists() else "not present"
        click.echo(f"{layer:10s} {path}  ({marker})")
    dotenv = Path.cwd() / ".env"
    click.echo(f"dotenv     {dotenv}  ({'present' if dotenv.exists() else 'not present'})")
    click.echo("env prefix LIB_SHOPWARE6_API_BASE___<SECTION>__<KEY>")


def main() -> int:
    """Entry point with logging setup and proper signal handling."""
    init_logging()
    # cli_main sets the process-global lib_cli_exit_tools.config.traceback from --traceback;
    # snapshot and restore it so the flag does not leak into later in-process invocations.
    traceback_default = lib_cli_exit_tools.config.traceback
    try:
        return lib_cli_exit_tools.run_cli(
            cli_main,
            exception_handler=_get_exit_code,
            install_signals=True,
        )
    finally:
        lib_cli_exit_tools.config.traceback = traceback_default
        shutdown_logging()


# entry point if main
if __name__ == "__main__":
    sys.exit(main())
