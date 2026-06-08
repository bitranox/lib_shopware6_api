# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-06-08

Complete overhaul aligning the project with its sibling
[lib_shopware6_api_base](https://github.com/bitranox/lib_shopware6_api_base).

### Changed

- **Project layout**: migrated to the `src/` layout (`src/lib_shopware6_api/`);
  minimum Python raised to **3.10+**.
- **Build system**: switched to [hatchling](https://hatch.pypa.io/) (from setuptools).
- **Tooling**: quality gate is now `ruff` (lint/format), `pyright` (types),
  `import-linter`, `bandit` and `pip-audit`, all driven by the standard BMK
  `Makefile` (`make test`, `make testintegration`, `make push`, `make release`,
  `make bump-*`). Replaces the previous flake8/black/mypy setup.
- **CI**: adopted the CI/CD workflows from `lib_shopware6_api_base` (unit and
  dockware integration suites across Linux/macOS/Windows for Python 3.10-3.14).
- **Docs**: documentation converted from reStructuredText to Markdown
  (`README.md`, `CHANGELOG.md`); added a "Development" section and an
  `example.env`.

### Added

- Unit test suite plus a dockware-backed integration test suite (the harness
  auto-starts/stops the container; integration tests are skipped when Docker is
  unavailable).
- The source doctests are wired into the suite via `tests/test_doctests.py`
  (`doctest.testmod`): the offline doctests run in `make test`, the resource
  doctests (Currency / Tax / Unit / DeliveryTime / Product / Media) run against
  dockware in `make testintegration`.

### Fixed

- **CLI no longer swallows error messages.** The custom `run_cli` exception
  handler returned an exit code but never printed, so a failing command (missing
  config, API error, bad argument) exited non-zero with no diagnostic. Non-signal
  errors now print their message (terse, or a full traceback under `--traceback`);
  signals still exit cleanly and quietly. `main()` also snapshots and restores the
  process-global `--traceback` state so it cannot leak across invocations.
- **Media upload against base >= 6.0.0**: `Media.upload_media_from_url` passed
  `extension` / `fileName` as a query string inlined into the endpoint path. The
  base client now validates the path and rejects `?`, `=` and `&`, which broke
  every media upload; the parameters are now passed via `additional_query_params`.
- A `Product.get_product_id_by_product_number` doctest still subscripted the
  admin response with `["data"]`; updated to `.data` for the `ShopwareApiResponse`
  envelope introduced by base 6.0.0.

### Removed

- Swapped `cli_exit_tools` -> `lib_cli_exit_tools` and `coloredlogs` -> `lib_log_rich`.
- Dropped `attrs` (the `ProductPicture` data class is now a Pydantic model) and
  `lib_detect_testenv`.
- Removed obsolete scaffolding: `README.rst`, `CHANGES.rst`, `.flake8`,
  `.coveragerc`, `MANIFEST.in`, `requirements.txt`, `requirements_test.txt`,
  and the `.3rd_party_stubs/` mypy stub directory.

## [2.0.6] - 2023-11-13

- Fix mypy error for `PathLike`.

## [2.0.5] - 2023-07-14

- Add CodeQL badge; add pypy 3.10 and python 3.12-dev tests.
- Move `3rd_party_stubs` outside the `src` directory to `./.3rd_party_stubs`.

## [2.0.4] - 2023-07-13

- Require minimum Python 3.8; remove Python 3.7 tests.

## [2.0.3] - 2023-07-13

- Adopt PEP 517 packaging and a `pyproject.toml` build system; remove
  `setup.cfg` and `setup.py`.

## [2.0.2] - 2023-06-30

- Tooling/CI maintenance: update GitHub Actions, drop travis/bettercodehub
  configs, add Python 3.11 tests, update pypy tests to 3.9.

## [2.0.1] - 2022-01-19

- Documentation update; enhance coverage.

## [2.0.0] - 2022-01-19

- Add `is_product_number_existing`, add `Unit` functions, rename some methods.

## [1.0.2] - 2022-01-18

- Clean `requirements.txt`.

## [1.0.1] - 2022-01-18

- Documentation update; first PyPI package.

## [1.0.0] - 2022-01-17

- Initial release.
