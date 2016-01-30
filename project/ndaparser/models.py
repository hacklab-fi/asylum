# -*- coding: utf-8 -*-
from django.db import models, transaction
# importing after asylum.mixins to get the monkeypatching done there
from reversion import revisions

from asylum.models import AsylumModel

# Create your models here.
