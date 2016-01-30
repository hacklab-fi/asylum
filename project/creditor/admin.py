# -*- coding: utf-8 -*-
import datetime

from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from reversion.admin import VersionAdmin

from .models import RecurringTransaction, Transaction, TransactionTag


class TransactionTagAdmin(VersionAdmin):
    pass


class TagListFilter(admin.SimpleListFilter):
    title = _("Transaction tags")
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        return ((x.pk, x.label) for x in TransactionTag.objects.all())

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
            (-1, _("Negative amount")),
            (1, _("Positive amount")),
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
        return format_html("<span style='color: {};'>{}</span>", color, "%+.02f" % obj.amount)
    amount_formatted.short_description = _("Amount")
    amount_formatted.admin_order_field = 'amount'


class RTActiveListFilter(admin.SimpleListFilter):
    title = _("Active")
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            ("-2", _("All")),
            ("-1", _("Inactive")),
            (None, _("Active")),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        today = datetime.datetime.now().date()
        v = self.value()
        if v is not None:
            if int(v) == -2:
                return queryset
            if int(v) == -1:
                return queryset.filter(
                    Q(Q(end__lte=today) & Q(start__lte=today))
                    | Q(start__gt=today)
                )
        return queryset.filter(
            Q(start__lte=today)
            & (Q(end__gte=today) | Q(end=None))
        )


class RecurringTransactionAdmin(VersionAdmin):
    list_display = (
        'owner_f',
        'dates_formatted',
        'amount_formatted',
        'tag',
    )
    list_filter = (TagListFilter, RTActiveListFilter)
    search_fields = ['amount', 'owner__fname', 'owner__lname', 'owner__email']

    def owner_f(self, obj):
        return obj.owner
    owner_f.short_description = _("Member")
    owner_f.admin_order_field = 'owner__lname'

    def amount_formatted(self, obj):
        color = "green"
        if obj.amount < 0:
            color = "red"
        return format_html("<span style='color: {};'>{}</span>", color, "%+.02f" % obj.amount)
    amount_formatted.short_description = _("Amount")
    amount_formatted.admin_order_field = 'amount'

    def dates_formatted(self, obj):
        today = datetime.datetime.now().date()
        color = "black"
        if (obj.end
                and obj.end < today):
            color = "red"
        if obj.start > today:
            color = "red"
        if obj.end:
            return format_html("<span style='color: {};'>{} / {}</span>", color, obj.start.isoformat(), obj.end.isoformat())
        return format_html("<span style='color: {};'>{}</span>", color, obj.start.isoformat())
    dates_formatted.short_description = _("Start / End")
    dates_formatted.admin_order_field = 'start'


admin.site.register(TransactionTag, TransactionTagAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(RecurringTransaction, RecurringTransactionAdmin)
