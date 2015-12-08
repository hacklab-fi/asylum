#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from members.importer import importer
import factory.django, factory.fuzzy

import os, codecs

RANDOM = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'randoms')

lastnames = [x.rstrip() for x in codecs.open(os.path.join(RANDOM, 'lastnames'), 'r' ,'utf-8').readlines()]
firstnames = [
    x.rstrip() for x in
    codecs.open(os.path.join(RANDOM, 'males'), 'r' ,'utf-8').readlines() +
    codecs.open(os.path.join(RANDOM, 'females'), 'r' ,'utf-8').readlines()
]

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'members.Member'  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ('fname', 'lname', 'email', 'city')
    fname = factory.fuzzy.FuzzyChoice(firstnames)
    lname = factory.fuzzy.FuzzyChoice(lastnames)
    email = factory.LazyAttribute(
        lambda o: '%s.%s@hacklab.hax' % (
            o.fname.encode('ascii','ignore').decode('utf-8').lower(),
            o.lname.encode('ascii','ignore').decode('utf-8').lower()
        )
    )
    city = 'Helsinki'

class Command(BaseCommand):
    help = 'generate randomised members'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for i in range(100):
            UserFactory()
