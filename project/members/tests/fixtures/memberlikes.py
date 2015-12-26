# -*- coding: utf-8 -*-
import datetime, pytz
import os, codecs
import random
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import factory.django, factory.fuzzy
from members.models import generate_unique_memberid, MemberType, MembershipApplicationTag
from asylum.utils import get_random_objects
from . import types

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# PONDER: Move under asylym ? these are used by other apps too
# TODO: convert to generators so we do not take the filesystem performance hit at import time
lastnames = [x.rstrip() for x in codecs.open(os.path.join(DATA_PATH, 'lastnames'), 'r' ,'utf-8').readlines()]
firstnames = [
    x.rstrip() for x in
    codecs.open(os.path.join(DATA_PATH, 'males'), 'r' ,'utf-8').readlines() +
    codecs.open(os.path.join(DATA_PATH, 'females'), 'r' ,'utf-8').readlines()
]
cities = ['Helsinki', 'Turku', 'Jyväskylä', 'Mikkeli', 'Pori', 'Kuopio', 'Tampere', 'Oulu', 'Joensuu', 'Vaasa']

# This is also used by other apps
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


class MemberlikeFactoryBase(factory.django.DjangoModelFactory):
    class Meta:
        model = None
        django_get_or_create = ('fname', 'lname', 'email', 'city')
    fname = factory.fuzzy.FuzzyChoice(firstnames)
    lname = factory.fuzzy.FuzzyChoice(lastnames)
    email = factory.LazyAttribute(generate_email)
    city = factory.fuzzy.FuzzyChoice(cities)


class MemberFactory(MemberlikeFactoryBase):
    class Meta:
        model = 'members.Member'
        django_get_or_create = ('fname', 'lname', 'email', 'city')
    accepted = factory.fuzzy.FuzzyDateTime(datetime.datetime.now(pytz.utc)-datetime.timedelta(weeks=5*52))

    @factory.post_generation
    def mtypes(self, create, extracted, **kwargs):
        mtypes = []
        if extracted:
            mtypes = extracted
        else:
            if not MemberType.objects.all().count():
                types.generate_standard_set()
            mtypes = get_random_objects(MemberType, random.randint(1, MemberType.objects.all().count()))
        for mtype in mtypes:
            self.mtypes.add(mtype)


class MembershipApplicationFactory(MemberlikeFactoryBase):
    class Meta:
        model = 'members.MembershipApplication'
        django_get_or_create = ('fname', 'lname', 'email', 'city')
    received = factory.fuzzy.FuzzyDateTime(datetime.datetime.now(pytz.utc)-datetime.timedelta(days=80))

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        tags = []
        if extracted:
            tags = extracted
        else:
            if MembershipApplicationTag.objects.all().count():
                tags = get_random_objects(MembershipApplicationTag, random.randint(1, MembershipApplicationTag.objects.all().count()))
        for tag in tags:
            self.tags.add(tag)
