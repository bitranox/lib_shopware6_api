"""Static package metadata surfaced to CLI commands and documentation.

Purpose
-------
Expose the current project metadata as simple constants. These values are kept
in sync with ``pyproject.toml`` by development automation (tests, push
pipelines), so runtime code does not query packaging metadata.
"""

from __future__ import annotations

import sys

#: Distribution name declared in ``pyproject.toml``.
name = "lib_shopware6_api"
#: Human-readable summary shown in CLI help output.
title = "python3 higher-level API client for shopware6"
#: Current release version pulled from ``pyproject.toml`` by automation.
version = "3.0.1"
#: Repository homepage presented to users.
url = "https://github.com/bitranox/lib_shopware6_api"
#: Author attribution surfaced in CLI output.
author = "bitranox"
#: Contact email surfaced in CLI output.
author_email = "bitranox@gmail.com"
#: Console-script name published by the package.
shell_command = "lib_shopware6_api"


def print_info() -> None:
    """Print the summarised metadata block used by the CLI ``info`` command.

    Examples
    --------
    >>> print_info()  # doctest: +ELLIPSIS
    Info for lib_shopware6_api:
    ...
    """
    fields = [
        ("name", name),
        ("title", title),
        ("version", version),
        ("url", url),
        ("author", author),
        ("author_email", author_email),
        ("shell_command", shell_command),
    ]
    pad = max(len(label) for label, _ in fields)
    lines = [f"Info for {name}:", ""]
    lines.extend(f"    {label.ljust(pad)} = {value}" for label, value in fields)
    sys.stdout.write("\n".join(lines) + "\n")
