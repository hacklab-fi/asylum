import random
from django.db import models
from django.utils.translation import ugettext_lazy as _
from reversion import revisions

def generate_unique_randomid():
    """Generate pseudorandom ids until a free one is found"""
    candidate = "0x%x" % random.randint(1,2**32)
    while Member.objects.filter(anonymized_id=candidate).count():
        candidate = "0x%x" % random.randint(1,2**32)
    return candidate

def generate_unique_memberid():
    """Gives the next highest member id"""
    try:
        highest_member = Member.objects.exclude(member_id=None).order_by('-member_id')[0]
        highest = highest_member.member_id
    except IndexError:
        highest = 0
    candidate = highest + 1
    while Member.objects.filter(member_id=candidate).count():
        candidate += 1
    return candidate
    

class MemberCommon(models.Model):
    fname = models.CharField(_("First name"), max_length=200, blank=False)
    lname = models.CharField(_("Last name"), max_length=200, blank=False)
    city = models.CharField(_("City of residence"), max_length=200, blank=False)
    email = models.EmailField(_("Email address"), unique=True, blank=False)
    phone = models.CharField(_("Phone number"), max_length=200, blank=True)
    nick = models.CharField(_("Nickname"), max_length=200, blank=True)

    def __str__(self):
        return '"%s, %s" <%s>' % (self.lname, self.fname, self.email)

    class Meta:
        abstract = True


class MemberType(models.Model):
    label = models.CharField(_("Label"), max_length=200, blank=False)

    def __str__(self):
        return self.label

revisions.default_revision_manager.register(MemberType)


class Member(MemberCommon):
    accepted = models.DateField(_("Date accepted"), auto_now_add=True)
    mtypes = models.ManyToManyField(MemberType, related_name='+', verbose_name=_("Membership types"), blank=True)
    anonymized_id = models.CharField(_("Anonymized id (for use in external databases)"), max_length=24, unique=True, blank=True, null=True, default=generate_unique_randomid)
    member_id = models.PositiveIntegerField(_("Member id no"), blank=True, null=True, unique=True, default=generate_unique_memberid)

revisions.default_revision_manager.register(Member)


class MembershipApplication(MemberCommon):
    received = models.DateField(auto_now_add=True)

    def approve(self, set_mtypes):
        m = Member()
        m.fname = self.fname
        m.lname = self.lname
        m.city = self.city
        m.email = self.email
        m.phone = self.phone
        m.nick = self.nick
        m.save()
        if set_mtypes:
            m.mtypes = set_mtypes
            m.save()
        self.delete()

revisions.default_revision_manager.register(MembershipApplication)
