import environ
from .paths import BASE_DIR

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")
