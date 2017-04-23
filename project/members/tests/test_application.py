# -*- coding: utf-8 -*-
import pytest
from django.core.urlresolvers import reverse
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

@pytest.mark.django_db
def test_get_application_form(client):
    response = client.get(reverse('members-apply'))
    assert b'Apply for membership' in response.content
