"""
Google Sheets tool functions.

These functions wrap common Sheets API operations behind simple Python
functions. Each helper uses the shared authentication helpers from
``google_auth.py`` and uses the scopes defined in the config module.
"""

from __future__ import annotations

from typing import Any, Dict, List

from ..google_auth import build_service
from .. import config


def create_spreadsheet(title: str) -> Dict[str, Any]:
    """Create a new Google Sheets spreadsheet.

    Args:
        title: Title of the spreadsheet.

    Returns:
        Metadata for the created spreadsheet as returned by the API.
    """
    service = build_service("sheets", "v4", config.SCOPES_MAP["sheets"])
    body = {"properties": {"title": title}}
    return service.spreadsheets().create(body=body).execute()


def read_sheet_values(spreadsheet_id: str, range: str) -> Dict[str, Any]:
    """Read values from a specified range in a sheet.

    Args:
        spreadsheet_id: The ID of the target spreadsheet.
        range: A1 notation of the range to read (e.g. 'Sheet1!A1:B10').

    Returns:
        The API response containing the values.
    """
    service = build_service("sheets", "v4", config.SCOPES_MAP["sheets"])
    return service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range).execute()


def append_sheet_values(
    spreadsheet_id: str,
    range: str,
    values: List[List[Any]],
    value_input_option: str = "RAW",
) -> Dict[str, Any]:
    """Append a 2D array of values to a sheet.

    Args:
        spreadsheet_id: The ID of the target spreadsheet.
        range: A1 notation of the range to append to (e.g. 'Sheet1!A1').
        values: A list of rows, each row itself a list of cell values.
        value_input_option: 'RAW' or 'USER_ENTERED'. Defaults to 'RAW'.

    Returns:
        The API response for the append operation.
    """
    service = build_service("sheets", "v4", config.SCOPES_MAP["sheets"])
    body = {"values": values}
    return (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=range,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )


__all__ = [
    "create_spreadsheet",
    "read_sheet_values",
    "append_sheet_values",
]