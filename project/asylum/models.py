# -*- coding: utf-8 -*-
from django.db import models

from .mixins import AtomicVersionMixin, CleanSaveMixin


class AsylumModel(AtomicVersionMixin, CleanSaveMixin, models.Model):
    """Baseclass for models in all Asylum apps, all the common mixins etc should be added here"""

    class Meta:
        abstract = True
