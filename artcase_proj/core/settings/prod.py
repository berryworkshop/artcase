from .base import *

DEBUG = False

ADMINS = [
    ('Allan', 'allan.berry@gmail.com'),
    ]

ALLOWED_HOSTS = [
    '.berryworkshop.com',
    '.allanberry.com',
    ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'artcase_db',
        'USER': 'artcase_admin',
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# should be moved to amazon?
STATIC_ROOT = '%s/static/' % BASE_DIR

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
