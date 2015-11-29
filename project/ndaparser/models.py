from django.db import models
from asylum.models import AsylumModel
# importing after asylum.mixins to get the monkeypatching done there
from reversion import revisions
from django.db import transaction

# Create your models here.
