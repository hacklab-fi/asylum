# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from velkoja.nordeachecker import NordeaOverdueInvoicesHandler


class Command(BaseCommand):
    help = 'Check overdue Nordea payments and send emails about them'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        handler = NordeaOverdueInvoicesHandler()
        notified = handler.process_overdue(send=True)
        if options['verbosity'] > 1:
            for n, t in notified:
                print("Notified  %s about %s" % (n.email, t))
