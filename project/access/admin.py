from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from reversion.admin import VersionAdmin
from .models import TokenType, Token, AccessType, Grant, NonMemberToken


class TokenTypeAdmin(VersionAdmin):
    pass


class TokenAdmin(VersionAdmin):
    list_display = (
        'owner',
        'ttype',
        'value_formatted',
    )
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
