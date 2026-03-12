"""
Google Drive tool functions.

This module encapsulates common Drive operations such as creating folders.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..google_auth import build_service
from .. import config


def create_folder(name: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
    """Create a folder in Google Drive.

    Args:
        name: Name of the folder.
        parent_id: Optional ID of the parent folder. If provided, the new
            folder will be created inside the given parent.

    Returns:
        The metadata of the created folder (id and name).
    """
    service = build_service("drive", "v3", config.SCOPES_MAP["drive"])
    metadata: Dict[str, Any] = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        metadata["parents"] = [parent_id]
    return service.files().create(body=metadata, fields="id,name").execute()


__all__ = ["create_folder"]