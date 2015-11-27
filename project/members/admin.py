from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import MemberType, Member, MembershipApplication


class MemberTypeAdmin(VersionAdmin):
    pass


class MemberAdmin(VersionAdmin):
    pass


class MembershipApplicationAdmin(VersionAdmin):
    pass


admin.site.register(MemberType, MemberTypeAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(MembershipApplication, MembershipApplicationAdmin)
