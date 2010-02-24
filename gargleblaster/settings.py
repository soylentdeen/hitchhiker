
from os import path

root = path.dirname( path.abspath( __file__ ) )
FILESYSTEM_ROOT = root

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = path.join( root, 'gargleblaster.sqlite' )
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = False

SITE_ID = 1
SECRET_KEY = 'ux=#z677gb4tpd+5844mz6hyvars=9^74u+$n3k*#svm(avmna'

STATIC_ROOT = path.join( root, 'static' )
STATIC_URL = '/static/'
STATIC_SERVE_LOCALLY = False

MEDIA_ROOT = path.join( root, 'media' )
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin_media/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
    'gargleblaster.support.template.settings_processor',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'gargleblaster.urls'
TEMPLATE_DIRS = ( path.join( root, 'templates' ), )
EXPOSED_SETTINGS = ( 'MEDIA_URL', 'STATIC_URL' )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
)

try:
    from settings_local import *
except ImportError:
    pass

