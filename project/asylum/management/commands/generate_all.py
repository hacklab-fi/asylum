# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from asylum.tests.fixtures.full import generate_all


class Command(BaseCommand):
    help = 'Generates full set of test data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        generate_all()
