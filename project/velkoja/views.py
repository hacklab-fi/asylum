# -*- coding: utf-8 -*-
from decimal import Decimal

from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.views import generic
from holviapi.utils import barcode as bank_barcode
from holviapp.utils import list_invoices


class EmailPreviewView(generic.TemplateView):
    template_name = "velkoja/preview.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        barcode_iban = settings.HOLVI_BARCODE_IBAN
        body_template = get_template('velkoja/notification_email_body.jinja')
        subject_template = get_template('velkoja/notification_email_subject.jinja')
        overdue = list_invoices(status='overdue')
        for invoice in overdue:
            # Quick check to make sure the invoice has not been credited
            if float(invoice._jsondata.get('credited_sum')) > 0:
                continue

            barcode = None
            if barcode_iban:
                barcode = bank_barcode(barcode_iban, invoice.rf_reference, Decimal(invoice.due_sum))

            mail = EmailMessage()
            mail.subject = subject_template.render(Context({"invoice": invoice, "barcode": barcode})).strip()
            mail.body = body_template.render(Context({"invoice": invoice, "barcode": barcode}))
            mail.to = [invoice.receiver.email]
            ctx['email'] = mail
            break
        return ctx
