from unipath import Path
from .base import *

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'cellini.allanberry.webfactional.com',
    'cellini.berryworkshop.com'
]

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'
STATIC_ROOT =  BASE_DIR.ancestor(3).child('cellini_static')

MEDIA_URL  = '/media/'
MEDIA_ROOT =  STATIC_ROOT.child('media')

#MEDIA_URL  = 'http://localhost:1917/media/'
UPLOAD_ROOT = MEDIA_ROOT + 'artcase/pictures/uploads/'

#email
EMAIL_HOST          = 'localhost'
EMAIL_PORT          = 1025

#EMAIL_HOST_USER     = '<mailbox>'
#EMAIL_HOST_PASSWORD = '<password>'
#DEFAULT_FROM_EMAIL  = '<address>'
#SERVER_EMAIL        = '<address>'
