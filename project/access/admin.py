from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from reversion.admin import VersionAdmin
from .models import TokenType, Token, AccessType, Grant, NonMemberToken


class TokenTypeAdmin(VersionAdmin):
    pass


class TokenTypeListFilter(admin.SimpleListFilter):
    title = _("Token types")
    parameter_name = 'ttype'

    def lookups(self, request, model_admin):
        return ( (x.pk, x.label) for x in TokenType.objects.all() )

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        return queryset.filter(ttype=v)


class RevokedListFilter(admin.SimpleListFilter):
    title = _("Revokation status")
    parameter_name = 'revoked'

    def lookups(self, request, model_admin):
        return ( ( -2, _("All")), (None, _("Not revoked")), (1, _("Revoked")) )

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
        v = self.value()
        if v is not None:
            if int(v) == -2:
                return queryset
            if int(v) == 1:
                return queryset.filter(revoked=True)
        return queryset.filter(revoked=False)


class TokenAdmin(VersionAdmin):
    list_display = (
        'owner',
        'ttype',
        'value_formatted',
    )
    list_filter = (TokenTypeListFilter, RevokedListFilter)

    def value_formatted(self, obj):
        if not obj.revoked:
            return obj.value
        color = "red"
        return format_html("<span style='color: {};'>{}</span>", color, obj.value)
    value_formatted.short_description = _("Token value")


class AccessTypeAdmin(VersionAdmin):
    pass


class GrantAdmin(VersionAdmin):
    pass


class NonMemberTokenAdmin(VersionAdmin):
    pass


admin.site.register(TokenType, TokenTypeAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(AccessType, AccessTypeAdmin)
admin.site.register(Grant, GrantAdmin)
admin.site.register(NonMemberToken, NonMemberTokenAdmin)
