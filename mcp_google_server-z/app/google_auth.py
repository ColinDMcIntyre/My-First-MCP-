"""
Authentication helpers for Google APIs.

This module centralizes loading of service account credentials and creation
of Google API client service objects. Credentials are loaded using the
``google.oauth2.service_account`` module and automatically impersonate a user if
``GOOGLE_IMPERSONATED_USER`` is set in the configuration. The helper
functions here are reused by the individual tool implementations.
"""

from __future__ import annotations

from typing import List

from google.oauth2 import service_account  # type: ignore
from googleapiclient.discovery import build  # type: ignore

from . import config


def get_credentials(scopes: List[str]):
    """Load service account credentials for the given scopes.

    Args:
        scopes: A list of OAuth scopes required for the API call.

    Returns:
        A ``Credentials`` object suitable for passing to Google API clients.

    Raises:
        RuntimeError: If the service account file is not configured.
    """
    if not config.GOOGLE_SERVICE_ACCOUNT_FILE:
        raise RuntimeError(
            "GOOGLE_SERVICE_ACCOUNT_FILE environment variable is not set. "
            "Please configure it with the path to your service account key file."
        )
    creds = service_account.Credentials.from_service_account_file(
        config.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=scopes
    )
    # Optionally impersonate a user if domain‑wide delegation is set up.
    if config.GOOGLE_IMPERSONATED_USER:
        creds = creds.with_subject(config.GOOGLE_IMPERSONATED_USER)
    return creds


def build_service(service_name: str, version: str, scopes: List[str]):
    """Construct a Google API service client.

    Args:
        service_name: Short name of the service (e.g. 'sheets', 'drive').
        version: API version string (e.g. 'v4', 'v3').
        scopes: List of OAuth scopes required for the service.

    Returns:
        A resource object created via ``googleapiclient.discovery.build``.

    Note:
        Caching of discovery documents is disabled by default to prevent
        attempts to write to the package directory when running in ReadOnly
        environments like Render.
    """
    creds = get_credentials(scopes)
    return build(service_name, version, credentials=creds, cache_discovery=False)


__all__ = ["get_credentials", "build_service"]