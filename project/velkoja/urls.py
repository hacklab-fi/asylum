# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^preview/?$', views.EmailPreviewView.as_view(), name="velkoja-email_preview"),
]
