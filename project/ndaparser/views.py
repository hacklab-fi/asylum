from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from .forms import UploadForm

class NordeaUploadView(FormView):
    form_class = UploadForm
    template_name = "ndaparser/admin/upload.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs['context'])
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        print("File received, FILES=%s" % repr(self.request.FILES))
        # TODO parse and handle, update context accordingly
        context['title'] = _("Transactions uploaded")
        return self.render_to_response(context)
