# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^preview/holvi/?$', views.HolviEmailPreviewView.as_view(), name="velkoja-holvi_email_preview"),
]
