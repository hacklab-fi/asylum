# -*- coding: utf-8 -*-
import factory.django
import factory.fuzzy


class TransactionTagFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'creditor.TransactionTag'
        django_get_or_create = ('label', 'tmatch')


def generate_standard_set():
    for x in (('Membership fee', '1'), ('Keyholder fee', '2'), ('Lost key fee', '3')):
        TransactionTagFactory(label=x[0], tmatch=x[1])
