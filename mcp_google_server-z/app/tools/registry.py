"""
Registry of available tools for the MCP server.

This module defines a mapping between fully qualified tool names and their
Python callables, descriptions and JSON schema definitions. The MCP server
uses this registry to advertise available tools and to dispatch calls at
runtime. When adding a new tool function to the ``tools`` package, you must
also register it here with an appropriate name and JSON schema.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, TypedDict

from . import sheets, docs, drive, calendar, gmail


class ToolEntry(TypedDict):
    """Structure describing a tool entry in the registry."""

    function: Callable[..., Any]
    description: str
    parameters: Dict[str, Any]


def _build_tools() -> Dict[str, ToolEntry]:
    """Construct the registry dictionary for all tools.

    Returns:
        A mapping from tool name to its function, description and parameter schema.
    """
    return {
        # Sheets API tools
        "sheets.create_spreadsheet": {
            "function": sheets.create_spreadsheet,
            "description": "Create a new Google Sheets spreadsheet with the given title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the new spreadsheet.",
                    },
                },
                "required": ["title"],
                "additionalProperties": False,
            },
        },
        "sheets.read_sheet_values": {
            "function": sheets.read_sheet_values,
            "description": "Read values from a specified range in a Google Sheet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The ID of the spreadsheet to read from.",
                    },
                    "range": {
                        "type": "string",
                        "description": "The A1 notation of the range to read (e.g. 'Sheet1!A1:B10').",
                    },
                },
                "required": ["spreadsheet_id", "range"],
                "additionalProperties": False,
            },
        },
        "sheets.append_sheet_values": {
            "function": sheets.append_sheet_values,
            "description": "Append rows of values to a sheet in Google Sheets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The ID of the spreadsheet to append values to.",
                    },
                    "range": {
                        "type": "string",
                        "description": "The A1 notation of the range to append values to (e.g. 'Sheet1!A1').",
                    },
                    "values": {
                        "type": "array",
                        "description": "A list of rows to append; each row is itself a list of cell values.",
                        "items": {
                            "type": "array",
                            "items": {"type": ["string", "number", "null"]},
                        },
                    },
                    "value_input_option": {
                        "type": "string",
                        "enum": ["RAW", "USER_ENTERED"],
                        "description": "How the input data should be interpreted. Defaults to 'RAW'.",
                    },
                },
                "required": ["spreadsheet_id", "range", "values"],
                "additionalProperties": False,
            },
        },
        # Docs API tools
        "docs.create_document": {
            "function": docs.create_document,
            "description": "Create a new Google Doc with the specified title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the new document.",
                    }
                },
                "required": ["title"],
                "additionalProperties": False,
            },
        },
        # Drive API tools
        "drive.create_folder": {
            "function": drive.create_folder,
            "description": "Create a folder in Google Drive. Optionally specify a parent folder ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the folder to create.",
                    },
                    "parent_id": {
                        "type": "string",
                        "description": "Optional ID of the parent folder.",
                    },
                },
                "required": ["name"],
                "additionalProperties": False,
            },
        },
        # Calendar API tools
        "calendar.create_event": {
            "function": calendar.create_event,
            "description": "Create a new event on the primary calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Short summary or title of the event.",
                    },
                    "start_datetime": {
                        "type": "string",
                        "description": "ISO 8601 timestamp for when the event starts (e.g. '2025-01-01T09:00:00').",
                    },
                    "end_datetime": {
                        "type": "string",
                        "description": "ISO 8601 timestamp for when the event ends.",
                    },
                    "timezone": {
                        "type": "string",
                        "description": "Time zone of the event (e.g. 'America/Los_Angeles').",
                    },
                    "attendees": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of attendee email addresses (optional).",
                    },
                    "location": {
                        "type": "string",
                        "description": "Physical or virtual location of the event (optional).",
                    },
                    "description": {
                        "type": "string",
                        "description": "Longer description of the event (optional).",
                    },
                },
                "required": ["summary", "start_datetime", "end_datetime", "timezone"],
                "additionalProperties": False,
            },
        },
        "calendar.list_events": {
            "function": calendar.list_events,
            "description": "List upcoming events on a calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "calendar_id": {
                        "type": "string",
                        "description": "The calendar ID to list events from. Defaults to 'primary'.",
                    },
                    "time_min": {
                        "type": "string",
                        "description": "ISO 8601 timestamp marking the start of the time window (optional).",
                    },
                    "time_max": {
                        "type": "string",
                        "description": "ISO 8601 timestamp marking the end of the time window (optional).",
                    },
                    "max_results": {
                        "type": "number",
                        "description": "Maximum number of events to return. Defaults to 10.",
                    },
                    "single_events": {
                        "type": "boolean",
                        "description": "Expand recurring events into single instances. Defaults to true.",
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
        # Gmail API tools
        "gmail.send_message": {
            "function": gmail.send_message,
            "description": "Send a plain‑text email via Gmail.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "Recipient email address.",
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject line of the email.",
                    },
                    "body": {
                        "type": "string",
                        "description": "Body text of the email.",
                    },
                },
                "required": ["to", "subject", "body"],
                "additionalProperties": False,
            },
        },
        "gmail.list_messages": {
            "function": gmail.list_messages,
            "description": "List messages from the authenticated user's mailbox.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Gmail search query string (optional).",
                    },
                    "max_results": {
                        "type": "number",
                        "description": "Maximum number of messages to return (optional).",
                    },
                    "label_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of label IDs to filter messages by (optional).",
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
        "gmail.read_message": {
            "function": gmail.read_message,
            "description": "Retrieve a specific Gmail message by ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message_id": {
                        "type": "string",
                        "description": "The ID of the Gmail message to read.",
                    },
                    "format": {
                        "type": "string",
                        "description": "The format of the returned message (e.g. 'full', 'metadata', 'raw').",
                    },
                },
                "required": ["message_id"],
                "additionalProperties": False,
            },
        },
    }


# Build the tool mapping once at import time. Exporting a static dictionary
# avoids re-generating the schema on every request.
TOOLS: Dict[str, ToolEntry] = _build_tools()


def list_tools() -> Dict[str, Dict[str, Any]]:
    """Return a view of available tools without the function objects.

    Returns:
        A mapping of tool names to their description and parameter schema. The
        function itself is omitted in this view.
    """
    return {
        name: {"description": entry["description"], "parameters": entry["parameters"]}
        for name, entry in TOOLS.items()
    }


def get_tool(name: str) -> ToolEntry:
    """Retrieve a tool entry by name.

    Args:
        name: The fully qualified tool name (e.g. ``'sheets.create_spreadsheet'``).

    Returns:
        The corresponding ToolEntry structure.

    Raises:
        KeyError: If the tool name is not registered.
    """
    return TOOLS[name]


__all__ = ["TOOLS", "list_tools", "get_tool"]