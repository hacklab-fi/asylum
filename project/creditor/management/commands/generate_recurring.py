# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from creditor.tests.fixtures.recurring import RecurringTransactionFactory, MembershipfeeFactory, KeyholderfeeFactory


class Command(BaseCommand):
    help = 'generate randomised recurring transactions'

    def add_arguments(self, parser):
        parser.add_argument('mode', type=str, choices = ('totalrandom', 'membership', 'keyholder'))
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        for i in range(options['amount']):
            if options['mode'] == 'totalrandom':
                rt = RecurringTransactionFactory()
            if options['mode'] == 'membership':
                rt = MembershipfeeFactory()
            if options['mode'] == 'keyholder':
                rt = KeyholderfeeFactory()
            if options['verbosity'] > 0:
                print("Generated RecurringTransaction %s" % rt)
