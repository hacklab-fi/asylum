# -*- coding: utf-8 -*-
import factory.django
import factory.fuzzy


class AccessTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'access.AccessType'
        django_get_or_create = ('bit',)


def generate_standard_set():
    for x in (('Front door', 0, '0x0'), ('Lathe', 1, '0x1'), ('Mill', 2, '0x2'), ('Plasma', 3, '0x3')):
        AccessTypeFactory(label=x[0], bit=x[1], external_id=x[2])
