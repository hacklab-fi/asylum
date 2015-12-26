from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from reversion.admin import VersionAdmin
from .models import TransactionTag, Transaction, RecurringTransaction


class TransactionTagAdmin(VersionAdmin):
    pass


class TagListFilter(admin.SimpleListFilter):
    title = _("Transaction tags")
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        return ( (x.pk, x.label) for x in TransactionTag.objects.all() )

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        return queryset.filter(tag=v)


class AmountListFilter(admin.SimpleListFilter):
    title = _("Amount")
    parameter_name = 'amount'

    def lookups(self, request, model_admin):
        return (
            ( -1, _("Negative amount" )),
            ( 1, _("Positive amount") ),
        )

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        if int(v) < 0:
            return queryset.filter(amount__lt=0)
        return queryset.filter(amount__gt=0)


class TransactionAdmin(VersionAdmin):
    list_display = (
        'stamp_formatted',
        'amount_formatted',
        'tag',
        'reference',
        'owner',
    )
    list_filter = (TagListFilter, AmountListFilter)
    search_fields = ['amount', 'reference', 'unique_id', 'owner__fname', 'owner__lname', 'owner__email']

    def stamp_formatted(self, obj):
        return obj.stamp.isoformat()
    stamp_formatted.short_description = _("Datetime")
    stamp_formatted.admin_order_field = 'stamp'

    def amount_formatted(self, obj):
        color = "green"
        if obj.amount < 0:
            color = "red"
        return format_html("<span style='color: {};'>{}</span>",color, "%+.02f" % obj.amount)
    amount_formatted.short_description = _("Amount")
    amount_formatted.admin_order_field = 'amount'


class RecurringTransactionAdmin(VersionAdmin):
    pass


admin.site.register(TransactionTag, TransactionTagAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(RecurringTransaction, RecurringTransactionAdmin)
