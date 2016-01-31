# -*- coding: utf-8 -*-
import json
import sqlite3

from access.utils import all_tokens
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Exports tokens and their access controls to sqlite file'

    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **options):
        # TODO: Check if the file exists and raise error or ask to unlink (and add option to automatically unlink)
        self.connection = sqlite3.connect(options['filepath'], detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE valid_tokens (value TEXT UNIQUE, type INTEGER, acl INTEGER, external_ids TEXT);")
        self.cursor.execute("CREATE TABLE revoked_tokens (value TEXT UNIQUE, type INTEGER);")
        self.connection.commit()
        # TODO: add TokenType filtering
        for t in all_tokens():
            if t.revoked:
                self.cursor.execute("INSERT INTO revoked_tokens VALUES (?,?);", (t.value, t.ttype.pk))
            else:
                acl = t.acl
                self.cursor.execute("INSERT INTO valid_tokens VALUES (?,?,?,?);", (t.value, t.ttype.pk, acl['bits'], json.dumps(acl['externals'])))
            self.connection.commit()
