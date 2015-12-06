from django.views.generic import FormView
from .forms import UploadForm

class NordeaUploadView(FormView):
    form_class = UploadForm
    template_name = "ndaparser/admin/upload.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(self.kwargs['context'])
        return context

    def form_valid(self, form):
        context = self.get_context_data(form)
        print("File received")
        # TODO parse and handle, update context accordingly
        context['title'] = _("Transactions uploaded")
        return self.render_to_response(context)
