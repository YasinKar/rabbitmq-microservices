from settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PRODUCTS_POSTGRES_NAME'),
        'USER': os.environ.get('PRODUCTS_POSTGRES_USER'),
        'PASSWORD': os.environ.get('PRODUCTS_POSTGRES_PASSWORD'),
        'HOST': os.environ.get('PRODUCTS_POSTGRES_HOST'),
        'PORT': os.environ.get('PRODUCTS_POSTGRES_PORT'),
    },
}
INSTALLED_APPS += [
    'api',
]