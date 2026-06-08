# STDLIB
from decimal import Decimal
from functools import cache
from typing import Any

# OWN
from lib_shopware6_api_base import ConfShopware6ApiBase, Shopware6AdminAPIClientBase
from lib_shopware6_api_base import lib_shopware6_api_base_criteria as dal

from ._conf_helper import resolve_config


# Tax{{{
class Tax:
    def __init__(
        self,
        admin_client: Shopware6AdminAPIClientBase | None = None,
        config: ConfShopware6ApiBase | None = None,
        use_docker_test_container: bool = False,
    ) -> None:
        """
        :param admin_client:
        :param config:
        :param use_docker_test_container:

        >>> # Setup
        >>> my_api = Tax()

        """
        # Tax}}}
        if admin_client is None:
            self._admin_client = Shopware6AdminAPIClientBase(config=resolve_config(config, use_docker_test_container))
        else:
            self._admin_client = admin_client

    # cache_clear_tax{{{
    def cache_clear_tax(self) -> None:
        """
        Cache of some functions has to be cleared if tax is inserted or deleted

        >>> # Setup
        >>> my_api = Tax()
        >>> # test
        >>> my_api.cache_clear_tax()

        """
        # cache_clear_tax}}}
        self.get_tax_id_by_name.cache_clear()
        self.get_tax_rate_by_name.cache_clear()

    # get_tax_id_by_name{{{
    @cache
    def get_tax_id_by_name(self, tax_name: str = "Standard rate") -> str:
        """
        :param tax_name: the name of the tax record, like 'Standard rate', 'Reduced rate', 'Reduced Rate2'
        :returns: the id of the tax record

        >>> # Setup
        >>> my_api = Tax()

        >>> # test get 'Standard rate' id
        >>> my_tax_id = my_api.get_tax_id_by_name()
        >>> assert 32 == len(my_tax_id)

        >>> # test not existing (int)
        >>> my_api.get_tax_id_by_name(tax_name='not_existing')
        Traceback (most recent call last):
            ...
        FileNotFoundError: tax record with name "not_existing" not found

        >>> # Test clear Cache -the Cache has to be cleared if tax records are inserted or deleted
        >>> my_api.get_tax_id_by_name.cache_clear()

        """
        # get_tax_id_by_name}}}

        payload = dal.Criteria()
        payload.page = 1
        payload.limit = 1
        payload.filter = [dal.EqualsFilter(field="name", value=tax_name)]
        payload.includes = {"tax": ["id"]}

        dict_response = self._admin_client.request_post(request_url="search/tax", payload=payload)
        try:
            tax_id = str(dict_response.data[0]["id"])
        except IndexError:
            raise FileNotFoundError(f'tax record with name "{tax_name}" not found') from None
        return tax_id

    # get_taxes{{{
    def get_taxes(self, payload: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """
        get all tax records - filters and so on can be set in the payload
        we read paginated (in junks of 100 items) - this is done automatically by function base_client.request_get_paginated()

        :parameters
            payload, to set filters etc.

        :returns
            l_dict_data,


        sample payload :
            page and limit will be overridden by function base_client.request_get_paginated() and will be ignored

        >>> # Setup
        >>> my_api = Tax()
        >>> my_l_dict_data = my_api.get_taxes()
        """
        # get_taxes}}}

        dict_response = self._admin_client.request_get_paginated(request_url="tax", payload=payload)
        l_dict_data = list(dict_response.data)
        return l_dict_data

    # get_tax_rate_by_name{{{
    @cache
    def get_tax_rate_by_name(self, tax_name: str = "Standard rate") -> Decimal:
        """
        :param tax_name: the name of the tax record, like 'Standard rate', 'Reduced rate', 'Reduced Rate2'
        :returns: the percent , like Decimal('19.00')

        >>> # Setup
        >>> my_api = Tax()

        >>> # test get 'Standard rate' percentage
        >>> my_tax_rate = my_api.get_tax_rate_by_name()
        >>> assert Decimal('19.00') == my_tax_rate

        >>> # test not existing (int)
        >>> my_api.get_tax_rate_by_name(tax_name='not_existing')
        Traceback (most recent call last):
            ...
        FileNotFoundError: tax record with name "not_existing" not found

        >>> # Test clear Cache -the Cache has to be cleared if tax records are inserted or deleted
        >>> my_api.get_tax_id_by_name.cache_clear()

        """
        # get_tax_rate_by_name}}}

        payload = dal.Criteria()
        payload.page = 1
        payload.limit = 1
        payload.filter = [dal.EqualsFilter(field="name", value=tax_name)]
        payload.includes = {"tax": ["taxRate"]}

        dict_response = self._admin_client.request_post(request_url="search/tax", payload=payload)
        try:
            tax_rate = str(dict_response.data[0]["taxRate"])
        except IndexError:
            raise FileNotFoundError(f'tax record with name "{tax_name}" not found') from None
        return Decimal(tax_rate)
