# -*- coding: utf-8 -*-
from creditor.admin import TransactionAdmin
from creditor.handlers import AbstractTransaction
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from asylum.utils import get_handler_instance

from .views import NordeaUploadView


class NordeaUploadMixin(object):
    nda_change_list_template = "ndaparser/admin/change_list.html"
    view_class = NordeaUploadView

    def get_urls(self):
        """Returns the additional urls used by the uploader."""
        urls = super().get_urls()
        admin_site = self.admin_site
        opts = self.model._meta
        info = opts.app_label, opts.model_name,
        my_urls = [
            url("^nordea/upload/$", admin_site.admin_view(self.upload_view), name='%s_%s_ndaupload' % info),
        ]
        return my_urls + urls

    def upload_view(self, request, extra_context=None):
        """Displays a form that can upload transactions form a Nordea "NDA" transaction file."""
        # The revisionform view will check for change permission (via changeform_view),
        # but we also need to check for add permissions here.
        if not self.has_add_permission(request):  # pragma: no cover
            raise PermissionDenied
        model = self.model
        opts = model._meta
        try:
            each_context = self.admin_site.each_context(request)
        except TypeError:  # Django <= 1.7 pragma: no cover
            each_context = self.admin_site.each_context()
        # Get the rest of the context.
        context = dict(
            each_context,
            opts=opts,
            app_label=opts.app_label,
            module_name=capfirst(opts.verbose_name),
            title=_("Upload Nordea transactions"),
            transactions_handler=get_handler_instance('TRANSACTION_CALLBACKS_HANDLER')
        )
        context.update(extra_context or {})
        view = self.view_class.as_view()

        return view(request, context=context)

    def changelist_view(self, request, extra_context=None):
        context = dict(
            orig_template=str(getattr(super(), 'change_list_template')),
        )
        context.update(extra_context or {})
        self.change_list_template = self.nda_change_list_template
        return super().changelist_view(request, context)


if settings.NORDEA_UPLOAD_ENABLED:
    # Dynamically inject the mixin to transactions admin
    TransactionAdmin.__bases__ = (NordeaUploadMixin, ) + TransactionAdmin.__bases__
