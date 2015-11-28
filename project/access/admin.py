from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import TokenType, Token, AccessType, Grant


class TokenTypeAdmin(VersionAdmin):
    pass


class TokenAdmin(VersionAdmin):
    pass


class AccessTypeAdmin(VersionAdmin):
    pass


class GrantAdmin(VersionAdmin):
    pass


admin.site.register(TokenType, TokenTypeAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(AccessType, AccessTypeAdmin)
admin.site.register(Grant, GrantAdmin)
