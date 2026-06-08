"""Execute the module doctests as part of the normal test suite.

Doctests carry no pytest marker, so the marker-based unit/integration split
(``make test`` = ``-m "not integration"``, ``make testintegration`` = ``-m
integration``) cannot route them on its own.  We therefore run them explicitly
through :func:`doctest.testmod`, in two buckets:

* **offline** doctests (the package metadata banner, the CLI ``info`` command
  and the facade constructor, which only wires up clients) need nothing external
  and run in the unit suite;
* the **resource** doctests (Currency / Tax / Unit / DeliveryTime / Product /
  Media) construct a bare ``Currency()`` / ``Media()`` / ... which reads the
  config from the environment, then talk to a live Shopware -- they run in the
  dockware-backed integration suite.

A shared namespace injects every public class (``Currency``, ``Product``,
``ProductPicture``, ...) so docstrings can reference them by bare name; the live
bucket additionally points the environment at the dockware container so the
``Resource()`` no-argument constructors resolve to ``http://localhost``.
"""

from __future__ import annotations

import doctest
import importlib

import pytest

import lib_shopware6_api as pkg

OPTIONFLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.IGNORE_EXCEPTION_DETAIL

# Names the docstrings use by bare identifier (Currency, Product, ProductPicture, ...).
_DOCTEST_NAMES: dict[str, object] = {name: getattr(pkg, name) for name in dir(pkg) if not name.startswith("_")}

OFFLINE_MODULES = [
    "lib_shopware6_api.__init__conf__",
    "lib_shopware6_api.lib_shopware6_api_cli",
    "lib_shopware6_api.lib_shopware6_api",
]

LIVE_MODULES = [
    "lib_shopware6_api.sub_currency",
    "lib_shopware6_api.sub_tax",
    "lib_shopware6_api.sub_unit",
    "lib_shopware6_api.sub_delivery_time",
    "lib_shopware6_api.sub_product",
    "lib_shopware6_api.sub_media",
]


def _run_doctests(module_name: str, extra: dict[str, object]) -> None:
    """Run every doctest in ``module_name`` with ``extra`` merged into the namespace."""
    module = importlib.import_module(module_name)
    failed, attempted = doctest.testmod(
        module,
        extraglobs=extra,
        optionflags=OPTIONFLAGS,
        verbose=False,
        report=False,
    )
    assert failed == 0, f"{failed}/{attempted} doctests failed in {module_name}"


@pytest.mark.os_agnostic
@pytest.mark.parametrize("module_name", OFFLINE_MODULES)
def test_offline_doctests(module_name: str) -> None:
    """The pure (no-network) module doctests must pass in the unit suite."""
    _run_doctests(module_name, dict(_DOCTEST_NAMES))


@pytest.mark.integration
@pytest.mark.parametrize("module_name", LIVE_MODULES)
@pytest.mark.usefixtures("docker_container", "dockware_env")
def test_resource_doctests(module_name: str) -> None:
    """The resource doctests run against the dockware container (config via the dockware_env fixture)."""
    _run_doctests(module_name, dict(_DOCTEST_NAMES))
