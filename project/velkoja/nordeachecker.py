# -*- coding: utf-8 -*-
import logging
import datetime

from decimal import Decimal

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from holviapi.utils import barcode as bank_barcode
from members.models import Member
from ndaparser.models import UploadedTransaction


from .models import NotificationSent

logger = logging.getLogger(__name__)

HOLVI_EXCLUDE_KWARGS = {"reference__startswith": "RF"}


class NordeaOverdueInvoicesHandler(object):
    def list_overdue(self):
        """Gets list of overdue Nordea transactions"""
        # TODO: Heuristics to determine which transactions are not paid...
        gd = settings.VELKOJA_NORDEACHECKER_GRACE_DAYS
        if not UploadedTransaction.objects.count():
            logger.warning("No uploaded transactions found defaulting to configured grace period of {} days".format(gd))
            cutoff_date = datetime.datetime.now().date() - datetime.timedelta(days=gd)
        else:
            cutoff_date = UploadedTransaction.objects.order_by('-last_transaction')[0].last_transaction
            today_delta = datetime.datetime.now().date() - cutoff_date
            if today_delta.days > gd:
                logger.warning("Last uploaded transaction was {} days ago".format(today_delta.days))

        ret = []

        # First get members with negative credit in general
        members_qs = Member.objects.all()
        members_qs = members_qs.annotate(credit_annotated=models.Sum('creditor_transactions__amount'))
        for member in members_qs.filter(credit_annotated__lt=0):
            # Then find distinct reference numbers that are not Holvi transactions
            ret += self._list_member_overdue(member, cutoff_date)
        return ret

    def _list_member_overdue(self, member, cutoff_date):
        """Figure out which debits of a given member are still unpaid"""
        base_qs = member.creditor_transactions.exclude(**HOLVI_EXCLUDE_KWARGS).filter(stamp__lte=cutoff_date)
        refnos = [x['reference'] for x in
                  base_qs.order_by('reference').distinct('reference').values('reference')]
        ret = []
        for refno in refnos:
            refno_qs = base_qs.filter(reference=refno)
            refno_credits = refno_qs.filter(amount__gte=0).aggregate(models.Sum('amount'))['amount__sum']
            if refno_credits is None:
                refno_credits = Decimal('0')
            refno_debits = refno_qs.filter(amount__lt=0).order_by('stamp')
            for transaction in refno_debits:
                refno_credits += transaction.amount  # remember: the amount is negative
                if refno_credits >= 0:
                    # While we have not expended all credit, keep spending
                    continue
                # After no more credits are left, put rest of transactions to the unpaid pile.
                ret.append(transaction)

        return ret

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
