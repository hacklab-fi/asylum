# -*- coding: utf-8 -*-
from django.db import transaction
from reversion import revisions

# Monkeypatch the revisions
try:
    revisions.create_revision
except AttributeError:
    revisions.create_revision = revisions.revision_context_manager.create_revision


class AtomicVersionMixin(object):
    """Makes sure saves and deletes go via transactions and version control
    even when objects are modified outside Django Admin"""

    def save(self, *args, **kwargs):
        with transaction.atomic(), revisions.create_revision():
            return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic(), revisions.create_revision():
            return super().delete(*args, **kwargs)


class CleanSaveMixin(object):
    """Makes sure clean() is checked before object is saved"""

    def save(self, *args, **kwargs):
        if not kwargs.pop('skip_clean', False):
            self.full_clean()
        return super().save(*args, **kwargs)
