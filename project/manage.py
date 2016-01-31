#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import environ

ROOT_DIR = environ.Path(__file__) - 1

if __name__ == "__main__":
    if os.path.isfile(str(ROOT_DIR + '.env')):
        environ.Env.read_env(str(ROOT_DIR + '.env'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
