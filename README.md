# lib_shopware6_api

<!-- Badges -->
[![CI](https://github.com/bitranox/lib_shopware6_api/actions/workflows/cicd_docker.yml/badge.svg)](https://github.com/bitranox/lib_shopware6_api/actions/workflows/cicd_docker.yml)
[![CodeQL](https://github.com/bitranox/lib_shopware6_api/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/bitranox/lib_shopware6_api/actions/workflows/codeql-analysis.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?logo=github&logoColor=white&style=flat-square)](https://codespaces.new/bitranox/lib_shopware6_api?quickstart=1)
[![PyPI](https://img.shields.io/pypi/v/lib_shopware6_api.svg)](https://pypi.org/project/lib_shopware6_api/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/lib_shopware6_api.svg)](https://pypi.org/project/lib_shopware6_api/)
[![Code Style: Ruff](https://img.shields.io/badge/Code%20Style-Ruff-46A3FF?logo=ruff&labelColor=000)](https://docs.astral.sh/ruff/)
[![codecov](https://codecov.io/gh/bitranox/lib_shopware6_api/graph/badge.svg)](https://codecov.io/gh/bitranox/lib_shopware6_api)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

A higher-level Python API client for Shopware 6, built on top of
[lib_shopware6_api_base](https://github.com/bitranox/lib_shopware6_api_base).

It wraps the raw Admin API in convenient, task-oriented helpers for currencies,
delivery times, media, products, taxes and units — including media-folder
management, product-picture upserts and id/number lookups with caching. It is
also a good starting point for your own API client functions, ready to be
extended further.

**Python 3.10+** required.

---

## Table of Contents

- [Configuration](#configuration)
- [Quick Start](#quick-start)
- [API Usage](#api-usage)
  - [Currency](#currency)
  - [DeliveryTime](#deliverytime)
  - [Tax](#tax)
  - [Unit](#unit)
  - [Media](#media)
  - [Product](#product)
- [CLI Usage](#cli-usage)
- [Installation](#installation)
- [Development](#development)
- [Requirements](#requirements)
- [Changelog](CHANGELOG.md)
- [License](#license)

---

## Configuration

Authentication and endpoints are configured through `lib_shopware6_api_base`'s
`ConfShopware6ApiBase` (Pydantic-based). It reads its settings from environment
variables or a `.env` file, all using the `SHOPWARE_` prefix.

Copy `example.env` to `.env` and adjust the values for your shop:

```bash
# API Endpoints
SHOPWARE_ADMIN_API_URL="https://shop.example.com/api"
SHOPWARE_STOREFRONT_API_URL="https://shop.example.com/store-api"

# OAuth2 Security (set to "1" only for local HTTP development)
SHOPWARE_INSECURE_TRANSPORT="0"

# Resource Owner Grant (for automation/CLI - no refresh tokens)
SHOPWARE_CLIENT_ID="SWIAXXXXXXXXXXXXXXXXXXXX"
SHOPWARE_CLIENT_SECRET="your-integration-secret"

# Grant type: USER_CREDENTIALS or RESOURCE_OWNER
SHOPWARE_GRANT_TYPE="RESOURCE_OWNER"
```

| Variable                           | Description             | Example                                |
|------------------------------------|-------------------------|----------------------------------------|
| `SHOPWARE_ADMIN_API_URL`           | Admin API endpoint      | `https://shop.example.com/api`         |
| `SHOPWARE_STOREFRONT_API_URL`      | Storefront API endpoint | `https://shop.example.com/store-api`   |
| `SHOPWARE_INSECURE_TRANSPORT`      | Allow HTTP (dev only)   | `0` (production) or `1` (dev)          |
| `SHOPWARE_USERNAME`                | Admin user email        | `admin@example.com`                    |
| `SHOPWARE_PASSWORD`                | Admin user password     | `secret`                               |
| `SHOPWARE_CLIENT_ID`               | Integration Access ID   | `SWIA...`                              |
| `SHOPWARE_CLIENT_SECRET`           | Integration Secret      | `...`                                  |
| `SHOPWARE_GRANT_TYPE`              | Auth method             | `USER_CREDENTIALS` or `RESOURCE_OWNER` |
| `SHOPWARE_STORE_API_SW_ACCESS_KEY` | Storefront access key   | `SWSC...`                              |

See the [base library's configuration docs](https://github.com/bitranox/lib_shopware6_api_base#configuration)
for the full reference and for loading helpers such as `load_config_from_env()`.

---

## Quick Start

`Shopware6API` is the facade. It builds one shared admin client and exposes the
domain helpers as attributes:

```python
from lib_shopware6_api import Shopware6API
from lib_shopware6_api_base import ConfShopware6ApiBase

# uses ConfShopware6ApiBase from the environment / .env by default
api = Shopware6API()

# or pass an explicit config
api = Shopware6API(config=ConfShopware6ApiBase(...))

api.currency       # currency helpers
api.delivery_time  # delivery-time helpers
api.media          # media + media-folder helpers
api.product        # product helpers
api.tax            # tax helpers
api.unit           # unit helpers
```

Each helper can also be instantiated on its own (`Currency()`, `Product()`, …),
in which case it creates its own admin client from the same config.

---

## API Usage

### Currency

```python
from lib_shopware6_api import Shopware6API

api = Shopware6API()

# resolve a currency id by ISO code (cached) — raises FileNotFoundError if missing
currency_id = api.currency.get_currency_id_by_iso_code("EUR")

# fetch all currency records (paginated automatically); pass a payload to filter
currencies = api.currency.get_currencies()

# clear the lookup cache after inserting/deleting currencies
api.currency.get_currency_id_by_iso_code.cache_clear()
```

### DeliveryTime

```python
api = Shopware6API()

# all delivery-time records (paginated)
delivery_times = api.delivery_time.get_delivery_times()

# search via a base-lib Criteria/dict payload
results = api.delivery_time.search_delivery_times()

# [{'name': ..., 'id': ..., 'position': 10}, ...] sorted by minimum days
sorted_times = api.delivery_time.get_delivery_times_sorted_by_min_days()

# clear caches after inserting/deleting delivery-time records
api.delivery_time.cache_clear_delivery_time()
```

### Tax

```python
from decimal import Decimal

api = Shopware6API()

# resolve a tax id / rate by name (cached) — defaults to "Standard rate"
tax_id = api.tax.get_tax_id_by_name("Standard rate")
tax_rate = api.tax.get_tax_rate_by_name("Standard rate")   # e.g. Decimal('19.00')

# all tax records (paginated)
taxes = api.tax.get_taxes()

# clear caches after inserting/deleting tax records
api.tax.cache_clear_tax()
```

### Unit

```python
api = Shopware6API()

# all unit records (paginated, cached)
units = api.unit.get_units()

# search via a payload
results = api.unit.search_units()

# clear caches after inserting/deleting units
api.unit.cache_clear_unit()
```

### Media

The `Media` helper manages media records and the media-folder tree. Folders are
created on demand; media ids are derived deterministically from the filename, so
the same file always maps to the same id.

```python
api = Shopware6API()

# create the media-folder tree for a path (returns the leaf folder id)
folder_id = api.media.upsert_media_folders_by_path("/Product Media/my_folder")

# insert a media record into a folder from a URL
media_id = api.media.insert_media(
    media_folder_id=folder_id,
    url="https://example.com/picture_1280.jpg",
)

# insert by target path (folders auto-created from the path)
media_id = api.media.insert_media_by_path(
    path_media="/Product Media/my_folder/picture_01.jpg",
    url="https://example.com/picture_1280.jpg",
)

# insert-or-update a product picture by product_number + position
media_id = api.media.upsert_media(
    product_number="123456789",
    position=1,
    url="https://example.com/picture_1280.jpg",
)

# lookups and existence checks
media_id = api.media.get_media_id_by_media_filename("picture_01.jpg")
exists = api.media.is_media_existing("picture_01.jpg")

# delete a media record, or remove a whole folder (force deletes content)
api.media.delete_media_by_id(media_id)
api.media.delete_media_folder_by_path("/Product Media/my_folder", force=True)
```

### Product

`ProductPicture` is the input model for picture upserts:

```python
from lib_shopware6_api.sub_product import ProductPicture

ProductPicture(
    position=10,                 # sort order in the shop; lowest position = cover
    url="https://example.com/picture_01_1280.jpg",
    media_alt="alt text",        # optional
    media_title="title",         # optional
    upload_media=True,           # optional, default True
)
```

```python
from decimal import Decimal
from lib_shopware6_api import Shopware6API
from lib_shopware6_api.sub_product import ProductPicture

api = Shopware6API()

# create a product (price_netto is derived from price_brutto + tax when 0.00)
product_id = api.product.insert_product(
    name="My Product",
    product_number="my-product-001",
    price_brutto=Decimal("100.00"),
    stock=0,
    tax_name="Standard rate",
    currency_iso_code="EUR",
)

# id/number lookups
product_id = api.product.get_product_id_by_product_number("my-product-001")
exists = api.product.is_product_number_existing("my-product-001")

# fetch products / product-media (paginated)
products = api.product.get_products()
product_medias = api.product.get_product_medias()

# upsert product pictures — first by position becomes the cover picture
pictures = [
    ProductPicture(position=10, url="https://example.com/pic_01_1280.jpg"),
    ProductPicture(position=20, url="https://example.com/pic_02_1280.jpg"),
]
api.product.upsert_product_pictures(
    product_number="my-product-001",
    l_product_pictures=pictures,
)

# remove all product-media relations of a product (keeps the media itself)
api.product.delete_product_media_relations_by_product_number("my-product-001")

# delete the product (cascades to its product-media relations)
api.product.delete_product_by_id(product_id)
```

> The `Product` helper exposes its own `.currency`, `.tax` and `.media`
> sub-clients, all sharing the same admin client.

---

## CLI Usage

```
Usage: lib_shopware6_api [OPTIONS] COMMAND [ARGS]...

  use the shopware 6 api

Options:
  --version                     Show the version and exit.
  --traceback / --no-traceback  return traceback information on cli
  -h, --help                    Show this message and exit.

Commands:
  info  get program information
```

---

## Installation

### Via uv (recommended)

```bash
# One-shot run
uvx lib_shopware6_api --help

# Install as CLI tool
uv tool install lib_shopware6_api

# Install as dependency
uv pip install lib_shopware6_api
```

### Via pip

```bash
pip install lib_shopware6_api
```

---

## Development

Project automation runs through a `Makefile` that delegates to
[`bmk`](https://pypi.org/project/bmk/) (installed automatically as a persistent
`uv` tool on first use). Run `make help` to list all targets.

### Running tests

```bash
make test               # lint (ruff), type-check (pyright), import-linter,
                        # bandit, pip-audit, and the unit test suite with coverage
make testintegration    # integration tests only (see prerequisites below)
```

`make test` runs the full quality gate but **excludes** the integration tests
(`pytest -m "not integration"`). `make testintegration` runs **only** the
integration suite (`pytest -m integration`).

### Integration tests

The integration tests exercise the higher-level helpers against a real Shopware
instance using the [dockware](https://developer.shopware.com/docs/guides/installation/dockware)
container. The test harness starts and stops the container automatically — no
manual setup or credentials are required.

Prerequisites:

- **Docker** installed and running, with a **Linux** container engine
  (`docker info --format '{{.OSType}}'` → `linux`). If Docker is unavailable or
  not Linux, the integration tests are **skipped** (not failed).
- **Port 80** free — the container is published on `-p 80:80`.
- First run pulls `dockware/dev:latest` (a few GB), so it takes a while.

Tip: for fast repeated runs, start the container once and leave it up — the
harness reuses a running container (and only tears down one it started itself):

```bash
docker run -d --rm -p 80:80 --name dockware dockware/dev:latest
make testintegration    # reuses the running container, finishes in seconds
```

---

## Requirements

Automatically installed dependencies:

- `lib_shopware6_api_base` - the base API client (config, Admin/Storefront clients, Criteria/DAL)
- `pydantic>=2.0.0` - data models (e.g. `ProductPicture`)
- `rich-click` - CLI
- `lib_cli_exit_tools` - CLI utilities
- `lib_log_rich` - structured logging

---

## License

[MIT License](http://en.wikipedia.org/wiki/MIT_License)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
