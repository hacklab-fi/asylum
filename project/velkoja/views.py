# -*- coding: utf-8 -*-
from decimal import Decimal

from creditor.models import Transaction
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.views import generic
from holviapi.utils import barcode as bank_barcode
from holviapp.utils import list_invoices

from .nordeachecker import HOLVI_EXCLUDE_KWARGS


class HolviEmailPreviewView(generic.TemplateView):
    template_name = "velkoja/holvi_preview.html"

    def get_context_data(self, **kwargs):
        # TODO: refactor together with HolviOverdueInvoicesHandler so there's one method to format the email.
        ctx = super().get_context_data(**kwargs)
        barcode_iban = settings.HOLVI_BARCODE_IBAN
        body_template = get_template('velkoja/holvi_notification_email_body.jinja')
        subject_template = get_template('velkoja/holvi_notification_email_subject.jinja')
        overdue = list_invoices(status='overdue')
        for invoice in overdue:
            # Quick check to make sure the invoice has not been credited
            if float(invoice._jsondata.get('credited_sum')) > 0:
                continue

            template_iban = invoice.iban
            barcode = None
            if barcode_iban:
                template_iban = barcode_iban
                barcode = bank_barcode(barcode_iban, invoice.rf_reference, Decimal(invoice.due_sum))

            mail = EmailMessage()
            jinja_ctx = Context({
                "invoice": invoice,
                "barcode": barcode,
                "iban": template_iban,
            })
            mail.subject = subject_template.render(jinja_ctx).strip()
            mail.body = body_template.render(jinja_ctx)
            mail.to = [invoice.receiver.email]
            ctx['email'] = mail
            break
        return ctx


class NordeaEmailPreviewView(generic.TemplateView):
    template_name = "velkoja/nordea_preview.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        barcode_iban = settings.NORDEA_BARCODE_IBAN
        body_template = get_template('velkoja/nordea_notification_email_body.jinja')
        subject_template = get_template('velkoja/nordea_notification_email_subject.jinja')

        transaction = Transaction.objects.exclude(**HOLVI_EXCLUDE_KWARGS).filter(amount__lt=0).order_by('-stamp')[0]

        barcode = None
        if barcode_iban:
            barcode = bank_barcode(barcode_iban, transaction.reference, -transaction.amount)

        mail = EmailMessage()
        mail.to = [transaction.owner.email]
        render_context = Context({
            "transaction": transaction, "due": -transaction.amount, "barcode": barcode, "iban": barcode_iban,
        })
        mail.subject = subject_template.render(render_context).strip()
        mail.body = body_template.render(render_context)
        ctx['email'] = mail
        return ctx
