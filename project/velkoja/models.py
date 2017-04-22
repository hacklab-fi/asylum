# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# importing after asylum.mixins to get the monkeypatching done there
from reversion import revisions

from asylum.models import AsylumModel
from asylum.utils import get_handler_instance


class NotificationSent(AsylumModel):
    """Used to track who was sent notification and when it was last done. For preventing spamming recipients too often"""
    stamp = models.DateTimeField(_("Datetime"), default=timezone.now, db_index=True)
    transaction_unique_id = models.CharField(_("Unique transaction id"), max_length=64, blank=False, unique=True)
    email = models.EmailField(_("Email address"), blank=False)
    notification_no = models.PositiveIntegerField(default=1)
