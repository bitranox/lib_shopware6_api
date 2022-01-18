lib_shopware6_api
=================


Version v1.0.2 as of 2022-01-18 see `Changelog`_

|build_badge| |license| |jupyter| |pypi| |pypi-downloads| |black|

|codecov| |better_code| |cc_maintain| |cc_issues| |cc_coverage| |snyk|



.. |build_badge| image:: https://github.com/bitranox/lib_shopware6_api/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/bitranox/lib_shopware6_api/actions/workflows/python-package.yml


.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License

.. |jupyter| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/bitranox/lib_shopware6_api/master?filepath=lib_shopware6_api.ipynb

.. for the pypi status link note the dashes, not the underscore !
.. |pypi| image:: https://img.shields.io/pypi/status/lib-shopware6-api?label=PyPI%20Package
   :target: https://badge.fury.io/py/lib_shopware6_api

.. |codecov| image:: https://img.shields.io/codecov/c/github/bitranox/lib_shopware6_api
   :target: https://codecov.io/gh/bitranox/lib_shopware6_api

.. |better_code| image:: https://bettercodehub.com/edge/badge/bitranox/lib_shopware6_api?branch=master
   :target: https://bettercodehub.com/results/bitranox/lib_shopware6_api

.. |cc_maintain| image:: https://img.shields.io/codeclimate/maintainability-percentage/bitranox/lib_shopware6_api?label=CC%20maintainability
   :target: https://codeclimate.com/github/bitranox/lib_shopware6_api/maintainability
   :alt: Maintainability

.. |cc_issues| image:: https://img.shields.io/codeclimate/issues/bitranox/lib_shopware6_api?label=CC%20issues
   :target: https://codeclimate.com/github/bitranox/lib_shopware6_api/maintainability
   :alt: Maintainability

.. |cc_coverage| image:: https://img.shields.io/codeclimate/coverage/bitranox/lib_shopware6_api?label=CC%20coverage
   :target: https://codeclimate.com/github/bitranox/lib_shopware6_api/test_coverage
   :alt: Code Coverage

.. |snyk| image:: https://img.shields.io/snyk/vulnerabilities/github/bitranox/lib_shopware6_api
   :target: https://snyk.io/test/github/bitranox/lib_shopware6_api

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/lib-shopware6-api
   :target: https://pypi.org/project/lib-shopware6-api/
   :alt: PyPI - Downloads

shopware6 higher level API client, based on `lib_shopware_api_base <https://github.com/bitranox/lib_shopware6_api_base>`_

this might be a good example for Your own API Client Functions - to be further extended

----

automated tests, Travis Matrix, Documentation, Badges, etc. are managed with `PizzaCutter <https://github
.com/bitranox/PizzaCutter>`_ (cookiecutter on steroids)

Python version required: 3.6.0 or newer

tested on recent linux with python 3.6, 3.7, 3.8, 3.9, 3.10.0, pypy-3.8 - architectures: amd64

`100% code coverage <https://codecov.io/gh/bitranox/lib_shopware6_api>`_, flake8 style checking ,mypy static type checking ,

----

- `Try it Online`_
- `Usage`_
- `Usage from Commandline`_
- `Installation and Upgrade`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/lib_shopware6_api/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/lib_shopware6_api/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/lib_shopware6_api/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----

Try it Online
-------------

You might try it right away in Jupyter Notebook by using the "launch binder" badge, or click `here <https://mybinder.org/v2/gh/{{rst_include.
repository_slug}}/master?filepath=lib_shopware6_api.ipynb>`_

Usage
-----------

Overview
========

- `API`_
- `Currency`_
- `DeliveryTime`_
- `Media`_
- `Product`_
- `Tax`_

-------------------

API
===
back to `Overview`_

.. code-block:: python

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

Currency
========
back to `Overview`_

.. code-block:: python

    class Currency(object):
        def __init__(
            self, admin_client: Optional[Shopware6AdminAPIClientBase] = None, config: Optional[ConfShopware6ApiBase] = None, use_docker_test_container: bool = False
        ) -> None:
            """
            >>> # Setup
            >>> my_api = Currency()
            """

.. code-block:: python

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

