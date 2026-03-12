"""
Gmail tool functions.

This module provides helper functions to send messages and interact with
Gmail. It uses the shared authentication helpers and scopes defined in
``config``. The send functions accept plain text and build the RFC 822
message appropriately.
"""

from __future__ import annotations

import base64
import email.mime.text
from typing import Any, Dict, List, Optional

from ..google_auth import build_service
from .. import config


def send_message(to: str, subject: str, body: str) -> Dict[str, Any]:
    """Send a simple plain‑text email via Gmail.

    Args:
        to: Recipient email address.
        subject: Subject line of the email.
        body: Body text of the email.

    Returns:
        The API response from the Gmail send call.
    """
    service = build_service("gmail", "v1", config.SCOPES_MAP["gmail"])
    message = email.mime.text.MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    # Encode the message in base64url as required by the Gmail API
    raw_bytes = base64.urlsafe_b64encode(message.as_bytes())
    raw_str = raw_bytes.decode("utf-8")
    return (
        service.users().messages().send(userId="me", body={"raw": raw_str}).execute()
    )


def list_messages(
    query: Optional[str] = None,
    max_results: int = 10,
    label_ids: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """List messages in the authenticated user's mailbox.

    Args:
        query: Optional Gmail search query string. Leave ``None`` to list all messages.
        max_results: Maximum number of messages to return. Defaults to 10.
        label_ids: Optional list of label IDs to filter messages.

    Returns:
        A dictionary containing the list of messages.
    """
    service = build_service("gmail", "v1", config.SCOPES_MAP["gmail"])
    list_call = service.users().messages().list(
        userId="me", q=query, maxResults=max_results, labelIds=label_ids
    )
    return list_call.execute()


def read_message(message_id: str, format: str = "full") -> Dict[str, Any]:
    """Retrieve a specific message by ID.

    Args:
        message_id: The ID of the Gmail message to read.
        format: The format of the returned message (e.g. 'full', 'metadata', 'raw').
            Defaults to 'full'.

    Returns:
        A dictionary containing the message details.
    """
    service = build_service("gmail", "v1", config.SCOPES_MAP["gmail"])
    return (
        service.users().messages().get(userId="me", id=message_id, format=format).execute()
    )


__all__ = ["send_message", "list_messages", "read_message"]