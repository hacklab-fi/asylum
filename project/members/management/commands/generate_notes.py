# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from members.tests.fixtures.notes import MemberNoteFactory


class Command(BaseCommand):
    help = 'generate randomised member notes'

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        for i in range(options['amount']):
            note = MemberNoteFactory()
            if options['verbosity'] > 0:
                print("Generated note to %s" % note.member)
