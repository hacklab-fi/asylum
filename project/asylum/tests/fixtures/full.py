# -*- coding: utf-8 -*-
import creditor.tests.fixtures.tags
import members.tests.fixtures.tags
import members.tests.fixtures.types
from access.models import AccessType
from access.tests.fixtures import accesstypes, tokentypes
from access.tests.fixtures.grants import GrantFactory
from access.tests.fixtures.nonmembertokens import NonMemberTokenFactory
from access.tests.fixtures.tokens import TokenFactory
from creditor.models import RecurringTransaction
from creditor.tests.fixtures.recurring import KeyholderfeeFactory, Membershipfee4all
from creditor.tests.fixtures.transactions import TransactionFactory
from django.db import transaction
from members.models import Member
from members.tests.fixtures.memberlikes import MemberFactory, MembershipApplicationFactory
from members.tests.fixtures.notes import MemberNoteFactory


def generate_all():
    with transaction.atomic():
        members.tests.fixtures.types.generate_standard_set()
        members.tests.fixtures.tags.generate_standard_set()
        MemberFactory.create_batch(100)
        MembershipApplicationFactory.create_batch(25)

        tokentypes.generate_standard_set()
        accesstypes.generate_standard_set()
        NonMemberTokenFactory.create_batch(10)

        creditor.tests.fixtures.tags.generate_standard_set()
        Membershipfee4all()

        TransactionFactory.build_batch(100)
        MemberNoteFactory.create_batch(50)
        TokenFactory.create_batch(50)
        GrantFactory.create_batch(50)

        for m in Member.objects.filter(access_granted__atype=AccessType.objects.get(bit=0)):
            KeyholderfeeFactory(owner=m)
        for t in RecurringTransaction.objects.all():
            ret = t.conditional_add_transaction()
