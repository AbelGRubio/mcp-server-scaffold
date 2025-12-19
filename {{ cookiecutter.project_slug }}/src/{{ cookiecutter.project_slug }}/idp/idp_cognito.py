from typing import Any

from {{ cookiecutter.project_slug }}.idp.idp_adapter import IDPAdapter


class CognitoAdapter(IDPAdapter):
    algorithms = ["RS256"]

    def __init__(self, jwks_url: str, audience: str, issuer: str):
        key_jwks_url = issuer + "/.well-known/jwks.json"
        super().__init__(key_jwks_url, audience, issuer)

    def get_roles(self, payload: dict[str, Any]) -> set[str]:
        roles = payload.get("scope", "").replace("mcp-api/", "").split(" ")
        return set(roles)
