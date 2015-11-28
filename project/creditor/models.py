from django.db import models
from django.utils.translation import ugettext_lazy as _
from reversion import revisions

class TransactionTag(models.Model):
    label = models.CharField(_("Label"), max_length=200, blank=False)

    def __str__(self):
        return self.label

revisions.default_revision_manager.register(TransactionTag)


class Transaction(models.Model):
    stamp = models.DateTimeField(_("Datetime"), auto_now_add=True)
    tag = models.ForeignKey(TransactionTag, blank=True, null=True, verbose_name=_("Tag"))
    reference = models.CharField(_("Reference"), max_length=200, blank=False)
    owner = models.ForeignKey('members.Member', blank=False, verbose_name=_("Member"), related_name='creditor_transactions')
    amount = models.DecimalField(verbose_name=_("Amount"), max_digits=6, decimal_places=2, blank=False, null=False)

    def __str__(self):
        if self.tag:
            return _("%+.2f for %s (%s)") % (self.amount, self.owner, self.tag)
        return _("%+.2f for %s") % (self.amount, self.owner)

revisions.default_revision_manager.register(Transaction)
