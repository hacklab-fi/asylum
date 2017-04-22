# -*- coding: utf-8 -*-
import datetime
import itertools

import dateutil.parser
from creditor.models import RecurringTransaction
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from asylum.utils import datetime_proxy, months


class Command(BaseCommand):
    help = 'Gets all RecurringTransactions and runs conditional_add_transaction()'

    def add_arguments(self, parser):
        parser.add_argument('since', type=str, nargs='?', default=datetime_proxy(), help='Run for each month since the date, defaults to yesterday midnight')

    def handle(self, *args, **options):
        since_parsed = timezone.make_aware(dateutil.parser.parse(options['since']))
        if options['verbosity'] > 2:
            print("Processing since %s" % since_parsed.isoformat())

        for t in RecurringTransaction.objects.all():
            if options['verbosity'] > 2:
                print("Processing: %s" % t)
            for month in months(since_parsed, timezone.now()):
                if options['verbosity'] > 2:
                    print("  month %s" % month.isoformat())
                ret = t.conditional_add_transaction(month)
                if ret:
                    if options['verbosity'] > 1:
                        print("Created transaction %s" % ret)
