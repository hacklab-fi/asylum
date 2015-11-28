from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import TransactionTag, Transaction


class TransactionTagAdmin(VersionAdmin):
    pass


class TransactionAdmin(VersionAdmin):
    pass


admin.site.register(TransactionTag, TransactionTagAdmin)
admin.site.register(Transaction, TransactionAdmin)
