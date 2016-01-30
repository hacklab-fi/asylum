# -*- coding: utf-8 -*-
import random

import factory.django
import factory.fuzzy
from access.models import TokenType
from members.models import Member


def generate_value(tokenlike):
    if "DESFire" in tokenlike.ttype.label:
        return "80" + "".join(["%02x" % random.randint(1, 255) for x in range(6)])
    if "Caller-id" in tokenlike.ttype.label:
        return "555-" + "".join(["%d" % random.randint(0, 9) for x in range(8)])
    return "random %x" % random.randint(1, 2 ** 32)


class TokenFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'access.Token'
        django_get_or_create = ('ttype', 'value')
    owner = factory.fuzzy.FuzzyChoice(Member.objects.all())
    ttype = factory.fuzzy.FuzzyChoice(TokenType.objects.all())
    value = factory.LazyAttribute(generate_value)
