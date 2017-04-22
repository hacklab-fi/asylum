# -*- coding: utf-8 -*-
import calendar
import datetime
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


# Adapted from http://www.ianlewis.org/en/python-date-range-iterator
def months(from_date=None, to_date=None):
    from_date = from_date or datetime.datetime.now().date()
    while to_date is None or from_date <= to_date:
        yield from_date
        from_date = from_date + datetime.timedelta(days=calendar.monthrange(from_date.year, from_date.month)[1])
    return


def datetime_proxy(delta=datetime.timedelta(days=1)):
    """Used by management commands needing datetime X days ago"""
    now_yesterday = datetime.datetime.now() - delta
    start_yesterday = datetime.datetime.combine(now_yesterday.date(), datetime.datetime.min.time())
    return start_yesterday.isoformat()
