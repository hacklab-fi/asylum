from django.utils import timezone
from holviapp.utils import list_invoices, get_invoice
from .models import NotificationSent
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

NOTIFICATION_INTERVAL_DAYS = 7

class HolviOverdueInvoicesHandler(object):
    def process_overdue(self):
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
                if (timezone.now() - notified.stamp).days < NOTIFICATION_INTERVAL_DAYS:
                    continue

            #invoice.send()
            barcode = None

            mail = EmailMessage()
            mail.subject = subject_template.render(Context({ "invoice": invoice, "barcode": barcode })).strip()
            mail.body = body_template.render(Context({ "invoice": invoice, "barcode": barcode }))
            mail.to = [invoice.receiver.email]
            mail.send()

            try:
                notified = NotificationSent.objects.get(transaction_unique_id=invoice.code)
            except NotificationSent.DoesNotExist:
                notified = NotificationSent()
                notified.transaction_unique_id = invoice.code
            notified.stamp = timezone.now()
            notified.email = invoice.receiver.email
            notified.save()
            ret.append((notified, invoice))
        return ret
