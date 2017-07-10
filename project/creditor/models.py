# -*- coding: utf-8 -*-
import calendar
import datetime
import hashlib
import uuid

from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# importing after asylum.mixins to get the monkeypatching done there
from reversion import revisions

from asylum.models import AsylumModel
from asylum.utils import get_handler_instance


class TransactionTag(AsylumModel):
    label = models.CharField(_("Label"), max_length=200, blank=False)
    tmatch = models.CharField(_("Transaction match"), max_length=20, blank=True, db_index=True)  # This can be used by transaction handlers to help them in some way.
    holvi_code = models.CharField(_("Holvi category code"), max_length=64, blank=True, db_index=True)  # This can be used by transaction handlers to match holvi categories to tags

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _('Transaction Tag')
        verbose_name_plural = _('Transaction Tags')
        ordering = ['label', ]


revisions.default_revision_manager.register(TransactionTag)


@transaction.atomic()
def generate_transaction_id():
    candidate = uuid.uuid4().hex
    while Transaction.objects.filter(unique_id=candidate).count():
        candidate = uuid.uuid4().hex
    return candidate


class Transaction(AsylumModel):
    stamp = models.DateTimeField(_("Datetime"), default=timezone.now, db_index=True)
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
        ordering = ['-stamp', 'reference']


revisions.default_revision_manager.register(Transaction)


class RecurringTransaction(AsylumModel):
    MONTHLY = 1
    YEARLY = 2
    QUARTERLY = 3
    RTYPE_READABLE = {
        MONTHLY: _("Monthly"),
        YEARLY: _("Yearly"),
        QUARTERLY: _("Quarterly"),
    }
    # Defined separately because we cannot do [ (x, RTYPE_READABLE[x]) for x in RTYPE_READABLE ]
    RTYPE_CHOICES = (
        (MONTHLY, _("Monthly")),
        (YEARLY, _("Yearly")),
        (QUARTERLY, _("Quarterly")),
    )

    start = models.DateField(_("Since"), db_index=True,  null=False, blank=False, default=timezone.now)
    end = models.DateField(_("Until"), db_index=True, null=True, blank=True)

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
        elif self.rtype == RecurringTransaction.QUARTERLY:
            if timescope.month in range(1,4):
                start = datetime.datetime(timescope.year, 1, 1)
            elif timescope.month in range(4,7):
                start = datetime.datetime(timescope.year, 4, 1)
            elif timescope.month in range(7,10):
                start = datetime.datetime(timescope.year, 7, 1)
            else:
                start = datetime.datetime(timescope.year, 10, 1)
            end = datetime.datetime(start.year, start.month + 3, calendar.monthrange(start.year, start.month)[1])
        else:
            raise NotImplementedError("Not implemented for %s (%d)" % (RecurringTransaction.RTYPE_READABLE[self.rtype], self.rtype))
        return (timezone.make_aware(start), timezone.make_aware(end))

    def make_uid_source(self, timescope=None):
        start, end = self.resolve_timescope(timescope)
        # NOTE: Do not localize anything in this string, also: DO NOT CHANGE IT or the unique_ids of transactions created will change
        return "RecurringTransaction #%d/#%d for %s" % (self.pk, self.rtype, start.date().isoformat())

    def in_timescope(self, timescope=None):
        # Check that we should actually add the transaction
        scope_start_ts, scope_end_ts = self.resolve_timescope(timescope)
        scope_start = scope_start_ts.date()
        scope_end = scope_end_ts.date()
        return (self.start <= scope_end
                and (not self.end
                     or self.end >= scope_end))

    @transaction.atomic()
    def transaction_exists(self, timescope=None):
        start, end = self.resolve_timescope(timescope)
        uid_source = self.make_uid_source(timescope)
        uid = hashlib.sha1(uid_source.encode('UTF-8')).hexdigest()
        qs = Transaction.objects.filter(
            owner=self.owner, tag=self.tag, unique_id=uid, stamp__gte=start, stamp__lte=end
        )
        if qs.count():
            return True
        return False

    @transaction.atomic()
    @revisions.create_revision()
    def conditional_add_transaction(self, timescope=None):
        if not self.in_timescope(timescope):
            return False
        if self.transaction_exists(timescope):
            return False
        t = Transaction()
        if timescope:
            t.stamp = timescope
        h = get_handler_instance('RECURRINGTRANSACTIONS_CALLBACKS_HANDLER')
        t.tag = self.tag
        t.owner = self.owner
        uid_source = self.make_uid_source(timescope)
        t.unique_id = hashlib.sha1(uid_source.encode('UTF-8')).hexdigest()
        t.reference = uid_source
        t.amount = self.amount
        if h:
            if not h.on_creating(self, t):
                return False
        t.save()
        if h:
            h.on_created(self, t)
        return t

    class Meta:
        verbose_name = _('Recurring Transaction')
        verbose_name_plural = _('Recurring Transactions')
        ordering = ['owner__lname', 'owner__fname', '-start']


revisions.default_revision_manager.register(RecurringTransaction)
