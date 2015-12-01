import datetime, calendar
import uuid, hashlib
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from asylum.mixins import AtomicVersionMixin, CleanSaveMixin
# importing after asylum.mixins to get the monkeypatching done there
from reversion import revisions
from django.db import transaction

class TransactionTag(AtomicVersionMixin, CleanSaveMixin, models.Model):
    label = models.CharField(_("Label"), max_length=200, blank=False)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _('Transaction Tag')
        verbose_name_plural = _('Transaction Tags')

revisions.default_revision_manager.register(TransactionTag)


@transaction.atomic()
def generate_transaction_id():
    candidate = uuid.uuid4().hex
    while Transaction.objects.filter(unique_id=candidate).count():
        candidate = uuid.uuid4().hex
    return candidate


class Transaction(AtomicVersionMixin, CleanSaveMixin, models.Model):
    stamp = models.DateTimeField(_("Datetime"), auto_now_add=True, db_index=True)
    tag = models.ForeignKey(TransactionTag, blank=True, null=True, verbose_name=_("Tag"), related_name='+')
    reference = models.CharField(_("Reference"), max_length=200, blank=False, db_index=True)
    owner = models.ForeignKey('members.Member', blank=False, verbose_name=_("Member"), related_name='creditor_transactions')
    amount = models.DecimalField(verbose_name=_("Amount"), max_digits=6, decimal_places=2, blank=False, null=False)
    unique_id = models.CharField(_("Unique transaction id"), max_length=64, blank=False, default=generate_transaction_id, unique=True)

    def __str__(self):
        if self.tag:
            return _("%+.2f for %s (%s)") % (self.amount, self.owner, self.tag)
        return _("%+.2f for %s") % (self.amount, self.owner)

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

revisions.default_revision_manager.register(Transaction)


class RecurringTransaction(AtomicVersionMixin, CleanSaveMixin, models.Model):
    MONTHLY = 1
    YEARLY = 2
    RTYPE_READABLE = {
        MONTHLY: _("Monthly"),
        YEARLY: _("Yearly"),
    }
    # Defined separately because we cannot do [ (x, RTYPE_READABLE[x]) for x in RTYPE_READABLE ]
    RTYPE_CHOICES = (
        (MONTHLY, _("Monthly")),
        (YEARLY, _("Yearly")),
    )

    label = models.CharField(_("Label"), max_length=200, blank=True)
    rtype = models.PositiveSmallIntegerField(verbose_name=_("Recurrence type"), choices=RTYPE_CHOICES)
    tag = models.ForeignKey(TransactionTag, blank=False, verbose_name=_("Tag"), related_name='+')
    owner = models.ForeignKey('members.Member', blank=False, verbose_name=_("Member"), related_name='+')
    amount = models.DecimalField(verbose_name=_("Amount"), max_digits=6, decimal_places=2, blank=False, null=False)

    def __str__(self):
        if self.label:
            return self.label
        return _("%+.2f %s for %s (%s)") % (self.amount, RecurringTransaction.RTYPE_READABLE[self.rtype], self.owner, self.tag)

    def resolve_timescope(self, timescope=None):
        if not timescope:
            timescope = datetime.datetime.now().date()
        if self.rtype == RecurringTransaction.MONTHLY:
            start = datetime.datetime(timescope.year, timescope.month, 1)
            end = datetime.datetime(start.year, start.month, calendar.monthrange(start.year, start.month)[1])
        elif self.rtype == RecurringTransaction.YEARLY:
            start = datetime.datetime(timescope.year, 1, 1)
            end = datetime.datetime(start.year, 12, calendar.monthrange(start.year, 12)[1])
        else:
            raise NotImplementedError("Not implemented for %s (%d)" % (RecurringTransaction.RTYPE_READABLE[self.rtype] ,self.rtype))
        return (timezone.make_aware(start), timezone.make_aware(end))

    def make_reference(self, timescope=None):
        start, end = self.resolve_timescope(timescope)
        # NOTE: Do not localize anything in this string
        return "RecurringTransaction #%d/#%d for %s" % (self.pk, self.rtype, start.date().isoformat())

    @transaction.atomic()
    def transaction_exists(self, timescope=None):
        start, end = self.resolve_timescope(timescope)
        ref = self.make_reference(timescope)
        uid = hashlib.sha1(ref.encode('UTF-8')).hexdigest()
        qs = Transaction.objects.filter(
            owner=self.owner, tag=self.tag, reference=ref, unique_id=uid,
            stamp__gte=start, stamp__lte=end
        )
        if qs.count():
            return True
        return False

    @transaction.atomic()
    @revisions.create_revision()
    def conditional_add_transaction(self, timescope=None):
        if self.transaction_exists(timescope):
            return False
        t = Transaction()
        if timescope:
            t.stamp = timescope
        t.tag = self.tag
        t.owner = self.owner
        t.reference = self.make_reference(timescope)
        t.unique_id = hashlib.sha1(t.reference.encode('UTF-8')).hexdigest()
        t.amount = self.amount
        t.save()
        return True

    class Meta:
        verbose_name = _('Recurring Transaction')
        verbose_name_plural = _('Recurring Transactions')

revisions.default_revision_manager.register(RecurringTransaction)
