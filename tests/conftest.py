"""Pytest fixtures and OS-specific markers.

Integration tests (``@pytest.mark.integration``) run against a local dockware
container, which this module auto-starts and stops. Resource clients are then
constructed with ``use_docker_test_container=True``.
"""

from __future__ import annotations

import subprocess
import sys
import time
from typing import TYPE_CHECKING

import httpx2
import pytest

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

    from _pytest.config import Config
    from _pytest.nodes import Item

DOCKER_CONTAINER_NAME = "dockware"
DOCKER_IMAGE = "dockware/dev:latest"
REQUEST_TIMEOUT = httpx2.Timeout(30.0, connect=10.0)


def pytest_collection_modifyitems(config: Config, items: list[Item]) -> None:
    """Auto-skip OS-specific tests on the wrong platform."""
    for item in items:
        if item.get_closest_marker("os_windows") and sys.platform != "win32":
            item.add_marker(pytest.mark.skip(reason="Windows-only test"))
        if item.get_closest_marker("os_macos") and sys.platform != "darwin":
            item.add_marker(pytest.mark.skip(reason="macOS-only test"))
        if item.get_closest_marker("os_linux") and not sys.platform.startswith("linux"):
            item.add_marker(pytest.mark.skip(reason="Linux-only test"))
        if item.get_closest_marker("os_posix") and sys.platform == "win32":
            item.add_marker(pytest.mark.skip(reason="POSIX-only test"))


#: The variables lib_layered_config reads the app and host layers' root from, one per platform.
#: All three are set on every OS: Windows looks up ``ProgramData`` in mixed case after
#: ``LIB_LAYERED_CONFIG_PROGRAMDATA``, while ``os.environ`` upper-cases its keys there, so redirecting
#: ``PROGRAMDATA`` alone still reads the real ``C:\ProgramData``.
SYSTEM_LAYER_ROOT_VARIABLES: tuple[str, ...] = (
    "LIB_LAYERED_CONFIG_ETC",
    "LIB_LAYERED_CONFIG_MAC_APP_ROOT",
    "LIB_LAYERED_CONFIG_PROGRAMDATA",
)


@pytest.fixture(autouse=True)
def system_layers_in_tmp_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Point the app and host configuration layers at an empty directory under ``tmp_path``.

    A machine with the CLI deployed system-wide would otherwise decide results: a value in its
    ``/etc/xdg/<slug>/config.d/`` fails tests there while a clean CI runner stays green. A
    subprocess inherits the redirect through ``os.environ``; one that builds its own environment
    must carry these variables over (see ``SYSTEM_LAYER_ROOT_VARIABLES``).

    Returns:
        The redirected root, so a test can place a file in the app or host layer.
    """
    root = tmp_path / "system-layers"
    for name in SYSTEM_LAYER_ROOT_VARIABLES:
        monkeypatch.setenv(name, str(root))
    return root


@pytest.fixture
def app_layer_config_file(system_layers_in_tmp_path: Path) -> Path:
    """Return where the app layer's ``config.toml`` lives under the redirect, its directory created.

    The location is asked of lib_layered_config, which shares it between its deploy and its reader,
    because the layout under the root differs per OS.
    """
    from lib_layered_config import deploy_config_paths
    from lib_shopware6_api_base import __init__conf__
    from lib_shopware6_api_base.config import get_default_config_path

    paths = deploy_config_paths(
        get_default_config_path(),
        vendor=__init__conf__.LAYEREDCONF_VENDOR,
        app=__init__conf__.LAYEREDCONF_APP,
        slug=__init__conf__.LAYEREDCONF_SLUG,
        targets=["app"],
    )
    config_file = next(path for path in paths if path.name == "config.toml")
    # Refuse before anything writes: without the redirect this is a real system directory, and the
    # elevated Windows runner would let a write through.
    assert config_file.is_relative_to(system_layers_in_tmp_path.resolve()), config_file
    config_file.parent.mkdir(parents=True)
    return config_file


def _docker_engine_is_linux() -> bool:
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{.OSType}}"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
    return result.stdout.strip().lower() == "linux"


def _is_docker_container_active() -> bool:
    try:
        response = httpx2.get("http://localhost/admin", timeout=REQUEST_TIMEOUT, follow_redirects=True)
        return response.status_code in (200, 302, 403)
    except (httpx2.ConnectError, httpx2.ReadError, httpx2.TimeoutException):
        return False


def _is_docker_container_running() -> bool:
    try:
        result = subprocess.run(
            ["docker", "ps", "-q", "-f", f"name={DOCKER_CONTAINER_NAME}"],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return False
    return bool(result.stdout.strip())


def _start_docker_container() -> None:
    try:
        subprocess.run(
            ["docker", "run", "-d", "--rm", "-p", "80:80", "--name", DOCKER_CONTAINER_NAME, DOCKER_IMAGE],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        pytest.skip("Docker not available for integration tests")
    except subprocess.CalledProcessError as exc:
        pytest.skip(f"Docker container failed to start: {exc.stderr}")


def _stop_docker_container() -> None:
    subprocess.run(["docker", "stop", DOCKER_CONTAINER_NAME], capture_output=True, text=True, check=False)


def _wait_for_docker_container_ready(timeout_s: int = 600) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if _is_docker_container_active():
            return True
        time.sleep(10)
    return False


@pytest.fixture(scope="session")
def docker_container() -> Generator[None, None, None]:
    """Ensure a dockware container is running for integration tests."""
    started_here = False
    if not _docker_engine_is_linux():
        pytest.skip("Docker engine is unavailable or not Linux; dockware/dev requires Linux containers")

    if not _is_docker_container_active():
        if _is_docker_container_running():
            if not _wait_for_docker_container_ready():
                pytest.skip("Docker container failed to become ready")
        else:
            _start_docker_container()
            started_here = True
            if not _wait_for_docker_container_ready():
                _stop_docker_container()
                pytest.skip("Docker container failed to start")

    yield

    if started_here:
        _stop_docker_container()


@pytest.fixture
def dockware_env(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Point the layered config at the dockware container, with the cache cleared on both ends.

    Seeds the ``LIB_SHOPWARE6_API_BASE___SHOPWARE__*`` environment from the single source of
    truth (``get_docker_test_config``) so the bare ``Resource()`` / ``require_config_from_env``
    paths resolve to ``http://localhost``. The cached config is cleared before (to drop any
    previously cached config) and after (so this dockware config never leaks into a later test).
    """
    from lib_shopware6_api_base.config import get_config

    from lib_shopware6_api._conf_helper import get_docker_test_config

    config = get_docker_test_config()
    env = {
        "ADMIN_API_URL": config.shopware_admin_api_url,
        "STOREFRONT_API_URL": config.shopware_storefront_api_url,
        "USERNAME": config.username,
        "PASSWORD": config.password,
        "GRANT_TYPE": config.grant_type.name,
    }
    prefix = "LIB_SHOPWARE6_API_BASE___SHOPWARE__"
    for key, value in env.items():
        monkeypatch.setenv(prefix + key, value)
    get_config.cache_clear()
    try:
        yield
    finally:
        get_config.cache_clear()
