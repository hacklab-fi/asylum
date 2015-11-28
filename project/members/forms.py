from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import MembershipApplication
from django.conf import settings

class ApplicationForm(forms.ModelForm):
    rules_accepted = forms.BooleanField(required=True, label=_("I have read and accept <a href='%s' target='_blank'>the rules</a>") % settings.APPLICATION_RULES_URL)

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
