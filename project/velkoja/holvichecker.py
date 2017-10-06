# -*- coding: utf-8 -*-
import logging
from decimal import Decimal

from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from holviapi.utils import barcode as bank_barcode
from holviapp.utils import list_invoices

from .models import NotificationSent

logger = logging.getLogger(__name__)


class HolviOverdueInvoicesHandler(object):
    def process_overdue(self, send=False):
        barcode_iban = settings.HOLVI_BARCODE_IBAN
        body_template = get_template('velkoja/notification_email_body.jinja')
        subject_template = get_template('velkoja/notification_email_subject.jinja')
        overdue = list_invoices(status='overdue')
        ret = []
        for invoice in overdue:
            # Quick check to make sure the invoice has not been credited
            if float(invoice._jsondata.get('credited_sum')) > 0:
                continue
            # If we have already sent notification recently, do not sent one just yet
            if NotificationSent.objects.filter(transaction_unique_id=invoice.code).count():
                notified = NotificationSent.objects.get(transaction_unique_id=invoice.code)
                if (timezone.now() - notified.stamp).days < settings.HOLVI_NOTIFICATION_INTERVAL_DAYS:
                    continue

            if send:
                invoice.send()

            template_iban = invoice.iban
            barcode = None
            if barcode_iban:
                template_iban = barcode_iban
                barcode = bank_barcode(barcode_iban, invoice.rf_reference, Decimal(invoice.due_sum))

            mail = EmailMessage()
            mail.from_email = settings.VELKOJA_FROM_EMAIL
            mail.to = [invoice.receiver.email]
            if settings.VELKOJA_CC_EMAIL:
                mail.cc = [settings.VELKOJA_CC_EMAIL]
            ctx = Context({
                "invoice": invoice,
                "barcode": barcode,
                "iban": template_iban,
            })
            mail.subject = subject_template.render(ctx).strip()
            mail.body = body_template.render(ctx)

            if send:
                try:
                    mail.send()
                except Exception as e:
                    logger.exception("Sending email failed")

            try:
                notified = NotificationSent.objects.get(transaction_unique_id=invoice.code)
                notified.notification_no += 1
            except NotificationSent.DoesNotExist:
                notified = NotificationSent()
                notified.transaction_unique_id = invoice.code
            notified.stamp = timezone.now()
            notified.email = invoice.receiver.email
            if send:
                notified.save()
            ret.append((notified, invoice))
        return ret
