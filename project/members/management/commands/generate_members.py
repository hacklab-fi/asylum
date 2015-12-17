#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import factory.django, factory.fuzzy
from members.models import generate_unique_memberid

import os, codecs

RANDOM = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'randoms')

lastnames = [x.rstrip() for x in codecs.open(os.path.join(RANDOM, 'lastnames'), 'r' ,'utf-8').readlines()]
firstnames = [
    x.rstrip() for x in
    codecs.open(os.path.join(RANDOM, 'males'), 'r' ,'utf-8').readlines() +
    codecs.open(os.path.join(RANDOM, 'females'), 'r' ,'utf-8').readlines()
]


def generate_email(memberlike):
    try:
        addr = '%s.%s@hacklab.hax' % (
            memberlike.fname.encode('ascii','ignore').decode('utf-8').lower(),
            memberlike.lname.encode('ascii','ignore').decode('utf-8').lower()
        )
        validate_email(addr)
        return addr
    except ValidationError as e:
        return 'member_%d@hacklab.hax' % generate_unique_memberid()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'members.Member'  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ('fname', 'lname', 'email', 'city')
    fname = factory.fuzzy.FuzzyChoice(firstnames)
    lname = factory.fuzzy.FuzzyChoice(lastnames)
    email = factory.LazyAttribute(generate_email)
    city = 'Helsinki' # TODO: Randomize city ?

class Command(BaseCommand):
    help = 'generate randomised members'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for i in range(100):
            UserFactory()
