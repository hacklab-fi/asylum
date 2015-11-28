from reversion import revisions
from django.db import transaction

# Monkeypatch the revisions
try:
    revisions.create_revision
except AttributeError:
    revisions.create_revision = revisions.revision_context_manager.create_revision

class AtomicVersionMixin(object):

    def save(self, *args, **kwargs):
        with transaction.atomic(), revisions.create_revision():
            return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic(), revisions.create_revision():
            return super().delete(*args, **kwargs)
