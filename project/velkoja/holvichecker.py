from django.utils import timezone
from holviapp.utils import list_invoices, get_invoice
from .models import NotificationSent
from cStringIO import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email import Charset
from email.generator import Generator
import smtplib

NOTIFICATION_INTERVAL_DAYS = 7

class HolviOverdueInvoicesHandler(object):
    smtp =  None

    def open_smtp_gracefull(self):
        if self.smtp:
            return
        # TODO Or just use Djangos email facility ?
        # TODO: use configuration for mail delivery info
        self.smtp = smtplib.SMTP('smtp.sparkpostmail.com', 587)
        r = s.starttls()
        r = s.login('SMTP_Injection', '')

    def close_smtp_gracefull(self):
        if not self.smtp:
            return
        self.smtp.quit()

    def process_overdue(self):
        overdue = list_invoices(status='overdue')
        ret = []
        for invoice in overdue:
            # Quick check to make sure the invoice has not been credited
            if float(i._jsondata.get('credited_sum')) > 0:
                continue
            # If we have already sent notification recently, do not sent one just yet
            if NotificationSent.objects.filter(transaction_unique_id=invoice.code).count():
                notified = NotificationSent.objects.get(transaction_unique_id=invoice.code)
                if (timezone.now() - notified.stamp).days < NOTIFICATION_INTERVAL_DAYS:
                    continue

            # TODO: format email and send it

            notified = NotificationSent.objects.get_or_create(transaction_unique_id=invoice.code)
            notified.stamp = timezone.now()
            notified.email = invoice.receiver.email
            notified.save()
            ret.append(notified)
        self.close_smtp_gracefull()

    def send_unicode_email(from_address, recipient, subject, text):
        self.open_smtp_gracefull()

        # Default encoding mode set to Quoted Printable. Acts globally!
        Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')

        # 'alternative’ MIME type – HTML and plain text bundled in one e-mail message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "%s" % Header(subject, 'utf-8')
        # Only descriptive part of recipient and sender shall be encoded, not the email address
        msg['From'] = "\"%s\" <%s>" % (Header(from_address[0], 'utf-8'), from_address[1])
        msg['To'] = "\"%s\" <%s>" % (Header(recipient[0], 'utf-8'), recipient[1])

        # Attach both parts
        textpart = MIMEText(text, 'plain', 'UTF-8')
        msg.attach(textpart)

        # Create a generator and flatten message object to 'file’
        str_io = StringIO()
        g = Generator(str_io, False)
        g.flatten(msg)
        # str_io.getvalue() contains ready to sent message

        # TODO Or just use Djangos email facility ?
        r = self.smtp.sendmail(from_address[1], recipient[1], str_io.getvalue())
        # TODO Check return value and return something ?
