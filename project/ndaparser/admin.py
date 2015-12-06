from django.contrib import admin
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404, render
from django.utils.text import capfirst

class NordeaUploadMixin(object):
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
            opts = opts,
            app_label = opts.app_label,
            module_name = capfirst(opts.verbose_name),
            title = _("Upload Nordea transactions"),
        )
        context.update(extra_context or {})

        return render(request, "ndaparser/admin/upload.html", context)
