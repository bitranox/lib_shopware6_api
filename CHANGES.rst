Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

v2.0.6
---------
2023-11-13:
    - fix mypy error for PathLike

v2.0.5
---------
2023-07-14:
    - add codeql badge
    - move 3rd_party_stubs outside the src directory to ``./.3rd_party_stubs``
    - add pypy 3.10 tests
    - add python 3.12-dev tests

v2.0.4
---------
2023-07-13:
    - require minimum python 3.8
    - remove python 3.7 tests

v2.0.3
---------
2023-07-13:
    - introduce PEP517 packaging standard
    - introduce pyproject.toml build-system
    - remove setup.cfg
    - remove setup.py
    - update black config
    - clean ./tests/test_cli.py

v2.0.2.4
---------
2023-06-30:
    - update black config
    - remove travis config
    - remove bettercodehub config
    - do not upload .egg files to pypi.org
    - update github actions : checkout@v3 and setup-python@v6
    - remove "better code" badges
    - remove python 3.6 tests
    - adding python 3.11 tests
    - update pypy tests to 3.9

v2.0.2.3
---------
2022-06-30: specify correct "attr" version in requirements

v2.0.2.2
---------
2022-06-02: update to github actions checkout@v3 and setup-python@v6

v2.0.2.1
--------
2022-06-01: update github actions test matrix

v2.0.2
--------
2022-03-29: remedy mypy Untyped decorator makes function "cli_info" untyped

v2.0.1
--------
2022-01-19: update documentation, enhance coverage

v2.0.0
--------
2022-01-19: add function is_product_number_existing, add Unit functions, changed some method names

v1.0.2
--------
2022-01-18: clean requirements.txt

v1.0.1
--------
2022-01-18: Documentation update, make PyPi package

v1.0.0
--------
2022-01-17: Initial Release
