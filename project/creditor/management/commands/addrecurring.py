# -*- coding: utf-8 -*-
from creditor.models import RecurringTransaction
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Gets all RecurringTransactions and runs conditional_add_transaction()'

    def handle(self, *args, **options):
        for t in RecurringTransaction.objects.all():
            ret = t.conditional_add_transaction()
            if ret:
                if options['verbosity'] > 1:
                    print("Created transaction %s" % ret)
