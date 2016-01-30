# -*- coding: utf-8 -*-
import os
import tempfile

from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from .forms import UploadForm
from .importer import NDAImporter


class NordeaUploadView(FormView):
    form_class = UploadForm
    template_name = "ndaparser/admin/upload.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs['context'])
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        # We have to write out the file in binary mode before we properly parse it by lines
        tmp = tempfile.NamedTemporaryFile(prefix="ndaupload", delete=False)
        with tmp as dest:
            for chunk in self.request.FILES['ndafile'].chunks():
                dest.write(chunk)

        transactions_handler = context['transactions_handler']
        transactions = []
        with open(tmp.name) as f:
            h = NDAImporter(f)
            transactions = h.import_transactions(transactions_handler)

        # Done with the temp file, get rid of it
        os.unlink(tmp.name)

        context['title'] = _("Transactions uploaded")
        context['transactions'] = transactions
        return self.render_to_response(context)
