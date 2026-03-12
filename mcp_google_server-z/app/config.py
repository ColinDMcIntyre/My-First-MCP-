"""
Configuration handling for the Google Tools MCP server.

The server reads most of its configuration from environment variables to make
it easy to deploy to hosting providers like Render. Environment variables are
the recommended way to configure services on Render because they protect
sensitive values and allow different settings per environment【455002010100200†L181-L191】.

If a `.env` file is present in the project root it will be loaded automatically
for local development. When running on Render, you should instead set
environment variables via the Render dashboard as described in their
documentation【455002010100200†L204-L215】.

The following variables are recognised:

* ``GOOGLE_SERVICE_ACCOUNT_FILE`` – Absolute or relative path to a service
  account key JSON file. This file must be present in the container at runtime.
  You can upload the key as a secret file in the Render dashboard and set this
  variable to the path where it will be mounted (e.g. ``/etc/secrets/key.json``).
* ``GOOGLE_IMPERSONATED_USER`` – (Optional) An email address to impersonate
  when using domain‑wide delegation. Leave unset to use the service account
  identity directly.
* ``GOOGLE_SCOPES_SHEETS``, ``GOOGLE_SCOPES_DOCS``, ``GOOGLE_SCOPES_DRIVE``,
  ``GOOGLE_SCOPES_CALENDAR`` and ``GOOGLE_SCOPES_GMAIL`` – Space‑separated
  lists of OAuth scopes for each Google API. If unset, sensible defaults are
  used that allow basic operations on the respective service.
* ``HOST`` and ``PORT`` – Network interface and port to bind the FastAPI
  application. Render automatically injects ``PORT`` for you and recommends
  binding to ``0.0.0.0`` and ``$PORT`` in your start command【406367926940681†L196-L200】.

Do not hardcode sensitive values in your source code. Use environment
variables instead as described above.
"""

from __future__ import annotations

import os
from typing import Dict, List

try:
    # Attempt to load a .env file if present for local development. The
    # dependency is optional; if python-dotenv is not installed the call
    # simply does nothing.
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()  # noqa: E402  # load environment variables from .env file
except Exception:
    # If dotenv is not available, ignore and rely solely on os.environ.
    pass


def _split_scopes(value: str, default: List[str]) -> List[str]:
    """Split a space‑separated string of scopes into a list.

    Args:
        value: The raw environment variable string. May be ``None``.
        default: A default list to return if ``value`` is falsy.

    Returns:
        A list of scopes.
    """
    if not value:
        return default
    return [scope.strip() for scope in value.split() if scope.strip()]


# Path to the service account key. This must be provided either via the
# GOOGLE_SERVICE_ACCOUNT_FILE environment variable or by uploading a secret file
# to Render and setting the path here.
GOOGLE_SERVICE_ACCOUNT_FILE: str | None = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")

# Email address to impersonate when performing API calls. Only set this if
# domain‑wide delegation is configured. Otherwise the service account itself
# will be used.
GOOGLE_IMPERSONATED_USER: str | None = os.getenv("GOOGLE_IMPERSONATED_USER")

# Default OAuth scopes per service. These defaults enable common operations for
# each API. You can override them via the environment variables below.
_DEFAULT_SCOPES: Dict[str, List[str]] = {
    "sheets": ["https://www.googleapis.com/auth/spreadsheets"],
    "docs": ["https://www.googleapis.com/auth/documents"],
    "drive": ["https://www.googleapis.com/auth/drive"],
    "calendar": ["https://www.googleapis.com/auth/calendar"],
    "gmail": ["https://www.googleapis.com/auth/gmail.send"],
}

# Merge defaults with overrides from environment variables. Each list is built
# using a space‑separated environment variable. If not provided, the default
# list is used.
SCOPES_MAP: Dict[str, List[str]] = {
    "sheets": _split_scopes(os.getenv("GOOGLE_SCOPES_SHEETS", ""), _DEFAULT_SCOPES["sheets"]),
    "docs": _split_scopes(os.getenv("GOOGLE_SCOPES_DOCS", ""), _DEFAULT_SCOPES["docs"]),
    "drive": _split_scopes(os.getenv("GOOGLE_SCOPES_DRIVE", ""), _DEFAULT_SCOPES["drive"]),
    "calendar": _split_scopes(os.getenv("GOOGLE_SCOPES_CALENDAR", ""), _DEFAULT_SCOPES["calendar"]),
    "gmail": _split_scopes(os.getenv("GOOGLE_SCOPES_GMAIL", ""), _DEFAULT_SCOPES["gmail"]),
}

# Network interface and port. On Render, you should bind to 0.0.0.0 and use
# the provided $PORT environment variable【406367926940681†L196-L200】. For local development
# defaults are provided.
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))


__all__ = [
    "GOOGLE_SERVICE_ACCOUNT_FILE",
    "GOOGLE_IMPERSONATED_USER",
    "SCOPES_MAP",
    "HOST",
    "PORT",
]