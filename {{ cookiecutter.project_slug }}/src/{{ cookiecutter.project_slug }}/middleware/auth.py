from collections.abc import Sequence
from typing import Any

import mcp.types as mt
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware.middleware import (
    CallNext,
    Middleware,
    MiddlewareContext,
    T,
)
from fastmcp.tools.tool import Tool

from {{ cookiecutter.project_slug }}.idp.idp_adapter import IDPAdapter
from {{ cookiecutter.project_slug }}.idp.idp_factory import IDPFactory


class AuthMiddleware(Middleware):

    idp_factory = IDPFactory()

    def __init__(self):
        super().__init__()
        self.idp_adapter: IDPAdapter = (  # type ignore[annotation-unchecked]
            self.idp_factory.get_idp()
        )

    async def __call__(
        self,
        context: MiddlewareContext[T],
        call_next: CallNext[T, Any],
    ) -> Any:
        """Main entry point that orchestrates the pipeline."""
        token = self._get_token()

        payload = self.idp_adapter.get_payload(token)
        context.fastmcp_context._state["payload"] = payload  # type: ignore

        roles = self.idp_adapter.get_roles(payload)
        context.fastmcp_context._state["roles"] = roles  # type: ignore

        return await super().__call__(context, call_next)

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        # El MCP funciona sobre HTTP, así que los headers vienen en:
        #   context.request.headers
        tool_obj = context.message.name
        roles = context.fastmcp_context._state.get(  # type: ignore
            "roles", set()
        )

        tool = await context.fastmcp_context.fastmcp.get_tool(  # type: ignore
            tool_obj
        )

        tool_tags = tool.tags

        if tool_tags and not (tool_tags & roles):
            raise ToolError(f"Access denied: for tool tags {tool_tags}")

        # Ejecutar la tool
        return await call_next(context)

    async def on_list_tools(
        self,
        context: MiddlewareContext[mt.ListToolsRequest],
        call_next: CallNext[mt.ListToolsRequest, Sequence[Tool]],
    ) -> Sequence[Tool]:
        res = await call_next(context)
        roles = context.fastmcp_context._state.get(  # type: ignore
            "roles", set()
        )
        return self._access_tag(roles, res)

    @staticmethod
    def _access_tag(tags: set, tools: Sequence[Tool]) -> Sequence[Tool]:
        # Aquí puedes extraer los tags de acceso del token decodificado
        filtered = [t for t in tools if not t.tags or (t.tags & tags)]
        return filtered

    @staticmethod
    def _get_token() -> str:
        """
        Docstring for _get_token

        :return: Description
        :rtype: str
        """
        try:
            headers = get_http_headers()
            token = headers.get("authorization", "").replace("Bearer ", "")
        except Exception:
            raise ToolError("Error getting authorization header", 401)

        return token
