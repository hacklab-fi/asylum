# -*- coding: utf-8 -*-
import datetime
import itertools as it
import random

import factory.django
import factory.fuzzy
import pytz
from creditor.models import TransactionTag
from members.models import Member


# TODO: Import these from python-holviapi when I get that further along
def int2fin_reference(n):
    """Calculates a checksum for a Finnish national reference number"""
    checksum = 10 - (sum([int(c) * i for c, i in zip(str(n)[::-1], it.cycle((7, 3, 1)))]) % 10)
    return "%s%s" % (n, checksum)


def int2iso_reference(n):
    """Calculates checksum (and adds the RF prefix) for an international reference number"""
    n = int(n)
    nt = n * 1000000 + 271500
    checksum = 98 - (nt % 97)
    return "RF%02d%d" % (checksum, n)


def generate_reference(t):
    return int2iso_reference(
        int2fin_reference(int(t.stamp.date().isoformat().replace('-', '') + '0' + str(random.randint(16, 2 ** 16)) + '0'))
    )


class TransactionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'creditor.Transaction'
        django_get_or_create = ('owner', 'tag', 'amount', 'reference', 'stamp')

    stamp = factory.LazyAttribute(lambda t: factory.fuzzy.FuzzyDateTime(datetime.datetime.combine(t.owner.accepted, datetime.datetime.min.time()).replace(tzinfo=pytz.utc)).fuzz())
    amount = factory.fuzzy.FuzzyInteger(-40, 40, 5)
    owner = factory.fuzzy.FuzzyChoice(Member.objects.all())
    tag = factory.fuzzy.FuzzyChoice(TransactionTag.objects.all())
    reference = factory.LazyAttribute(generate_reference)
