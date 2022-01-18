# STDLIB
import sys
from typing import Optional

# OWN
from lib_shopware6_api_base import Shopware6AdminAPIClientBase, ShopwareAPIError, ConfShopware6ApiBase, PayLoad
from lib_shopware6_api_base import lib_shopware6_api_base_criteria as dal

# PROJ
try:
    from sub_currency import Currency
    from sub_delivery_time import DeliveryTime
    from sub_tax import Tax
    from sub_media import Media
    from sub_product import Product
except ImportError:  # pragma: no cover
    from .sub_currency import Currency  # type: ignore # pragma: no cover
    from .sub_delivery_time import DeliveryTime  # type: ignore # pragma: no cover
    from .sub_tax import Tax  # type: ignore # pragma: no cover
    from .sub_media import Media  # type: ignore # pragma: no cover
    from .sub_product import Product  # type: ignore # pragma: no cover


# Shopware6API{{{
class Shopware6API(object):
    def __init__(self, config: Optional[ConfShopware6ApiBase] = None, use_docker_test_container: bool = False) -> None:
        """
        :param config, type ConfShopware6ApiBase
        :param use_docker_test_container: if to use the docker test container

        >>> my_api=Shopware6API()
        >>> my_api_currency=my_api.currency
        >>> my_api_delivery_time=my_api.delivery_time
        >>> my_api_media=my_api.media
        >>> my_api_product=my_api.product
        >>> my_api_tax=my_api.tax

        """
        # Shopware6API}}}
        self._admin_client = Shopware6AdminAPIClientBase(config=config, use_docker_test_container=use_docker_test_container)
        self.currency = Currency(admin_client=self._admin_client)
        self.delivery_time = DeliveryTime(admin_client=self._admin_client)
        self.tax = Tax(admin_client=self._admin_client)
        self.media = Media(admin_client=self._admin_client)
        self.product = Product(admin_client=self._admin_client)


if __name__ == "__main__":
    print(b'this is a library only, the executable is named "lib_shopware6_api_cli.py"', file=sys.stderr)
