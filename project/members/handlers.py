import importlib
import functools
from django.conf import settings
from django.db import transaction


class BaseHandler(object):
    """Baseclass for the callback based handlers"""
    def on_saving(self, instance, *args, **kwargs):
        """Called just before passing control to save()"""
        #print("on_saving called %s %s %s" % (instance, repr(args), repr(kwargs)))
        pass

    def on_saved(self, instance, *args, **kwargs):
        """Called after save() returns"""
        #print("on_saved called %s %s %s" % (instance, repr(args), repr(kwargs)))
        pass


class BaseApplicationHandler(BaseHandler):
    """Baseclass for callback handlers for MembershipApplication processing"""

    def on_approving(self, application, member):
        """Called just before member.save()"""
        #print("on_approving called %s %s" % (application, member))
        pass

    def on_approved(self, application, member):
        """Called just after member.save()"""
        #print("on_approved called %s %s" % (application, member))
        pass


class BaseMemberHandler(BaseHandler):
    """Baseclass for callback handlers for Member processing"""
    pass


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


def call_saves(setting):
    def decorator(f):
        instance = get_handler_instance(setting)
        if not instance:
            #print("Could not get handler instance for %s" % setting)
            return f

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            with transaction.atomic():
                instance.on_saving(*args, **kwargs)
                r = f(*args, **kwargs)
                instance.on_saved(*args, **kwargs)
                return r
        return wrapper
    return decorator
