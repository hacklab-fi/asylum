# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _


class UploadForm(forms.Form):
    ndafile = forms.FileField(required=True, label=_("Transactions file"))
