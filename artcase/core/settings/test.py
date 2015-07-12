from .base import *

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0'
]

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'
STATIC_ROOT =  PROJ_DIR.child('static')
STATICFILES_DIRS = (BASE_DIR.child('artcase').child('static'),)


MEDIA_URL = '/media/test/'
TEST_DATA = os.path.join(BASE_DIR, 'artcase/tests/test_data/')


MEDIA_ROOT =  PROJ_DIR.child('media')
#MEDIA_URL  = 'http://localhost:1917/media/'
UPLOAD_ROOT = MEDIA_ROOT + 'artcase/pictures/uploads/'

#email
EMAIL_HOST          = 'localhost'
EMAIL_PORT          = 1025
#EMAIL_HOST_USER     = '<mailbox>'
#EMAIL_HOST_PASSWORD = '<password>'
#DEFAULT_FROM_EMAIL  = '<address>'
#SERVER_EMAIL        = '<address>'
