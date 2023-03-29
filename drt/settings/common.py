# -*- coding: utf-8 -*-

import sys
import os
import datetime
from os.path import abspath, basename, dirname, join, normpath
from sys import path

from path import Path


##################################################################
# Application configuration
##################################################################

# The ID of the current site in the django_site database table.
SITE_ID = 1

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
    )

# Directories
PROJECT_DIR = Path(__file__).abspath().realpath().dirname().parent
PROJECT_NAME = PROJECT_DIR.basename()
SITE_DIR = PROJECT_DIR.parent
APPS_DIR = PROJECT_DIR / 'apps'
LIBS_DIR = PROJECT_DIR / 'libs'

# Append directories to sys.path
sys.path.append(SITE_DIR)
sys.path.append(APPS_DIR)
sys.path.append(LIBS_DIR)

# Root URLs module
ROOT_URLCONF = 'drt.urls'

# WSGI application
WSGI_APPLICATION = 'drt.wsgi.application'

# Secret key
# This is used to provide cryptographic signing, and should be set
# to a unique, unpredictable value.
SECRET_KEY = 'WJ62giCN9p3gpYkOaNHSf67OTq8YYKUummPXdUVt'

##################################################################
# Language and timezone settings
##################################################################

# Specifies whether Django’s translation system should be enabled.
USE_I18N = True

# Specifies if localized formatting of data will be enabled by
# default or not.
USE_L10N = True

# Specifies if datetimes will be timezone-aware by default or not.
USE_TZ = True

# A string representing the time zone for this installation.
TIME_ZONE = 'America/Chicago'

# A string representing the language code for this installation.
LANGUAGE_CODE = 'en'

##################################################################
# Authentication settings
##################################################################

# The model to use to represent a User.
# AUTH_USER_MODEL = 'auth.User'
# SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL = 'users.User'

# The URL where requests are redirected for login.
LOGIN_URL = '/accounts/login/'

# The URL where requests are redirected for logout.
LOGOUT_URL = '/accounts/logout/'

# The URL where requests are redirected after login.
LOGIN_REDIRECT_URL = '/accounts/profile/'

##################################################################
# Middleware settings
##################################################################

# The default number of seconds to cache a page when the caching
# middleware or cache_page() decorator is used.
CACHE_MIDDLEWARE_SECONDS = 5

# The cache key prefix that the cache middleware should use.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_NAME + '_'

# A tuple of middleware classes to use.
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

##################################################################
# Static settings
##################################################################

# The absolute path to the directory where collectstatic will
# collect static files for deployment.

STATIC_ROOT = os.path.join(PROJECT_DIR, 'assets')

# URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = '/static/'

# Additional locations the staticfiles app will traverse if the
# FileSystemFinder finder is enabled.
STATICFILES_DIRS = (
    PROJECT_DIR / 'static',
)

BOWER_COMPONENTS_ROOT = normpath(join(PROJECT_DIR, 'static', 'vendor'))
# The list of finder backends that know how to find static files
# in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_assets.finders.AssetsFinder',
    'djangobower.finders.BowerFinder',
)

# AWS keys
AWS_ACCESS_KEY_ID = 'AKIAI4IOEUFRQSK6VKXQ'
AWS_STORAGE_BUCKET_NAME = 'drt-resources'
AWS_SECRET_ACCESS_KEY = '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'

S3DIRECT_REGION = 'us-east-1'

S3DIRECT_DESTINATIONS = {
    # Allow anybody to upload any MIME type
    'audio': {
        'key': 'uploads/audio',
        'acl': 'public-read',
        'allowed': [
            'audio/mpeg3',
            'audio/x-mpeg-3',
            'video/mpeg',
            'video/x-mpeg',
            'audio/mp3',
            'audio/mpeg',
            'audio/x-mpeg',
            'audio/x-mp3',
            'audio/x-mpeg3',
            'audio/mpg',
            'audio/x-mpg',
            'audio/x-mpegaudio',
        ],
    },
    # Limit uploads to jpeg's and png's.
    'image': {
        'key': 'uploads/images',
        'acl': 'public-read',
        'allowed': ['image/jpeg', 'image/png'],
    },
}

########## EMAIL CONFIGURATION
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
# EMAIL_HOST_USER = 'AKIAJBMUUDMSHGZZLN5Q'
# EMAIL_HOST_PASSWORD = 'AtcvS52cTziIFp7XvkZjPFevUhoXLKSlp4PNb+m9psoe'
# EMAIL_PORT = 25
# EMAIL_USE_TLS = True
# SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'Codeberry Inc <support@codeberry.io>'
########## END EMAIL CONFIGURATION

##################################################################
# Templates settings
##################################################################

# List of locations of the template source files.
TEMPLATE_DIRS = (
    PROJECT_DIR / 'templates',
)

# A tuple of template loader classes, specified as strings.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# A tuple of callables that are used to populate the context in
# RequestContext.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

##################################################################
# Installed apps
##################################################################

EXTERNAL_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'robots',
    # Other external apps
    'rest_framework',
    'djangobower',
    'rest_framework_swagger',
    'django_assets',
    's3direct',
    'xmltodict',
    'django_user_agents',
    'admin_reorder',
    'ordered_model'
)

INTERNAL_APPS = (
    # Application specific apps
    # 'authentication',
    'main',
    'post',
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = False
REGISTRATION_API_ACTIVATION_SUCCESS_URL = '/'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Simeon Iliev', 'simeon@codeberry.io'),
    ('Petar Krivoshiev', 'petar@codeberry.io'),
    ('Atanas Mahony', 'atanas@codeberry.io'),
)
DEFAULT_FROM_EMAIL = ADMINS[0][1][2]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION

####################################
# BOWER APPS
####################################

BOWER_INSTALLED_APPS = (
    'jquery#1.9',
    'angular',
    'angular-cookies',
    'angular-resource',
    'angular-ui-router',
    'angular-sanitize',
    'angular-animate',
    'lodash',
    'underscore',
    'restangular',
    'angular-svg-base-fix',
    'angular-soundmanager2',
    'sroze/ngInfiniteScroll#6fbf4b41947f9a3023b4aba0e613231950ccc4a1',
    'https://github.com/micku7zu/vanilla-tilt.js.git#1.4.0',
    'ngtweet',
    'slick-carousel',
    'angular-slick-carousel',
    'plyr'
)

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=14)
}
