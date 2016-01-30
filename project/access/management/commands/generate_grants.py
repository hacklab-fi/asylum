# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from access.tests.fixtures.grants import GrantFactory


class Command(BaseCommand):
    help = 'generate randomised (member) access grants'

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        for i in range(options['amount']):
            grant = GrantFactory()
            if options['verbosity'] > 0:
                print("Generated grant %s" % grant)
