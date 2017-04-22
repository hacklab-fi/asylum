# -*- coding: utf-8 -*-
import random
from decimal import Decimal

from access.models import AccessType
from access.utils import resolve_acl
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_markdown.models import MarkdownField
from reversion import revisions

from asylum.models import AsylumModel

from .handlers import call_saves, get_handler_instance


def generate_unique_randomid():
    """Generate pseudorandom ids until a free one is found"""
    candidate = "0x%x" % random.randint(1, 2 ** 32)
    while Member.objects.filter(anonymized_id=candidate).count():
        candidate = "0x%x" % random.randint(1, 2 ** 32)
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


class MemberCommon(AsylumModel):
    fname = models.CharField(_("First name"), max_length=200, blank=False)
    lname = models.CharField(_("Last name"), max_length=200, blank=False)
    city = models.CharField(_("City of residence"), max_length=200, blank=False)
    email = models.EmailField(_("Email address"), unique=True, blank=False)
    phone = models.CharField(_("Phone number"), max_length=200, blank=True)
    nick = models.CharField(_("Nickname"), max_length=200, blank=True)

    def __str__(self):
        return '"%s, %s" <%s>' % (self.lname, self.fname, self.email)

    @property
    def name(self):
        return "%s %s" % (self.fname, self.lname)

    @property
    def rname(self):
        return "%s, %s" % (self.lname, self.fname)

    @property
    def access_acl(self):
        return resolve_acl(AccessType.objects.filter(pk__in=self.access_granted.select_related('atype').values_list('atype', flat=True)))

    class Meta:
        abstract = True
        ordering = ['lname', 'fname']


class MemberType(AsylumModel):
    label = models.CharField(_("Label"), max_length=200, blank=False)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _('Member Type')
        verbose_name_plural = _('Member Types')


revisions.default_revision_manager.register(MemberType)


class Member(MemberCommon):
    accepted = models.DateField(_("Date accepted"), default=timezone.now)
    mtypes = models.ManyToManyField(MemberType, related_name='+', verbose_name=_("Membership types"), blank=True)
    anonymized_id = models.CharField(_("Anonymized id (for use in external databases)"), max_length=24, unique=True, blank=True, null=True, default=generate_unique_randomid)
    member_id = models.PositiveIntegerField(_("Member id no"), blank=True, null=True, unique=True, default=generate_unique_memberid)

    @property
    def credit(self):
        ret = self.creditor_transactions.all().aggregate(models.Sum('amount'))['amount__sum']
        if ret == None:
            return Decimal(0.0)
        return ret

    @call_saves('MEMBER_CALLBACKS_HANDLER')
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')


revisions.default_revision_manager.register(Member)


class MembershipApplicationTag(AsylumModel):
    label = models.CharField(_("Label"), max_length=200, blank=False)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _('Membership Application Tag')
        verbose_name_plural = _('Membership Application Tags')


revisions.default_revision_manager.register(MembershipApplicationTag)


class MembershipApplication(MemberCommon):
    received = models.DateField(default=timezone.now)
    tags = models.ManyToManyField(MembershipApplicationTag, related_name='+', verbose_name=_("Application tags"), blank=True)
    notes = MarkdownField(verbose_name=_("Notes"), blank=True)

    @call_saves('MEMBERAPPLICATION_CALLBACKS_HANDLER')
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def validate_unique(self, exclude=None):
        if exclude and 'email' in exclude:
            return super().validate_unique(exclude)
        if Member.objects.filter(email=self.email).count():
            # TODO: Figure out the exact format the default form validators use and use that ?
            raise ValidationError({'email': ValidationError(_('Member with this email already exists'), code='unique')})
        return super().validate_unique(exclude)

    def approve(self, set_mtypes):
        h = get_handler_instance('MEMBERAPPLICATION_CALLBACKS_HANDLER')
        with transaction.atomic(), revisions.create_revision():
            m = Member()
            m.fname = self.fname
            m.lname = self.lname
            m.city = self.city
            m.email = self.email
            m.phone = self.phone
            m.nick = self.nick
            if h:
                h.on_approving(self, m)
            m.save()
            if set_mtypes:
                m.mtypes = set_mtypes
                m.save()
            if self.notes:
                n = MemberNote()
                n.notes = self.notes
                n.member = m
                n.save()
            if h:
                h.on_approved(self, m)
            self.delete()

    class Meta:
        verbose_name = _('Membership Application')
        verbose_name_plural = _('Membership Applications')


revisions.default_revision_manager.register(MembershipApplication)


class MemberNote(AsylumModel):
    stamp = models.DateTimeField(_("Datetime"), default=timezone.now, db_index=True)
    notes = MarkdownField(verbose_name=_("Notes"), blank=False)
    member = models.ForeignKey(Member, verbose_name=_("Member"), blank=True, null=True, on_delete=models.CASCADE, related_name='notes')

    class Meta:
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')
        ordering = ['member__lname', 'member__fname', '-stamp']

    def __str__(self):
        return _("Notes about %s on %s") % (self.member, self.stamp)


revisions.default_revision_manager.register(MemberNote)
