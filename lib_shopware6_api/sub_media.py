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

PathMedia = Union[str, PathLike, pathlib.Path]
PathMediaFolder = Union[str, PathLike, pathlib.Path]


# Media{{{
class Media(object):
    def __init__(
        self, admin_client: Optional[Shopware6AdminAPIClientBase] = None, config: Optional[ConfShopware6ApiBase] = None, use_docker_test_container: bool = False
    ) -> None:
        """
        >>> # Setup
        >>> my_api = Media()

        """
        # Media}}}
        if admin_client is None:
            self._admin_client = Shopware6AdminAPIClientBase(config=config, use_docker_test_container=use_docker_test_container)
        else:
            self._admin_client = admin_client

        # CONF
        self.conf_path_media_folder_root = "/Product Media/api_imported"

    # cache_clear_media{{{
    def cache_clear_media(self) -> None:
        """
        Cache of some functions has to be cleared if media is inserted or deleted

        >>> # Setup
        >>> my_api = Media()
        >>> # test
        >>> my_api.cache_clear_media()

        """
        # cache_clear_media}}}
        pass

    # cache_clear_media_folder{{{
    def cache_clear_media_folder(self) -> None:
        """
        Cache of some functions has to be cleared if media_folders are inserted or deleted

        >>> # Setup
        >>> my_api = Media()
        >>> # test
        >>> my_api.cache_clear_media_folder()

        """
        # cache_clear_media_folder}}}
        self.get_media_folder_id.cache_clear()
        self.get_media_folder_id_by_path.cache_clear()
        self.get_media_folder_configuration_id_from_media_folder_id.cache_clear()
        self.get_media_folder_configuration_id_from_media_folder_name.cache_clear()

    # calc_media_filename_from_product_number{{{
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
        # calc_media_filename_from_product_number}}}
        media_filename = "{num:0>9}".format(num=str(product_number)) + f"_{position}" + pathlib.Path(url).suffix
        return media_filename

    # calc_new_media_id{{{
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
        # calc_new_media_id}}}
        path_media_filename = pathlib.Path(media_filename)
        if not path_media_filename.suffix:
            raise ValueError(f'media_filename "{media_filename}" must have an extension')
        media_filename = str(path_media_filename.name)
        media_id = hashlib.md5(media_filename.encode("utf-8")).hexdigest()
        return media_id

    # calc_path_media_folder_from_product_number{{{
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
        # calc_path_media_folder_from_product_number}}}
        product_number_md5 = hashlib.md5(str(product_number).encode("utf-8")).hexdigest()
        path_media_folder = pathlib.Path(self.conf_path_media_folder_root)
        path_media_folder = path_media_folder / product_number_md5[0:2] / product_number_md5[2:4] / product_number_md5[4:6] / product_number_md5[6:]
        return path_media_folder.as_posix()

    # delete_media_by_id{{{
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
        # delete_media_by_id}}}
        self._admin_client.request_delete(f"media/{media_id}")
        self.cache_clear_media()

    # delete_media_folder{{{
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
        # delete_media_folder}}}
        if media_folder_id is None:
            raise OSError("the root folder can not be deleted")

        if not force:
            if not self.is_media_folder_empty(media_folder_id=media_folder_id):
                raise OSError(f'media_folder_id "{media_folder_id}" is not empty')

        self._admin_client.request_delete(f"media-folder/{media_folder_id}")
        self.cache_clear_media_folder()

    # delete_media_folder_by_path{{{
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
        # delete_media_folder_by_path}}}
        media_folder_id = self.get_media_folder_id_by_path(path_media_folder=path_media_folder)  # type: ignore
        if not force:
            if not self.is_media_folder_empty_by_path(path_media_folder=path_media_folder):
                raise OSError(f'media_folder "{path_media_folder}" is not empty')
        self.delete_media_folder(media_folder_id=media_folder_id, force=True)

    # get_media_folder_configuration_id_from_media_folder_id{{{
    @lru_cache(maxsize=None)
    def get_media_folder_configuration_id_from_media_folder_id(self, media_folder_id: str) -> str:
        """
        get the configuration_id of a media_folder. this configuration_id can be passed to child folders,
        in order to inherit the configuration from the parent folder
        :param media_folder_id: the id of a folder
        :returns: the configuration id of the folder

        >>> # Setup
        >>> my_api = Media()
        >>> my_folder_id = my_api.get_media_folder_id(name='Product Media', parent_id=None)

        >>> # test get 'Product Media' id
        >>> my_folder_configuration_id = my_api.get_media_folder_configuration_id_from_media_folder_id(media_folder_id=my_folder_id)
        >>> assert 32 == len(my_folder_configuration_id)

        >>> # test not existing (int)
        >>> my_api.get_media_folder_configuration_id_from_media_folder_id(media_folder_id='0123456789')
        Traceback (most recent call last):
            ...
        FileNotFoundError: media folder with id "0123456789" not found

        >>> # Test clear Cache -the Cache has to be cleared if media_folders are inserted or deleted
        >>> my_api.get_media_folder_configuration_id_from_media_folder_id.cache_clear()

        """
        # get_media_folder_configuration_id_from_media_folder_id}}}

        payload = dal.Criteria()
        payload.page = 1
        payload.limit = 1
        payload.filter = [dal.EqualsFilter(field="id", value=media_folder_id)]
        payload.includes = {"media_folder": ["configurationId"]}

        dict_response = self._admin_client.request_post(request_url="search/media-folder", payload=payload)
        try:
            media_folder_configuration_id = str(dict_response["data"][0]["configurationId"])
        except IndexError:
            raise FileNotFoundError(f'media folder with id "{media_folder_id}" not found')
        return media_folder_configuration_id

    # get_media_folder_configuration_id_from_media_folder_name{{{
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
        # get_media_folder_configuration_id_from_media_folder_name}}}

        payload = dal.Criteria()
        payload.page = 1
        payload.limit = 1
        payload.filter = [dal.EqualsFilter(field="name", value=media_folder_name), dal.EqualsFilter(field="parentId", value=parent_id)]
        payload.includes = {"media_folder": ["configurationId"]}

        dict_response = self._admin_client.request_post(request_url="search/media-folder", payload=payload)
        try:
            media_folder_configuration_id = str(dict_response["data"][0]["configurationId"])
        except IndexError:
            raise FileNotFoundError(f'media folder with name "{media_folder_name}" not found')
        return media_folder_configuration_id

    # get_media_folder_configurations{{{
    def get_media_folder_configurations(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
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
        >>> my_l_dict_data = my_api.get_media_folder_configurations()
        """
        # get_media_folder_configurations}}}

        dict_response = self._admin_client.request_get_paginated(request_url="media-folder-configuration", payload=payload)
        l_dict_data = list(dict_response["data"])
        return l_dict_data

    # get_media_folder_id{{{
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
        # get_media_folder_id}}}
        payload: Dict[str, Any] = {"limit": "1", "page": "1"}  # noqa
        payload["filter"] = [{"type": "equals", "field": "name", "value": name}, {"type": "equals", "field": "parentId", "value": parent_id}]
        payload["includes"] = {"media_folder": ["id"]}
        response_dict = self._admin_client.request_post("search/media-folder", payload)
        try:
            media_folder_id = str(response_dict["data"][0]["id"])
        except IndexError:
            raise FileNotFoundError(f'media_folder, name: "{name}", parent_id: "{parent_id}" not found')
        return media_folder_id

    # get_media_folder_id_by_path{{{
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
        # get_media_folder_id_by_path}}}
        l_media_folder_names = self._get_media_folder_parts(path_media_folder=path_media_folder)
        media_folder_id = None
        parent_id: Optional[str] = None
        for media_folder_name in l_media_folder_names:
            try:
                media_folder_id = self.get_media_folder_id(name=media_folder_name, parent_id=parent_id)
            except FileNotFoundError:
                raise FileNotFoundError(f'media_folder path "{path_media_folder}" not found')
            parent_id = media_folder_id
        return media_folder_id

    # get_media_folders{{{
    def get_media_folders(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
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
        >>> my_l_dict_data = my_api.get_media_folders()
        """
        # get_media_folders}}}
        dict_response = self._admin_client.request_get_paginated(request_url="media-folder", payload=payload)
        l_dict_data = list(dict_response["data"])
        return l_dict_data

    # get_media_id_by_media_filename{{{
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
        # get_media_id_by_media_filename}}}

        media_filename_stem = str(pathlib.Path(media_filename).stem)
        media_filename_suffix = str(pathlib.Path(media_filename).suffix).lstrip(".")

        payload = dal.Criteria()
        payload.page = 1
        payload.limit = 1
        payload.filter = [dal.EqualsFilter(field="fileName", value=media_filename_stem), dal.EqualsFilter(field="fileExtension", value=media_filename_suffix)]
        payload.includes = {"media": ["id"]}
        try:
            media_id = str(self._admin_client.request_post("search/media", payload)["data"][0]["id"])
            return media_id
        except IndexError:
            raise FileNotFoundError(f'media_filename: "{media_filename_stem}.{media_filename_suffix}" not found')

    # get_medias{{{
    def get_medias(self, payload: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
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
        >>> my_l_dict_data = my_api.get_medias()
        """
        # get_medias}}}

        dict_response = self._admin_client.request_get_paginated(request_url="media", payload=payload)
        l_dict_data = list(dict_response["data"])
        return l_dict_data

    # insert_media{{{
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
        # insert_media}}}
        if not media_filename:
            media_filename = str(pathlib.Path(url).name)

        media_filename_stem = str(pathlib.Path(media_filename).stem)
        media_filename_suffix = str(pathlib.Path(media_filename).suffix).lstrip(".")

        media_id = self.calc_new_media_id(media_filename=media_filename)
        payload = {"mediaFolderId": media_folder_id, "id": media_id, "alt": media_alt_txt, "title": media_title}
        self._admin_client.request_post("media", payload)

        # upload the url to the article if needed
        if upload_media:
            self.upload_media_from_url(media_id=media_id, url=url, filename_suffix=media_filename_suffix, filename_stem=media_filename_stem)

        self.cache_clear_media()
        return media_id

    # insert_media_by_path{{{
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
        # insert_media_by_path}}}
        path_media_folder = pathlib.Path(path_media).parent
        media_filename = pathlib.Path(path_media).name
        media_folder_id = self.upsert_media_folders_by_path(path_media_folder=path_media_folder)
        media_id = self.insert_media(
            media_folder_id=media_folder_id, url=url, media_alt_txt=media_alt_txt, media_title=media_title, media_filename=media_filename
        )
        return media_id

    # insert_media_folder_by_name_and_parent_id{{{
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
        # insert_media_folder_by_name_and_parent_id}}}
        if configuration_id is None:
            configuration_id = self.get_media_folder_configuration_id_from_media_folder_id(media_folder_id=parent_id)
        payload = {"name": name, "parentId": parent_id, "configurationId": configuration_id}
        self._admin_client.request_post("media-folder", payload)
        self.cache_clear_media_folder()

    # is_media_existing{{{
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
        # is_media_existing}}}
        if not str(pathlib.Path(media_filename).suffix):
            raise ValueError(f'media "{media_filename}" does not have an extension')

        media_filename = str(pathlib.Path(media_filename).name)

        try:
            self.get_media_id_by_media_filename(media_filename=media_filename)
            return True
        except FileNotFoundError:
            return False

    # is_media_existing_by_media_id{{{
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
        # is_media_existing_by_media_id}}}
        payload = dal.Criteria()
        payload.limit = 1
        payload.page = 1
        payload.filter = [dal.EqualsFilter(field="id", value=media_id)]
        payload.includes = {"media": ["id"]}
        response_dict = self._admin_client.request_post("search/media", payload)
        l_data_dict = list(response_dict["data"])
        return bool(l_data_dict)

    # is_media_folder_containing_subfolders{{{
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
        # is_media_folder_containing_subfolders}}}
        payload = dal.Criteria()
        payload.limit = 1
        payload.page = 1
        payload.filter = [dal.EqualsFilter(field="parentId", value=media_folder_id)]
        payload.includes = {"media_folder": ["id"]}
        l_media = self.search_media_folders(payload=payload)
        is_subfolder = bool(l_media)
        if not is_subfolder:
            if not self.is_media_folder_existing(media_folder_id=media_folder_id):
                raise FileNotFoundError(f'media_folder id "{media_folder_id}" not found')
        return bool(l_media)

    # is_media_folder_empty{{{
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
        # is_media_folder_empty}}}

        if self.is_media_in_media_folder(media_folder_id=media_folder_id):
            return False
        if self.is_media_folder_containing_subfolders(media_folder_id=media_folder_id):
            return False
        return True

    # is_media_folder_empty_by_path{{{
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
        # is_media_folder_empty_by_path}}}
        media_folder_id = self.get_media_folder_id_by_path(path_media_folder=path_media_folder)  # type: ignore
        return self.is_media_folder_empty(media_folder_id=media_folder_id)

    # is_media_folder_existing{{{
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
        # is_media_folder_existing}}}
        payload = dal.Criteria()
        payload.limit = 1
        payload.page = 1
        payload.filter = [dal.EqualsFilter(field="id", value=media_folder_id)]
        payload.includes = {"media_folder": ["id"]}
        l_data_dict = self.search_media_folders(payload=payload)
        return bool(l_data_dict)

    # is_media_folder_existing_by_path{{{
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
        # is_media_folder_existing_by_path}}}
        try:
            self.get_media_folder_id_by_path(path_media_folder=path_media_folder)  # type: ignore
            return True
        except FileNotFoundError:
            return False

    # is_media_in_media_folder{{{
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
        # is_media_in_media_folder}}}

        payload = dal.Criteria()
        payload.page = 1
        payload.limit = 1
        payload.filter = [dal.EqualsFilter(field="mediaFolderId", value=media_folder_id)]
        payload.includes = {"media": ["id"]}
        try:
            response_dict = self._admin_client.request_post("search/media", payload)
            l_data_dict = list(response_dict["data"])
        except ShopwareAPIError:
            raise FileNotFoundError(f'media_folder id "{media_folder_id}" not found')
        return bool(l_data_dict)

    # search_media_folders{{{
    def search_media_folders(self, payload: PayLoad = None) -> List[Dict[str, Any]]:
        """
        get all the media folders

        >>> # Setup
        >>> my_api = Media()

        >>> # test
        >>> my_l_data_dict = my_api.search_media_folders()

        """
        # search_media_folders}}}
        if payload is None:
            payload = {}
        # response_dict = self.admin_client.request_post_paginated("search/media-folder", payload)
        response_dict = self._admin_client.request_post("search/media-folder", payload)
        l_dict_data = list(response_dict["data"])
        return l_dict_data

    # search_medias{{{
    def search_medias(self, payload: PayLoad = None) -> List[Dict[str, Any]]:
        """
        get all the media

        >>> # Setup
        >>> my_api = Media()

        >>> # insert article
        >>> ignore = my_api.search_medias()

        """
        # search_medias}}}
        response_dict = self._admin_client.request_post_paginated("search/media", payload)
        l_data_dict = list(response_dict["data"])
        return l_data_dict

    # update_media{{{
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
        # update_media}}}
        if not media_filename:
            media_filename = str(pathlib.Path(url).name)

        media_id = self.get_media_id_by_media_filename(media_filename=media_filename)
        media_filename_stem = str(pathlib.Path(media_filename).stem)
        media_filename_suffix = str(pathlib.Path(media_filename).suffix).lstrip(".")

        # update Media "mediaFolderId", "alt" and "title"
        payload = {"mediaFolderId": media_folder_id, "alt": media_alt_txt, "title": media_title}
        self._admin_client.request_patch(f"media/{media_id}", payload)

        # upload the url to the article
        if upload_media:
            self.upload_media_from_url(media_id=media_id, url=url, filename_suffix=media_filename_suffix, filename_stem=media_filename_stem)
        return media_id

    # upload_media_from_url{{{
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
        # upload_media_from_url}}}
        # upload the media via url
        filename_suffix = filename_suffix.lstrip(".")
        payload = {"url": url}
        self._admin_client.request_post(f"_action/media/{media_id}/upload?extension={filename_suffix}&fileName={filename_stem}", payload)

    # upsert_media{{{
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
        # upsert_media}}}
        media_filename = self.calc_media_filename_from_product_number(product_number=product_number, position=position, url=url)
        path_media_folder = self.calc_path_media_folder_from_product_number(product_number=product_number)
        media_folder_id = self.upsert_media_folders_by_path(path_media_folder=path_media_folder)

        if self.is_media_existing(media_filename=media_filename):
            media_id = self.update_media(
                media_folder_id=media_folder_id,
                url=url,
                media_alt_txt=media_alt,
                media_title=media_title,
                media_filename=media_filename,
                upload_media=upload_media,
            )
        else:
            media_id = self.insert_media(
                media_folder_id=media_folder_id,
                url=url,
                media_alt_txt=media_alt,
                media_title=media_title,
                media_filename=media_filename,
                upload_media=upload_media,
            )
        return media_id

    # upsert_media_folders_by_path{{{
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
        # upsert_media_folders_by_path}}}
        if configuration_id is None:
            configuration_id = self.get_media_folder_configuration_id_from_media_folder_name(media_folder_name="Product Media")

        l_media_folder_names = self._get_media_folder_parts(path_media_folder=path_media_folder)
        media_folder_id = None
        parent_id: Optional[str] = None
        for media_folder_name in l_media_folder_names:
            try:
                media_folder_id = self.get_media_folder_id(name=media_folder_name, parent_id=parent_id)
            except FileNotFoundError:
                self.insert_media_folder_by_name_and_parent_id(name=media_folder_name, parent_id=parent_id, configuration_id=configuration_id)
                media_folder_id = self.get_media_folder_id(name=media_folder_name, parent_id=parent_id)
            parent_id = media_folder_id
        return media_folder_id

    @staticmethod
    def _get_media_folder_parts(path_media_folder: PathMediaFolder) -> Tuple[str, ...]:
        """
        Provide the parts of the media folder: /Product Media/a000/000/000/test001_01.jpg --> ('Product Media','a000','000','000','test001_01.jpg')

        :param path_media_folder:
        :return: the parts of the path as tuple

        >>> # Setup
        >>> my_api = Media()

        >>> # test
        >>> my_api._get_media_folder_parts('/')
        ()
        >>> my_api._get_media_folder_parts('/Product Media/a000/000/000')
        ('Product Media', 'a000', '000', '000')
        >>> my_api._get_media_folder_parts('/Product Media/a000/000/000/test001_01.jpg')
        ('Product Media', 'a000', '000', '000', 'test001_01.jpg')

        >>> # Test Relative
        >>> my_api._get_media_folder_parts('a000/000/000')
        Traceback (most recent call last):
            ...
        OSError: media_folder path "a000/000/000" is invalid, it must be absolute

        """
        l_media_folder_parts = pathlib.Path(path_media_folder).parts
        anchor = l_media_folder_parts[0].replace("\\", "/")
        if not anchor == "/":
            raise OSError(f'media_folder path "{path_media_folder}" is invalid, it must be absolute')
        l_media_folder_parts = l_media_folder_parts[1:]
        return l_media_folder_parts
