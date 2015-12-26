# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from creditor.tests.fixtures import tags


class Command(BaseCommand):
    help = 'generate standard set of TransactionTags'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        tags.generate_standard_set()
