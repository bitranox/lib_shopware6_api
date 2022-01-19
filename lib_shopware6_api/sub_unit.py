# STDLIB
from functools import lru_cache
from typing import Any, Dict, List, Optional

# OWN
from lib_shopware6_api_base import Shopware6AdminAPIClientBase, ConfShopware6ApiBase, PayLoad


# Unit{{{
class Unit(object):
    def __init__(
        self, admin_client: Optional[Shopware6AdminAPIClientBase] = None, config: Optional[ConfShopware6ApiBase] = None, use_docker_test_container: bool = False
    ) -> None:
        """
        :param admin_client:
        :param config:
        :param use_docker_test_container:

        >>> # Setup
        >>> my_api = Unit()

        """
        # Unit}}}
        if admin_client is None:
            self._admin_client = Shopware6AdminAPIClientBase(config=config, use_docker_test_container=use_docker_test_container)
        else:
            self._admin_client = admin_client

    # cache_clear_unit{{{
    def cache_clear_unit(self) -> None:
        """
        Cache of some functions has to be cleared if unit records are inserted or deleted

        >>> # Setup
        >>> my_api = Unit()
        >>> # Test
        >>> my_api.cache_clear_unit()

        """
        # cache_clear_unit}}}
        self.get_units.cache_clear()

    # get_units{{{
    @lru_cache(maxsize=None)
    def get_units(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        get all delivery-time records - filters and so on can be set in the payload
        we read paginated (in junks of 100 items) - this is done automatically by function base_client.request_get_paginated()

        :parameters
            payload, to set filters etc.

        :returns
            l_dict_data,


        sample payload :
            page and limit will be overridden by function base_client.request_get_paginated() and will be ignored

        >>> # Setup
        >>> my_api = Unit()

        >>> # Test
        >>> my_l_dict_data = my_api.get_units()
        """
        # get_units}}}
        dict_response = self._admin_client.request_get_paginated(request_url="unit", payload=payload)
        l_dict_data = list(dict_response["data"])
        return l_dict_data

    # search_units{{{
    def search_units(self, payload: PayLoad = None) -> List[Dict[str, Any]]:
        """
        search delivery-time records

        >>> # Setup
        >>> my_api = Unit()

        >>> # Test
        >>> ignore = my_api.search_units()

        """
        # search_units}}}
        response_dict = self._admin_client.request_post_paginated("search/unit", payload)
        l_data_dict = list(response_dict["data"])
        return l_data_dict
