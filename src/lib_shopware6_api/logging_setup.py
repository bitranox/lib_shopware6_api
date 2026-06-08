"""Centralized ``lib_log_rich`` logging setup for the CLI entry point.

Why
    Library modules emit records through the standard library
    (``logging.getLogger(__name__)``) and must not configure logging themselves.
    The application entry point (the CLI) owns logging setup; this module is the
    single place that initializes the ``lib_log_rich`` runtime and bridges stdlib
    logging into it, so library log records are rendered consistently.

Notes
    Configuration overrides are read from ``LOG_*`` environment variables (and a
    local ``.env`` via :func:`lib_log_rich.config.enable_dotenv`). No external
    config schema is required, so this module deliberately avoids pulling in
    ``lib_layered_config`` — it is not needed for basic logging setup.
"""

from __future__ import annotations

import os

import lib_log_rich.config
import lib_log_rich.runtime

from . import __init__conf__

__all__ = ["init_logging", "shutdown_logging"]


def init_logging(console_level: str | None = None, environment: str | None = None) -> None:
    """Initialize the ``lib_log_rich`` runtime exactly once (idempotent).

    Args:
        console_level: Console log level (e.g. ``"info"``, ``"debug"``). Defaults
            to ``$LOG_CONSOLE_LEVEL`` or ``"info"``.
        environment: Deployment environment label. Defaults to
            ``$LOG_ENVIRONMENT`` or ``"prod"``.

    Side Effects:
        Loads ``.env`` into the process environment and initializes the global
        ``lib_log_rich`` runtime + stdlib-logging bridge on first call. Subsequent
        calls return immediately.
    """
    if lib_log_rich.runtime.is_initialised():
        return
    lib_log_rich.config.enable_dotenv()
    runtime_config = lib_log_rich.runtime.RuntimeConfig(
        service=__init__conf__.name,
        environment=environment or os.environ.get("LOG_ENVIRONMENT", "prod"),
        console_level=console_level or os.environ.get("LOG_CONSOLE_LEVEL", "info"),
    )
    lib_log_rich.runtime.init(runtime_config)
    lib_log_rich.runtime.attach_std_logging()


def shutdown_logging() -> None:
    """Flush and shut down the ``lib_log_rich`` runtime if it was initialized."""
    if lib_log_rich.runtime.is_initialised():
        lib_log_rich.runtime.shutdown()
