# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from members.importer import importer


class Command(BaseCommand):
    help = 'Imports a CSV file of members, first row headers must match member properties'

    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **options):
        with open(options['filepath']) as fp:
            i = importer(fp)
            i.import_members()
