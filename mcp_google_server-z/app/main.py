"""
FastAPI application entrypoint for the Google Tools MCP server.

This module wires together the tool registry with a simple REST API. It
provides endpoints for health checks, a ping endpoint for warming up the
service, and endpoints to list and call the registered tools. The design
follows the pattern recommended by Render for hosting FastAPI apps: bind
to ``0.0.0.0`` and read the port from the ``PORT`` environment variable【406367926940681†L196-L200】.

Note:
    While the Model Context Protocol (MCP) specification defines a single
    streamable HTTP endpoint for remote servers【234112806764233†L109-L117】, this implementation retains
    separate ``/v1/tools`` and ``/v1/tools/call`` routes for simplicity and
    backwards compatibility. These routes return JSON responses that can
    easily be adapted into the JSON‑RPC style used by MCP clients.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from . import config
from .tools import registry


app = FastAPI(title="Google Tools MCP Server")


class CallToolRequest(BaseModel):
    """Schema for a tool call request body."""

    name: str
    arguments: Dict[str, Any] = {}


@app.get("/health", tags=["System"])
async def health() -> Dict[str, str]:
    """Health check endpoint.

    Returns a simple status dictionary to indicate the service is running.
    """
    return {"status": "ok"}


@app.get("/ping", tags=["System"])
async def ping() -> str:
    """Lightweight ping endpoint.

    Returns a plain text response that can be used to warm up the service
    before sending actual tool requests. On Render, free dynos may spin
    down after periods of inactivity; hitting this endpoint wakes the
    service without side effects.
    """
    return "ok"


@app.get("/v1/tools", tags=["Tools"])
async def list_tools() -> Dict[str, Dict[str, Any]]:
    """List available tools and their JSON schema definitions.

    Returns:
        A mapping of tool names to their descriptions and parameter schemas.
    """
    return registry.list_tools()


@app.post("/v1/tools/call", tags=["Tools"])
async def call_tool(request: CallToolRequest) -> Any:
    """Invoke a registered tool with the provided arguments.

    Args:
        request: Parsed request body containing the tool name and arguments.

    Returns:
        The result of executing the tool function. The format depends on the
        underlying Google API response.

    Raises:
        HTTPException: If the tool is not found or the call fails.
    """
    try:
        entry = registry.get_tool(request.name)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Tool '{request.name}' not found")
    func = entry["function"]
    # Execute the function in a thread pool to avoid blocking the event loop
    try:
        result = await asyncio.to_thread(func, **request.arguments)
    except Exception as exc:  # catch broad exceptions to surface errors
        # Wrap any exception into an HTTP 500 error for the client
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return result


# When this module is run directly (e.g. ``python -m mcp_google_server.app.main``)
# start the FastAPI server using uvicorn. This allows local testing via
# ``python -m mcp_google_server.app.main``. When deployed on Render, the
# service will run using the command provided in the Render dashboard.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "mcp_google_server.app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True,
    )