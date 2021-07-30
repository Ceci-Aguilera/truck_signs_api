import django_heroku
# import dj-database-url
from .base import *


django_heroku.settings(locals())


DEBUG = False

SECRET_KEY= os.environ["SECRET_KEY"]

# db_from_env = dj_database_url.config()
# DATABASES["default"].update(db_from_env)

DEBUG = True

CORS_ALLOWED_ORIGINS = [
    "https://truck-signs-frontend-nextjs-4f1tbf3c3-ceci-aguilera.vercel.app",
    "https://truck-signs-frontend-nextjs.vercel.app",
    "https://truck-signs-frontend-nextjs-git-vercelpre-ceci-aguilera.vercel.app",
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ['CLOUD_NAME'],
    'API_KEY': os.environ['CLOUD_API_KEY'],
    'API_SECRET': os.environ['CLOUD_API_SECRET'],
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd2ogscp4tbudaf',
        'USER': 'eeklkdmvimbrcc',
        'PASSWORD': '969ab031e3af90c4b7260b1448cff4d80e786103c7485081b8f70c31b1ed58dc',
        'HOST': 'ec2-54-211-160-34.compute-1.amazonaws.com',
        'PORT': 5432,
    }
}

STRIPE_PUBLISHABLE_KEY=os.environ["STRIPE_PUBLISHABLE_KEY"]
STRIPE_SECRET_KEY=os.environ["STRIPE_SECRET_KEY"]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
