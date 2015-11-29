from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from reversion.admin import VersionAdmin
from .models import MemberType, Member, MembershipApplication, MembershipApplicationTag
from access.models import Token, Grant

class MemberTypeAdmin(VersionAdmin):
    pass

# TODO: how to make this a multiselect
class GrantInline(admin.TabularInline):
    model = Grant
    extra = 0


class TokenInline(admin.TabularInline):
    model = Token
    extra = 0


class MemberAdmin(VersionAdmin):
    list_display = (
        'rname',
        'email',
        'nick',
        'credit_formatted',
    )
    inlines = [ GrantInline, TokenInline ]

    def credit_formatted(self, obj):
        color = "green"
        if obj.credit < 0:
            color = "red"
        return format_html("<span style='color: {};'>{}</span>",color, "%+.02f" % obj.credit)
    credit_formatted.short_description = _("Credit")


class MembershipApplicationAdmin(VersionAdmin):
    pass


class MembershipApplicationTagAdmin(VersionAdmin):
    pass


admin.site.register(MemberType, MemberTypeAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(MembershipApplication, MembershipApplicationAdmin)
admin.site.register(MembershipApplicationTag, MembershipApplicationTagAdmin)
