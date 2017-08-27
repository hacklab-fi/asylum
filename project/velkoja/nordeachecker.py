# -*- coding: utf-8 -*-
from decimal import Decimal

from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from holviapi.utils import barcode as bank_barcode
from members.models import Member
from ndaparser.models import UploadedTransaction

from .models import NotificationSent


class NordeaOverdueInvoicesHandler(object):
    def list_overdue(self):
        raise NotImplemented()
        # TODO: Heuristics to determine which transactions are not paid...

    def process_overdue(self, send=False):
        barcode_iban = settings.NORDEA_BARCODE_IBAN
        body_template = get_template('velkoja/nordea_notification_email_body.jinja')
        subject_template = get_template('velkoja/nordea_notification_email_subject.jinja')
        overdue = self.list_overdue()
        ret = []
        for transaction in overdue:
            # If we have already sent notification recently, do not sent one just yet
            if NotificationSent.objects.filter(transaction_unique_id=transaction.unique_id).count():
                notified = NotificationSent.objects.get(transaction_unique_id=transaction.unique_id)
                if (timezone.now() - notified.stamp).days < settings.HOLVI_NOTIFICATION_INTERVAL_DAYS:
                    continue

            barcode = None
            if barcode_iban:
                barcode = bank_barcode(barcode_iban, transaction.reference, -transaction.amount)

            mail = EmailMessage()
            mail.from_email = settings.VELKOJA_FROM_EMAIL
            mail.to = [transaction.owner.email]
            if settings.VELKOJA_CC_EMAIL:
                mail.cc = [settings.VELKOJA_CC_EMAIL]
            mail.subject = subject_template.render(Context({"transaction": transaction, "barcode": barcode})).strip()
            mail.body = body_template.render(Context({"transaction": transaction, "barcode": barcode}))
            if send:
                mail.send()

            try:
                notified = NotificationSent.objects.get(transaction_unique_id=transaction.unique_id)
                notified.notification_no += 1
            except NotificationSent.DoesNotExist:
                notified = NotificationSent()
                notified.transaction_unique_id = transaction.unique_id
            notified.stamp = timezone.now()
            notified.email = transaction.owner.email
            if send:
                notified.save()
            ret.append((notified, transaction))
        return ret
