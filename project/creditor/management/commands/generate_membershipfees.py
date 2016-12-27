# -*- coding: utf-8 -*-
import datetime

from creditor.models import RecurringTransaction, TransactionTag
from creditor.tests.fixtures.recurring import MembershipfeeFactory
from django.core.management.base import BaseCommand, CommandError
from members.models import Member


class Command(BaseCommand):
    help = 'Generate membership fee RecurringTransactions for all members'

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        today = datetime.datetime.now().date()
        tgt_tag = TransactionTag.objects.get(label='Membership fee', tmatch='1')
        for m in Member.objects.all():
            for rt in RecurringTransaction.objects.filter(owner=m, rtype=RecurringTransaction.YEARLY, tag=tgt_tag, end=None):
                scope_start, scope_end = rt.resolve_timescope(today)
                rt.end = scope_start.date() - datetime.timedelta(days=1)
                if rt.start > rt.end:
                    rt.start = rt.end - datetime.timedelta(days=1)
                rt.save()
            newrt = MembershipfeeFactory.create(amount=options["amount"], start=today, end=None, owner=m)
            if options['verbosity'] > 0:
                print("Generated RecurringTransaction %s" % newrt)
