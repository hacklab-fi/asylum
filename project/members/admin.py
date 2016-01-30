# -*- coding: utf-8 -*-
import itertools

from access.models import AccessType, Grant, Token
from creditor.models import RecurringTransaction
from django import forms
from django.contrib import admin
from django.db import models
from django.utils.functional import allow_lazy, lazy
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from reversion.admin import VersionAdmin

from .models import Member, MemberNote, MembershipApplication, MembershipApplicationTag, MemberType


class MemberTypeAdmin(VersionAdmin):
    pass

# TODO: how to make this a multiselect


class GrantInline(admin.TabularInline):
    model = Grant
    extra = 0


class TokenInline(admin.TabularInline):
    model = Token
    extra = 0


class RTInline(admin.TabularInline):
    model = RecurringTransaction
    extra = 0


class MemberNoteInline(admin.TabularInline):
    model = MemberNote
    extra = 0


class MemberTypeListFilter(admin.SimpleListFilter):
    title = _("Membership types")
    parameter_name = 'mtype'

    def lookups(self, request, model_admin):
        return ((x.pk, x.label) for x in MemberType.objects.all())

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        return queryset.filter(mtypes=v)


class GrantListFilter(admin.SimpleListFilter):
    title = _("Grants")
    parameter_name = 'atype'

    def lookups(self, request, model_admin):
        return ((x.pk, x.label) for x in AccessType.objects.all())

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        return queryset.filter(access_granted__atype=v)


class CreditListFilter(admin.SimpleListFilter):
    title = _("Credit")
    parameter_name = 'credit'

    def lookups(self, request, model_admin):
        return (
            (-1, _("Negative credit")),
            (1, _("Positive credit")),
        )

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        # self.creditor_transactions.all().aggregate(models.Sum('amount'))['amount__sum']
        queryset = queryset.annotate(credit_annotated=models.Sum('creditor_transactions__amount'))
        if int(v) < 0:
            return queryset.filter(credit_annotated__lt=0)
        return queryset.filter(credit_annotated__gt=0)


class MemberAdmin(VersionAdmin):
    list_display = (
        'rname',
        'email',
        'nick',
        'credit_formatted',
        'mtypes_formatted',
        'grants_formatted',
    )
    list_filter = (MemberTypeListFilter, GrantListFilter, CreditListFilter)
    inlines = [MemberNoteInline, GrantInline, TokenInline, RTInline]
    search_fields = ['lname', 'fname', 'email', 'nick']
    ordering = ['lname', 'fname']

    def rname(self, object):
        return object.rname
    rname.short_description = _("Name")
    rname.admin_order_field = 'lname'

    def credit_formatted(self, obj):
        if obj.credit_annotated is not None:
            credit = obj.credit_annotated
        else:
            credit = 0.0
        color = "green"
        if credit < 0:
            color = "red"
        return format_html("<span style='color: {};'>{}</span>", color, "%+.02f" % credit)
    credit_formatted.short_description = _("Credit")
    credit_formatted.admin_order_field = 'credit_annotated'

    def mtypes_formatted(self, obj):
        return ', '.join((x.label for x in obj.mtypes.all()))
    mtypes_formatted.short_description = _("Membership types")

    def grants_formatted(self, obj):
        return ', '.join((x.atype.label for x in Grant.objects.filter(owner=obj)))
    grants_formatted.short_description = _("Grants")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(credit_annotated=models.Sum('creditor_transactions__amount'))
        return qs


class TagListFilter(admin.SimpleListFilter):
    title = _("Tags")
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        return ((x.pk, x.label) for x in MembershipApplicationTag.objects.all())

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        return queryset.filter(tags=v)


def mtypes_choices():
    return itertools.chain((('', '----'), ), ((x.pk, x.label) for x in MemberType.objects.all()))


class MembershipApplicationsForm(admin.helpers.ActionForm):
    mtypes = forms.MultipleChoiceField(
        label=_("Membership types"),  # TODO: Read from the member model meta ?
        choices=lazy(mtypes_choices, tuple)
    )


class MembershipApplicationAdmin(VersionAdmin):
    list_display = (
        'rname',
        'email',
        'nick',
        'tags_formatted',
    )
    list_filter = (TagListFilter,)
    actions = ['approve_selected']
    action_form = MembershipApplicationsForm
    search_fields = ['lname', 'fname', 'email', 'nick']

    def tags_formatted(self, obj):
        return ', '.join((x.label for x in obj.tags.all()))
    tags_formatted.short_description = _("Tags")

    def approve_selected(modeladmin, request, queryset):
        add_types = []
        for x in request.POST.getlist('mtypes'):
            if x:
                add_types.append(int(x))
        for a in queryset.all():
            a.approve(add_types)
    approve_selected.short_description = _("Approve selected applications")


class MembershipApplicationTagAdmin(VersionAdmin):
    pass


class MemberNoteAdmin(VersionAdmin):
    pass


admin.site.register(MemberType, MemberTypeAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(MembershipApplication, MembershipApplicationAdmin)
admin.site.register(MembershipApplicationTag, MembershipApplicationTagAdmin)
admin.site.register(MemberNote, MemberNoteAdmin)
