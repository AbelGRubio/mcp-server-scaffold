import configparser
import os

__version__ = "{{ cookiecutter.version }}"


conf_file = os.getenv("CONF_FILE", "./conf/config.cfg")

config = configparser.ConfigParser()
config.read(conf_file)

cors_ = config.get("conf", "cors_origins", fallback="").split(",")
CORS_ORIGINS = [c_ for c_ in cors_ if c_ != ""]

API_IP = os.getenv("API_IP", "localhost")
API_PORT = int(os.getenv("API_PORT", 5005))

