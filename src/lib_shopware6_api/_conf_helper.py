"""Configuration resolution shared by the facade and the resource sub-clients.

Why
    ``lib_shopware6_api_base`` 3.x changed ``Shopware6AdminAPIClientBase`` to take
    a required :class:`ConfShopware6ApiBase` and dropped the old
    ``use_docker_test_container`` constructor flag (dockware setup now lives in the
    base lib's test harness). This project keeps ``use_docker_test_container`` as a
    convenience in its own public API and resolves it to a concrete config here, so
    callers and doctests keep working against a local dockware container.
"""

from __future__ import annotations

from lib_shopware6_api_base import ConfShopware6ApiBase, GrantType, load_config_from_env

__all__ = ["get_docker_test_config", "resolve_config"]


def get_docker_test_config() -> ConfShopware6ApiBase:
    """Return a config pointed at a local dockware container (admin API, plain HTTP).

    The admin-API helpers in this package use the User-Credentials grant, so the
    default dockware admin user (``admin`` / ``shopware``) is sufficient; no
    integration keys or storefront access key are required.
    """
    return ConfShopware6ApiBase(
        shopware_admin_api_url="http://localhost/api",
        shopware_storefront_api_url="http://localhost/store-api",
        username="admin",
        password="shopware",  # noqa: S106  # nosec B106 - public dockware default credential
        grant_type=GrantType.USER_CREDENTIALS,
    )


def resolve_config(config: ConfShopware6ApiBase | None, use_docker_test_container: bool) -> ConfShopware6ApiBase:  # noqa: FBT001
    """Resolve the effective config for a resource client.

    Precedence: an explicit ``config`` wins; otherwise a dockware config when
    ``use_docker_test_container`` is set; otherwise the config discovered from the
    environment / ``.env`` via ``lib_shopware6_api_base.load_config_from_env``.
    """
    if config is not None:
        return config
    if use_docker_test_container:
        return get_docker_test_config()
    return load_config_from_env()
