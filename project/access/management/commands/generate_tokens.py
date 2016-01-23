# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from access.tests.fixtures.tokens import TokenFactory


class Command(BaseCommand):
    help = 'generate randomised (member) tokens'

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        for i in range(options['amount']):
            token = TokenFactory()
            if options['verbosity'] > 0:
                print("Generated token %s" % token)
