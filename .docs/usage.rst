Overview
========

- `API`_
- `Currency`_
- `DeliveryTime`_
- `Media`_
- `Product`_
- `Tax`_
- `Unit`_

-------------------

API
===
back to `Overview`_

.. include:: ../lib_shopware6_api/lib_shopware6_api.py
    :code: python
    :start-after: # Shopware6API{{{
    :end-before:  # Shopware6API}}}

Currency
========
back to `Overview`_

.. include:: ../lib_shopware6_api/sub_currency.py
    :code: python
    :start-after: # Currency{{{
    :end-before:  # Currency}}}

.. include:: ../lib_shopware6_api/sub_currency.py
    :code: python
    :start-after: # get_currency_id_by_iso_code{{{
    :end-before:  # get_currency_id_by_iso_code}}}

.. include:: ../lib_shopware6_api/sub_currency.py
    :code: python
    :start-after: # get_currencies{{{
    :end-before:  # get_currencies}}}

DeliveryTime
============
back to `Overview`_

.. include:: ../lib_shopware6_api/sub_delivery_time.py
    :code: python
    :start-after: # DeliveryTime{{{
    :end-before:  # DeliveryTime}}}

.. include:: ../lib_shopware6_api/sub_delivery_time.py
    :code: python
    :start-after: # cache_clear_delivery_time{{{
    :end-before:  # cache_clear_delivery_time}}}

.. include:: ../lib_shopware6_api/sub_delivery_time.py
    :code: python
    :start-after: # get_delivery_times{{{
    :end-before:  # get_delivery_times}}}

.. include:: ../lib_shopware6_api/sub_delivery_time.py
    :code: python
    :start-after: # search_delivery_times{{{
    :end-before:  # search_delivery_times}}}

.. include:: ../lib_shopware6_api/sub_delivery_time.py
    :code: python
    :start-after: # get_delivery_times_sorted_by_min_days{{{
    :end-before:  # get_delivery_times_sorted_by_min_days}}}

Media
=====
back to `Overview`_

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # Media{{{
    :end-before:  # Media}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # cache_clear_media{{{
    :end-before:  # cache_clear_media}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # cache_clear_media_folder{{{
    :end-before:  # cache_clear_media_folder}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # calc_media_filename_from_product_number{{{
    :end-before:  # calc_media_filename_from_product_number}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # calc_new_media_id{{{
    :end-before:  # calc_new_media_id}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # calc_path_media_folder_from_product_number{{{
    :end-before:  # calc_path_media_folder_from_product_number}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # delete_media_by_id{{{
    :end-before:  # delete_media_by_id}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # delete_media_folder{{{
    :end-before:  # delete_media_folder}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # delete_media_folder_by_path{{{
    :end-before:  # delete_media_folder_by_path}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # get_media_folder_configuration_id_from_media_folder_name{{{
    :end-before:  # get_media_folder_configuration_id_from_media_folder_name}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # get_media_folder_configurations{{{
    :end-before:  # get_media_folder_configurations}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # get_media_folder_id{{{
    :end-before:  # get_media_folder_id}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # get_media_folder_id_by_path{{{
    :end-before:  # get_media_folder_id_by_path}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # get_media_folders{{{
    :end-before:  # get_media_folders}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # get_media_id_by_media_filename{{{
    :end-before:  # get_media_id_by_media_filename}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # get_medias{{{
    :end-before:  # get_medias}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # insert_media{{{
    :end-before:  # insert_media}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # insert_media_by_path{{{
    :end-before:  # insert_media_by_path}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # insert_media_folder_by_name_and_parent_id{{{
    :end-before:  # insert_media_folder_by_name_and_parent_id}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # is_media_existing{{{
    :end-before:  # is_media_existing}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # is_media_existing_by_media_id{{{
    :end-before:  # is_media_existing_by_media_id}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # is_media_folder_containing_subfolders{{{
    :end-before:  # is_media_folder_containing_subfolders}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # is_media_folder_empty{{{
    :end-before:  # is_media_folder_empty}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # is_media_folder_empty_by_path{{{
    :end-before:  # is_media_folder_empty_by_path}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # is_media_folder_existing{{{
    :end-before:  # is_media_folder_existing}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # is_media_folder_existing_by_path{{{
    :end-before:  # is_media_folder_existing_by_path}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # is_media_in_media_folder{{{
    :end-before:  # is_media_in_media_folder}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # search_media_folders{{{
    :end-before:  # search_media_folders}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # search_medias{{{
    :end-before:  # search_medias}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # update_media{{{
    :end-before:  # update_media}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # upload_media_from_url{{{
    :end-before:  # upload_media_from_url}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # upsert_media{{{
    :end-before:  # upsert_media}}}

