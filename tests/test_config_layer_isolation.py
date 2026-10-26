"""The suite never reads the app, host or user configuration layer of the machine it runs on.

A host with the CLI deployed system-wide (``/etc/xdg/<slug>/`` on Linux, ``/Library/Application
Support/<vendor>/<app>/`` on macOS, ``C:\\ProgramData\\<vendor>\\<app>\\`` on Windows), or a
developer with a user-layer deploy (``~/.config/<slug>/``, ``~/Library/Application Support/``,
``%APPDATA%``), would otherwise decide test results: a ``config.d/99-*.toml`` setting a value there
makes tests fail on that machine while a clean CI runner stays green. These tests ask
lib_layered_config where those layers live, with the code its deploy and its reader share, rather
than inspecting the environment variables the conftest sets.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from lib_layered_config import deploy_config_paths
from lib_shopware6_api_base import __init__conf__
from lib_shopware6_api_base.config import get_config, get_default_config_path

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path


@pytest.fixture
def fresh_config_cache() -> Iterator[None]:
    """Clear ``get_config``'s cache before and after, so the probe value cannot reach another test."""
    get_config.cache_clear()
    yield
    get_config.cache_clear()


@pytest.mark.os_agnostic
@pytest.mark.parametrize("target", ["app", "host", "user"])
def test_every_config_layer_resolves_inside_the_test_s_own_directory(target: str, tmp_path: Path) -> None:
    paths = deploy_config_paths(
        get_default_config_path(),
        vendor=__init__conf__.LAYEREDCONF_VENDOR,
        app=__init__conf__.LAYEREDCONF_APP,
        slug=__init__conf__.LAYEREDCONF_SLUG,
        targets=[target],
    )
    outside = sorted(path for path in paths if not path.is_relative_to(tmp_path.resolve()))

    assert outside == [], f"the {target} layer resolves outside this test's directory: {outside}"


@pytest.mark.os_agnostic
def test_a_file_in_the_redirected_app_layer_is_what_the_loader_reads(
    app_layer_config_file: Path, fresh_config_cache: None
) -> None:
    app_layer_config_file.write_text('[layer_isolation_probe]\nread_from = "redirected app layer"\n', encoding="utf-8")

    config = get_config()

    assert config.get("layer_isolation_probe.read_from") == "redirected app layer"


@pytest.mark.os_agnostic
def test_a_file_in_the_redirected_user_layer_is_what_the_loader_reads(
    user_layer_config_file: Path, fresh_config_cache: None
) -> None:
    user_layer_config_file.write_text('[layer_isolation_probe]\nread_from = "redirected user layer"\n', encoding="utf-8")

    config = get_config()

    assert config.get("layer_isolation_probe.read_from") == "redirected user layer"
