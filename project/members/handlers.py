# -*- coding: utf-8 -*-
import functools

from django.db import transaction

from asylum.utils import get_handler_instance


class BaseHandler(object):
    """Baseclass for the callback based handlers"""

    def on_saving(self, instance, *args, **kwargs):
        """Called just before passing control to save()"""
        pass

    def on_saved(self, instance, *args, **kwargs):
        """Called after save() returns"""
        pass


class BaseApplicationHandler(BaseHandler):
    """Baseclass for callback handlers for MembershipApplication processing"""

    def on_approving(self, application, member):
        """Called just before member.save()"""
        pass

    def on_approved(self, application, member):
        """Called just after member.save()"""
        pass


class BaseMemberHandler(BaseHandler):
    """Baseclass for callback handlers for Member processing"""
    pass


def call_saves(setting):
    def decorator(f):
        instance = get_handler_instance(setting)
        if not instance:
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
