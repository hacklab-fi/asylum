# -*- coding: utf-8 -*-
import random
import factory.django, factory.fuzzy
from access.models import AccessType, TokenType
from asylum.utils import get_random_objects
from asylum.tests.utils import FuzzyLoremipsum
from members.tests.fixtures.memberlikes import lastnames, firstnames, generate_email
from members.models import MemberCommon

def generate_contact(x):
    tmp = MemberCommon()
    tmp.fname = random.choice(firstnames)
    tmp.lname = random.choice(lastnames)
    tmp.email = generate_email(tmp)
    return "%s, %s <%s>" % (tmp.lname, tmp.fname, tmp.email)


def generate_value(tokenlike):
    if "DESFire" in tokenlike.ttype.label:
        return "80" + "".join([ "%02x" % random.randint(1,255) for x in range(6) ])
    if "Caller-id" in tokenlike.ttype.label:
        return "555-" + "".join([ "%d" % random.randint(0,9) for x in range(8) ])
    return "random %x" % random.randint(1,2**32)


class NonMemberTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'access.NonMemberToken'
        django_get_or_create = ('ttype','value')
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
