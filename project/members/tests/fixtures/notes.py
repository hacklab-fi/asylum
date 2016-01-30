# -*- coding: utf-8 -*-
import datetime

import factory.django
import factory.fuzzy
import pytz
from members.models import Member, MemberNote

from asylum.tests.utils import FuzzyLoremipsum


class MemberNoteFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = MemberNote
        django_get_or_create = ('stamp', 'member')
    stamp = factory.fuzzy.FuzzyDateTime(datetime.datetime.now(pytz.utc) - datetime.timedelta(days=180))
    member = factory.fuzzy.FuzzyChoice(Member.objects.all())
    notes = FuzzyLoremipsum()
