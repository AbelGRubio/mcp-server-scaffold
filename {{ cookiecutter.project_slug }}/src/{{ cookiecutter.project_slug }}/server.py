import os

from fastmcp import FastMCP

from {{ cookiecutter.project_slug }}.load_tools import load_tools
from {{ cookiecutter.project_slug }}.middleware.auth import AuthMiddleware


mcp = FastMCP(
    name="MCP + TOON + OAuth2 AuthCode",
)

if os.getenv("IS_PROD", "true") == "true":
    mcp.add_middleware(AuthMiddleware())


# ======================================================
#  TOOLS MCP
# ======================================================
for tool in load_tools():
    mcp.add_tool(tool)
