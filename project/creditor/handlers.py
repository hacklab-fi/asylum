from django.db import models
from django.utils.translation import ugettext_lazy as _
from .models import Transaction



class AbstractTransaction(models.Model):
    stamp = models.DateTimeField(_("Datetime"), blank=False)
    name = models.CharField(_("Name"), max_length=200, blank=False)
    reference = models.CharField(_("Reference"), max_length=200, blank=False)
    amount = models.DecimalField(verbose_name=_("Amount"), max_digits=6, decimal_places=2, blank=False, null=False)
    unique_id = models.CharField(_("Unique transaction id"), max_length=64, blank=False)

    class Meta:
        abstract = True
        managed = False

    def __str__(self):
        return _("AbstractTransaction %s: %+.2f ") % (self.unique_id, self.amount)

    def get_local(self):
        """Uses the unique_id field to get Transaction instance from the local database, or initializes a new one"""
        try:
            obj = Transaction.objects.get(unique_id=self.unique_id)
        except Transaction.DoesNotExist:
            obj = Transaction()
            obj.unique_id = self.unique_id
            obj.stamp = self.stamp
            obj.amount = self.amount
            obj.reference = self.reference
        return obj



class BaseTransactionHandler(object):
    """Baseclass for transaction importer callbacks"""
    def import_transaction(self, transaction):
        """This method must accpet AbstractTransaction and must return Transaction or None if it would not handle 
        the AbstractTransaction for whatever reason.

        It must handle Transactions existing in the database gracefully, preferably updating them but it may
        choose to simply return the existing Transaction
        """
        pass

    def __str__(self):
        return _("Transaction handler baseclass, this does nothing")



class BaseRecurringTransactionsHandler(object):
    """Baseclass for callback handlers for MembershipApplication processing"""

    def on_creating(self, recurring, transaction):
        """Called just before transaction.save(), must return True or the save is aborted"""
        return True

    def on_created(self, recurring, transaction):
        """Called just after transaction.save()"""
        pass
