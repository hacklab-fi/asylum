import tempfile
import os
import datetime, pytz
import hashlib
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from .forms import UploadForm
from .ndaparser import parseLine
from creditor.handlers import AbstractTransaction


HELSINKI = pytz.timezone('Europe/Helsinki')


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
            for line in f:
                nt = parseLine(line)
                if nt is not None:
                    if transactions_handler:
                        at = AbstractTransaction()
                        at.name = str(nt.name)
                        at.reference = str(nt.referenceNumber)
                        at.amount = nt.amount # We know this is Decimal instance
                        at.stamp = HELSINKI.fromutc(datetime.datetime.combine(nt.timestamp, datetime.datetime.min.time()))
                        # DO NOT EVER CHANGE THIS, it must always and forever yield same unique_id for same transaction.
                        at.unique_id = hashlib.sha1(str(nt.archiveID).encode('utf-8') + nt.timestamp.isoformat().encode('utf-8') + str(nt.referenceNumber).encode('utf-8')).hexdigest()
                        ret = transactions_handler.import_transaction(at)
                        if ret is not None:
                            transactions.append(ret)
                    else:
                        transactions.append(nt)
                else:
                    # Raise error ? AFAIK there should be no unparseable lines
                    pass

        # Done with the temp file, get rid of it
        os.unlink(tmp.name)

        context['title'] = _("Transactions uploaded")
        context['transactions'] = transactions
        return self.render_to_response(context)
