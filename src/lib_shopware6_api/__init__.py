"""lib_shopware6_api — higher-level Shopware 6 API client built on lib_shopware6_api_base."""

from . import __init__conf__
from .lib_shopware6_api import Shopware6API
from .sub_currency import Currency
from .sub_delivery_time import DeliveryTime
from .sub_media import Media
from .sub_product import Product, ProductPicture
from .sub_tax import Tax
from .sub_unit import Unit

__title__ = __init__conf__.title
__version__ = __init__conf__.version
__url__ = __init__conf__.url
__author__ = __init__conf__.author
__author_email__ = __init__conf__.author_email
__shell_command__ = __init__conf__.shell_command

__all__ = [
    "Shopware6API",
    "Currency",
    "DeliveryTime",
    "Media",
    "Product",
    "ProductPicture",
    "Tax",
    "Unit",
]