.. code-block:: python

        def get_currency_l_dict_all(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
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
            >>> my_l_dict_data = my_api.get_currency_l_dict_all()
            """

DeliveryTime
============
back to `Overview`_

.. code-block:: python

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

.. code-block:: python

        def cache_clear_delivery_time(self) -> None:
            """
            Cache of some functions has to be cleared if delivery_time records are inserted or deleted

            >>> # Setup
            >>> my_api = DeliveryTime()
            >>> # Test
            >>> my_api.cache_clear_delivery_time()

            """

.. code-block:: python

        @lru_cache(maxsize=None)
        def get_delivery_time_l_dict_all(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
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
            >>> my_l_dict_data = my_api.get_delivery_time_l_dict_all()
            """

.. code-block:: python

        def search_delivery_time_l_dict(self, payload: PayLoad = None) -> List[Dict[str, Any]]:
            """
            search delivery-time records

            >>> # Setup
            >>> my_api = DeliveryTime()

            >>> # insert article
            >>> ignore = my_api.search_delivery_time_l_dict()

            """

.. code-block:: python

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

Media
=====
back to `Overview`_

.. code-block:: python

    class Media(object):
        def __init__(
            self, admin_client: Optional[Shopware6AdminAPIClientBase] = None, config: Optional[ConfShopware6ApiBase] = None, use_docker_test_container: bool = False
        ) -> None:
            """
            >>> # Setup
            >>> my_api = Media()

            """

.. code-block:: python

        def cache_clear_media(self) -> None:
            """
            Cache of some functions has to be cleared if media is inserted or deleted

            >>> # Setup
            >>> my_api = Media()
            >>> # test
            >>> my_api.cache_clear_media()

            """

.. code-block:: python

        def cache_clear_media_folder(self) -> None:
            """
            Cache of some functions has to be cleared if media_folders are inserted or deleted

            >>> # Setup
            >>> my_api = Media()
            >>> # test
            >>> my_api.cache_clear_media_folder()

            """

.. code-block:: python

        @staticmethod
        def calc_media_filename_from_product_number(
            product_number: Union[int, str],
            position: int,
            url: str,
        ) -> str:
            """
            media_filenamescan only exist once - so we build the filename from product_number, position, and extension of the url

            :param product_number:
            :param position:
            :param url:             we take the extension from here
            :return:

            >>> # Setup
            >>> my_api = Media()

            >>> # Test
            >>> my_api.calc_media_filename_from_product_number(product_number=123456789, position=1, url='something.jpg')
            '123456789_1.jpg'
            >>> my_api.calc_media_filename_from_product_number(product_number='test_get_media_filename_from_product_number', position=1, url='something.jpg')
            'test_get_media_filename_from_product_number_1.jpg'
            """

.. code-block:: python

        @staticmethod
        def calc_new_media_id(media_filename: PathMedia) -> str:
            """
            calculates a new media_id (to insert) from media_filename.
            since a media_filename (with extension) must only exist once in shopware6,
            we can calculate the is from that name.

            :param media_filename: filename (or url) with extension
            :return:

            >>> # Setup
            >>> my_api = Media()

            >>> # Test
            >>> my_new_media_id = my_api.calc_new_media_id(media_filename='123.jpg')
            >>> assert 32 == len(my_new_media_id)

            >>> # Test no extension
            >>> my_new_media_id = my_api.calc_new_media_id(media_filename='123')
            Traceback (most recent call last):
                ...
            ValueError: media_filename "123" must have an extension
            """

.. code-block:: python

        def calc_path_media_folder_from_product_number(self, product_number: Union[int, str]) -> str:
            """
            get the path of the complete media folder for a given product_number.
            the directory structure will be created as follows :
            'xxxx...' the md5-hash buil out of the product number

            conf_path_media_folder_root/xx/xx/xx/xxxxxxxxxxxxxxxxxxxxxxxxxx

            that gives us 16.7 Million directories, in order to spread products evenly in folders (sharding).

            >>> # Setup
            >>> my_api = Media()

            >>> # test
            >>> my_api.calc_path_media_folder_from_product_number(product_number=456789)
            '/Product Media/api_imported/e3/5c/f7/b66449df565f93c607d5a81d09'

            >>> # test2
            >>> my_api.calc_path_media_folder_from_product_number(product_number='123456789abcdefg')
            '/Product Media/api_imported/94/08/f8/da307c543595e92ded30cf4193'

            """

.. code-block:: python

        def delete_media_by_id(self, media_id: str) -> None:
            """
            :param media_id: the media_id
            :return:


            >>> # Setup
            >>> import time
            >>> my_api = Media()
            >>> my_media_folder_id = my_api.upsert_media_folders_by_path('/Product Media/test_delete_media_by_id')
            >>> # insert two medias
            >>> ignore1 = my_api.insert_media(media_folder_id=my_media_folder_id, url='https://pics.rotek.at/test/test001/bilder/test001_01_1280.jpg')
            >>> ignore2 = my_api.insert_media(media_folder_id=my_media_folder_id, url='https://pics.rotek.at/test/test001/bilder/test001_02_1280.jpg')

            >>> # Test delete
            >>> my_api.delete_media_by_id(media_id=my_api.get_media_id_by_media_filename(media_filename='test001_01_1280.jpg'))  # noqa
            >>> my_api.delete_media_by_id(media_id=my_api.get_media_id_by_media_filename(media_filename='test001_02_1280.jpg'))  # noqa

            >>> # teardown
            >>> my_api.delete_media_folder_by_path('/Product Media/test_delete_media_by_id', force=True)

            """

.. code-block:: python

        def delete_media_folder(self, media_folder_id: Optional[str], force: bool = False) -> None:
            """
            delete a media folder. on force, also containing media is deleted
            DANGER - API DELETES FOLDERS RUTHLESS - including Subfolders and pictures

            :param media_folder_id: the folder to delete
            :param force: if True, delete even if there are Subfolders or Media in that folder
            :return:    None

            >>> # Setup
            >>> my_api = Media()

            >>> # insert Folder
            >>> my_media_folder_id = my_api.upsert_media_folders_by_path('/Product Media/test_delete_media_folder')
            >>> assert True == my_api.is_media_folder_existing_by_path('/Product Media/test_delete_media_folder')

            >>> # delete the inserted Folder
            >>> my_api.delete_media_folder(media_folder_id=my_media_folder_id)
            >>> assert False == my_api.is_media_folder_existing_by_path('/Product Media/test_delete_media_folder')

            >>> # insert Folder with subfolder
            >>> my_media_sub_folder_id = my_api.upsert_media_folders_by_path('/Product Media/test_delete_media_folder/subfolder')
            >>> assert True == my_api.is_media_folder_existing_by_path('/Product Media/test_delete_media_folder/subfolder')

            >>> # can not delete non-empty Folder
            >>> my_media_folder_id = my_api.get_media_folder_id_by_path('/Product Media/test_delete_media_folder')
            >>> my_api.delete_media_folder(media_folder_id=my_media_folder_id)
            Traceback (most recent call last):
                ...
            OSError: media_folder_id "..." is not empty

            >>> # force-delete non-empty Folder
            >>> my_api.delete_media_folder(media_folder_id=my_media_folder_id, force=True)
            >>> assert False == my_api.is_media_folder_existing_by_path('/Product Media/test_delete_media_folder')

            >>> # try to delete Root Folder
            >>> my_api.delete_media_folder(media_folder_id=None)
            Traceback (most recent call last):
                ...
            OSError: the root folder can not be deleted

            """

.. code-block:: python

        def delete_media_folder_by_path(self, path_media_folder: PathMediaFolder, force: bool = False) -> None:
            """
            delete a media folder by path
            DANGER - API DELETES FOLDERS RUTHLESS - including Subfolders and pictures

            :param path_media_folder: like '/Product Media/a000/000/001
            :param force: if True, delete even if there are Subfolders or Media in that folder
            :return:    None

            >>> # Setup
            >>> my_api = Media()
            >>> ignore = my_api.upsert_media_folders_by_path(path_media_folder='/Product Media/test_delete_media_folder_by_path/subfolder1/subfolder2/subfolder3')

            >>> # Test delete Empty Folder
            >>> my_api.delete_media_folder_by_path(path_media_folder='/Product Media/test_delete_media_folder_by_path/subfolder1/subfolder2/subfolder3')

            >>> # Test delete Empty Folder without force
            >>> my_api.delete_media_folder_by_path(path_media_folder='/Product Media/test_delete_media_folder_by_path/subfolder1')
            Traceback (most recent call last):
                ...
            OSError: media_folder "/Product Media/test_delete_media_folder_by_path/subfolder1" is not empty

            >>> # Test delete Folder with force
            >>> my_api.delete_media_folder_by_path(path_media_folder='/Product Media/test_delete_media_folder_by_path', force=True)
            >>> assert False == my_api.is_media_folder_existing_by_path(path_media_folder='/Product Media/test_delete_media_folder_by_path')

            """

.. code-block:: python

        @lru_cache(maxsize=None)
        def get_media_folder_configuration_id_from_media_folder_name(self, media_folder_name: str = "Product Media", parent_id: Optional[str] = None) -> str:
            """
            get the configuration_id of a media folder. this configuration_id can be passed to child folders,
            in order to inherit the configuration from the parent folder

            Parameter :
                media_folder_name: the name of the parent folder, like 'Product Media'
                parent_id        : the parent id of the Folder

            :returns: the configuration id

            >>> # Setup
            >>> my_api = Media()

            >>> # test get 'Product Media' id
            >>> my_folder_configuration_id = my_api.get_media_folder_configuration_id_from_media_folder_name()
            >>> assert 32 == len(my_folder_configuration_id)

            >>> # test not existing (int)
            >>> my_api.get_media_folder_configuration_id_from_media_folder_name(media_folder_name='not_existing')
            Traceback (most recent call last):
                ...
            FileNotFoundError: media folder with name "not_existing" not found

            >>> # Test clear Cache -the Cache has to be cleared if media_folders are inserted or deleted
            >>> my_api.get_media_folder_configuration_id_from_media_folder_name.cache_clear()

            """

.. code-block:: python

        def get_media_folder_configuration_l_dict_all(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
            """
            get all media_folder_configurations - filters and so on can be set in the payload
            we read paginated (in junks of 100 items) - this is done automatically by function base_client.request_get_paginated()

            :parameters
                payload, to set filters etc.

            :returns
                l_dict_data,

            sample payload :
                page and limit will be overridden by function base_client.request_get_paginated() and will be ignored

            >>> # Setup
            >>> my_api = Media()
            >>> my_l_dict_data = my_api.get_media_folder_configuration_l_dict_all()
            """

.. code-block:: python

        @lru_cache(maxsize=None)
        def get_media_folder_id(self, name: str, parent_id: Optional[str]) -> str:
            """
            get the id of a media folder
            >>> # Setup
            >>> my_api = Media()

            >>> # Test get existing Folder
            >>> assert my_api.get_media_folder_id(name='Product Media', parent_id=None)  # noqa

            >>> # Test get non-existing Folder
            >>> my_api.get_media_folder_id(name='not-existing', parent_id=None)  # noqa
            Traceback (most recent call last):
                ...
            FileNotFoundError: media_folder, name: "not-existing", parent_id: "None" not found

            >>> # Test clear Cache -the Cache has to be cleared if media_folders are inserted or deleted
            >>> my_api.get_media_folder_id.cache_clear()

            """

.. code-block:: python

        @lru_cache(maxsize=None)
        def get_media_folder_id_by_path(self, path_media_folder: PathMediaFolder) -> Optional[str]:
            """
            get the id of a media folder
            :param path_media_folder: path - for instance /Product Media/a000/000/001

            >>> # Setup
            >>> my_api = Media()
            >>> my_folder_id = my_api.upsert_media_folders_by_path('/Product Media/test_get_media_folder_id_by_path/999/999')

            >>> # Test Existing
            >>> assert my_folder_id == my_api.get_media_folder_id_by_path('/Product Media/test_get_media_folder_id_by_path/999/999')

            >>> # Test Invalid
            >>> my_api.get_media_folder_id_by_path('not-existing-folder')
            Traceback (most recent call last):
                ...
            OSError: media_folder path "not-existing-folder" is invalid, it must be absolute

            >>> # Test Not Existing
            >>> my_api.get_media_folder_id_by_path('/not-existing-folder')
            Traceback (most recent call last):
                ...
            FileNotFoundError: media_folder path "/not-existing-folder" not found

            >>> # Test clear Cache -the Cache has to be cleared if media_folders are inserted or deleted
            >>> my_api.get_media_folder_id_by_path.cache_clear()

            >>> # Teardown
            >>> my_api.delete_media_folder_by_path('/Product Media/test_get_media_folder_id_by_path', force=True)

            """

.. code-block:: python

        def get_media_folder_l_dict_all(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
            """
            get all media_folder - filters and so on can be set in the payload
            we read paginated (in junks of 100 items) - this is done automatically by function base_client.request_get_paginated()

            :parameters
                payload, to set filters etc.

            :returns
                l_dict_data,

            sample payload :
                page and limit will be overridden by function base_client.request_get_paginated() and will be ignored

            >>> # Setup
            >>> my_api = Media()
            >>> my_l_dict_data = my_api.get_media_folder_l_dict_all()
            """

.. code-block:: python

        def get_media_id_by_media_filename(self, media_filename: PathMedia) -> str:
            """
            gets the media_id from media_folder_id and media_filename
            this can only work if the picture is already uploaded !
            :param media_filename:  the filename (with extension) as string, like 'test001_01_1280.jpg', or the url link that ends with '.../test001_01_1280.jpg'
            :return:

            >>> # Setup
            >>> my_api = Media()
            >>> my_media_folder_id = my_api.upsert_media_folders_by_path('/Product Media/test_get_media_id/999/999')
            >>> my_media_id = my_api.insert_media(media_folder_id=my_media_folder_id, url='https://pics.rotek.at/test/test001/bilder/test001_07_1280.jpg')

            >>> # test existing Folder, existing Media
            >>> my_media_filename = 'test001_07_1280.jpg'
            >>> assert my_media_id == my_api.get_media_id_by_media_filename(media_filename=my_media_filename)

            >>> # test non-existing Media
            >>> my_media_filename = 'bat013_77_7777.jpg'
            >>> my_api.get_media_id_by_media_filename(media_filename=my_media_filename)
            Traceback (most recent call last):
                ...
            FileNotFoundError: media_filename: "bat013_77_7777.jpg" not found

            >>> # Teardown
            >>> my_api.delete_media_folder_by_path(path_media_folder = '/Product Media/test_get_media_id', force=True)
            """

.. code-block:: python

        def get_media_l_dict_all(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
            """
            get all media records - filters and so on can be set in the payload
            we read paginated (in junks of 100 items) - this is done automatically by function base_client.request_get_paginated()

            :parameters
                payload, to set filters etc.

            :returns
                l_dict_data,


            sample payload :
                page and limit will be overridden by function base_client.request_get_paginated() and will be ignored

            >>> # Setup
            >>> my_api = Media()
            >>> my_l_dict_data = my_api.get_media_l_dict_all()
            """

.. code-block:: python

        def insert_media(
            self,
            media_folder_id: Union[str, None],
            url: str,
            media_alt_txt: Union[str, None] = None,
            media_title: Union[str, None] = None,
            media_filename: Optional[PathMedia] = None,
            upload_media: bool = True,
        ) -> str:
            """
            creates a single "media record" and uploads the media from the url - the media filename is taken from the url if not provided
            note that the same media_filename must not exist twice in the shop, even if on different media folders !

            this should only be used if You upload the media indipendently from products -
            otherwise You should use associations to update the product with one request - see :
            https://shopware.stoplight.io/docs/admin-api/ZG9jOjEyNjI1Mzkw-media-handling
            https://shopware.stoplight.io/docs/admin-api/ZG9jOjEyMzA4NTUw-associationsundefined

            if upload_media == False, You can only rely on the returned media_id to find the inserted record -
                all other fields are "None" so the api functions is_media_existing, etc. will not work !
                You need to store the media_id and upload the media to complete the record.

            :param media_folder_id:     id des folders
            :param url:                 url des files zum hochladen
            :param media_alt_txt:       optional, 'alt'
            :param media_title:         optional, 'title'
            :param media_filename:      optional, the filename (with extension) as string, like 'test001_01_1280.jpg', otherwise taken from url
            :param upload_media         if to upload the media
            :return: the new Media ID

            see : https://shopware.stoplight.io/docs/admin-api/c2NoOjE0MzUxMjU3-media
            see : https://shopware.stoplight.io/docs/admin-api/ZG9jOjEyNjI1Mzkw-media-handling

            >>> # Setup
            >>> my_api = Media()
            >>> my_media_folder_id = my_api.upsert_media_folders_by_path(path_media_folder='/Product Media/test_insert_media')

            >>> # insert media
            >>> ignore = my_api.insert_media(media_folder_id=my_media_folder_id, url='https://pics.rotek.at/test/test001/bilder/test001_07_1280.jpg',
            ...     media_filename = 'test001_07_1280.jpg')

            >>> # insert media, without stating filename
            >>> ignore = my_api.insert_media(media_folder_id=my_media_folder_id, url='https://pics.rotek.at/test/test001/bilder/test001_08_1280.jpg')

            >>> # cleanup
            >>> my_api.delete_media_folder_by_path(path_media_folder='/Product Media/test_insert_media', force=True)

            """

.. code-block:: python

        def insert_media_by_path(self, path_media: PathMedia, url: str, media_alt_txt: Union[str, None] = None, media_title: Union[str, None] = None) -> str:
            """
            Inserts a Media by Path, and upload the media from the url.
            note that the same media_filename must not exist twice in the shop, even if on different media folders !

            this should only be used if You upload the media indipendently from products -
            otherwise You should use associations to update the product with one request - see :
            https://shopware.stoplight.io/docs/admin-api/ZG9jOjEyNjI1Mzkw-media-handling
            https://shopware.stoplight.io/docs/admin-api/ZG9jOjEyMzA4NTUw-associationsundefined

            since associations will only be upserted but not deleted we make following approach :
            - delete the product_media relations for a product
            -

            :param path_media: '/Product Media/a000/123/456/000123456_01_1280.jpg'
            :param url:  url='https://pics.rotek.at/test/test003/bilder/test003_01_1280.jpg'
            :param media_alt_txt:   optional
            :param media_title:     optional
            :return: the new media id


            >>> # Setup
            >>> my_api = Media()

            >>> # insert media
            >>> ignore = my_api.insert_media_by_path(path_media='/Product Media/insert_media_by_path/test001_07_1280.jpg',
            ...     url='https://pics.rotek.at/test/test001/bilder/test001_07_1280.jpg')

            >>> # insert media, without stating filename
            >>> ignore = my_api.insert_media_by_path(path_media='/Product Media/insert_media_by_path/test001_08_1280.jpg',
            ...     url='https://pics.rotek.at/test/test001/bilder/test001_07_1280.jpg')

            >>> # cleanup
            >>> my_api.delete_media_folder_by_path(path_media_folder='/Product Media/insert_media_by_path', force=True)

            """

.. code-block:: python

        def insert_media_folder_by_name_and_parent_id(self, name: str, parent_id: Optional[str], configuration_id: Optional[str] = None) -> None:
            """
            insert a media folder

            :param name:             the name of the folder
            :param parent_id:        the id of the parent folder
            :param configuration_id: the folder configuration id. taken from parent folder if none
            :return: None

            >>> # Setup
            >>> my_api = Media()

            >>> # insert Folder
            >>> id_root = my_api.get_media_folder_id(name='Product Media', parent_id=None)  # noqa
            >>> my_api.insert_media_folder_by_name_and_parent_id(name='test_insert_media_folder_by_name_and_parent_id', parent_id=id_root)
            >>> assert True == my_api.is_media_folder_existing_by_path('/Product Media/test_insert_media_folder_by_name_and_parent_id')

            >>> # delete the inserted Folder
            >>> my_api.delete_media_folder_by_path('/Product Media/test_insert_media_folder_by_name_and_parent_id')

            """

.. code-block:: python

        def is_media_existing(self, media_filename: str) -> bool:
            """
            True if the media ID exists -
            the media_id is read from the filename or the filename of the url. filename needs to have extension for the media mime type

            :param media_filename: filename or url of the media (if the filename is the same like the name in the url)
            :return:

            >>> # Setup
            >>> my_api = Media()

            >>> # insert media
            >>> ignore01 = my_api.insert_media_by_path(path_media='/Product Media/test_is_media_existing/is_media_existing_01.jpg', \
                    url='https://pics.rotek.at/test/test001/bilder/test001_05_1280.jpg')

            >>> # test check exist
            >>> assert True == my_api.is_media_existing(media_filename='https://pics.rotek.at/test/test001/bilder/is_media_existing_01.jpg')
            >>> assert True == my_api.is_media_existing(media_filename='is_media_existing_01.jpg')

            >>> # test check not exist
            >>> assert False == my_api.is_media_existing(media_filename='does_not_exist.jpg')

            >>> # test no extension
            >>> my_api.is_media_existing(media_filename='no_extension')
            Traceback (most recent call last):
                ...
            ValueError: media "no_extension" does not have an extension

            >>> # cleanup
            >>> my_api.delete_media_folder_by_path(path_media_folder='/Product Media/test_is_media_existing', force=True)

            """

.. code-block:: python

        def is_media_existing_by_media_id(self, media_id: str) -> bool:
            """
            :param media_id:
            :return:

            >>> # Setup
            >>> my_api = Media()
            >>> my_media_id = my_api.insert_media_by_path(path_media='/Product Media/test_is_media_existing_by_media_id/is_media_existing_by_media_id.jpg', \
                    url='https://pics.rotek.at/test/test001/bilder/test001_05_1280.jpg')

            >>> # Test Existing
            >>> assert True == my_api.is_media_existing_by_media_id(my_media_id)

            >>> # Test not Existing
            >>> assert False == my_api.is_media_existing_by_media_id('0123456789')

            >>> # TearDown
            >>> my_api.delete_media_folder_by_path('/Product Media/test_is_media_existing_by_media_id', force=True)

            """

.. code-block:: python

        def is_media_folder_containing_subfolders(self, media_folder_id: Optional[str]) -> bool:
            """
            :returns True if there is a subfolder in the media folder
            :param media_folder_id:
            :return:

            >>> # Setup
            >>> my_api = Media()
            >>> ignore = my_api.upsert_media_folders_by_path(path_media_folder='/Product Media/test_is_media_folder_containing_subfolders')

            >>> # Test subfolder existing
            >>> my_media_folder_id=my_api.get_media_folder_id_by_path(path_media_folder='/')
            >>> assert True == my_api.is_media_folder_containing_subfolders(media_folder_id=my_media_folder_id)

            >>> # test no Subfolder
            >>> my_media_folder_id=my_api.get_media_folder_id_by_path(path_media_folder='/Product Media/test_is_media_folder_containing_subfolders')
            >>> assert False == my_api.is_media_folder_containing_subfolders(media_folder_id=my_media_folder_id)

            >>> # test Media Folder not existing
            >>> my_api.is_media_folder_containing_subfolders(media_folder_id='0123456789')
            Traceback (most recent call last):
                ...
            FileNotFoundError: media_folder id "0123456789" not found

            >>> # teardown
            >>> my_api.delete_media_folder_by_path(path_media_folder='/Product Media/test_is_media_folder_containing_subfolders')

            """

.. code-block:: python

        def is_media_folder_empty(self, media_folder_id: Optional[str]) -> bool:
            """
            true if the media_folder does not contain any media files or subfolders
            :param media_folder_id:
            :return:

            >>> # Setup
            >>> my_api = Media()
            >>> ignore1 = my_api.insert_media_by_path(path_media='/Product Media/test_is_media_folder_empty_with_media/test003_01_1280.jpg',
            ...     url='https://pics.rotek.at/test/test003/bilder/test003_01_1280.jpg')
            >>> ignore2 = my_api.upsert_media_folders_by_path(path_media_folder='/Product Media/test_is_media_folder_empty_with_subfolder/subfolder')
            >>> ignore3 = my_api.upsert_media_folders_by_path(path_media_folder='/Product Media/test_is_media_folder_empty_empty')

            >>> # test no subfolder, media files existing
            >>> my_media_folder_id=my_api.get_media_folder_id_by_path(path_media_folder='/Product Media/test_is_media_folder_empty_with_media')
            >>> assert False == my_api.is_media_folder_containing_subfolders(media_folder_id=my_media_folder_id)

            >>> # Test subfolder existing, no media files
            >>> my_media_folder_id=my_api.get_media_folder_id_by_path(path_media_folder='/Product Media/test_is_media_folder_empty_with_subfolder')
            >>> assert False == my_api.is_media_folder_empty(media_folder_id=my_media_folder_id)

            >>> # Test no subfolder, no media files existing
            >>> my_media_folder_id=my_api.get_media_folder_id_by_path(path_media_folder='/Product Media/test_is_media_folder_empty_empty')
            >>> assert True == my_api.is_media_folder_empty(media_folder_id=my_media_folder_id)

            >>> # Test Folder not existing
            >>> my_api.is_media_folder_containing_subfolders(media_folder_id='0123456789')
            Traceback (most recent call last):
                ...
            FileNotFoundError: media_folder id "0123456789" not found

            >>> # Teardown
            >>> my_api.delete_media_folder_by_path('/Product Media/test_is_media_folder_empty_with_media', force=True)
            >>> my_api.delete_media_folder_by_path('/Product Media/test_is_media_folder_empty_with_subfolder', force=True)
            >>> my_api.delete_media_folder_by_path('/Product Media/test_is_media_folder_empty_empty', force=True)

            """

.. code-block:: python

        def is_media_folder_empty_by_path(self, path_media_folder: PathMediaFolder) -> bool:
            """
            true if the media_folder does not contain any media files or subfolders
            :param path_media_folder: like '/Product Media/a000/000/001
            :return:

                    >>> # Setup
            >>> my_api = Media()
            >>> ignore1 = my_api.insert_media_by_path(path_media='/Product Media/test_is_media_folder_empty_by_path_with_media/test003_01_1280.jpg',
            ...     url='https://pics.rotek.at/test/test003/bilder/test003_01_1280.jpg')
            >>> ignore2 = my_api.upsert_media_folders_by_path(path_media_folder='/Product Media/test_is_media_folder_empty_by_path_with_subfolder/subfolder')
            >>> ignore3 = my_api.upsert_media_folders_by_path(path_media_folder='/Product Media/test_is_media_folder_empty_by_path_empty')

            >>> # Test no subfolder, media files existing
            >>> assert False == my_api.is_media_folder_empty_by_path(path_media_folder='/Product Media/test_is_media_folder_empty_by_path_with_media')

            >>> # Test subfolder existing, no media files
            >>> assert False == my_api.is_media_folder_empty_by_path(path_media_folder='/Product Media/test_is_media_folder_empty_by_path_with_subfolder')

            >>> # Test no subfolder, no media files existing
            >>> assert True == my_api.is_media_folder_empty_by_path(path_media_folder='/Product Media/test_is_media_folder_empty_by_path_empty')

            >>> # test Folder not existing
            >>> my_api.is_media_folder_containing_subfolders(media_folder_id='0123456789')
            Traceback (most recent call last):
                ...
            FileNotFoundError: media_folder id "0123456789" not found

            >>> # Teardown
            >>> my_api.delete_media_folder_by_path('/Product Media/test_is_media_folder_empty_by_path_with_media', force=True)
            >>> my_api.delete_media_folder_by_path('/Product Media/test_is_media_folder_empty_by_path_with_subfolder', force=True)
            >>> my_api.delete_media_folder_by_path('/Product Media/test_is_media_folder_empty_by_path_empty', force=True)

            """

.. code-block:: python

        def is_media_folder_existing(self, media_folder_id: Optional[str]) -> bool:
            """
            True if the folder exists, False if it does not exist
            :param media_folder_id:
            :return:

            >>> # Setup
            >>> my_api = Media()

            >>> # Test media_folder existing
            >>> my_media_folder_id=my_api.get_media_folder_id_by_path(path_media_folder='/Product Media')
            >>> assert True == my_api.is_media_folder_existing(media_folder_id=my_media_folder_id)

            >>> # Test media_folder not existing
            >>> assert False == my_api.is_media_folder_existing(media_folder_id='0123456789')
            """

.. code-block:: python

        def is_media_folder_existing_by_path(self, path_media_folder: PathMediaFolder) -> bool:
            """
            True if the folder exists, False if it does not exist
            :param path_media_folder: like '/Product Media/a000/000/001
            :return:

            >>> # Setup
            >>> my_api = Media()

            >>> # Test media_folder existing
            >>> assert True == my_api.is_media_folder_existing_by_path(path_media_folder='/Product Media')

            >>> # Test media_folder not existing
            >>> assert False == my_api.is_media_folder_existing_by_path(path_media_folder='/test_is_media_folder_existing_by_path/sub1/sub2')

            """

.. code-block:: python

        def is_media_in_media_folder(self, media_folder_id: Optional[str]) -> bool:
            """
            :returns True if there is some media files in the media folder
            :param media_folder_id:

            >>> # Setup
            >>> my_api = Media()
            >>> ignore01 = my_api.upsert_media_folders_by_path(path_media_folder='/Product Media/test_is_media_in_media_folder_no_media')
            >>> ignore02 = my_api.insert_media_by_path(path_media='/Product Media/test_is_media_in_media_folder_with_media/test001_07_1280.jpg',
            ...     url='https://pics.rotek.at/test/test001/bilder/test001_07_1280.jpg')


            >>> # Test no Media in Folder
            >>> my_media_folder_id = my_api.get_media_folder_id_by_path('/Product Media/test_is_media_in_media_folder_no_media')
            >>> assert False == my_api.is_media_in_media_folder(media_folder_id = my_media_folder_id)
            >>> # Test Media in Folder
            >>> my_media_folder_id = my_api.get_media_folder_id_by_path('/Product Media/test_is_media_in_media_folder_with_media')
            >>> assert True == my_api.is_media_in_media_folder(media_folder_id = my_media_folder_id)
            >>> # Test Folder not existing
            >>> my_api.is_media_in_media_folder(media_folder_id = '01234567890')
            Traceback (most recent call last):
                ...
            FileNotFoundError: media_folder id "01234567890" not found

            >>> # Teardown
            >>> my_api.delete_media_folder_by_path(path_media_folder='/Product Media/test_is_media_in_media_folder_no_media', force=True)
            >>> my_api.delete_media_folder_by_path(path_media_folder='/Product Media/test_is_media_in_media_folder_with_media', force=True)

            """

.. code-block:: python

        def search_media_folders_l_dict(self, payload: PayLoad = None) -> List[Dict[str, Any]]:
            """
            get all the media folders

            >>> # Setup
            >>> my_api = Media()

            >>> # test
            >>> my_l_data_dict = my_api.search_media_folders_l_dict()

            """

.. code-block:: python

        def search_media_l_dict(self, payload: PayLoad = None) -> List[Dict[str, Any]]:
            """
            get all the media

            >>> # Setup
            >>> my_api = Media()

            >>> # insert article
            >>> ignore = my_api.search_media_l_dict()

            """

.. code-block:: python

        def update_media(
            self,
            media_folder_id: Union[str, None],
            url: str,
            media_alt_txt: Union[str, None] = None,
            media_title: Union[str, None] = None,
            media_filename: Optional[PathMedia] = None,
            upload_media: bool = True,
        ) -> str:
            """
            find the media record by media_filename and media_folder_id,
            update Media "mediaFolderId", "alt" and "title"
            upload the image from url.
            if no "media_filename" is provided, the media filename is taken from the url.

            :param media_folder_id:     folder id
            :param url:                 url of the file to upload
            :param media_alt_txt:       'alt'
            :param media_title:         'title'
            :param media_filename:      the filename (with extension) as string, like 'test001_01_1280.jpg'
            :param upload_media:        if to upload the media
            :return: the media_id

            see : https://shopware.stoplight.io/docs/admin-api/c2NoOjE0MzUxMjU3-media
            see : https://shopware.stoplight.io/docs/admin-api/ZG9jOjEyNjI1Mzkw-media-handling

            >>> # Setup
            >>> my_api = Media()
            >>> my_media_folder_id = my_api.upsert_media_folders_by_path(path_media_folder='/Product Media/test_update_media')

            >>> # insert media
            >>> ignore01 = my_api.insert_media(media_folder_id=my_media_folder_id, url='https://pics.rotek.at/test/test001/bilder/test001_09_1280.jpg',
            ...     media_filename = 'test001_09_1280.jpg')

            >>> # update media, with url different from filename
            >>> ignore02 = my_api.update_media(media_folder_id=my_media_folder_id, url='https://pics.rotek.at/test/test003/bilder/test003_01_1280.jpg',
            ...     media_filename = 'test001_09_1280.jpg')

            >>> # cleanup
            >>> my_api.delete_media_folder_by_path(path_media_folder='/Product Media/test_update_media', force=True)

            """

.. code-block:: python

        def upload_media_from_url(self, media_id: str, url: str, filename_suffix: str, filename_stem: str) -> None:
            """
            uploads the media to an existing media_id
            note that the same media_filename must not exist twice in the shop, even if on different media folders !
            :param media_id:        the media id
            :param url:             the url to upload the media from
            :param filename_suffix: the extension, like "jpg"
            :param filename_stem:   the filename (without extension)
            :return:
            """

.. code-block:: python

        def upsert_media(
            self,
            product_number: Union[int, str],
            position: int,
            url: str,
            media_alt: Union[str, None] = None,
            media_title: Union[str, None] = None,
            upload_media: bool = True,
        ) -> str:
            """
            Insert or updates the Media and its folder. On insert, the media_id is calculated from product_number
            media folders are created as needed

            if upload_media == False, You can only rely on the returned media_id to find the inserted record -
                all other fields are "None" so the api functions is_media_existing, etc. will not work !
                You need to store the media_id and upload the media to complete the record.

            :param product_number: 9 digit rotek artikelnummer
            :param position: the position when sorting pictures
            :param url:
            :param media_alt:
            :param media_title:
            :param upload_media:
            :return: the new, or updated media_id

            >>> # Setup
            >>> my_api = Media()
            >>> my_api.conf_path_media_folder_root = '/Product Media/api_test_upsert_product_media'
            >>> my_url='https://pics.rotek.at/test/test001/bilder/test001_03_1280.jpg'
            >>> my_product_number = '997997997'
            >>> my_media_filename = my_api.calc_media_filename_from_product_number(
            ...     product_number=my_product_number, position=1, url=my_url)

            >>> # Test media is not existing now
            >>> assert False == my_api.is_media_existing(media_filename=my_media_filename)

            >>> # Test media upsert (insert)
            >>> ignore01 = my_api.upsert_media(product_number=my_product_number, position=1, url=my_url)
            >>> assert True == my_api.is_media_existing(media_filename=my_media_filename)

            >>> # Test media upsert (update)
            >>> ignore02 = my_api.upsert_media(product_number=my_product_number, position=1, url=my_url)
            >>> assert True == my_api.is_media_existing(media_filename=my_media_filename)
            >>> assert ignore01 == ignore02

            >>> # cleanup
            >>> my_api.delete_media_folder_by_path(my_api.conf_path_media_folder_root, force=True)

            """

.. code-block:: python

        def upsert_media_folders_by_path(self, path_media_folder: PathMediaFolder, configuration_id: Optional[str] = None) -> Optional[str]:
            """
            upsert media folders - including the parents, exist is ok

            :param path_media_folder: like '/Product Media/a000/000/001
            :param configuration_id: the folder configuration id. taken from parent folder if none
            :return: the id of the last created folder

            >>> # Setup
            >>> my_api = Media()

            >>> # Test
            >>> discard = my_api.upsert_media_folders_by_path(path_media_folder='/Product Media/test_insert_media_folder_by_path/subfolder1/subfolder2')
            >>> assert True == my_api.is_media_folder_existing_by_path(path_media_folder='/Product Media/test_insert_media_folder_by_path/subfolder1/subfolder2')

            >>> # test Exist = Ok
            >>> discard = my_api.upsert_media_folders_by_path(path_media_folder='/Product Media/test_insert_media_folder_by_path/subfolder1/subfolder2')
            >>> assert True == my_api.is_media_folder_existing_by_path(path_media_folder='/Product Media/test_insert_media_folder_by_path/subfolder1/subfolder2')

            >>> # Teardown
            >>> my_api.delete_media_folder_by_path(path_media_folder='/Product Media/test_insert_media_folder_by_path', force=True)

            """

Product
=======
back to `Overview`_

.. code-block:: python

    @attrs.define
    class ProductPicture:
        """
        dataclass to upsert a picture
        """

.. code-block:: python

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

.. code-block:: python

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

.. code-block:: python

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

.. code-block:: python

        def cache_clear_product(self) -> None:
            """
            Cache of some functions has to be cleared if articles are inserted or deleted

            >>> # Setup
            >>> my_api = Product()
            >>> # Test
            >>> my_api.cache_clear_product()

            """

.. code-block:: python

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

.. code-block:: python

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

.. code-block:: python

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

.. code-block:: python

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

.. code-block:: python

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

.. code-block:: python

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

.. code-block:: python

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

.. code-block:: python

        def upsert_product_payload(self, product_number: Union[int, str], payload: Dict[str, Any]) -> str:

.. code-block:: python

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

.. code-block:: python

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

.. code-block:: python

        def search_product_media_l_dict(self, payload: PayLoad = None) -> List[Dict[str, Any]]:
            """
            search product_media

            >>> # Setup
            >>> my_api = Product()

            >>> # insert article
            >>> ignore = my_api.search_product_media_l_dict()

            """

.. code-block:: python

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

Tax
===
back to `Overview`_

.. code-block:: python

    class Tax(object):
        def __init__(
            self, admin_client: Optional[Shopware6AdminAPIClientBase] = None, config: Optional[ConfShopware6ApiBase] = None, use_docker_test_container: bool = False
        ) -> None:
            """
            :param admin_client:
            :param config:
            :param use_docker_test_container:

            >>> # Setup
            >>> my_api = Tax()

            """

.. code-block:: python

        def cache_clear_tax(self) -> None:
            """
            Cache of some functions has to be cleared if tax is inserted or deleted

            >>> # Setup
            >>> my_api = Tax()
            >>> # test
            >>> my_api.cache_clear_tax()

            """

.. code-block:: python

        @lru_cache(maxsize=None)
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

.. code-block:: python

        def get_tax_l_dict_all(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
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
            >>> my_l_dict_data = my_api.get_tax_l_dict_all()
            """

.. code-block:: python

        @lru_cache(maxsize=None)
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

Usage from Commandline
------------------------

.. code-block::

   Usage: lib_shopware6_api [OPTIONS] COMMAND [ARGS]...

     use the shopware 6 api

   Options:
     --version                     Show the version and exit.
     --traceback / --no-traceback  return traceback information on cli
     -h, --help                    Show this message and exit.

   Commands:
     info  get program informations

Installation and Upgrade
------------------------

- Before You start, its highly recommended to update pip and setup tools:


.. code-block::

    python -m pip --upgrade pip
    python -m pip --upgrade setuptools

- to install the latest release from PyPi via pip (recommended):

.. code-block::

    python -m pip install --upgrade lib_shopware6_api

- to install the latest version from github via pip:


.. code-block::

    python -m pip install --upgrade git+https://github.com/bitranox/lib_shopware6_api.git


- include it into Your requirements.txt:

.. code-block::

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi:
    lib_shopware6_api

    # for the latest development version :
    lib_shopware6_api @ git+https://github.com/bitranox/lib_shopware6_api.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python -m pip install --upgrade -r /<path>/requirements.txt


- to install the latest development version from source code:

.. code-block::

    # cd ~
    $ git clone https://github.com/bitranox/lib_shopware6_api.git
    $ cd lib_shopware6_api
    python setup.py install

- via makefile:
  makefiles are a very convenient way to install. Here we can do much more,
  like installing virtual environments, clean caches and so on.

.. code-block:: shell

    # from Your shell's homedirectory:
    $ git clone https://github.com/bitranox/lib_shopware6_api.git
    $ cd lib_shopware6_api

    # to run the tests:
    $ make test

    # to install the package
    $ make install

    # to clean the package
    $ make clean

    # uninstall the package
    $ make uninstall

Requirements
------------
following modules will be automatically installed :

.. code-block:: bash

    ## Project Requirements
    attrs
    click
    cli_exit_tools
    lib_detect_testenv
    lib_shopware6_api_base

Acknowledgements
----------------

- special thanks to "uncle bob" Robert C. Martin, especially for his books on "clean code" and "clean architecture"

Contribute
----------

I would love for you to fork and send me pull request for this project.
- `please Contribute <https://github.com/bitranox/lib_shopware6_api/blob/master/CONTRIBUTING.md>`_

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

---

Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

v1.0.2
--------
- clean requirements.txt

v1.0.1
--------
2022-01-18: Documentation update, make PyPi package

v1.0.0
--------
2022-01-17: Initial Release

