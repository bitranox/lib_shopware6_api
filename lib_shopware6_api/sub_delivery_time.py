# STDLIB
from functools import lru_cache
from typing import Any, Dict, List, Optional

# OWN
from lib_shopware6_api_base import Shopware6AdminAPIClientBase, ConfShopware6ApiBase, PayLoad
from lib_shopware6_api_base import lib_shopware6_api_base_criteria as dal


# DeliveryTime{{{
class DeliveryTime(object):
    def __init__(
        self, admin_client: Optional[Shopware6AdminAPIClientBase] = None, config: Optional[ConfShopware6ApiBase] = None, use_docker_test_container: bool = False
    ) -> None:
        """
        :param admin_client:
        :param config:
        :param use_docker_test_container:

        >>> # Setup
        >>> my_api = DeliveryTime()

        """
        # DeliveryTime}}}
        if admin_client is None:
            self._admin_client = Shopware6AdminAPIClientBase(config=config, use_docker_test_container=use_docker_test_container)
        else:
            self._admin_client = admin_client

    # cache_clear_delivery_time{{{
    def cache_clear_delivery_time(self) -> None:
        """
        Cache of some functions has to be cleared if delivery_time records are inserted or deleted

        >>> # Setup
        >>> my_api = DeliveryTime()
        >>> # Test
        >>> my_api.cache_clear_delivery_time()

        """
        # cache_clear_delivery_time}}}
        self.get_delivery_times.cache_clear()
        self.get_delivery_times_sorted_by_min_days.cache_clear()

    # get_delivery_times{{{
    @lru_cache(maxsize=None)
    def get_delivery_times(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
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
        >>> my_api = DeliveryTime()
        >>> my_l_dict_data = my_api.get_delivery_times()
        """
        # get_delivery_times}}}
        dict_response = self._admin_client.request_get_paginated(request_url="delivery-time", payload=payload)
        l_dict_data = list(dict_response["data"])
        return l_dict_data

    # search_delivery_times{{{
    def search_delivery_times(self, payload: PayLoad = None) -> List[Dict[str, Any]]:
        """
        search delivery-time records

        >>> # Setup
        >>> my_api = DeliveryTime()

        >>> # insert article
        >>> ignore = my_api.search_delivery_times()

        """
        # search_delivery_times}}}
        response_dict = self._admin_client.request_post_paginated("search/delivery-time", payload)
        l_data_dict = list(response_dict["data"])
        return l_data_dict

    # get_delivery_times_sorted_by_min_days{{{
    @lru_cache(maxsize=None)
    def get_delivery_times_sorted_by_min_days(self) -> List[Dict[str, Any]]:
        """
        returns a list of 'id' and 'name' of delivery_times, sorted by minimal time
        the key 'position' starts with 10, 20 ....
        :returns : [{'name': '...', 'id': '...', 'position': 10}, ...]

        >>> # Setup
        >>> my_api = DeliveryTime()

        >>> # Test
        >>> my_api.get_delivery_times_sorted_by_min_days()
        [{'name': '...', 'id': '...', 'position': 10}, ...]

        """
        # get_delivery_times_sorted_by_min_days}}}
        days = {"hour": 0.0416667, "day": 1, "week": 7, "month": 31, "year": 365}
        payload = dal.Criteria()
        payload.includes["delivery_time"] = ["id", "name", "min", "unit"]
        l_dict_delivery_times = self.search_delivery_times(payload=payload)
        l_dict_delivery_times = sorted(l_dict_delivery_times, key=lambda dt: dt["min"] * days[dt["unit"]])  # type: ignore
        position = 10
        for delivery_time in l_dict_delivery_times:
            delivery_time["position"] = position
            del delivery_time["apiAlias"]
            del delivery_time["min"]
            del delivery_time["unit"]
            position = position + 10
        return l_dict_delivery_times
