import environ
import logging
import environ
import datetime, calendar
from django.utils import timezone
from django.core.mail import EmailMessage
from members.handlers import BaseApplicationHandler, BaseMemberHandler
from creditor.handlers import BaseTransactionHandler, BaseRecurringTransactionsHandler
from creditor.models import Transaction, TransactionTag
from django.utils.translation import ugettext_lazy as _
from .utils import get_holvi_singleton
import environ
import holviapi

logger = logging.getLogger('example.handlers')
env = environ.Env()


env = environ.Env()

class ExampleBaseHandler(BaseMemberHandler):
    def on_saving(self, instance, *args, **kwargs):
        msg = "on_saving called for %s %s" % (type(instance) , instance)
        logger.info(msg)
        print(msg)

    def on_saved(self, instance, *args, **kwargs):
        msg = "on_saved called for %s %s" % (type(instance) , instance)
        logger.info(msg)
        print(msg)


class MemberHandler(ExampleBaseHandler):
    pass


class ApplicationHandler(ExampleBaseHandler):
    def on_approving(self, application, member):
        msg = "on_approving called for %s" % application
        logger.info(msg)
        print(msg)

    def on_approved(self, application, member):
        msg = "on_approved called for %s" % application
        logger.info(msg)
        print(msg)
        mail = EmailMessage()
        mail.to = [ member.email, ]
        mail.body = """Your membership has been approved, your member id is #%d""" % member.member_id
        mail.send()

        # Auto-add the membership fee as recurring transaction
        membership_fee = env.float('MEMBEREXAMPLE_MEMBERSHIP_FEE', default=None)
        membership_tag = env.int('MEMBEREXAMPLE_MEMBERSHIP_TAG_PK', default=None)
        if membership_fee and membership_tag:
            from creditor.models import RecurringTransaction, TransactionTag
            rt = RecurringTransaction()
            rt.tag = TransactionTag.objects.get(pk=membership_tag)
            rt.owner = member
            rt.amount = -membership_fee
            rt.rtype = RecurringTransaction.YEARLY
            # If application was received in Q4 set the recurringtransaction to start from next year
            if application.received.month >= 10:
                rt.start = datetime.date(year=application.received.year+1, month=1, day=1)
            rt.save()
            rt.conditional_add_transaction()

        mailman_subscribe = env('MEMBEREXAMPLE_MAILMAN_SUBSCRIBE', default=None)
        if mailman_subscribe:
            mail = EmailMessage()
            mail.from_email = member.email
            mail.to = [ mailman_subscribe, ]
            mail.subject = 'subscribe'
            mail.body = 'subscribe'
            mail.send()



class TransactionHandler(BaseTransactionHandler):
    def __init__(self, *args, **kwargs):
        # We have to do this late to avoid problems with circular imports
        from members.models import Member
        self.memberclass = Member
        self.try_methods = [
            self.import_generic_transaction,
            self.import_tmatch_transaction,
        ]
        super().__init__(*args, **kwargs)

    def import_transaction(self, at):
        msg = "import_transaction called for %s" % at
        logger.info(msg)
        print(msg)

        # We only care about transactions with reference numbers
        if not at.reference:
            msg = "No reference number for %s, skip" % at
            logger.info(msg)
            print(msg)
            return None

        # If local transaction exists, return as-is
        lt = at.get_local()
        if lt.pk:
            msg = "Found local transaction #%d with unique_id=%s" % (lt.pk, lt.unique_id)
            logger.info(msg)
            print(msg)
            return lt

        # We have few importers to try
        for m in self.try_methods:
            new_lt = m(at, lt)
            if new_lt is not None:
                return new_lt

        # Nothing worked, return None
        return None

    def import_generic_transaction(self, at, lt):
        """Look for a transaction with same reference but oppsite value. If found use that for owner and tag"""
        qs = Transaction.objects.filter(reference=at.reference, amount=-at.amount).order_by('-stamp')
        if not qs.count():
            return None
        base = qs[0]
        msg = "Found opposite transaction %s" % base
        logger.info(msg)
        print(msg)
        lt.tag = base.tag
        lt.owner = base.owner
        lt.save()
        return lt

    def import_tmatch_transaction(self, at, lt):
        # In  this example the last meaningful number (last number is checksum) of the reference is used to recognize the TransactionTag
        try:
            lt.tag = TransactionTag.objects.get(tmatch=at.reference[-2])
        except TransactionTag.DoesNotExist:
            msg = "No TransactionTag with tmatch=%s" % at.reference[-2]
            logger.info(msg)
            print(msg)
            # No tag matched, skip...
            return None
        # In this example the second number and up to the tag identifier in the reference is the member number, it might have zero prefix
        try:
            lt.owner = self.memberclass.objects.get(member_id=int(at.reference[1:-2], 10))
        except self.memberclass.DoesNotExist:
            msg = "No Member with member_id=%d" % int(at.reference[1:-2], 10)
            logger.info(msg)
            print(msg)
            # No member matched, skip...
            return None

        # Rest of the fields are directly mapped already by get_local()
        lt.save()
        return lt

    def __str__(self):
        return str(_("Example application transactions handler"))



class RecurringTransactionsHolviHandler(BaseRecurringTransactionsHandler):
    def on_creating(self, rt, t, *args, **kwargs):
        msg = "on_creating called for %s (from %s)" % (t, rt)
        logger.info(msg)
        print(msg)
        # Only care about amounts
        if t.amount >= 0.0:
            return True
        # If holvi is configured, make invoice
        HOLVI_CNC = get_holvi_singleton()
        if HOLVI_CNC:
            return self.create_holvi_invoice(rt, t)
        # otherwise make reference number that matches the tmatch logic above
        t.reference = holviapi.utils.int2fin_reference(int("1%03d%s" % (rt.owner.member_id, rt.tag.tmatch)))
        return True

    def create_holvi_invoice(self, rt, t):
        HOLVI_CNC = get_holvi_singleton()
        invoice_api = holviapi.InvoiceAPI(HOLVI_CNC)
        invoice = holviapi.Invoice(invoice_api)
        invoice.receiver = holviapi.contacts.InvoiceContact(**{
            'email': t.owner.email,
            'name': t.owner.name,
        })
        invoice.items.append(holviapi.InvoiceItem(invoice))
        if t.stamp:
            year = t.stamp.year
        else:
            year = datetime.datetime.now().year
        invoice.items[0].description = "Jäsenmaksu %s" % year
        invoice.items[0].net = -t.amount # Negative amount transaction -> positive amount invoice
        invoice.subject = "%s / %s" % (invoice.items[0].description, invoice.receiver.name)
        invoice = invoice.save()
        invoice.send()
        print("Created (and sent) Holvi invoice %s" % invoice.code)
        t.reference = invoice.rf_reference
        return True

    def on_created(self, rt, t, *args, **kwargs):
        msg = "on_created called for %s (from %s)" % (t, rt)
        logger.info(msg)
        print(msg)
