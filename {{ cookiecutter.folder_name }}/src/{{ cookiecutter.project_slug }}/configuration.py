import configparser
import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


__version__ = "{{ cookiecutter.version }}"



class Settings(BaseSettings):
    """
    Configuración global de la aplicación.
    Prioridad: 1. Variables de entorno → 2. Archivo .cfg → 3. Valores por defecto
    """
    model_config = SettingsConfigDict(
        env_file=".env",             
        env_file_encoding="utf-8",
        env_prefix="",             
        env_ignore_empty=True,
        case_sensitive=False,
        extra="ignore",
    )

    # Variables que se pueden sobreescribir por entorno o .cfg
    api_ip: str = Field(default="localhost", validation_alias="API_IP") 
    api_port: int = Field(default=5005, validation_alias="API_PORT")
    debug: bool = False

    cors_origins: List[str] = Field(default_factory=list)
    # Ejemplo de secreto (si lo necesitas en el futuro)
    # api_key: SecretStr = Field(default=None)

    idp_provider: str = Field(default='logto', validation_alias='IDP_PROVIDER')
    idp_url: str = Field(default='http://localhost:3001/oidc/jwks', validation_alias="IDP_URL")
    idp_audience: str = Field(default='mcp-client', validation_alias="IDP_AUDIENCE")
    idp_issuer: str = Field(default='http://localhost:3001/oidc', validation_alias="IDP_ISSUER")

    # Ruta al archivo de configuración
    conf_file: str = Field(default='./conf/config.cfg', validation_alias='CONF_FILE')

    def __init__(self, **data):
        super().__init__()

        # Leer el archivo .cfg solo si existe
        if os.path.exists(self.conf_file):
            parser = configparser.ConfigParser()
            parser.read(self.conf_file)

            # Actualizar valores desde el .cfg (si no fueron sobreescritos por env)
            self._update_from_ini(parser)

    def _update_from_ini(self, parser: configparser.ConfigParser):
        """Actualiza los atributos desde el archivo .cfg si no fueron seteados por entorno."""
        section = "conf"

        # CORS_ORIGINS
        if "cors_origins" in parser[section]:
            cors_str = parser[section]["cors_origins"].strip()
            if cors_str:
                self.cors_origins = [
                    origin.strip() for origin in cors_str.split(",") if origin.strip()
                ]

        # Puedes añadir más campos aquí según necesites

    @property
    def cors_origins_clean(self) -> List[str]:
        return [o.strip() for o in self.cors_origins if o.strip()]

    @property
    def api_base_url(self) -> str:
        return f"http://{self.api_ip}:{self.api_port}"


SETTINGS = Settings()
