import importlib
import functools
from django.conf import settings


def get_handler_instance(setting):
    try:
        setting_value = getattr(settings, setting)
        #print("Got value %s for %s" % (setting_value, setting))
    except AttributeError:
        #print("Got AttributeError for %s" % (setting))
        return None
    if not setting_value:
        return None
    module_name, class_name = setting_value.rsplit(".", 1)
    HandlerClass = getattr(importlib.import_module(module_name), class_name)
    instance = HandlerClass()
    return instance
