import json

from fastapi import HTTPException, Request
from fastmcp.server.middleware import Middleware

from {{ cookiecutter.project_slug }}.helpers import toon_response


class ToonMiddleware(Middleware):
    """
    Middleware para:
    1) Decodificar TOON → Python a nivel de request
    2) Convertir JSON → TOON en las respuestas
    """

    def __init__(self):
        super().__init__()

    async def dispatch(self, request: Request, call_next):
        # Entrada: TOON → Python
        if request.headers.get("content-type") == "text/toon":
            body = await request.body()
            try:
                request.state.toon = body.decode()
            except Exception:
                raise HTTPException(400, "TOON decode error")

        response = await call_next(request)

        # Salida: JSON → TOON
        if response.media_type == "application/json":
            body = await request.body()
            data = json.loads(body.decode())
            return toon_response(data)

        return response
