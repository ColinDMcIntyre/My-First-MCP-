"""
Google Docs tool functions.

This module contains helper functions for interacting with the Google Docs API.
"""

from __future__ import annotations

from typing import Any, Dict

from ..google_auth import build_service
from .. import config


def create_document(title: str) -> Dict[str, Any]:
    """Create a blank Google Doc with the given title.

    Args:
        title: The title of the new document.

    Returns:
        The API response containing the document metadata.
    """
    service = build_service("docs", "v1", config.SCOPES_MAP["docs"])
    body = {"title": title}
    return service.documents().create(body=body).execute()


__all__ = ["create_document"]