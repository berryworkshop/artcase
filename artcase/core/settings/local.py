from .base import *

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0'
]

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'
STATIC_ROOT =  PROJ_DIR.child('static')

MEDIA_URL  = '/media/'
MEDIA_ROOT =  '/Users/aljabear/Projects/cellini_2015/media'

#MEDIA_URL  = 'http://localhost:1917/media/'
UPLOAD_ROOT = MEDIA_ROOT + 'artcase/pictures/uploads/'

#email
EMAIL_HOST          = 'localhost'
EMAIL_PORT          = 1025
#EMAIL_HOST_USER     = '<mailbox>'
#EMAIL_HOST_PASSWORD = '<password>'
#DEFAULT_FROM_EMAIL  = '<address>'
#SERVER_EMAIL        = '<address>'
