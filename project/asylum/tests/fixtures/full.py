# -*- coding: utf-8 -*-
import members.tests.fixtures.types
import members.tests.fixtures.tags
from members.tests.fixtures.memberlikes import MemberFactory, MembershipApplicationFactory
from members.tests.fixtures.notes import MemberNoteFactory
from access.tests.fixtures import tokentypes, accesstypes
from access.tests.fixtures.grants import GrantFactory
from access.tests.fixtures.nonmembertokens import NonMemberTokenFactory
from access.tests.fixtures.tokens import TokenFactory
import creditor.tests.fixtures.tags
from creditor.tests.fixtures.recurring import KeyholderfeeFactory, Membershipfee4all
from creditor.tests.fixtures.transactions import TransactionFactory
from creditor.models import RecurringTransaction
from django.db import transaction
from members.models import Member
from access.models import AccessType

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
