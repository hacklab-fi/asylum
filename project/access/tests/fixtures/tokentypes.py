# -*- coding: utf-8 -*-
import factory.django
import factory.fuzzy


class TokenTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'access.TokenType'
        django_get_or_create = ('label',)


def generate_standard_set():
    for x in ('DESFire', 'Caller-id'):
        TokenTypeFactory(label=x)
