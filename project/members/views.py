from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from .models import MembershipApplication
from .forms import ApplicationForm


class ApplyView(generic.CreateView):
    model = MembershipApplication
    template_name = "members/application_form.html"
    form_class = ApplicationForm

    def get_success_url(self):
        return reverse('members-application_received')


class ApplicationReceivedView(generic.TemplateView):
    template_name = "members/application_received.html"


class HomeView(generic.base.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('members-apply')

