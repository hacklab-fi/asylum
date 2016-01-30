# -*- coding: utf-8 -*-
from creditor.tests.fixtures import tags
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'generate standard set of TransactionTags'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        tags.generate_standard_set()
