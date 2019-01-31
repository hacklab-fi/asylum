# -*- coding: utf-8 -*-
import pytest
from django.core.urlresolvers import reverse
from members.models import Member
from members.tests.fixtures.memberlikes import MemberFactory, MembershipApplicationFactory
from members.tests.fixtures.types import MemberTypeFactory


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
    assert b'name="fname"' in response.content

# TODO: Figure out a good way to submitting the form


@pytest.mark.django_db
def test_get_admin_members_list(admin_client):
    # Create a test member
    member = MemberFactory()
    response = admin_client.get('/admin/members/member/')
    assert member.email in response.content.decode('utf-8')


@pytest.mark.django_db
def test_get_admin_applications_list(admin_client):
    application = MembershipApplicationFactory()
    response = admin_client.get('/admin/members/membershipapplication/')
    assert application.email in response.content.decode('utf-8')
