# -*- coding: utf-8 -*-
import pytest
from members.tests.fixtures.memberlikes import MembershipApplicationFactory
from members.tests.fixtures.types import MemberTypeFactory
from members.models import Member

@pytest.mark.django_db
def test_application_approve():
    mtypes = [MemberTypeFactory(label='Normal member')]
    application = MembershipApplicationFactory()
    email = application.email
    application.approve(set_mtypes=mtypes)
    Member.objects.get(email=email)
