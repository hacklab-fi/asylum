# -*- coding: utf-8 -*-
import itertools

from .models import NonMemberToken, Token


def all_tokens(cfilters={}, nmtfilters={}, tfilters={}):
    """Chains all token-like models' querysets, first filters dict is applied to all, second only to NonMemberToken, third only to Token"""
    nmtfilters.update(cfilters)
    tfilters.update(cfilters)
    return itertools.chain(
        NonMemberToken.objects.filter(**nmtfilters),
        Token.objects.filter(**tfilters)
    )


def resolve_acl(atypes):
    """Resolves the bits of accesstypes into single int and externals to unique set"""
    ret = {
        'bits': int(0),
        'externals': set(),
    }
    for at in atypes:
        ret['bits'] |= 1 << at.bit
        ret['externals'].add(at.external_id)
    return ret