.. include:: ../lib_shopware6_api/sub_media.py
    :code: python
    :start-after: # upsert_media_folders_by_path{{{
    :end-before:  # upsert_media_folders_by_path}}}

Product
=======
back to `Overview`_

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # ProductPicture{{{
    :end-before:  # ProductPicture}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # Product{{{
    :end-before:  # Product}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # calc_new_product_id{{{
    :end-before:  # calc_new_product_id}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # calc_new_product_media_id{{{
    :end-before:  # calc_new_product_media_id}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # cache_clear_product{{{
    :end-before:  # cache_clear_product}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # delete_product_by_id{{{
    :end-before:  # delete_product_by_id}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # get_product_id_by_product_number{{{
    :end-before:  # get_product_id_by_product_number}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # delete_product_media_relation_by_id{{{
    :end-before:  # delete_product_media_relation_by_id}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # delete_product_media_relations_by_product_number{{{
    :end-before:  # delete_product_media_relations_by_product_number}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # get_product_medias{{{
    :end-before:  # get_product_medias}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # get_products{{{
    :end-before:  # get_products}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # insert_product{{{
    :end-before:  # insert_product}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # upsert_product_payload{{{
    :end-before:  # upsert_product_payload}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # insert_product_media_relation{{{
    :end-before:  # insert_product_media_relation}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # is_media_used_in_product_media{{{
    :end-before:  # is_media_used_in_product_media}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # is_product_number_existing{{{
    :end-before:  # is_product_number_existing}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # search_product_medias{{{
    :end-before:  # search_product_medias}}}

.. include:: ../lib_shopware6_api/sub_product.py
    :code: python
    :start-after: # upsert_product_pictures{{{
    :end-before:  # upsert_product_pictures}}}

Tax
===
back to `Overview`_

.. include:: ../lib_shopware6_api/sub_tax.py
    :code: python
    :start-after: # Tax{{{
    :end-before:  # Tax}}}

.. include:: ../lib_shopware6_api/sub_tax.py
    :code: python
    :start-after: # cache_clear_tax{{{
    :end-before:  # cache_clear_tax}}}

.. include:: ../lib_shopware6_api/sub_tax.py
    :code: python
    :start-after: # get_tax_id_by_name{{{
    :end-before:  # get_tax_id_by_name}}}

.. include:: ../lib_shopware6_api/sub_tax.py
    :code: python
    :start-after: # get_taxes{{{
    :end-before:  # get_taxes}}}

.. include:: ../lib_shopware6_api/sub_tax.py
    :code: python
    :start-after: # get_tax_rate_by_name{{{
    :end-before:  # get_tax_rate_by_name}}}

Unit
========
back to `Overview`_

.. include:: ../lib_shopware6_api/sub_unit.py
    :code: python
    :start-after: # Unit{{{
    :end-before:  # Unit}}}

.. include:: ../lib_shopware6_api/sub_unit.py
    :code: python
    :start-after: # cache_clear_unit{{{
    :end-before:  # cache_clear_unit}}}

.. include:: ../lib_shopware6_api/sub_unit.py
    :code: python
    :start-after: # get_units{{{
    :end-before:  # get_units}}}

.. include:: ../lib_shopware6_api/sub_unit.py
    :code: python
    :start-after: # search_units{{{
    :end-before:  # search_units}}}
