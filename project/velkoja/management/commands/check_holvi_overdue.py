# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from velkoja.holvichecker import HolviOverdueInvoicesHandler

class Command(BaseCommand):
    help = 'Import transaction data from Holvi API'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        handler = HolviOverdueInvoicesHandler()
        notified = handler.process_overdue(send=True)
        if options['verbosity'] > 1:
            for n,i in notified:
                print("Notified  %s about %s" % (n.email, i.subject))
