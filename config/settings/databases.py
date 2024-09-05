from .environ import env

DATABASES = {"default": env.db_url("DJANGO_DB_URL", "sqlite:///db.sqlite3")}
