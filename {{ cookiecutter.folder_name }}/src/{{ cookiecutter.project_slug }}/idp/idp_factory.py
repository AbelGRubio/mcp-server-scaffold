import os

from {{ cookiecutter.project_slug }}.idp.authentik_adapter import AuthentikAdapter
from {{ cookiecutter.project_slug }}.idp.idp_adapter import IDPAdapter
from {{ cookiecutter.project_slug }}.idp.idp_cognito import CognitoAdapter
from {{ cookiecutter.project_slug }}.idp.keycloak_adapter import KeycloakAdapter
from {{ cookiecutter.project_slug }}.idp.logto_adapter import LogtoAdapter
from {{ cookiecutter.project_slug }}.configuration import SETTINGS

class IDPFactory:
    @staticmethod
    def get_idp() -> IDPAdapter:
        provider = SETTINGS.idp_provider.lower()
        print(f"\n\nUsing IDP provider: {provider}\n\n")

        idps_ = {
            "keycloak": KeycloakAdapter,
            "logto": LogtoAdapter,
            "authentik": AuthentikAdapter,
            "cognito": CognitoAdapter,
        }

        idp_adapter = idps_.get(provider, None)

        if not idp_adapter:
            raise ValueError(f"Unknown IDP provider: {provider}")

        return idp_adapter(
            jwks_url=SETTINGS.idp_url,
            audience=SETTINGS.idp_audience,
            issuer=SETTINGS.idp_issuer,
        )
