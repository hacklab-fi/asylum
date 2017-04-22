# -*- coding: utf-8 -*-
"""
WSGI config for asylum project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

import environ
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

ROOT_DIR = environ.Path(__file__) - 2  # (/a/b/myfile.py - 3 = /)
env = environ.Env()
# If the project root contains a .env file, read it
if os.path.isfile(str(ROOT_DIR + '.env')):
    environ.Env.read_env(str(ROOT_DIR + '.env'))



if env.bool('USE_SENTRY', False):
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()

# Use Whitenoise to serve static files
# See: https://whitenoise.readthedocs.org/
application = DjangoWhiteNoise(application)
if env.bool('USE_SENTRY', False):
    application = Sentry(application)

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
