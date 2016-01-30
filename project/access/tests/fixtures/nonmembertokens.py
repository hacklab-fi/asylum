# -*- coding: utf-8 -*-
import random

import factory.django
import factory.fuzzy
from access.models import AccessType, TokenType
from members.models import MemberCommon
from members.tests.fixtures.memberlikes import firstnames, generate_email, lastnames

from asylum.tests.utils import FuzzyLoremipsum
from asylum.utils import get_random_objects

from .tokens import generate_value


def generate_contact(x):
    tmp = MemberCommon()
    tmp.fname = random.choice(firstnames)
    tmp.lname = random.choice(lastnames)
    tmp.email = generate_email(tmp)
    return "%s, %s <%s>" % (tmp.lname, tmp.fname, tmp.email)


class NonMemberTokenFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'access.NonMemberToken'
        django_get_or_create = ('ttype', 'value')
    ttype = factory.fuzzy.FuzzyChoice(TokenType.objects.all())
    notes = FuzzyLoremipsum()
    contact = factory.LazyAttribute(generate_contact)
    value = factory.LazyAttribute(generate_value)

    @factory.post_generation
    def grants(self, create, extracted, **kwargs):
        grants = []
        if extracted:
            grants = extracted
        else:
            if AccessType.objects.all().count():
                grants = get_random_objects(AccessType, random.randint(1, AccessType.objects.all().count()))
        for grant in grants:
            self.grants.add(grant)
