# STDLIB
import sys

# OWN
from lib_shopware6_api_base import ConfShopware6ApiBase, Shopware6AdminAPIClientBase

# PROJ
from ._conf_helper import resolve_config
from .sub_currency import Currency
from .sub_delivery_time import DeliveryTime
from .sub_media import Media
from .sub_product import Product
from .sub_tax import Tax
from .sub_unit import Unit


# Shopware6API{{{
class Shopware6API:
    def __init__(self, config: ConfShopware6ApiBase | None = None, use_docker_test_container: bool = False) -> None:
        """
        :param config: type ConfShopware6ApiBase (loaded from the environment when omitted)
        :param use_docker_test_container: use a local dockware test container

        >>> my_api = Shopware6API(use_docker_test_container=True)
        >>> my_api_currency = my_api.currency
        >>> my_api_delivery_time = my_api.delivery_time
        >>> my_api_media = my_api.media
        >>> my_api_product = my_api.product
        >>> my_api_tax = my_api.tax
        >>> my_api_unit = my_api.unit

        """
        # Shopware6API}}}
        self._admin_client = Shopware6AdminAPIClientBase(config=resolve_config(config, use_docker_test_container))
        self.currency = Currency(admin_client=self._admin_client)
        self.delivery_time = DeliveryTime(admin_client=self._admin_client)
        self.media = Media(admin_client=self._admin_client)
        self.product = Product(admin_client=self._admin_client)
        self.tax = Tax(admin_client=self._admin_client)
        self.unit = Unit(admin_client=self._admin_client)


if __name__ == "__main__":
    print(b'this is a library only, the executable is named "lib_shopware6_api_cli.py"', file=sys.stderr)  # noqa: T201
