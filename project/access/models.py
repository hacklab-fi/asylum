from django.db import models
from django.utils.translation import ugettext_lazy as _
from reversion import revisions

class TokenType(models.Model):
    label = models.CharField(_("Label"), max_length=200, blank=False)

    def __str__(self):
        return self.label

revisions.default_revision_manager.register(TokenType)


class Token(models.Model):
    label = models.CharField(_("Label"), max_length=200, blank=True)
    owner = models.ForeignKey('members.Member', blank=False, verbose_name=_("Member"), related_name='access_tokens')
    ttype = models.ForeignKey(TokenType, blank=False, verbose_name=_("Token type"), related_name='+')
    value = models.CharField(_("Token value"), max_length=200, blank=False)
    revoked = models.BooleanField(_("Revoked"), default=False)

    def __str__(self):
        if self.label:
            return self.label
        return _("%s '%s' for %s") % (self.ttype, self.value, self.owner)

revisions.default_revision_manager.register(Token)


class AccessType(models.Model):
    label = models.CharField(_("Label"), max_length=200, blank=False)
    bit = models.PositiveSmallIntegerField(_("Bit number"), blank=True, null=True, unique=True) # For systems that utilize bitwise checks
    external_id = models.CharField(_("External identifier"), max_length=200, blank=True, null=True, unique=True) # For other systems

    def __str__(self):
        return self.label

revisions.default_revision_manager.register(AccessType)


class Grant(models.Model):
    owner = models.ForeignKey('members.Member', blank=False, verbose_name=_("Member"), related_name='access_granted')
    atype = models.ForeignKey(AccessType, related_name='+', verbose_name=_("Access"))

    def __str__(self):
        return _("%s for %s") % (self.atype, self.owner)

revisions.default_revision_manager.register(Grant)
