# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.functional import allow_lazy, lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from .models import MembershipApplication


def rules_accepted_proxy(msg):
    return msg % settings.APPLICATION_RULES_URL

rules_accepted_proxy = allow_lazy(rules_accepted_proxy, str)


class ApplicationForm(forms.ModelForm):
    rules_accepted = forms.BooleanField(required=True, label=rules_accepted_proxy(_("I have read and accept <a href=\"%s\" target=\"_blank\">the rules</a>")))
    required_css_class = 'required'

    class Meta:
        model = MembershipApplication
        fields = [
            'fname',
            'lname',
            'city',
            'email',
            'phone',
            'nick',
        ]
