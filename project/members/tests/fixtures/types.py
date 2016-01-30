# -*- coding: utf-8 -*-
import factory.django
import factory.fuzzy


class MemberTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'members.MemberType'
        django_get_or_create = ('label',)


def generate_standard_set():
    for x in ('Normal member', 'Keyholder', 'Special case 1', 'Special case 2'):
        MemberTypeFactory(label=x)
