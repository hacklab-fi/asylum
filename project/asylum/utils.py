# -*- coding: utf-8 -*-
import importlib
import random

from django.conf import settings


def get_handler_instance(setting):
    """Gets instance of class defined in the given setting"""
    try:
        setting_value = getattr(settings, setting)
    except AttributeError:
        return None
    if not setting_value:
        return None
    module_name, class_name = setting_value.rsplit(".", 1)
    HandlerClass = getattr(importlib.import_module(module_name), class_name)
    instance = HandlerClass()
    return instance


def get_random_objects(klass, num=1):
    ret = []
    count = klass.objects.all().count()
    for x in range(num):
        random_index = random.randint(0, count - 1)
        ret.append(klass.objects.all()[random_index])
    return ret
