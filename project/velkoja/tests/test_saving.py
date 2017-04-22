# -*- coding: utf-8 -*-
import datetime

import pytest
from creditor.tests.fixtures.tags import generate_standard_set
from creditor.tests.fixtures.transactions import TransactionFactory
from members.tests.fixtures.memberlikes import MemberFactory
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
