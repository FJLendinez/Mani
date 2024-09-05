# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
from .paths import BASE_DIR

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static", BASE_DIR / "components"]
STATIC_ROOT = "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
