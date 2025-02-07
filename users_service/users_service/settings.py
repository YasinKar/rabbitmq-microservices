from settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('USERS_POSTGRES_NAME'),
        'USER': os.environ.get('USERS_POSTGRES_USER'),
        'PASSWORD': os.environ.get('USERS_POSTGRES_PASSWORD'),
        'HOST': os.environ.get('USERS_POSTGRES_HOST'),
        'PORT': os.environ.get('USERS_POSTGRES_PORT'),
    },
}
INSTALLED_APPS += [
    'api',
]