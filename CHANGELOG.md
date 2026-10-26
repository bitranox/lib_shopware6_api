# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- The test suite no longer reads the app and host configuration layers of the machine it runs on. An
  autouse fixture points lib_layered_config's three app-root variables (`LIB_LAYERED_CONFIG_ETC`,
  `_MAC_APP_ROOT`, `_PROGRAMDATA`) at an empty directory under `tmp_path`, so a system-wide deploy
  (for example a `/etc/xdg/<slug>/config.d/99-*.toml`) can no longer fail tests locally while CI
  stays green.

## [3.0.4] 2026-10-15 16:36:41

### Fixed

- The source distribution ships only the package, its tests, `README.md`, `LICENSE`,
  `CHANGELOG.md` and `pyproject.toml` (an include list). Earlier sdists also carried every other
  root file and, in a local build, anything hidden only through `.git/info/exclude` or a nested
  `.gitignore`. `tests/test_packaging.py` builds the sdist and wheel and checks both; `hatchling`
  joins the dev extra for it.

### Tests

- The `os_posix` marker now skips a test on Windows, like `os_windows`, `os_macos` and `os_linux`
  already did off their platforms; it was registered but wired to nothing, so a test trusting it ran on
  Windows. `tests/test_platform_markers.py` pins all four.

## [3.0.3] 2026-10-13 15:49:53

### Added
- Python 3.15 is a supported version: declared in the classifiers, so CI and `make test-all` run it.
- `uv.lock` is committed, and `[tool.uv] exclude-newer` sets a cooldown that keeps releases younger
  than it out of the lock. CI installs exactly the locked tree on push and pull request; the nightly
  scheduled run still resolves afresh to catch upstream breakage early.

### Changed
- The install section explains why installing with uv protects against supply-chain attacks and why
  a plain `pip install` from PyPI does not.
- `rtoml` floor raised to 0.14.0, the first release with Python 3.15 wheels.

## [3.0.2] 2026-07-24 13:07:30

### Fixed
- `PLR0917` (too many positional arguments) on `Media.insert_media`, `Media.update_media`,
  `Media.upsert_media`, and `Product.insert_product`, newly enforced by latest ruff: made the
  trailing parameters keyword-only (`*,`). All call sites already passed these by keyword, so
  no call-site changes were needed.

### Changed
- Removed the blanket `ignore = [RUF002, RUF022, PLC0415, TC001, TC002, TC003, TC006]` list from
  `[tool.ruff.lint]` and fixed each rule at the root instead of suppressing it:
  - `RUF022`: re-sorted `__all__` in `src/lib_shopware6_api/__init__.py`.
  - `PLC0415` (deferred imports) only occurred in `tests/`, a deliberate idiom there (exercising
    import/cache behaviour); added it to the existing `tests/**/*.py` per-file-ignore instead of
    a blanket repo-wide ignore.
  - `RUF002`/`TC001`/`TC002`/`TC003`/`TC006` had zero remaining hits under latest ruff.
- Added `[tool.ruff.lint.flake8-type-checking] runtime-evaluated-base-classes = ["pydantic.BaseModel"]`
  so pydantic model fields are not moved into `TYPE_CHECKING`-only imports by TC0xx autofixes.

## [3.0.1] 2026-06-14

### Changed
- Added a `typed_click.py` facade wrapping rich-click's `option` / `version_option` / `argument` decorators behind explicit, fully-known signatures, keeping the CLI strict-clean under pyright 1.1.410 (`reportUnknownMemberType`) without disabling the rule (ignore isolated to the facade).
- Bumped internal dependency floors: `lib_cli_exit_tools>=2.3.2`, `lib_log_rich>=6.3.5`, `lib_shopware6_api_base>=6.0.2`.

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
