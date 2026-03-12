# This package contains individual modules implementing actions for specific
# Google Workspace APIs. Keeping the implementations separate makes it easy to
# extend or modify behaviour without touching the core server or registry.

from .sheets import create_spreadsheet, read_sheet_values, append_sheet_values
from .docs import create_document
from .drive import create_folder
from .calendar import create_event
from .gmail import send_message

__all__ = [
    "create_spreadsheet",
    "read_sheet_values",
    "append_sheet_values",
    "create_document",
    "create_folder",
    "create_event",
    "send_message",
]