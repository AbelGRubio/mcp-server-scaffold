import json
from typing import Any

from {{ cookiecutter.project_slug }}.idp.idp_adapter import IDPAdapter


class LogtoAdapter(IDPAdapter):
    algorithms = ["ES384"]

    try:
        with open("roles.json", "r", encoding="utf-8") as f:
            ROLES = json.load(f)
    except Exception:
        ROLES = []

    def get_roles(self, payload: dict[str, Any]) -> set[str]:
        client_id = payload.get("client_id", "")
        rol = next(
            (c["name"] for c in self.ROLES if c["client_id"] == client_id),
            None,
        )
        return set(payload.get("roles", [rol]))
