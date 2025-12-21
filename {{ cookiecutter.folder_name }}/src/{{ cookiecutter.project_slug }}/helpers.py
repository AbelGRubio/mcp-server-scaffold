from fastapi import Request
from fastapi.responses import PlainTextResponse
from toon_python import encode as toon_encode


# ----------------------------
# Helpers TOON
# ----------------------------
def toon_response(obj):
    """
    Docstring for toon_response

    :param obj: Description
    """
    return PlainTextResponse(toon_encode(obj), media_type="text/toon")


async def load_toon(request: Request):
    raw = await request.body()
    if not raw:
        return None
    return raw.decode()
