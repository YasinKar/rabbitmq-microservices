from settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('ORDERS_POSTGRES_NAME'),
        'USER': os.environ.get('ORDERS_POSTGRES_USER'),
        'PASSWORD': os.environ.get('ORDERS_POSTGRES_PASSWORD'),
        'HOST': os.environ.get('ORDERS_POSTGRES_HOST'),
        'PORT': os.environ.get('ORDERS_POSTGRES_PORT'),
    },
}
INSTALLED_APPS += [
    'api',
]