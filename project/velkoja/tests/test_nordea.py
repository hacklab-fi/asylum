# -*- coding: utf-8 -*-
import datetime
import pytest


from django.conf import settings

from creditor.tests.fixtures.tags import generate_standard_set
from creditor.models import TransactionTag
from creditor.tests.fixtures.transactions import TransactionFactory
from members.tests.fixtures.memberlikes import MemberFactory

from velkoja.nordeachecker import NordeaOverdueInvoicesHandler


@pytest.mark.django_db
@pytest.fixture
def basic_setup():
    generate_standard_set()
    member = MemberFactory()
    return member


@pytest.mark.django_db
@pytest.fixture
def uniform_transactions_zerosum(basic_setup):
    member = basic_setup
    cutoff = datetime.datetime.now().date() - datetime.timedelta(days=settings.VELKOJA_NORDEACHECKER_GRACE_DAYS+2)
    tag = TransactionTag.objects.get(tmatch='2')
    months = 6
    for refno, amount in [ ('109', 40), ('107', 20) ]:
        for x in range(months):
            credit_date = cutoff - datetime.timedelta(days=x*30)
            debit_date = credit_date - datetime.timedelta(days=3)
            debit = TransactionFactory(
                owner = member,
                reference = refno,
                amount = -amount,
                tag = tag,
                stamp = datetime.datetime.combine(debit_date, datetime.datetime.min.time())
            )
            credit = TransactionFactory(
                owner = member,
                reference = refno,
                amount = amount,
                tag = tag,
                stamp = datetime.datetime.combine(credit_date, datetime.datetime.min.time())
            )
    return (member, cutoff)


@pytest.mark.django_db
@pytest.fixture
def nonuniform_transactions_zerosum(basic_setup):
    member = basic_setup
    cutoff = datetime.datetime.now().date() - datetime.timedelta(days=settings.VELKOJA_NORDEACHECKER_GRACE_DAYS+2)
    tag = TransactionTag.objects.get(tmatch='2')
    months = 6
    for refno, amount in [ ('109', 40), ('107', 20) ]:
        for x in range(months):
            debit_date = cutoff - datetime.timedelta(days=x*30)
            debit = TransactionFactory(
                owner = member,
                reference = refno,
                amount = -amount,
                tag = tag,
                stamp = datetime.datetime.combine(debit_date, datetime.datetime.min.time())
            )
        credit_date = cutoff - datetime.timedelta(days=months/3*30)
        first_amount = amount*(months/3)
        credit = TransactionFactory(
            owner = member,
            reference = refno,
            amount = first_amount,
            tag = tag,
            stamp = datetime.datetime.combine(credit_date, datetime.datetime.min.time())
        )
        credit2 = TransactionFactory(
            owner = member,
            reference = refno,
            amount = months*amount-first_amount,
            tag = tag,
            stamp = datetime.datetime.combine(cutoff, datetime.datetime.min.time())
        )

    return (member, cutoff)


@pytest.mark.django_db
def test_uniform_no_overdue(uniform_transactions_zerosum):
    member, cutoff = uniform_transactions_zerosum
    assert member.creditor_transactions.count() > 0
    handler = NordeaOverdueInvoicesHandler()
    overdue = handler.list_overdue()
    assert not overdue


@pytest.mark.django_db
def test_uniform_overdue(uniform_transactions_zerosum):
    member, cutoff = uniform_transactions_zerosum
    old_count = member.creditor_transactions.count()
    assert old_count > 0
    templ = member.creditor_transactions.filter(amount__lt=0).order_by('-stamp')[0]
    debit = TransactionFactory(
        owner=member,
        reference=templ.reference,
        amount=templ.amount,
        tag=templ.tag,
        stamp=templ.stamp + datetime.timedelta(days=2)
    )
    print(debit, debit.unique_id)
    assert member.creditor_transactions.count() > old_count
    handler = NordeaOverdueInvoicesHandler()
    overdue = handler.list_overdue()
    assert overdue
    assert overdue[0].unique_id == debit.unique_id


@pytest.mark.django_db
def test_nonuniform_no_overdue(nonuniform_transactions_zerosum):
    member, cutoff = nonuniform_transactions_zerosum
    assert member.creditor_transactions.count() > 0
    # Make sure the distribution is non-uniform
    debits = member.creditor_transactions.filter(amount__lt=0)
    credits = member.creditor_transactions.filter(amount__gt=0)
    assert debits.count() != credits.count()
    # Make sure nothing is overdue
    handler = NordeaOverdueInvoicesHandler()
    overdue = handler.list_overdue()
    assert not overdue
