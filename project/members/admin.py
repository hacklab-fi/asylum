import itertools
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django import forms
from reversion.admin import VersionAdmin
from .models import MemberType, Member, MembershipApplication, MembershipApplicationTag
from access.models import Token, Grant, AccessType
from creditor.models import RecurringTransaction

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


class MemberTypeListFilter(admin.SimpleListFilter):
    title = _("Membership types")
    parameter_name = 'mtype'

    def lookups(self, request, model_admin):
        return ( (x.pk, x.label) for x in MemberType.objects.all() )

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        return queryset.filter(mtypes=v)


class GrantListFilter(admin.SimpleListFilter):
    title = _("Grants")
    parameter_name = 'atype'

    def lookups(self, request, model_admin):
        return ( (x.pk, x.label) for x in AccessType.objects.all() )

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        return queryset.filter(access_granted__atype=v)


class MemberAdmin(VersionAdmin):
    list_display = (
        'rname',
        'email',
        'nick',
        'credit_formatted',
        'mtypes_formatted',
        'grants_formatted',
    )
    list_filter = (MemberTypeListFilter, GrantListFilter)
    inlines = [ GrantInline, TokenInline, RTInline ]

    def credit_formatted(self, obj):
        color = "green"
        if obj.credit < 0:
            color = "red"
        return format_html("<span style='color: {};'>{}</span>",color, "%+.02f" % obj.credit)
    credit_formatted.short_description = _("Credit")

    def mtypes_formatted(self, obj):
        return ', '.join(( x.label for x in obj.mtypes.all() ))
    mtypes_formatted.short_description = _("Membership types")
    def grants_formatted(self, obj):
        return ', '.join(( x.atype.label for x in Grant.objects.filter(owner=obj) ))
    grants_formatted.short_description = _("Grants")


class TagListFilter(admin.SimpleListFilter):
    title = _("Tags")
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        return ( (x.pk, x.label) for x in MembershipApplicationTag.objects.all() )

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        return queryset.filter(tags=v)


class MembershipApplicationsForm(admin.helpers.ActionForm):
    mtypes = forms.MultipleChoiceField(
        label=_("Membership types"), # TODO: Read from the member model meta ?
        choices=itertools.chain( ( ('', '----' ), ) ,( (x.pk, x.label) for x in MemberType.objects.all() ))
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

    def tags_formatted(self, obj):
        return ', '.join(( x.label for x in obj.tags.all() ))
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


admin.site.register(MemberType, MemberTypeAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(MembershipApplication, MembershipApplicationAdmin)
admin.site.register(MembershipApplicationTag, MembershipApplicationTagAdmin)
