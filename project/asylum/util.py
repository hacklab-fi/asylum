import importlib
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
