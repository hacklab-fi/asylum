# -*- coding: utf-8 -*-
import random

import factory.django
import factory.fuzzy
from access.models import AccessType, TokenType
from members.models import Member
from members.tests.fixtures.memberlikes import MemberFactory

from asylum.tests.utils import FuzzyLoremipsum


class GrantFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'access.Grant'
        django_get_or_create = ('atype', 'owner')
    atype = factory.fuzzy.FuzzyChoice(AccessType.objects.all())
    owner = factory.fuzzy.FuzzyChoice(Member.objects.filter(access_tokens__ttype__in=TokenType.objects.all()))  # It only makes sense to generate grants for members that have tokens
    #owner = factory.SubFactory(MemberFactory)
    #notes = FuzzyLoremipsum()
