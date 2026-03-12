"""
Google Calendar tool functions.

This module contains helpers to create and read calendar events. Each helper
uses the shared authentication from ``google_auth.py`` and the scopes
configured in the ``config`` module. These functions wrap the Google
Calendar API for easy consumption by the MCP server.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..google_auth import build_service
from .. import config


def create_event(
    summary: str,
    start_datetime: str,
    end_datetime: str,
    timezone: str,
    attendees: Optional[List[str]] = None,
    location: Optional[str] = None,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a calendar event on the primary calendar.

    Args:
        summary: A short summary or title for the event.
        start_datetime: ISO 8601 timestamp for the event start (e.g. ``2025-01-01T09:00:00``).
        end_datetime: ISO 8601 timestamp for the event end.
        timezone: IANA time zone string (e.g. ``America/Los_Angeles``).
        attendees: Optional list of attendee email addresses.
        location: Optional event location.
        description: Optional longer description of the event.

    Returns:
        The API response containing the created event's metadata.
    """
    service = build_service("calendar", "v3", config.SCOPES_MAP["calendar"])
    event: Dict[str, Any] = {
        "summary": summary,
        "start": {"dateTime": start_datetime, "timeZone": timezone},
        "end": {"dateTime": end_datetime, "timeZone": timezone},
    }
    if attendees:
        event["attendees"] = [{"email": email} for email in attendees]
    if location:
        event["location"] = location
    if description:
        event["description"] = description
    return service.events().insert(calendarId="primary", body=event).execute()


def list_events(
    calendar_id: str = "primary",
    time_min: Optional[str] = None,
    time_max: Optional[str] = None,
    max_results: int = 10,
    single_events: bool = True,
) -> Dict[str, Any]:
    """List upcoming events on a calendar.

    Args:
        calendar_id: The calendar ID to list events from. Defaults to ``"primary"``.
        time_min: ISO 8601 timestamp representing the start of the time window. If provided, only events
            occurring after this time are returned.
        time_max: ISO 8601 timestamp representing the end of the time window. If provided, only events
            occurring before this time are returned.
        max_results: Maximum number of events to return. Defaults to 10.
        single_events: Whether to expand recurring events into single instances. Defaults to True.

    Returns:
        A dictionary containing the events list.
    """
    service = build_service("calendar", "v3", config.SCOPES_MAP["calendar"])
    events_call = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=single_events,
            orderBy="startTime",
        )
    )
    return events_call.execute()


__all__ = ["create_event", "list_events"]