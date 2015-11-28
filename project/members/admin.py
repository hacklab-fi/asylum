from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import MemberType, Member, MembershipApplication, MembershipApplicationTag


class MemberTypeAdmin(VersionAdmin):
    pass


class MemberAdmin(VersionAdmin):
    pass


class MembershipApplicationAdmin(VersionAdmin):
    pass


class MembershipApplicationTagAdmin(VersionAdmin):
    pass


admin.site.register(MemberType, MemberTypeAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(MembershipApplication, MembershipApplicationAdmin)
admin.site.register(MembershipApplicationTag, MembershipApplicationTagAdmin)
