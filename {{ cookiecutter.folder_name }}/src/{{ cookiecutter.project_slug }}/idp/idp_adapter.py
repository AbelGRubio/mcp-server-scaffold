import os
from abc import ABC
from typing import Any, Callable

import jwt
from jwt import PyJWKClient


class IDPAdapter(ABC):
    """Interfaz base para adaptadores de IDP."""

    get_payload: Callable[[str], dict[str, Any]]

    algorithms = ["ES384"]

    def __init__(self, jwks_url: str, audience: str, issuer: str):
        self.jwks_url = jwks_url
        self.audience = audience
        self.issuer = issuer
        self.jwks_client = PyJWKClient(jwks_url)

        verify = os.environ.get("VERIFY_TOKEN", "true").lower() == "true"
        if verify:
            self.get_payload = self.get_payload_verified
        else:
            self.get_payload = self.get_payload_unverified

    def get_payload_unverified(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, options={"verify_signature": False})

    def get_payload_verified(self, token: str) -> dict[str, Any]:
        key = self._get_key(token)
        return jwt.decode(
            token,
            key,
            algorithms=self.algorithms,
            audience=self.audience,
            issuer=self.issuer,
        )

    def get_roles(self, payload: dict[str, Any]) -> set[str]:
        return set(payload.get("roles", []))

    def _get_key(self, token: str) -> Any:
        return self.jwks_client.get_signing_key_from_jwt(token).key
