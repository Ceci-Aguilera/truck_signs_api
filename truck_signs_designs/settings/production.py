import django_heroku
import dj-database-url
from .base import *

DEBUG = False

# SECRET_KEY= env("SECRET_KEY")

db_from_env = dj_database_url.config()
DATABASES["default"].update(db_from_env)


# STRIPE_PUBLISHABLE_KEY=env("STRIPE_PUBLISHABLE_KEY")
# STRIPE_SECRET_KEY=env("STRIPE_SECRET_KEY")
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = env("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

django_heroku.settings(locals())