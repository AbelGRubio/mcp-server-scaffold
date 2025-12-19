from {{ cookiecutter.project_slug }}.idp.idp_adapter import IDPAdapter


class AuthentikAdapter(IDPAdapter):
    algorithms = ["RS256"]
