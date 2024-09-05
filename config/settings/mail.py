from config.settings.environ import env

#  Email config based on URL
#  https://django-environ.readthedocs.io/en/latest/types.html#environ-env-email-url
EMAIL_CONFIG = env.email_url("DJANGO_EMAIL_URL", default="filemail://./emails/")

SERVER_EMAIL = '' # Changeit
DEFAULT_FROM_EMAIL = '' # Changeit

vars().update(EMAIL_CONFIG)
