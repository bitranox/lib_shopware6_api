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
