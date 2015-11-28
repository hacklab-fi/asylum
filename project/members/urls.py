from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^apply/?$', views.ApplyView.as_view(), name="members-apply"),
    url(r'^apply/done/?$', views.ApplicationReceivedView.as_view(), name="members-application_received"),
]
