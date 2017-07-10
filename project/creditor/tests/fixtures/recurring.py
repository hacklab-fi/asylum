# -*- coding: utf-8 -*-
import random

import factory.django
import factory.fuzzy
from creditor.models import RecurringTransaction, TransactionTag
from members.models import Member
from members.tests.fixtures.memberlikes import MemberFactory

from .tags import TransactionTagFactory

def get_tag():
    if TransactionTag.objects.count():
        return factory.fuzzy.FuzzyChoice(TransactionTag.objects.all())
    return factory.SubFactory(TransactionTagFactory, label='Membership fee', tmatch='1')

class RecurringTransactionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'creditor.RecurringTransaction'
        django_get_or_create = ('tag', 'owner', 'end')

    end = None
    rtype = factory.fuzzy.FuzzyChoice(RecurringTransaction.RTYPE_READABLE.keys())
    owner = factory.SubFactory(MemberFactory)  # ternary expression does not really help us since the import is done before the test-db is created, TODO: Make a special helper class that can will evaluate the count later
    tag = get_tag
    amount = factory.fuzzy.FuzzyInteger(-40, -10, 5)
    start = factory.LazyAttribute(lambda t: factory.fuzzy.FuzzyDate(t.owner.accepted).fuzz())


class MembershipfeeFactory(RecurringTransactionFactory):
    tag = factory.SubFactory(TransactionTagFactory, label='Membership fee', tmatch='1')
    rtype = RecurringTransaction.YEARLY
    amount = -28
    start = factory.LazyAttribute(lambda t: t.owner.accepted)

class QuarterlyFactory(RecurringTransactionFactory):
    tag = factory.SubFactory(TransactionTagFactory, label= 'Quarterly fee', tmatch='3')
    rtype = RecurringTransaction.Quarterly
    amount = amount = factory.fuzzy.FuzzyInteger(-40, -20, 10)


class KeyholderfeeFactory(RecurringTransactionFactory):
    tag = factory.SubFactory(TransactionTagFactory, label='Keyholder fee', tmatch='2')
    rtype = RecurringTransaction.MONTHLY
    amount = factory.fuzzy.FuzzyInteger(-40, -20, 10)


def Membershipfee4all(output=False):
    for m in Member.objects.all():
        rt = MembershipfeeFactory(owner=m)
        if output:
            print("Generated RecurringTransaction %s" % rt)
