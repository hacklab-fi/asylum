# -*- coding: utf-8 -*-
import factory.django
import factory.fuzzy


class MembershipApplicationTagFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'members.MembershipApplicationTag'
        django_get_or_create = ('label',)


def generate_standard_set():
    for x in ('Welcome email sent', 'Special tag 1', 'Special tag 2'):
        MembershipApplicationTagFactory(label=x)
