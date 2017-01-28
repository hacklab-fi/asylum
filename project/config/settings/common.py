# -*- coding: utf-8 -*-
"""
Django settings for asylum project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import os.path

import django.template.defaultfilters
import environ
# Monkeypatch djangos own slugify with Mozilla teams Unicode-aware one
import slugify as unicodeslugify
from django.utils.translation import ugettext_lazy as _

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path('asylum')

env = environ.Env()
# If the project root contains a .env file, read it
if os.path.isfile(str(ROOT_DIR + '.env')):
    environ.Env.read_env(str(ROOT_DIR + '.env'))

django.template.defaultfilters.slugify = lambda x: unicodeslugify.slugify(x, only_ascii=True, lower=True, spaces=False)

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'crispy_forms',  # Form layouts
    'bootstrap3',
    'reversion',
    'rest_framework',
    'rest_framework.authtoken',
    'django_markdown',
    'django_jinja',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    # Your stuff: custom apps go here
    'asylum',
    'members',
    'access',
    'creditor',
    'ndaparser',
    'holviapp',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    # Make sure djangosecure.middleware.SecurityMiddleware is listed first
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'asylum.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = []

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ("""Hacklab.fi""", 'info@hacklab.fi'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db("DATABASE_URL", default="postgres:///asylum"),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Helsinki'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'fi-FI'

LANGUAGES = (
    ('fi', _('Finnish')),
    ('en', _('English')),
)


# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
_TEMPLATE_CONTEXT_PROCESSORS = [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    # Your stuff: custom template context processors go here
    'django_settings_export.settings_export',
]

TEMPLATES = [
    {
        'BACKEND': "django_jinja.backend.Jinja2",
        'APP_DIRS': False,
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            'match_extension': '.jinja',
            'context_processors': _TEMPLATE_CONTEXT_PROCESSORS,
            'newstyle_gettext': True
        }
    },
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'APP_DIRS': False,
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'asylum.apptemplateloader.NameSpacedLoader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': _TEMPLATE_CONTEXT_PROCESSORS,
        },
    },
]

# See: http://django-crispy-forms.readthedocs.org/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',

)


# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'django.template.defaultfilters.slugify'

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# Your common stuff: Below this line define 3rd party library settings
APPLICATION_RULES_URL = env('APPLICATION_RULES_URL', default='http://hacklab.fi/')

# Give path to a class implementing the api outlined in member.handers baseclasses
MEMBERAPPLICATION_CALLBACKS_HANDLER = env('MEMBERAPPLICATION_CALLBACKS_HANDLER', default=None)
MEMBER_CALLBACKS_HANDLER = env('MEMBER_CALLBACKS_HANDLER', default=None)
TRANSACTION_CALLBACKS_HANDLER = env('TRANSACTION_CALLBACKS_HANDLER', default=None)
NORDEA_UPLOAD_ENABLED = env.bool('NORDEA_UPLOAD_ENABLED', default=False)
ORGANIZATION_NAME = env('ORGANIZATION_NAME', default="hacklab.fi asylum for the inane")
RECURRINGTRANSACTIONS_CALLBACKS_HANDLER = env('RECURRINGTRANSACTIONS_CALLBACKS_HANDLER', default=None)
HOLVI_POOL = env('HOLVI_POOL', default=None)
HOLVI_APIKEY = env('HOLVI_APIKEY', default=None)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    # Use Django's standard `django.contrib.auth` permissions,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions',
    ],
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework_filters.backends.DjangoFilterBackend',
    ],
}

MARKDOWN_EXTENSIONS = ['extra', 'CodeHilite']

# Keep last as reminder
SETTINGS_EXPORT = [
    'ORGANIZATION_NAME',
    'APPLICATION_RULES_URL',
]
