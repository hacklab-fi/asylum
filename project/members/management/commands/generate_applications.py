# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from members.tests.fixtures.memberlikes import MembershipApplicationFactory


class Command(BaseCommand):
    help = 'generate randomised membership applications'

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        for i in range(options['amount']):
            MembershipApplicationFactory()
