# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from members.tests.fixtures import tags, types


class Command(BaseCommand):
    help = 'generate standard set of MemberTypes, ApplicationTags etc'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        types.generate_standard_set()
        tags.generate_standard_set()
