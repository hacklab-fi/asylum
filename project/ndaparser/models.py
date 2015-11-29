from django.db import models
from asylum.mixins import AtomicVersionMixin, CleanSaveMixin
# importing after asylum.mixins to get the monkeypatching done there
from reversion import revisions
from django.db import transaction

# Create your models here.
