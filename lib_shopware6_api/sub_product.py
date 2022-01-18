# STDLIB
from decimal import Decimal
from functools import lru_cache
import hashlib
from typing import Any, Dict, List, Optional, Tuple, Union

# EXT
import attrs

# OWN
from lib_shopware6_api_base import Shopware6AdminAPIClientBase, ShopwareAPIError, ConfShopware6ApiBase, PayLoad
from lib_shopware6_api_base import lib_shopware6_api_base_criteria as dal

# PROJ
try:
    from sub_currency import Currency
    from sub_tax import Tax
    from sub_media import Media
except ImportError:  # pragma: no cover
    from .sub_currency import Currency  # type: ignore # pragma: no cover
    from .sub_tax import Tax  # type: ignore # pragma: no cover
    from .sub_media import Media  # type: ignore # pragma: no cover


# ProductPicture{{{
@attrs.define
class ProductPicture:
    """
    dataclass to upsert a picture
    """

    # ProductPicture}}}
    position: int = 0  # the position in the shop
    url: str = ""  # the url to upload from
    media_alt: Optional[str] = None  # optional picture alt
    media_title: Optional[str] = None  # optional picture title
    upload_media: bool = True  # if to upload the media (default= True)


# Product{{{
class Product(object):
    def __init__(
        self, admin_client: Optional[Shopware6AdminAPIClientBase] = None, config: Optional[ConfShopware6ApiBase] = None, use_docker_test_container: bool = False
    ) -> None:
        """
        :param admin_client:
        :param config:
        :param use_docker_test_container:

        >>> # Setup
        >>> my_api = Product()

        """
        # Product}}}
        if admin_client is None:
            self._admin_client = Shopware6AdminAPIClientBase(config=config, use_docker_test_container=use_docker_test_container)
        else:
            self._admin_client = admin_client

        self.currency = Currency(admin_client=self._admin_client)
        self.tax = Tax(admin_client=self._admin_client)
        self.media = Media(admin_client=self._admin_client)

    # calc_new_product_id{{{
    @staticmethod
    def calc_new_product_id(product_number: Union[int, str]) -> str:
        """
        :param product_number:
        :return: the new id

        >>> # Setup
        >>> my_api = Product()
        >>> # Test
        >>> my_new_product_id = my_api.calc_new_product_id(product_number='123')
        >>> my_new_product_id2 = my_api.calc_new_product_id(product_number='1234')
        >>> assert 32 == len(my_new_product_id)
        >>> assert my_new_product_id != my_new_product_id2

        """
        # calc_new_product_id}}}
        media_id = hashlib.md5(str(product_number).encode("utf-8")).hexdigest()
        return media_id

    # calc_new_product_media_id{{{
    @staticmethod
    def calc_new_product_media_id(product_id: str, position: int) -> str:
        """
        the new product_media_id is calculated from product_id and position

        :param product_id:
        :param position:
        :return:

        >>> # Setup
        >>> my_api = Product()
        >>> # Test
        >>> my_new_product_media_id = my_api.calc_new_product_media_id(product_id='123', position=0)
        >>> my_new_product_media_id2 = my_api.calc_new_product_media_id(product_id='123', position=1)
        >>> assert 32 == len(my_new_product_media_id)
        >>> assert my_new_product_media_id != my_new_product_media_id2

        """
        # calc_new_product_media_id}}}
        hash_string = f"{product_id}{position}"
        media_id = hashlib.md5(hash_string.encode("utf-8")).hexdigest()
        return media_id

    # cache_clear_product{{{
    def cache_clear_product(self) -> None:
        """
        Cache of some functions has to be cleared if articles are inserted or deleted

        >>> # Setup
        >>> my_api = Product()
        >>> # Test
        >>> my_api.cache_clear_product()

        """
        # cache_clear_product}}}
        self.get_product_id_by_product_number.cache_clear()

    # delete_product_by_id{{{
    def delete_product_by_id(self, product_id: str) -> None:
        """
        :param product_id:
        :return:


        >>> # Setup
        >>> my_api = Product()
        >>> my_article_id = my_api.insert_product(name='rn-doctest-article', product_number='test_delete_article_by_id_001', price_brutto=Decimal(0), stock=0)

        >>> # delete_article
        >>> my_api.delete_product_by_id(product_id=my_article_id)

        """
        # delete_product_by_id}}}
        self._admin_client.request_delete(f"product/{product_id}")
        self.cache_clear_product()

    # get_product_id_by_product_number{{{
    @lru_cache(maxsize=None)
    def get_product_id_by_product_number(self, product_number: Union[int, str]) -> str:
        """
        :param product_number:
        :return:

        >>> # Setup
        >>> my_api = Product()
        >>> my_payload = dal.Criteria(limit=1, page=1)
        >>> first_article = my_api._admin_client.request_get(request_url="product", payload=my_payload)["data"][0]
        >>> my_article_id = first_article['id']
        >>> my_article_product_number = first_article['productNumber']

        >>> # Test get article_id
        >>> assert my_article_id == my_api.get_product_id_by_product_number(product_number=my_article_product_number)

        >>> # test not existing (int)
        >>> my_api.get_product_id_by_product_number(product_number='get_article_id_by_product_number9999_not_existing')
        Traceback (most recent call last):
            ...
        FileNotFoundError: article with productNumber(mysql_artikelnummer) "..." not found

        >>> # test not existing (str)
        >>> my_api.get_product_id_by_product_number(product_number='not_existing')
        Traceback (most recent call last):
            ...
        FileNotFoundError: article with productNumber(mysql_artikelnummer) "not_existing" not found

        >>> # Test clear Cache - the Cache has to be cleared if products are inserted or deleted
        >>> my_api.get_product_id_by_product_number.cache_clear()

        """
        # get_product_id_by_product_number}}}

        payload = dal.Criteria()
        payload.page = 1
        payload.limit = 1
        payload.filter = [dal.EqualsFilter(field="productNumber", value=product_number)]
        payload.includes = {"product": ["id"]}

        dict_response = self._admin_client.request_post(request_url="search/product", payload=payload)
        try:
            article_id = str(dict_response["data"][0]["id"])
            self.get_product_id_by_product_number.cache_clear()
        except IndexError:
            raise FileNotFoundError(f'article with productNumber(mysql_artikelnummer) "{product_number}" not found')
        return article_id

    # delete_product_media_relation_by_id{{{
    def delete_product_media_relation_by_id(self, product_media_id: str) -> None:
        """
        delete product-media relation - but not the media itself.

        :param product_media_id:
        :return:

        >>> # Setup
        >>> my_api = Product()
        >>> my_api.media.conf_path_media_folder_root = '/Product Media/api_test_delete_product_media_by_id'
        >>> product_number = 'test_delete_product_media_by_id'
        >>> my_url='https://pics.rotek.at/test/test001/bilder/test001_01_1280.jpg'
        >>> my_position = 10

        >>> my_product_id = my_api.insert_product(name='rn-doctest-article', product_number=product_number, price_brutto=Decimal(0), stock=0)
        >>> my_media_id = my_api.media.upsert_media(product_number=product_number, position=my_position, url=my_url)
        >>> my_product_media_id = my_api.insert_product_media_relation(product_id=my_product_id, media_id=my_media_id, position=my_position)

        >>> # Test
        >>> assert True == my_api.is_media_used_in_product_media(media_id=my_media_id)
        >>> my_api.delete_product_media_relation_by_id(product_media_id=my_product_media_id)
        >>> assert False == my_api.is_media_used_in_product_media(media_id=my_media_id)

        >>> # Teardown
        >>> my_api.delete_product_by_id(product_id=my_product_id)
        >>> my_api.media.delete_media_folder_by_path(my_api.media.conf_path_media_folder_root, force=True)

        """
        # delete_product_media_relation_by_id}}}
        self._admin_client.request_delete(f"product-media/{product_media_id}")

    # delete_product_media_relations_by_product_number{{{
    def delete_product_media_relations_by_product_number(self, product_number: Union[int, str]) -> None:
        """
        Delete all product_media relations of a product , but not the media itself,
        because there will be a reorg which deletes unused pictures.
        it does not change the cover picture

        It is neccessary to delete the product_media_relations before updating them, because otherwise
        deletion of pictures on the source database would not be propagated.

        If someone need to update the product pictures very frequently on a huge amount of products,
        there might be more efficient (but much more complicated) methods.

        >>> # Setup
        >>> my_api = Product()
        >>> my_api.media.conf_path_media_folder_root = '/Product Media/api_test_delete_product_picture_relations'
        >>> my_product_number = 'api_test_delete_product_picture_relations'
        >>> my_url='https://pics.rotek.at/test/test001/bilder/test001_01_1280.jpg'


        >>> my_product_id = my_api.insert_product(name='rn-doctest-article', product_number=my_product_number, price_brutto=Decimal(0), stock=0)

        >>> my_position = 10
        >>> my_media_id_10 = my_api.media.upsert_media(product_number=my_product_number, position=my_position, url=my_url)
        >>> my_product_media_id_10 = my_api.insert_product_media_relation(product_id=my_product_id, media_id=my_media_id_10, position=my_position)

        >>> my_position = 20
        >>> my_media_id_20 = my_api.media.upsert_media(product_number=my_product_number, position=my_position, url=my_url)
        >>> my_product_media_id_20 = my_api.insert_product_media_relation(product_id=my_product_id, media_id=my_media_id_20, position=my_position)

        >>> # Test
        >>> assert True == my_api.is_media_used_in_product_media(media_id=my_media_id_10)
        >>> assert True == my_api.is_media_used_in_product_media(media_id=my_media_id_20)
        >>> my_api.delete_product_media_relations_by_product_number(product_number=my_product_number)
        >>> assert False == my_api.is_media_used_in_product_media(media_id=my_media_id_10)
        >>> assert False == my_api.is_media_used_in_product_media(media_id=my_media_id_20)

        >>> # Teardown
        >>> my_api.delete_product_by_id(product_id=my_product_id)
        >>> my_api.media.delete_media_folder_by_path(my_api.media.conf_path_media_folder_root, force=True)

        """
        # delete_product_media_relations_by_product_number}}}
        try:
            product_id = self.get_product_id_by_product_number(product_number)
        except FileNotFoundError:
            return

        payload = dal.Criteria()
        payload.filter = [dal.EqualsFilter(field="productId", value=product_id)]
        payload.includes = {"product-media": ["id"]}
        l_dict_product_media = self.search_product_media_l_dict(payload=payload)
        for dict_product_media in l_dict_product_media:
            self.delete_product_media_relation_by_id(product_media_id=dict_product_media["id"])

    # get_product_l_dict_all{{{
    def get_product_l_dict_all(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        get all articles back - filters and so on can be set in the payload
        we read paginated (in junks of 100 items) - this is done automatically by function base_client.request_get_paginated()

        :parameters
            payload, to set filters etc.

        :returns
            l_dict_data,


        sample payload :
            page and limit will be overridden by function base_client.request_get_paginated() and will be ignored

        >>> # Setup
        >>> my_api = Product()
        >>> dict_data = my_api.get_product_l_dict_all()
        >>> assert len(dict_data) > 5

        """
        # get_product_l_dict_all}}}

        dict_response = self._admin_client.request_get_paginated(request_url="product", payload=payload)
        l_dict_data = list(dict_response["data"])
        return l_dict_data

    # get_product_media_l_dict_all{{{
    def get_product_media_l_dict_all(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        get all product_media - filters and so on can be set in the payload
        we read paginated (in junks of 100 items) - this is done automatically by function base_client.request_get_paginated()

        :parameters
            payload, to set filters etc.

        :returns
            l_dict_data,

        sample payload :
            page and limit will be overridden by function base_client.request_get_paginated() and will be ignored

        >>> # Setup
        >>> my_api = Product()
        >>> my_l_dict_data = my_api.get_product_media_l_dict_all()
        """
        # get_product_media_l_dict_all}}}

        dict_response = self._admin_client.request_get_paginated(request_url="product-media", payload=payload)
        l_dict_data = list(dict_response["data"])
        return l_dict_data

    # insert_product{{{
    def insert_product(
        self,
        name: str,
        product_number: Union[int, str],
        stock: int = 0,
        price_brutto: Decimal = Decimal("0.00"),
        price_netto: Decimal = Decimal("0.00"),
        tax_name: str = "Standard rate",
        currency_iso_code: str = "EUR",
        linked: bool = True,
    ) -> str:
        """
        see : https://shopware.stoplight.io/docs/admin-api/ZG9jOjEyMzA4NTUy-product-data#simple-payload

        :param name:                        'Stromerzeuger GD4-1A-6000-5EBZ'
        :param product_number:              productNumber, mysql_artikelnummer
        :param stock:                       Anzahl auf Lager (?)
        :param tax_name:                    default tax record ('Standard rate')
        :param price_brutto:                this price is displayed to customers who see gross prices in the shop
        :param price_netto:                 this price is shown to customers who see net prices in the shop
                                            if the price_netto is 0.00 it will be calculated from brutto price with the
                                            tax rate of the 'tax_name' stated
        :param currency_iso_code:           the currency isoCode like 'EUR', 'CHF', ...
        :param linked:                      this is a flag for the administration. If it is set to true,
                                            the gross or net counterpart is calculated when a price is entered in the administration.

        :return: the new product id

        >>> # Setup
        >>> my_api = Product()

        >>> # insert article
        >>> my_new_product_id = my_api.insert_product(name='rn-doctest-article', product_number='test_insert_article_by_product_number_999',
        ...                                           price_brutto=Decimal(0), stock=0)
        >>> assert 32 == len(my_new_product_id)

        >>> # Teardown
        >>> my_api.delete_product_by_id(product_id=my_new_product_id)

        """
        # insert_product}}}

        tax_id = self.tax.get_tax_id_by_name(tax_name=tax_name)

        if not price_netto:
            tax_rate = self.tax.get_tax_rate_by_name(tax_name=tax_name)
            price_netto = price_brutto / (1 + tax_rate / 100)
        currency_id = self.currency.get_currency_id_by_iso_code(currency_iso_code=currency_iso_code)
        new_product_id = self.calc_new_product_id(product_number=product_number)
        payload = {
            "id": new_product_id,
            "name": name,
            "productNumber": str(product_number),
            "stock": stock,
            "taxId": tax_id,
            "price": [{"currencyId": currency_id, "gross": str(price_brutto), "net": str(price_netto), "linked": linked}],
        }
        self._admin_client.request_post("product", payload)
        self.cache_clear_product()
        return new_product_id

    # upsert_product_payload{{{
    def upsert_product_payload(self, product_number: Union[int, str], payload: Dict[str, Any]) -> str:
        # upsert_product_payload}}}
        try:
            product_id = self.get_product_id_by_product_number(product_number=product_number)
            self._update_product_payload(product_id=product_id, payload=payload)
        except FileNotFoundError:
            product_id = self.calc_new_product_id(product_number=product_number)
            payload["productNumber"] = product_number
            self._insert_product_payload(product_id=product_id, payload=payload)
        return product_id

    def _update_product_payload(self, product_id: str, payload: Dict[str, Any]) -> None:
        self._admin_client.request_patch(f"product/{product_id}", payload)

    def _insert_product_payload(self, product_id: str, payload: Dict[str, Any]) -> None:
        payload["id"] = product_id
        self._admin_client.request_post("product", payload)
        self.cache_clear_product()

    # insert_product_media_relation{{{
    def insert_product_media_relation(self, product_id: str, media_id: str, position: int) -> str:
        """
        inserts a single product_media Relation.
        the new product_media_relation_id is calculated from product_id and position
        this should only be used if You uploaded the media indipendently from products -
        otherwise You should use associations to update the product with one request - see :
        https://shopware.stoplight.io/docs/admin-api/ZG9jOjEyNjI1Mzkw-media-handling
        https://shopware.stoplight.io/docs/admin-api/ZG9jOjEyMzA4NTUw-associationsundefined

        :param product_id:
        :param media_id:
        :param position: 0-based
        :return: the new product_media_relation_id

        >>> # Setup
        >>> my_api = Product()
        >>> my_new_product_id = my_api.insert_product(name='rn-doctest-article', product_number='test_insert_product_media_999')
        >>> my_new_media_id = my_api.media.insert_media_by_path( \
                path_media='/Product Media/test_insert_product_media_999/test_insert_product_media_999_01_1280.jpg', \
                url='https://pics.rotek.at/test/test001/bilder/test001_07_1280.jpg')

        >>> # Test
        >>> my_new_product_media_id = my_api.insert_product_media_relation(product_id=my_new_product_id, media_id=my_new_media_id, position=0)
        >>> # Assert Media is used in product_media
        >>> assert True == my_api.is_media_used_in_product_media(media_id=my_new_media_id)

        >>> # Test delete Product, cascading delete to product_media
        >>> my_api.delete_product_by_id(product_id=my_new_product_id)
        >>> assert False == my_api.is_media_used_in_product_media(media_id=my_new_media_id)

        >>> # Teardown
        >>> my_api.media.delete_media_folder_by_path(path_media_folder = '/Product Media/test_insert_product_media_999/', force=True)

        """
        # insert_product_media_relation}}}
        product_media_id = self.calc_new_product_media_id(product_id=product_id, position=position)
        payload = {"id": product_media_id, "productId": product_id, "mediaId": media_id, "position": position}

        # insert the record
        self._admin_client.request_post("product-media", payload)
        return product_media_id

    # is_media_used_in_product_media{{{
    def is_media_used_in_product_media(self, media_id: str) -> bool:
        """
        :returns True if the media is used in a product
        :param media_id:

        >>> # Setup
        >>> my_api = Product()
        >>> my_new_product_id = my_api.insert_product(name='rn-doctest-article', product_number='test_is_media_used_in_product_media_999')
        >>> my_new_media_id = my_api.media.insert_media_by_path(
        ...     path_media='/Product Media/test_is_media_used_in_product_media_999/test_is_media_used_in_product_media_999_01_1280.jpg',
        ...     url='https://pics.rotek.at/test/test001/bilder/test001_07_1280.jpg')

        >>> # Test
        >>> my_new_product_media_id = my_api.insert_product_media_relation(product_id=my_new_product_id, media_id=my_new_media_id, position=0)
        >>> # Assert Media is used in product_media
        >>> assert True == my_api.is_media_used_in_product_media(media_id=my_new_media_id)

        >>> # Test delete Product, cascading delete to product_media
        >>> my_api.delete_product_by_id(product_id=my_new_product_id)
        >>> assert False == my_api.is_media_used_in_product_media(media_id=my_new_media_id)

        >>> # Teardown
        >>> my_api.media.delete_media_folder_by_path(path_media_folder = '/Product Media/test_is_media_used_in_product_media_999', force=True)

        """
        # is_media_used_in_product_media}}}
        payload = dal.Criteria()
        payload.page = 1
        payload.limit = 1
        payload.filter = [dal.EqualsFilter(field="mediaId", value=media_id)]
        payload.includes = {"product_media": ["id"]}

        l_product_media = self.search_product_media_l_dict(payload=payload)
        return bool(l_product_media)

    # search_product_media_l_dict{{{
    def search_product_media_l_dict(self, payload: PayLoad = None) -> List[Dict[str, Any]]:
        """
        search product_media

        >>> # Setup
        >>> my_api = Product()

        >>> # insert article
        >>> ignore = my_api.search_product_media_l_dict()

        """
        # search_product_media_l_dict}}}
        response_dict = self._admin_client.request_post_paginated("search/product-media", payload)
        l_data_dict = list(response_dict["data"])
        return l_data_dict

    # upsert_product_pictures{{{
    def upsert_product_pictures(self, product_number: Union[int, str], l_product_pictures: List[ProductPicture]) -> None:
        """
        upsert product pictures and cover picture. The first picture (by Position Number) is automatically the cover picture

        :parameter product_number
        :parameter l_product_pictures  list of Pictures

        >>> # Setup
        >>> my_api = Product()
        >>> my_api.media.conf_path_media_folder_root = '/Product Media/api_test_upsert_product_pictures'
        >>> my_product_number = 'test_upsert_product_pictures'

        >>> my_product_id = my_api.insert_product(name='test_upsert_product_pictures', product_number=my_product_number, price_brutto=Decimal(0), stock=0)

        >>> my_pictures=list()
        >>> my_pictures.append(ProductPicture(position=20, url='https://pics.rotek.at/test/test001/bilder/test001_02_1280.jpg', media_alt='', media_title=''))
        >>> my_pictures.append(ProductPicture(position=30, url='https://pics.rotek.at/test/test001/bilder/test001_03_1280.jpg', media_alt='', media_title=''))
        >>> my_pictures.append(ProductPicture(position=40, url='https://pics.rotek.at/test/test001/bilder/test001_04_1280.jpg', media_alt='', media_title=''))
        >>> my_pictures.append(ProductPicture(position=50, url='https://pics.rotek.at/test/test001/bilder/test001_05_1280.jpg', media_alt='', media_title=''))
        >>> my_pictures.append(ProductPicture(position=10, url='https://pics.rotek.at/test/test001/bilder/test001_01_1280.jpg', media_alt='', media_title=''))

        >>> # Test
        >>> my_api.upsert_product_pictures(product_number=my_product_number, l_product_pictures=my_pictures)

        >>> # Teardown
        >>> my_api.delete_product_media_relations_by_product_number(product_number=my_product_number)
        >>> my_api.delete_product_by_id(product_id=my_product_id)
        >>> my_api.media.delete_media_folder_by_path(my_api.media.conf_path_media_folder_root, force=True)

        """
        # upsert_product_pictures}}}
        product_id = self.get_product_id_by_product_number(product_number=product_number)
        self.delete_product_media_relations_by_product_number(product_number=product_number)

        l_product_pictures = sorted(l_product_pictures, key=lambda picture: picture.position)

        is_cover_picture = True
        for product_picture in l_product_pictures:
            media_id = self.media.upsert_media(
                product_number=product_number,
                position=product_picture.position,
                url=product_picture.url,
                media_alt=product_picture.media_alt,
                media_title=product_picture.media_title,
                upload_media=True,
            )
            media_relation_id = self.insert_product_media_relation(product_id=product_id, media_id=media_id, position=product_picture.position)

            if is_cover_picture:
                self._update_product_payload(product_id=product_id, payload={"coverId": media_relation_id})
                is_cover_picture = False
