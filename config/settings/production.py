from .base import *  # noqa

# TODO: as soon as the project goes to production fix allowed hosts
SERVER_IP = os.environ.get("13.233.123.235")
ALLOWED_HOSTS = ["*"]
DEBUG = True
