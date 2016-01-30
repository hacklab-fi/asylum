# -*- coding: utf-8 -*-
from access.tests.fixtures import accesstypes, tokentypes
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'generate standard set of TokenType, AccessTypes etc'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        tokentypes.generate_standard_set()
        accesstypes.generate_standard_set()
