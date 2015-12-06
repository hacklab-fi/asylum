import tempfile
import os
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from .forms import UploadForm
from .ndaparser import parseLine


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

        transactions = []
        with open(tmp.name) as f:
            for line in f:
                transaction = parseLine(line)
                if transaction is not None:
                    # TODO: Check if there is transaction mapper defined, if so call it
                    transactions.append(transaction)
                else:
                    # Raise error ? AFAIK there should be no unparseable lines
                    pass

        # Done with the temp file, get rid of it
        os.unlink(tmp.name)

        context['title'] = _("Transactions uploaded")
        context['transactions'] = transactions
        return self.render_to_response(context)
