# -*- coding: utf-8 -*-
import datetime

import pytest

from members.tests.fixtures.memberlikes import MemberFactory
from creditor.tests.fixtures.transactions import TransactionFactory
from creditor.tests.fixtures.tags import generate_standard_set
from velkoja.models import NotificationSent

@pytest.mark.django_db
def test_model_can_be_saved():
    generate_standard_set()
    member = MemberFactory()
    transaction = TransactionFactory(owner=member)
    ns = NotificationSent(
        email=member.email,
        transaction_unique_id=transaction.unique_id
    )
    ns.save()
    assert ns.pk > 0
