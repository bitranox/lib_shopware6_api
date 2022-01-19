# STDLIB
from decimal import Decimal
from functools import lru_cache
import hashlib
import logging
from os import PathLike
import pathlib
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

# OWN
from lib_shopware6_api_base import Shopware6AdminAPIClientBase, ShopwareAPIError, ConfShopware6ApiBase, PayLoad
from lib_shopware6_api_base import lib_shopware6_api_base_criteria as dal


# Currency{{{
class Currency(object):
    def __init__(
        self, admin_client: Optional[Shopware6AdminAPIClientBase] = None, config: Optional[ConfShopware6ApiBase] = None, use_docker_test_container: bool = False
    ) -> None:
        """
        >>> # Setup
        >>> my_api = Currency()
        """
        # Currency}}}
        if admin_client is None:
            self._admin_client = Shopware6AdminAPIClientBase(config=config, use_docker_test_container=use_docker_test_container)
        else:
            self._admin_client = admin_client

    # get_currency_id_by_iso_code{{{
    @lru_cache(maxsize=None)
    def get_currency_id_by_iso_code(self, currency_iso_code: str = "EUR") -> str:
        """
        :param currency_iso_code: the currency iso code, like 'EUR', 'CHF', ...
        :returns: the id of the currency record

        >>> # Setup
        >>> my_api = Currency()

        >>> # test get currency id
        >>> my_currency_id = my_api.get_currency_id_by_iso_code('EUR')
        >>> assert 32 == len(my_currency_id)

        >>> # test not existing (int)
        >>> my_api.get_currency_id_by_iso_code(currency_iso_code='not_existing')
        Traceback (most recent call last):
            ...
        FileNotFoundError: currency record with isoCode "not_existing" not found

        >>> # Test clear Cache - the Cache has to be cleared if currencies are inserted or deleted
        >>> my_api.get_currency_id_by_iso_code.cache_clear()

        """
        # get_currency_id_by_iso_code}}}

        payload = dal.Criteria()
        payload.page = 1
        payload.limit = 1
        payload.filter = [dal.EqualsFilter(field="isoCode", value=currency_iso_code)]
        payload.includes = {"currency": ["id"]}

        dict_response = self._admin_client.request_post(request_url="search/currency", payload=payload)
        try:
            currency_id = str(dict_response["data"][0]["id"])
        except IndexError:
            raise FileNotFoundError(f'currency record with isoCode "{currency_iso_code}" not found')
        return currency_id

    # get_currencies{{{
    def get_currencies(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        get all currency records - filters and so on can be set in the payload
        we read paginated (in junks of 100 items) - this is done automatically by function base_client.request_get_paginated()

        :parameters
            payload, to set filters etc.

        :returns
            l_dict_data,


        sample payload :
            page and limit will be overridden by function base_client.request_get_paginated() and will be ignored

        >>> # Setup
        >>> my_api = Currency()
        >>> my_l_dict_data = my_api.get_currencies()
        """
        # get_currencies}}}

        dict_response = self._admin_client.request_get_paginated(request_url="currency", payload=payload)
        l_dict_data = list(dict_response["data"])
        return l_dict_data
