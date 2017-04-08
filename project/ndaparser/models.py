# -*- coding: utf-8 -*-
import datetime
import slugify as unicodeslugify

from django.db import models, transaction
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


from asylum.models import AsylumModel



def get_sentinel_user():
    """Gets a "sentinel" user ("deleted") and for assigning as uploader"""
    return get_user_model().objects.get_or_create(username='deleted')[0]



def datestamped_and_normalized(instance, filename):
    """Normalized filename and places in datestamped path"""
    file_parts = filename.split('.')
    if len(file_parts) > 1:
        name = '.'.join(file_parts[:-1])
        ext = '.' + file_parts[-1]
    else:
        ext = ''
        name = filename
    filename_normalized = unicodeslugify.slugify(
        name, only_ascii=True, lower=True,
        spaces=False, space_replacement='_'
    ) + ext
    return datetime.datetime.now().strftime("ndaparser/%Y/%m/%d/{}").format(filename_normalized)



class UploadedTransaction(AsylumModel):
    """Track uploaded transaction files"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    file = models.FileField(upload_to=datestamped_and_normalized)
    stamp = models.DateTimeField(auto_now_add=True, editable=False)
    last_transaction = models.DateField()

    class Meta:
        verbose_name = _('Uploaded transaction')
        verbose_name_plural = _('Uploaded transaction')
        ordering = [ '-stamp' ]
