from typing import Any, Dict, Set

import jwt

from {{ cookiecutter.project_slug }}.idp.idp_adapter import IDPAdapter


class KeycloakAdapter(IDPAdapter):
    algorithms = ["RS256"]

    def __init__(self, jwks_url: str, audience: str, issuer: str):
        key_jwks_url = (
            jwks_url + f"/realms/{issuer}/protocol/openid-connect/certs"
        )
        key_audience = audience
        self._audience = audience
        key_issuer = f"{jwks_url}/realms/{issuer}"
        super().__init__(key_jwks_url, key_audience, key_issuer)

    def get_roles(self, payload: Dict[str, Any]) -> Set[str]:
        return set(
            payload.get("resource_access", {})
            .get(self.audience, {})
            .get("roles", [])
        )

    def get_payload_verified(self, token):
        """Keycloak sometimes uses 'account' as audience."""
        try:
            key = self._get_key(token)
            return jwt.decode(
                token,
                key,
                algorithms=self.algorithms,
                audience="account",
                issuer=self.issuer,
            )
        except Exception:
            return super().get_payload_verified(token)
