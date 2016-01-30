# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from access.tests.fixtures.nonmembertokens import NonMemberTokenFactory


class Command(BaseCommand):
    help = 'generate randomised nonmembertokens'

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        for i in range(options['amount']):
            token = NonMemberTokenFactory()
            if options['verbosity'] > 0:
                print("Generated token %s" % token)
