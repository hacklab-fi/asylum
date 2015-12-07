import logging
from django.core.mail import EmailMessage
from members.handlers import BaseApplicationHandler, BaseMemberHandler
from creditor.handlers import BaseTransactionHandler
from creditor.models import Transaction, TransactionTag
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger('example.handlers')


class ExampleBaseHandler(BaseMemberHandler):
    def on_saving(self, instance):
        msg = "on_saving called for %s %s" % (type(instance) , instance)
        logger.info(msg)
        print(msg)

    def on_saved(self, instance):
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


class TransactionHandler(BaseTransactionHandler):
    def __init__(self, *args, **kwargs):
        # We have to do this late to avoid problems with circular imports
        from members.models import Member
        self.memberclass = Member
        super().__init__(*args, **kwargs)

    def import_transaction(self, at):
        msg = "import_transaction called for %s" % at
        logger.info(msg)
        print(msg)
        # We only care about transactions with reference numbers
        if not at.reference:
            return None

        lt = at.get_local()
        if lt.pk:
            # TODO update ? though it should not change...
            msg = "Found local transaction #%d with unique_id=%s" % (lt.pk, lt.unique_id)
            logger.info(msg)
            print(msg)
            return lt

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

        # Rest of the fields map directly (unique_id was already taken care of by at.get_local())
        lt.amount = at.amount
        lt.reference = at.reference
        lt.save()
        return lt

    def __str__(self):
        return str(_("Example application transactions handler"))
