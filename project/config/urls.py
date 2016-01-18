# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views
import members.rest
import creditor.rest
import access.rest

router = routers.DefaultRouter()
router.register(r'members/types',        members.rest.MemberTypeViewSet)
router.register(r'members/tags',         members.rest.MembershipApplicationTagViewSet)
router.register(r'members/applications', members.rest.MembershipApplicationSerializerViewSet)
router.register(r'members',              members.rest.MemberViewSet)
router.register(r'creditor/transactions/recurring', creditor.rest.RecurringTransactionViewSet)
router.register(r'creditor/transactions',           creditor.rest.TransactionViewSet)
router.register(r'creditor/tags',                   creditor.rest.TransactionTagViewSet)
router.register(r'access/tokens/types', access.rest.TokenTypeViewSet)
router.register(r'access/tokens',       access.rest.TokenViewSet)
router.register(r'access/types',        access.rest.AccessTypeViewSet)
router.register(r'access/grants',       access.rest.GrantViewSet)



urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name="about"),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # Your stuff: custom urls includes go here
    url(r'^members/', include('members.urls')),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/get-token/', authtoken_views.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^markdown/', include( 'django_markdown.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request),
        url(r'^403/$', default_views.permission_denied),
        url(r'^404/$', default_views.page_not_found),
        url(r'^500/$', default_views.server_error),
    ]
